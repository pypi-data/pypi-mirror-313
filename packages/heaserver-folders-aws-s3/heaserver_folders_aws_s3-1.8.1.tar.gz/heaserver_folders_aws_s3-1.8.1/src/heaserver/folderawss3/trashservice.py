"""
The HEA Trash Microservice provides deleted file management.
"""

import asyncio
from functools import partial
import itertools
from heaserver.service import response
from heaobject.data import AWSS3FileObject
from heaobject.folder import AWSS3Folder
from heaobject.trash import AWSS3FolderFileTrashItem
from heaobject.awss3key import decode_key, encode_key, KeyDecodeException, is_folder, display_name, parent
from heaobject.user import NONE_USER
from heaobject.root import ViewerPermissionContext, PermissionContext, Permission
from heaobject.project import AWSS3Project
from heaserver.service.runner import init_cmd_line, routes, start, web
from heaserver.service.db import awsservicelib
from heaserver.service.db.aws import S3Manager, S3ClientContext
from heaserver.service.db.mongo import MongoContext, Mongo
from heaserver.service.wstl import builder_factory, action
from heaserver.service.appproperty import HEA_CACHE, HEA_BACKGROUND_TASKS
from heaserver.service.oidcclaimhdrs import SUB
from heaserver.service.sources import AWS_S3
from heaserver.service.wstl import action
from aiohttp import web
import logging
from typing import AsyncGenerator, AsyncIterator, Any, Generator
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import ListObjectVersionsOutputTypeDef, DeleteMarkerEntryTypeDef, ObjectVersionTypeDef
from botocore.exceptions import ClientError
from yarl import URL
from datetime import datetime, timezone
from operator import itemgetter
from heaserver.service.customhdrs import PREFER, PREFERENCE_RESPOND_ASYNC


TRASHAWSS3_COLLECTION = 'awss3trashitems'
MAX_VERSIONS_TO_RETRIEVE = 50000
MONGODB_AWS_S3_FOLDER_METADATA_COLLECTION = 'awss3foldersmetadata'


_status_id = 0


@routes.get('/ping')
async def ping(request: web.Request) -> web.Response:
    """
    For testing whether the service is up.

    :param request: the HTTP request.
    :return: Always returns status code 200.
    """
    return response.status_ok()


@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}')
async def get_item_options(request: web.Request) -> web.Response:
    """
    Gets the allowed HTTP methods for a trash item.

    :param request: a HTTP request (required).
    :return: the HTTP response.
    ---
    summary: Allowed HTTP methods.
    tags:
        - heaserver-trash-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            text/plain:
                schema:
                    type: string
                    example: "200: OK"
      '403':
        $ref: '#/components/responses/403'
      '404':
        $ref: '#/components/responses/404'
    """
    return await response.get_options(request, ['GET', 'HEAD', 'OPTIONS'])


@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/opener')
async def get_item_opener_options(request: web.Request) -> web.Response:
    """
    Gets the allowed HTTP methods for a trash item opener.

    :param request: a HTTP request (required).
    :return: the HTTP response.
    ---
    summary: Allowed HTTP methods.
    tags:
        - heaserver-trash-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            text/plain:
                schema:
                    type: string
                    example: "200: OK"
      '403':
        $ref: '#/components/responses/403'
      '404':
        $ref: '#/components/responses/404'
    """
    return await response.get_options(request, ['GET', 'HEAD', 'OPTIONS'])


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}')
@action(name='heaserver-awss3trash-item-get-open-choices',
        rel='hea-opener-choices hea-context-menu',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/opener',
        itemif='actual_object_type_name == "heaobject.folder.AWSS3Folder"')
@action(name='heaserver-awss3trash-item-get-properties',
        rel='hea-properties hea-context-menu')
@action('heaserver-awss3trash-item-restore',
        rel='hea-trash-restore-confirmer hea-context-menu hea-confirm-prompt',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/restorer')
@action('heaserver-awss3trash-item-permanently-delete',
        rel='hea-trash-delete-confirmer hea-context-menu hea-confirm-prompt',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/deleter')
@action('heaserver-awss3trash-item-get-self', rel='self',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}')
@action('heaserver-awss3trash-item-get-volume',
        rel='hea-volume',
        path='volumes/{volume_id}')
@action('heaserver-awss3trash-item-get-awsaccount',
        rel='hea-account',
        path='volumes/{volume_id}/awsaccounts/me')
async def get_deleted_item(request: web.Request) -> web.Response:
    """
    Gets a delete item.

    :param request: the HTTP request.
    :return the deleted item in a list, or Not Found.
    ---
    summary: A deleted item.
    tags:
        - heaserver-trash-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    sub = request.headers.get(SUB, NONE_USER)
    context: PermissionContext[AWSS3FolderFileTrashItem] = ViewerPermissionContext(sub)
    result = await _get_deleted_item(request)
    if result is None:
        return await response.get(request, None)
    else:
        return await response.get(request, result.to_dict(),
                                  permissions=await result.get_permissions(context),
                                  attribute_permissions=await result.get_all_attribute_permissions(context))


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3trashfolders/{trash_folder_id}/items/')
@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3trashfolders/{trash_folder_id}/items')
@action(name='heaserver-awss3trash-item-get-open-choices',
        rel='hea-opener-choices hea-context-menu',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/opener',
        itemif='actual_object_type_name == "heaobject.folder.AWSS3Folder"')
@action(name='heaserver-awss3trash-item-get-properties',
        rel='hea-properties hea-context-menu')
@action('heaserver-awss3trash-item-restore',
        rel='hea-trash-restore-confirmer hea-context-menu hea-confirm-prompt',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/restorer')
@action('heaserver-awss3trash-item-permanently-delete',
        rel='hea-trash-delete-confirmer hea-context-menu hea-confirm-prompt',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/deleter')
@action('heaserver-awss3trash-item-get-self', rel='self',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}')
async def get_items_in_trash_folder(request: web.Request) -> web.Response:
    """
    Gets a list of all deleted items in a volume, bucket, and trash folder. It
    only retrieves items with the folder as a parent, not including any
    subfolders.

    :param request: the HTTP request.
    :return: the list of items with delete markers in the requested folder, or
    Not Found.
    ---
    summary: Gets a list of the deleted items from the given folder.
    tags:
        - heaserver-trash-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - name: trash_folder_id
          in: path
          required: true
          description: The id of the trash folder to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A trash folder id
              value: root
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    sub = request.headers.get(SUB, NONE_USER)
    context: PermissionContext[AWSS3FolderFileTrashItem] = ViewerPermissionContext(sub)
    result: list[AWSS3FolderFileTrashItem] = []
    async for i in _get_deleted_items(request, recursive=False):
        result.append(i)
    perms = []
    attr_perms = []
    for r in result:
        perms.append(await r.get_permissions(context))
        attr_perms.append(await r.get_all_attribute_permissions(context))
    return await response.get_all(request, tuple(r.to_dict() for r in result), permissions=perms,
                                  attribute_permissions=attr_perms)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/awss3trash/')
@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/awss3trash')
@action(name='heaserver-awss3trash-item-get-open-choices',
        rel='hea-opener-choices hea-context-menu',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/opener',
        itemif='actual_object_type_name == "heaobject.folder.AWSS3Folder"')
@action(name='heaserver-awss3trash-item-get-properties',
        rel='hea-properties hea-context-menu')
@action('heaserver-awss3trash-item-restore',
        rel='hea-trash-restore-confirmer hea-context-menu hea-confirm-prompt',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/restorer')
@action('heaserver-awss3trash-item-permanently-delete',
        rel='hea-trash-delete-confirmer hea-context-menu hea-confirm-prompt',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/deleter')
@action('heaserver-awss3trash-item-get-self', rel='self',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}')
async def get_deleted_items_in_folder(request: web.Request) -> web.Response:
    """
    Gets a list of all deleted items in a volume, bucket, and folder. It only
    retrieves items with the folder as a parent, not including any subfolders.

    :param request: the HTTP request.
    :return: the list of items with delete markers or the requested bucket, or
    Not Found.
    ---
    summary: Gets a list of the deleted items from the given folder.
    tags:
        - heaserver-trash-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - name: folder_id
          in: path
          required: true
          description: The id of the folder to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    sub = request.headers.get(SUB, NONE_USER)
    context: PermissionContext[AWSS3FolderFileTrashItem] = ViewerPermissionContext(sub)
    result: list[AWSS3FolderFileTrashItem] = []
    async for i in _get_deleted_items(request, recursive=False):
        result.append(i)
    perms = []
    attr_perms = []
    for r in result:
        perms.append(await r.get_permissions(context))
        attr_perms.append(await r.get_all_attribute_permissions(context))
    return await response.get_all(request, tuple(r.to_dict() for r in result), permissions=perms,
                                  attribute_permissions=attr_perms)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3trash/')
@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3trash')
@action(name='heaserver-awss3trash-item-get-open-choices',
        rel='hea-opener-choices hea-context-menu',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/opener',
        itemif='isheaobject(heaobject.folder.AWSS3Folder)')
@action('heaserver-awss3trash-item-get-properties',
        rel='hea-properties hea-context-menu')
@action('heaserver-awss3trash-item-restore',
        rel='hea-trash-restore-confirmer hea-context-menu hea-confirm-prompt',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/restorer')
@action('heaserver-awss3trash-item-permanently-delete',
        rel='hea-trash-delete-confirmer hea-context-menu hea-confirm-prompt',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/deleter')
@action('heaserver-awss3trash-item-get-self', rel='self',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}')
@action('heaserver-awss3trash-do-empty-trash', rel='hea-trash-emptier',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trashemptier')
async def get_all_deleted_items(request: web.Request) -> web.Response:
    """
    Gets a list of all deleted items in a volume and bucket.

    :param request: the HTTP request.
    :return: the list of items with delete markers or the requested bucket, Not
    Found.
    ---
    summary: Gets a list of all deleted items.
    tags:
        - heaserver-trash-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to check for deleted files.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    logger = logging.getLogger(__name__)
    sub = request.headers.get(SUB, NONE_USER)
    context: PermissionContext[AWSS3FolderFileTrashItem] = ViewerPermissionContext(sub)
    async def coro(app: web.Application):
        logger.debug('Getting deleted items...')
        result: list[AWSS3FolderFileTrashItem] = []
        async for i in _get_deleted_items(request):
            logger.debug('Got item %s', i)
            result.append(i)
        perms = []
        attr_perms = []
        for r in result:
            logger.debug('Getting permissions for %s...', r)
            perms.append(await r.get_permissions(context))
            attr_perms.append(await r.get_all_attribute_permissions(context))
        logger.debug('Generating response...')
        return await response.get_all(request, tuple(r.to_dict() for r in result),
                                      permissions=perms, attribute_permissions=attr_perms)
    async_requested = PREFERENCE_RESPOND_ASYNC in request.headers.get(PREFER, [])
    if async_requested:
        logger.debug('Asynchronous get all trash')
        global _status_id
        status_location = f'{str(request.url).rstrip("/")}asyncstatus{_status_id}'
        _status_id += 1
        task_name = f'{sub}^{status_location}'
        await request.app[HEA_BACKGROUND_TASKS].add(coro, task_name)
        return response.status_see_other(status_location)
    else:
        logger.debug('Synchronous get all trash')
        return await coro(request.app)




@routes.get('/volumes/{volume_id}/awss3trash/')
@routes.get('/volumes/{volume_id}/awss3trash')
@action(name='heaserver-awss3trash-item-get-open-choices',
        rel='hea-opener-choices hea-context-menu',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/opener',
        itemif='isheaobject(heaobject.folder.AWSS3Folder)')
@action('heaserver-awss3trash-item-get-properties',
        rel='hea-properties hea-context-menu')
@action('heaserver-awss3trash-item-restore',
        rel='hea-trash-restore-confirmer hea-context-menu hea-confirm-prompt',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/restorer')
@action('heaserver-awss3trash-item-permanently-delete',
        rel='hea-trash-delete-confirmer hea-context-menu hea-confirm-prompt',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/deleter')
@action('heaserver-awss3trash-item-get-self', rel='self',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}')
@action('heaserver-awss3trash-do-empty-trash', rel='hea-trash-emptier',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trashemptier')
async def get_all_deleted_items_all_buckets(request: web.Request) -> web.Response:
    """
    Gets a list of all deleted items in a volume.

    :param request: the HTTP request.
    :return: the list of items with delete markers.
    ---
    summary: Gets a list of all deleted items.
    tags:
        - heaserver-trash-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to check for deleted files.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    logger = logging.getLogger(__name__)
    sub = request.headers.get(SUB, NONE_USER)
    context: PermissionContext[AWSS3FolderFileTrashItem] = ViewerPermissionContext(sub)
    try:
        volume_id = request.match_info['volume_id']
    except KeyError as e:
        return response.status_bad_request(str(e))
    loop = asyncio.get_running_loop()

    async def coro(app: web.Application) -> web.Response:
        async with S3ClientContext(request, volume_id) as s3:
            async with MongoContext(request) as mongo:
                asyncgens: list[asyncio.Task[Any]] = []
                try:
                    resp_ = await loop.run_in_executor(None, s3.list_buckets)
                    result: list[AWSS3FolderFileTrashItem] = []
                    perms: list[list[Permission]] = []
                    attr_perms: list[dict[str, list[Permission]]] = []
                    for bucket in resp_.get('Buckets', []):
                        async def asyncgen(volume_id: str, bucket_id: str, sub: str | None):
                            metadata_dict = metadata_dict = await _get_deleted_version_metadata(mongo, bucket_id)
                            async for item in _get_deleted_items_private(s3, volume_id, bucket_id, prefix=None, sub_user=sub, metadata_dict=metadata_dict):
                                logger.debug('Got item %s', item)
                                result.append(item)
                                logger.debug('Getting permissions for %s', item)
                                perms.append(await item.get_permissions(context))
                                attr_perms.append(await item.get_all_attribute_permissions(context))
                        bucket_id = bucket['Name']
                        logger.debug('Getting deleted items for bucket %s', bucket_id)
                        asyncgens.append(asyncio.create_task(asyncgen(volume_id, bucket_id, request.headers.get(SUB))))
                    await asyncio.gather(*asyncgens)
                    logger.debug('Generating response...')
                    return await response.get_all(request, tuple(r.to_dict() for r in result),
                                                permissions=perms, attribute_permissions=attr_perms)
                except ValueError as e:
                    return response.status_forbidden(str(e))
    async_requested = PREFERENCE_RESPOND_ASYNC in request.headers.get(PREFER, [])
    if async_requested:
        logger.debug('Asynchronous get all trash')
        global _status_id
        status_location = f'{str(request.url).rstrip("/")}asyncstatus{_status_id}'
        _status_id += 1
        task_name = f'{sub}^{status_location}'
        await request.app[HEA_BACKGROUND_TASKS].add(coro, task_name)
        return response.status_see_other(status_location)
    else:
        logger.debug('Synchronous get all trash')
        return await coro(request.app)

@routes.get('/volumes/{volume_id}/awss3trashasyncstatus{status_id}')
@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3trashasyncstatus{status_id}')
async def get_trash_async_status(request: web.Request) -> web.Response:
    return response.get_async_status(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3trashemptier')
async def do_empty_trash(request: web.Request) -> web.Response:
    """
    Empties a version-enabled bucket's trash.

    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: Empties the bucket's trash.
    tags:
        - heaserver-trash-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
    responses:
      '204':
        $ref: '#/components/responses/204'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _do_empty_trash(request)


@routes.delete('/volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}')
async def permanently_delete_object_with_delete(request: web.Request) -> web.Response:
    """
    Delete all versions of a version enabled file

    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: Permanent file deletion
    tags:
        - heaserver-trash-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume containing file.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to containing file.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '204':
        $ref: '#/components/responses/204'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _permanently_delete_object(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/deleter')
async def permanently_delete_object(request: web.Request) -> web.Response:
    """
    Delete all versions of a version enabled file

    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: Permanent file deletion
    tags:
        - heaserver-trash-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume containing file.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to containing file.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '204':
        $ref: '#/components/responses/204'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _permanently_delete_object(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/restorer')
async def restore_object(request: web.Request) -> web.Response:
    """
    Removes the delete marker for a specified file

    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: File deletion
    tags:
        - heaserver-trash-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '204':
        $ref: '#/components/responses/204'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _undelete_object(request)



@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3trash/{id}/opener')
@action('heaserver-awss3trash-item-open-default',
        rel='hea-opener hea-default application/x.item',
        path='volumes/{volume_id}/buckets/{bucket_id}/awss3trashfolders/{id}/items/',
        itemif='isheaobject(heaobject.folder.AWSS3Folder)')
async def get_trash_item_opener(request: web.Request) -> web.Response:
    """
    Opens the requested trash forder.

    :param request: the HTTP request. Required.
    :return: the opened folder, or Not Found if the requested item does not exist.
    ---
    summary: Folder opener choices
    tags:
        - heaserver-trash-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    result = await _get_deleted_item(request)
    if result is None:
        return await response.get_multiple_choices(request, None)
    else:
        return await response.get_multiple_choices(request, result.to_dict())


def main() -> None:
    config = init_cmd_line(description='Deleted file management',
                           default_port=8080)
    start(package_name='heaserver-trash-aws-s3', db=S3Manager,
          wstl_builder_factory=builder_factory(__package__), config=config)


async def _get_version_objects(s3: S3Client, bucket_id: str, prefix: str | None,
                              loop: asyncio.AbstractEventLoop | None = None) -> AsyncIterator[ListObjectVersionsOutputTypeDef]:
    logger = logging.getLogger(__name__)
    if not loop:
        loop_ = asyncio.get_running_loop()
    else:
        loop_ = loop
    try:
        paginate_partial = partial(s3.get_paginator('list_object_versions').paginate, Bucket=bucket_id)
        if prefix is not None:
            paginate_partial = partial(paginate_partial, Prefix=prefix)
        pages = await loop_.run_in_executor(None, lambda: iter(paginate_partial()))
        while (page := await loop_.run_in_executor(None, next, pages, None)) is not None:
            logger.debug('page %s', page)
            yield page
    except ClientError as e:
        raise awsservicelib.handle_client_error(e)



async def _get_deleted_item(request: web.Request) -> AWSS3FolderFileTrashItem | None:
    logger = logging.getLogger(__name__)
    try:
        volume_id = request.match_info['volume_id']
        bucket_id = request.match_info['bucket_id']
    except KeyError as e:
        raise response.status_bad_request(str(e))
    try:
        item = AWSS3FolderFileTrashItem()
        item.id = request.match_info['id']
        key_ = item.key
    except ValueError as e:
        return None
    async with MongoContext(request) as mongo:
        metadata_dict = await _get_deleted_version_metadata(mongo, bucket_id, id_=item.id)
    try:
        async with S3ClientContext(request, volume_id) as s3:
            async for deleted_item in _get_deleted_items_private(s3, volume_id, bucket_id, key_, request.headers.get(SUB),
                                                                version=item.version, recursive=False,
                                                                metadata_dict=metadata_dict):
                return deleted_item
    except ValueError as e:
        logger.exception('Error getting deleted items')
    return None


async def _get_deleted_version_metadata(mongo: Mongo, bucket_id: str, id_: str | None = None, version: str | None = None) -> dict:
    metadata_dict = {}
    filter = {
        'bucket_id': bucket_id,
        'deleted': True,
    }
    if id_ is not None:
        filter['encoded_key'] = id_
    if version is not None:
        filter['version'] = version
    async for metadata in mongo.get_all_admin(MONGODB_AWS_S3_FOLDER_METADATA_COLLECTION, filter):
        if 'version' in metadata and 'actual_object_type_name' in metadata:
            metadata_dict[(bucket_id, id_, metadata['actual_object_type_name'], metadata['version'])] = metadata
    return metadata_dict


async def _get_deleted_items(request: web.Request, recursive=True) -> AsyncIterator[AWSS3FolderFileTrashItem]:
    """
    Gets all deleted items (with a delete marker) in a volume and bucket.
    The request's match_info is expected to have volume_id and bucket_id keys
    containing the volume id and bucket name, respectively. It can optionally
    contain a folder_id or trash_folder_id, which will restrict returned items
    to a folder or trash folder, respectively.

    :param request: the HTTP request (required).
    :return: an asynchronous iterator of AWSS3FolderFileItems.
    :raises HTTPBadRequest: if the request doesn't have a volume id or bucket
    name.
    """
    try:
        volume_id = request.match_info['volume_id']
        bucket_id = request.match_info['bucket_id']
    except KeyError as e:
        raise response.status_bad_request(str(e))
    folder_id = request.match_info.get('folder_id', None)
    trash_folder_id = request.match_info.get('trash_folder_id', None)
    try:
        if folder_id:
            prefix: str | None = decode_key(folder_id) if folder_id != 'root' else ''
        elif trash_folder_id:
            if trash_folder_id != 'root':
                item = AWSS3FolderFileTrashItem()
                item.id = trash_folder_id
                prefix = item.key
            else:
                prefix = ''
        else:
            prefix = None

        async with S3ClientContext(request, volume_id) as s3:
            async with MongoContext(request) as mongo:
                metadata_dict = await _get_deleted_version_metadata(mongo, bucket_id)
            async for item in _get_deleted_items_private(s3, volume_id, bucket_id, prefix,
                                                            request.headers.get(SUB), recursive=recursive,
                                                            metadata_dict=metadata_dict):
                yield item
    except (KeyDecodeException, ValueError) as e:
        raise response.status_not_found()



#count = 0
def _process_resp(volume_id: str, bucket_id: str, sub_user: str | None, version: str | None, recursive: bool, response_, metadata_dict: dict | None = None) -> Generator[AWSS3FolderFileTrashItem, None, None]:
    logger = logging.getLogger(__name__)
    # count += len(response_.get('Versions', []))
    # if count > MAX_VERSIONS_TO_RETRIEVE:
    #     raise ValueError(f'The bucket {bucket_id} has too many objects to display the trash!')
    def truncate(key: str):
        try:
            return key[:key.index('/') + 1]
        except ValueError:
            return key
    if not recursive:
        truncated_key_dict: dict[str, AWSS3FolderFileTrashItem] = {}
    timezone_aware_min = datetime.min.replace(tzinfo=timezone.utc)
    delete_markers = {item['Key']: item['LastModified'] for item in response_.get('DeleteMarkers', []) if item['IsLatest']}
    if not delete_markers:
        return
    logger.debug('delete_markers: %s', delete_markers)
    # Assume the data coming from AWS is already sorted by Key.
    def version_iter(r, dms):
        # This function is necessary due to python's late binding closures. We need it to bind to the right
        # response_ and delete_markers objects.
        return (vers for vers in r.get('Versions', [])
                    if vers['VersionId'] != 'null' and
                    vers['VersionId'] is not None and
                    (version is None or version == vers['VersionId']) and
                    vers['Key'] in dms)
    non_null_versions = version_iter(response_, delete_markers)
    folder_url = URL('volumes') / volume_id / 'buckets' / bucket_id / 'awss3folders'
    project_url = URL('volumes') / volume_id / 'buckets' / bucket_id / 'awss3projects'
    file_url = URL('volumes') / volume_id / 'buckets' / bucket_id / 'awss3files'
    for key, versions in itertools.groupby(non_null_versions, itemgetter('Key')):
        if not recursive:
            if key not in truncated_key_dict.keys():
                for item in truncated_key_dict.values():
                    yield item
                truncated_key_dict.clear()
        # Versions are returned by S3 in the order in which they are stored, with the most recently stored returned
        # first.
        version_ = next(v for v in versions if v['LastModified'] < delete_markers[key])
        logger.debug('Version response for key %s and version %s', key, version_)
        if version_:
            deleted = delete_markers[key]
            key = key if recursive else truncate(key)
            encoded_key = encode_key(key)
            last_modified = version_['LastModified']
            storage_class = version_['StorageClass']
            size = version_['Size']
            if recursive:
                item = AWSS3FolderFileTrashItem()
            else:
                item = truncated_key_dict.setdefault(key, AWSS3FolderFileTrashItem())
            item.bucket_id = bucket_id
            item.key = key
            item.version = version_['VersionId']
            item.modified = last_modified if recursive else max(item.modified or timezone_aware_min, last_modified)
            item.created = last_modified if recursive else max(item.modified or timezone_aware_min, last_modified)
            item.deleted = deleted
            item.owner = (sub_user if sub_user is not None else NONE_USER) if recursive else NONE_USER
            item.volume_id = volume_id
            item.source = AWS_S3
            item.storage_class = storage_class if recursive else None
            item.size = size if recursive else (item.size or 0) + size
            if is_folder(key):
                metadata = metadata_dict.get((bucket_id, encode_key(key), AWSS3Project.get_type_name(), version_['VersionId'])) if metadata_dict else None
                if metadata is not None:
                    item.actual_object_uri = str(project_url / encoded_key)
                    item.actual_object_type_name = AWSS3Project.get_type_name()
                else:
                    item.actual_object_uri = str(folder_url / encoded_key)
                    item.actual_object_type_name = AWSS3Folder.get_type_name()
            else:
                item.actual_object_uri = str(file_url / encoded_key)
                item.actual_object_type_name = AWSS3FileObject.get_type_name()
            if recursive:
                yield item
    if not recursive:
        yield from truncated_key_dict.values()


async def _get_deleted_items_private(s3: S3Client, volume_id: str, bucket_id: str, prefix: str | None = None,
                                       sub_user: str | None = None, version: str | None = None, recursive=True,
                                       metadata_dict: dict | None = None) -> AsyncGenerator[AWSS3FolderFileTrashItem, None]:
    logger = logging.getLogger(__name__)
    loop_ = asyncio.get_running_loop()

    async for response_ in _get_version_objects(s3, bucket_id, prefix if prefix else '', loop_):
        logger.debug('Processing version object list %s', response_)
        for result in _process_resp(volume_id, bucket_id, sub_user, version, recursive, response_, metadata_dict):
            yield result
        logger.debug('Done processing version object list %s', response_)


async def _undelete_object(request: web.Request) -> web.Response:
    """
    Undeletes a versioned file that was deleted by removing the file's active
    delete marker. A versioned file presents as deleted when its latest version
    is a delete marker. By removing the delete marker, we make the previous
    version the latest version and the file then presents as *not* deleted.

    The volume id must be in the volume_id entry of the
    request's match_info dictionary. The bucket id must be in the bucket_id
    entry of the request's match_info dictionary. The file id must be in the id
    entry of the request's match_info dictionary.

    :param request: the aiohttp Request (required).
    :return: the HTTP response with a 204 status code if the file was
    successfully deleted, 403 if access was denied, 404 if the file was not
    found, 405 if delete marker doesn't have the latest modified time or 500 if
    an internal error occurred.
    """
    logger = logging.getLogger(__name__)
    sub = request.headers.get(SUB, NONE_USER)
    try:
        volume_id = request.match_info['volume_id']
        bucket_name = request.match_info['bucket_id']
        item = AWSS3FolderFileTrashItem()
        item.id = request.match_info['id']
        key_ = item.key
        assert key_ is not None, 'key_ cannot be None'
    except KeyError as e:
        return response.status_bad_request(f'{e} is required')
    except KeyDecodeException as e:
        return response.status_bad_request(f'{e}')

    loop = asyncio.get_running_loop()

    try:
        if not await _get_deleted_item(request):
            return response.status_not_found(f'Object {display_name(key_)} is not in the trash')
        async with S3ClientContext(request, volume_id) as s3_client:
            async with MongoContext(request) as mongo:
                async for response_ in _get_version_objects(s3_client, bucket_name, key_, loop):
                    keyfunc = lambda x: x['Key']

                    # Preflight
                    for key, versions in itertools.groupby(sorted((resp for resp in itertools.chain((vers for vers in response_['DeleteMarkers'] if vers['VersionId'] != 'null'), (vers for vers in response_.get('Versions', []) if vers['VersionId'] != 'null'))), key=keyfunc), key=keyfunc):
                        resps = sorted(versions, key=lambda x: x['LastModified'], reverse=True)
                        if resps and 'Size' in resps[0]:
                            if not is_folder(resps[0]['Key']):
                                return response.status_bad_request(f'Object {display_name(key)} has been overwritten')

                    # Actual
                    key_to_version: dict[str, str | None] = {}
                    for key, versions in itertools.groupby(sorted((resp for resp in itertools.chain((vers for vers in response_['DeleteMarkers'] if vers['VersionId'] != 'null'), (vers for vers in response_.get('Versions', []) if vers['VersionId'] != 'null'))), key=keyfunc), key=keyfunc):
                        resps = sorted(versions, key=lambda x: x['LastModified'], reverse=True)

                        for resp_ in resps:
                            if 'Size' not in resp_:  # Delete the delete markers until we reach actual version objects.
                                await loop.run_in_executor(None, partial(s3_client.delete_object, Bucket=bucket_name, Key=resp_['Key'], VersionId=resp_['VersionId']))
                                key_to_version[key] = resp_['VersionId']
                            else:
                                break
                    path = key_
                    while path:
                        if is_folder(path):
                            logger.debug('Checking for metadata for %s', path)
                            metadata = await mongo.get_admin_nondesktop_object(MONGODB_AWS_S3_FOLDER_METADATA_COLLECTION, mongoattributes={'bucket_id': bucket_name, 'encoded_key': encode_key(path), 'version': key_to_version.get(path)})
                            if metadata is not None:
                                metadata['deleted'] = False
                                metadata['version'] = None
                                logger.debug('Updating metadata %s for %s', metadata, path)
                                await mongo.update_admin_nondesktop_object(metadata, MONGODB_AWS_S3_FOLDER_METADATA_COLLECTION)
                        path = parent(path)
        request.app[HEA_CACHE].pop((sub, volume_id, bucket_name, item.id, None, 'items'), None)
    except ClientError as e:
        return awsservicelib.handle_client_error(e)

    return response.status_no_content()


# async def rollback_file(request: web.Request) -> web.Response:
#     """
#     Makes the specified version the current version by deleting all recent versions
#     The volume id must be in the volume_id entry of the
#     request's match_info dictionary. The bucket id must be in the bucket_id entry of the request's match_info
#     dictionary. The file id must be in the id entry of the request's match_info dictionary.
#     And the version_id must be in the version id entry of the request's match_info dictionary.

#     :param request: the aiohttp Request (required).
#     :return: the HTTP response with a 204 status code if the file was successfully deleted, 403 if access was denied,
#     404 if the file was not found, 405 if delete marker doesn't have the latest modified time or 500 if an internal error occurred.
#     """
#     logger = logging.getLogger(__name__)

#     if 'volume_id' not in request.match_info:
#         return response.status_bad_request('volume_id is required')
#     if 'bucket_id' not in request.match_info:
#         return response.status_bad_request('bucket_id is required')
#     if 'id' not in request.match_info and 'name' not in request.match_info:
#         return response.status_bad_request('either id or name is required')
#     if 'version_id' not in request.match_info:
#         return response.status_bad_request('version_id is required')

#     volume_id = request.match_info['volume_id']
#     bucket_name = request.match_info['bucket_id']
#     file_name = request.match_info['id'] if 'id' in request.match_info else request.match_info['name']
#     version_id = request.match_info['version_id']

#     loop = asyncio.get_running_loop()

#     try:
#         s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)

#         # Get the latest version for the object.
#         vresponse = await loop.run_in_executor(None, partial(s3_client.meta.client.list_object_versions(Bucket=bucket_name, Prefix=file_name)))

#         if version_id in [ver['VersionId'] for ver in vresponse['Versions']]:
#             for version in vresponse['Versions']:
#                 if (version['VersionId'] != version_id) and (version['Key'] == file_name):
#                     s3_client.ObjectVersion(
#                         bucket_name, file_name, version['VersionId']).delete()
#                 else:
#                     break

#         else:
#             return response.status_bad_request(f"{version_id} was not found in the list of versions for "f"{file_name}.")

#     except ClientError as e:
#         return awsservicelib.handle_client_error(e)

#     return await get_file(request)


# async def rollforward_file(request: web.Request) -> web.Response:
#     """
#     Makes the specified version the current version by deleting all recent versions
#     The volume id must be in the volume_id entry of the
#     request's match_info dictionary. The bucket id must be in the bucket_id entry of the request's match_info
#     dictionary. The file id must be in the id entry of the request's match_info dictionary.
#     And the version_id must be in the version id entry of the request's match_info dictionary.

#     :param request: the aiohttp Request (required).
#     :return: the HTTP response with a 204 status code if the file was successfully deleted, 403 if access was denied,
#     404 if the file was not found, 405 if delete marker doesn't have the latest modified time or 500 if an internal error occurred.
#     """
#     logger = logging.getLogger(__name__)

#     if 'volume_id' not in request.match_info:
#         return response.status_bad_request('volume_id is required')
#     if 'bucket_id' not in request.match_info:
#         return response.status_bad_request('bucket_id is required')
#     if 'id' not in request.match_info and 'name' not in request.match_info:
#         return response.status_bad_request('either id or name is required')
#     if 'version_id' not in request.match_info:
#         return response.status_bad_request('version_id is required')

#     volume_id = request.match_info['volume_id']
#     bucket_name = request.match_info['bucket_id']
#     file_name = request.match_info['id'] if 'id' in request.match_info else request.match_info['name']
#     version_id = request.match_info['version_id']

#     loop = asyncio.get_running_loop()

#     try:
#         s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)

#         # copy the specified version into the file
#         copy_source = {'Bucket': bucket_name,
#                        'Key': file_name, 'VersionId': version_id}

#         s3_client.meta.client.copy_object(
#             CopySource=copy_source, Bucket=bucket_name, Key=file_name)

#         # delete the original version
#         s3_client.ObjectVersion(bucket_name, file_name, version_id).delete()

#     except ClientError as e:
#         return awsservicelib.handle_client_error(e)

#     return await get_file(request)


async def _permanently_delete_object(request: web.Request) -> web.Response:
    """
    Makes the specified version the current version by deleting all recent versions
    The volume id must be in the volume_id entry of the
    request's match_info dictionary. The bucket id must be in the bucket_id entry of the request's match_info
    dictionary. The file id must be in the id entry of the request's match_info dictionary.
    And the version_id must be in the version id entry of the request's match_info dictionary.

    :param request: the aiohttp Request (required).
    :return: the HTTP response with a 204 status code if the file was successfully deleted, 403 if access was denied,
    404 if the file was not found, 405 if delete marker doesn't have the latest modified time or 500 if an internal error occurred.
    """
    logger = logging.getLogger(__name__)

    try:
        volume_id = request.match_info['volume_id']
        bucket_name = request.match_info['bucket_id']
        item = AWSS3FolderFileTrashItem()
        item.id = request.match_info['id']
        key = item.key
        assert key is not None, 'key cannot be None'
        version = item.version
    except KeyError as e:
        return response.status_bad_request(f'{e} is required')
    except (ValueError, KeyDecodeException) as e:
        return response.status_not_found()

    loop = asyncio.get_running_loop()

    try:
        async with S3ClientContext(request, volume_id) as s3_client:
            async with MongoContext(request) as mongo:
                async for response_ in _get_version_objects(s3_client, bucket_name, key, loop):
                    delete_markers_to_delete: list[DeleteMarkerEntryTypeDef | ObjectVersionTypeDef] = []
                    versions_to_delete: list[DeleteMarkerEntryTypeDef | ObjectVersionTypeDef] = []
                    delete_marker = False
                    for resp_ in sorted((resp for resp in itertools.chain((vers for vers in response_.get('DeleteMarkers', []) if vers['VersionId'] != 'null'), (vers for vers in response_.get('Versions', []) if vers['VersionId'] != 'null')) if resp['Key'] == key), key=lambda x: x['LastModified'], reverse=True):
                        if not delete_marker and resp_['VersionId'] == version:
                            delete_marker = True
                            delete_markers_to_delete.append(resp_)
                            continue
                        if delete_marker and 'Size' not in resp_ and versions_to_delete:
                            delete_marker = False
                            break
                        if 'Size' not in resp_:
                            delete_markers_to_delete.append(resp_)
                        else:
                            versions_to_delete.append(resp_)
                    if not delete_markers_to_delete:
                        return response.status_not_found(f'Object {display_name(key)} is not in the trash')
                    for version_to_delete in itertools.chain(versions_to_delete, delete_markers_to_delete):
                        await loop.run_in_executor(None, partial(s3_client.delete_object, Bucket=bucket_name, Key=key, VersionId=version_to_delete['VersionId']))
                        await mongo.delete_admin(MONGODB_AWS_S3_FOLDER_METADATA_COLLECTION, mongoattributes={'bucket_id': bucket_name, 'encoded_key': item.id, 'version': version_to_delete['VersionId']})
                    path = key
                    logger.debug('About to check versions for %s', path)
                    while path := parent(path):
                        logger.debug('Checking versions for %s', path)
                        async for _ in awsservicelib.list_object_versions(s3_client, bucket_name, path):
                            logger.debug('Found versions for %s', path)
                            break
                        else:
                            logger.debug('No versions found for %s', path)
                            await mongo.delete_admin(MONGODB_AWS_S3_FOLDER_METADATA_COLLECTION, mongoattributes={'bucket_id': bucket_name, 'encoded_key': encode_key(path), 'version': None})

    except ClientError as e:
        return awsservicelib.handle_client_error(e)

    return response.status_no_content()


async def _do_empty_trash(request: web.Request) -> web.Response:
    """
    Makes the specified version the current version by deleting all recent versions
    The volume id must be in the volume_id entry of the
    request's match_info dictionary. The bucket id must be in the bucket_id entry of the request's match_info
    dictionary. The file id must be in the id entry of the request's match_info dictionary.
    And the version_id must be in the version id entry of the request's match_info dictionary.

    :param request: the aiohttp Request (required).
    :return: the HTTP response with a 204 status code if the file was successfully deleted, 403 if access was denied,
    404 if the file was not found, 405 if delete marker doesn't have the latest modified time or 500 if an internal error occurred.
    """
    logger = logging.getLogger(__name__)

    try:
        volume_id = request.match_info['volume_id']
        bucket_name = request.match_info['bucket_id']
    except KeyError as e:
        return response.status_bad_request(f'{e} is required')

    loop = asyncio.get_running_loop()

    try:
        async with S3ClientContext(request, volume_id) as s3_client:
            async with MongoContext(request) as mongo:
                async for response_ in _get_version_objects(s3_client, bucket_name, None, loop):
                    keyfunc = lambda x: x['Key']
                    for key, versions in itertools.groupby(sorted((resp for resp in itertools.chain((vers for vers in response_.get('DeleteMarkers', []) if vers['VersionId'] != 'null'), (vers for vers in response_.get('Versions', []) if vers['VersionId'] != 'null'))), key=keyfunc), key=keyfunc):
                        delete_markers_to_delete = []
                        versions_to_delete = []
                        delete_markers = True
                        for resp_ in sorted((resp for resp in versions), key=lambda x: x['LastModified'], reverse=True):
                            if delete_markers and 'Size' not in resp_:
                                delete_markers_to_delete.append(resp_)
                            elif 'Size' in resp_ and delete_markers_to_delete:
                                delete_markers = False
                                versions_to_delete.append(resp_)
                            else:
                                break
                        for version_to_delete in itertools.chain(versions_to_delete, delete_markers_to_delete):
                            await loop.run_in_executor(None, partial(s3_client.delete_object, Bucket=bucket_name, Key=key, VersionId=version_to_delete['VersionId']))
                            await mongo.delete_admin(MONGODB_AWS_S3_FOLDER_METADATA_COLLECTION, mongoattributes={'bucket_id': bucket_name, 'encoded_key': encode_key(key), 'version': version_to_delete['VersionId']})

    except ClientError as e:
        return awsservicelib.handle_client_error(e)

    return response.status_no_content()
