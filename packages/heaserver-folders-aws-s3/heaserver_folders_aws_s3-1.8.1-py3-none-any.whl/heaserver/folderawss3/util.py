

from collections.abc import Mapping, Callable, Awaitable, Iterator
from datetime import datetime, timezone
import logging
from typing import Any
from uuid import uuid4
from aiohttp import hdrs, web, client_exceptions
from heaobject.aws import S3StorageClass, S3Object
from heaobject.awss3key import display_name, encode_key, is_folder, replace_parent_folder, join, split, parent, decode_key, KeyDecodeException
from heaobject.root import DesktopObject
from heaobject.user import NONE_USER
from heaobject.activity import Activity
from heaserver.service.appproperty import HEA_CACHE, HEA_MESSAGE_BROKER_PUBLISHER
from heaserver.service.backgroundtasks import BackgroundTasks
from heaserver.service.db import awsservicelib, aws, mongo
from heaserver.service import response
from heaserver.service.oidcclaimhdrs import SUB
from heaserver.service.messagebroker import publish_desktop_object

from humanize import naturaldelta
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import ObjectTypeDef, CommonPrefixTypeDef, HeadObjectOutputTypeDef
import asyncio
from zipfile import ZipFile, ZipInfo
from functools import partial
from heaserver.service.util import queued_processing
from botocore.exceptions import ClientError as BotoClientError
from heaserver.service.activity import DesktopObjectAction
import time
import io
import threading

MONGODB_AWS_S3_FOLDER_METADATA_COLLECTION = 'awss3foldersmetadata'


async def response_folder_as_zip(s3_client: S3Client, request: web.Request, bucket_name: str, folder_key: str) -> web.StreamResponse:
    """
    Creates a HTTP streaming response with the contents of all S3 objects with the given prefix packaged into a ZIP
    file. S3 allows folders to have no name (just a slash), and for maximum compatibility with operating systems like
    Windows that do not, such folders are replaced in the zip file with "No name <random string>". The resulting ZIP
    files are uncompressed, but this may change in the future. Files that cannot be downloaded are returned as zero
    byte files. Objects in an incompatible storage class are skipped.

    :param s3_client: the S3Client (required).
    :param request: the HTTP request (required).
    :param bucket_name: the bucket name (required).
    :param folder_key: the folder key (required).
    :return: the HTTP response.
    """
    logger = logging.getLogger(__name__)
    folder_display_name = display_name(folder_key)
    if not folder_display_name:
        folder_display_name = 'archive'

    response_ = web.StreamResponse(status=200, reason='OK',
                                               headers={hdrs.CONTENT_DISPOSITION: f'attachment; filename={folder_display_name}.zip'})
    response_.content_type = 'application/zip'
    await response_.prepare(request)
    class FixedSizeBuffer:
        def __init__(self, size: int) -> None:
            self.size = size
            self.buffer = io.BytesIO()
            self.condition = threading.Condition()
            self.length = 0  # length of current content
            self.eof = False
            self.closed = False

        def write(self, b: bytes | bytearray) -> int:
            if not isinstance(b, (bytes, bytearray)):
                raise TypeError(f"a bytes-like object is required, not '{type(b).__name__}'")
            with self.condition:
                if self.eof:
                    raise ValueError('Cannot write to buffer after EOF has been set')
                while not self.closed and len(b) > self.size - self.length:
                    self.condition.wait()  # Wait until there is enough space
                self.buffer.seek(self.length % self.size)
                written = self.buffer.write(b)
                self.length += written
                self.condition.notify_all()  # Notify any waiting threads
                return written

        def read(self, size: int = -1) -> bytes:
            with self.condition:
                while not self.closed and self.length == 0:
                    if self.eof:
                        logger.debug('Reading empty bytes due to EOF')
                        return b''
                    self.condition.wait()  # Wait until there is data to read

                if size == -1 or size > self.length:
                    size = self.length

                self.buffer.seek((self.length - size) % self.size)
                result = self.buffer.read(size)
                self.length -= size
                self.condition.notify_all()  # Notify any waiting threads
                return result

        def truncate(self, size: int | None = None) -> int:
            with self.condition:
                if size is None:
                    size = self.buffer.tell()
                self.buffer.truncate(size)
                logger.debug('Truncated')
                self.length = min(self.length, size)
                self.condition.notify_all()
                return size

        def flush(self) -> None:
            with self.condition:
                self.buffer.flush()
                logger.debug('Flushed')

        def set_eof(self) -> None:
            logger.debug('Waiting to set EOF')
            with self.condition:
                logger.debug('Setting EOF')
                self.eof = True
                self.condition.notify_all()

        def close(self) -> None:
            with self.condition:
                self.buffer.close()
                logger.debug('Closed')
                self.closed = True
                self.condition.notify_all()



    fileobj = FixedSizeBuffer(1024*10)
    def list_objects(s3: S3Client,
                    bucket_id: str,
                    prefix: str | None = None,
                    max_keys: int | None = None,
                    delimiter: str | None = None,
                    include_restore_status: bool | None = None) -> Iterator[ObjectTypeDef | CommonPrefixTypeDef]:
        list_partial = partial(s3.get_paginator('list_objects_v2').paginate, Bucket=bucket_id)
        if max_keys is not None:
            list_partial = partial(list_partial, PaginationConfig={'MaxItems': max_keys})
        if prefix is not None:  # Boto3 will raise an exception if Prefix is set to None.
            list_partial = partial(list_partial, Prefix=prefix)
        if delimiter is not None:
            list_partial = partial(list_partial, Delimiter=delimiter)
        if include_restore_status is not None and include_restore_status:
            list_partial = partial(list_partial, OptionalObjectAttributes=['RestoreStatus'])
        pages = iter(list_partial())
        while (page := next(pages, None)) is not None:
            for common_prefix in page.get('CommonPrefixes', []):
                yield common_prefix
            for content in page.get('Contents', []):
                yield content

    import queue
    q: queue.Queue[Exception] = queue.Queue()
    def zip_all(q):
        try:
            logger.debug('Starting zip...')
            #with ZipFile(fileobj, mode='w', compression=ZIP_DEFLATED) as zf:
            with ZipFile(fileobj, mode='w') as zf:
                for obj in list_objects(s3_client, bucket_name, folder_key, include_restore_status=True):
                    try:
                        folder = obj['Key'].removeprefix(folder_key)
                        if not folder:
                            continue
                        if obj['StorageClass'] in (S3StorageClass.STANDARD.name, S3StorageClass.GLACIER_IR.name)\
                            or ((restore:= obj.get('RestoreStatus')) and restore.get('RestoreExpiryDate')):
                            filename = _fill_in_folders_with_no_name(folder)
                            zinfo = ZipInfo(filename=filename, date_time=obj['LastModified'].timetuple()[:6])
                            zinfo.file_size = obj['Size']
                            # zinfo.compress_type = ZIP_DEFLATED  # Causes downloads to hang, possibly because something gets confused about file size.
                            if zinfo.is_dir():  # Zip also denotes a folders as names ending with a slash.
                                zf.writestr(zinfo, '')
                            else:
                                logger.debug('Zipping %s', obj['Key'])
                                with zf.open(zinfo, mode='w') as dest:
                                    body = s3_client.get_object(Bucket=bucket_name, Key=obj['Key'])['Body']
                                    try:
                                        while True:
                                            data = body.read(1024 * 10)
                                            if not data:
                                                break
                                            dest.write(data)
                                    finally:
                                        body.close()
                                logger.debug('Zipping %s complete', filename)
                    except BotoClientError as e:
                        logger.warning('Error downloading %s in bucket %s: %s', obj['Key'], bucket_name, e)
                logger.debug('All files zipped')
            logger.debug('Entire zipfile generated')
            fileobj.set_eof()
            logger.debug('Sent EOF')
        except Exception as e:
            q.put(e)
    thread = threading.Thread(target=zip_all, args=(q,))
    thread.start()
    try:
        loop = asyncio.get_running_loop()
        while True:
            while True:
                if not q.empty():
                    raise q.get()
                try:
                    data = await asyncio.wait_for(loop.run_in_executor(None, fileobj.read, 1024 * 10), timeout=1)
                    break
                except TimeoutError:
                    continue
            if not data:
                break
            await response_.write(data)
        await response_.write_eof()
        if not q.empty():
            raise q.get()
    except client_exceptions.ClientConnectionResetError:
        logger.info('Lost connection with the browser making zipfile %s, probably because the user closed/refreshed their tab or lost their internet connection', folder_key)
    finally:
        fileobj.close()
        thread.join()

    logger.debug('Done writing Zipfile to response stream')
    return response_


def _fill_in_folders_with_no_name(filename: str) -> str:
    """
    S3 allows folders to have no name (just a slash). This function replaces those "empty" names with a randomly
    generated name.

    :param filename: the filename.
    :return: the filename with empty names replaced.
    """
    logger = logging.getLogger(__name__)
    def split_and_rejoin(fname_: str) -> str:
        return '/'.join(part if part else f'No name {str(uuid4())}' for part in fname_.split('/'))
    if is_folder(filename):
        filename = split_and_rejoin(filename.rstrip('/')) + '/'
    else:
        filename = split_and_rejoin(filename)
    logger.debug('filename to download %s', filename)
    return filename


def set_file_source(obj: Mapping[str, Any], item: DesktopObject):
    item.source = None
    item.source_detail = None
    retrieval = obj.get('RestoreStatus')
    if retrieval is not None:
        if (retrieval.get("IsRestoreInProgress")):
            item.source = "AWS S3 (Unarchiving...)"
            item.source_detail = "Typically completes within 12 hours"
        if (retrieval.get("RestoreExpiryDate") is not None):
            item.source = "AWS S3 (Unarchived)"
            temporarily_available_until = retrieval.get("RestoreExpiryDate")
            item.source_detail = f"Available for {naturaldelta(temporarily_available_until - datetime.now(timezone.utc))}"
    if item.source is None:
        s = f'AWS S3 ({S3StorageClass[obj["StorageClass"]].display_name})'
        item.source = s
        item.source_detail = s


async def move_object(s3_client: S3Client, source_bucket_id: str, source_key: str, target_bucket_id: str, target_key: str,
               move_completed_cb: Callable[[str, str, str | None, str, str, str | None], Awaitable[None]] | None = None):
    """
    Moves object with source_key and in source_bucket_id to target_bucket_id and target_key. A preflight process
    checks whether the object (or for a folder, every object in the folder) is movable.

    :param s3_client: the S3 client (required).
    :param source_bucket_id: the source bucket name (required).
    :param source_key: the key of the object to move (required).
    :param target_bucket_id: the name of the target bucket (required).
    :param target_key: the key of the target folder (required).
    :param move_completed_cb: a callback that is invoked upon successfully moving an object (optional). For folders,
    this function is invoked separately for every object within the folder.
    :raises HTTPBadRequest: if preflight fails.
    :raises BotoClientError: if an error occurs while attempting to move the object (or for folders, the folder's
    contents).
    """
    logger = logging.getLogger(__name__)
    loop = asyncio.get_running_loop()
    def copy_and_delete(source_key, target_key) -> HeadObjectOutputTypeDef:
        s3_client.copy(CopySource={'Bucket': source_bucket_id, 'Key': source_key}, Bucket=target_bucket_id, Key=target_key)
        s3_client.delete_object(Bucket=source_bucket_id, Key=source_key)
        return s3_client.head_object(Bucket=target_bucket_id, Key=target_key)
    async def gen():
        # Preflight
        cached_values = []
        async for obj in awsservicelib.list_objects(s3_client, source_bucket_id, source_key, max_keys=1000, loop=loop, include_restore_status=True):
            if obj['StorageClass'] in (S3StorageClass.DEEP_ARCHIVE.name, S3StorageClass.GLACIER.name) and not ((restore := obj.get('RestoreStatus')) and restore.get('RestoreExpiryDate')):
                raise response.status_bad_request(f'{awsservicelib._activity_object_display_name(source_bucket_id, source_key)} contains archived objects')
            elif len(cached_values) < 1000:
                cached_values.append(obj)
        if len(cached_values) <= 1000:
            for val in cached_values:
                yield val
        else:
            async for obj in awsservicelib.list_objects(s3_client, source_bucket_id, source_key, max_keys=1000, loop=loop):
                yield obj
    async def obj_processor(obj):
        source_key_ = obj['Key']
        target_key_ = replace_parent_folder(source_key=source_key_, target_key=target_key, source_key_folder=source_key)
        logger.debug('Moving %s/%s to %s/%s', source_bucket_id, source_key_, target_bucket_id, target_key_)
        resp_ = await loop.run_in_executor(None, partial(copy_and_delete, source_key_, target_key_))
        if move_completed_cb:
            await move_completed_cb(source_bucket_id, source_key_, obj.get('VersionId'), target_bucket_id, target_key_, resp_.get('VersionId'))
    await queued_processing(gen, obj_processor)


async def clear_target_in_cache(request):
    logger = logging.getLogger(__name__)
    logger.debug('clearing target in cache')
    sub = request.headers.get(SUB, NONE_USER)
    _, target_bucket_name, target_folder_name, target_volume_id = await awsservicelib._copy_object_extract_target(
            await request.json())
    logger.debug('Target bucket %s, folder %s, volume %s', target_bucket_name, target_folder_name, target_volume_id)
    request.app[HEA_CACHE].pop(
            (sub, target_volume_id, target_bucket_name, encode_key(target_folder_name) if target_folder_name else 'root', None, 'items'), None)


def client_line_ending(request: web.Request) -> str:
    """
    Returns the web client's line ending.

    :return: the web client's line ending.
    """
    user_agent = request.headers.get(hdrs.USER_AGENT, 'Windows')
    return '\r\n' if 'Windows' in user_agent else '\n'


async def get_result_or_see_other(background_tasks: BackgroundTasks, task_name: str, status_location: str) -> web.Response:
    start_time = time.time()
    await asyncio.sleep(0)
    while (time.time() - start_time < 30) and not background_tasks.done(task_name):
        await asyncio.sleep(.1)
    if background_tasks.done(task_name):
        error = background_tasks.error(task_name)
        if error:
            background_tasks.remove(task_name)
            # In case we get an exception other than an HTTPException, raise it so it gets wrapped in an internal server
            # error response.
            raise error
        else:
            resp = background_tasks.result(task_name)
            background_tasks.remove(task_name)
            return resp
    else:
        return response.status_see_other(status_location)


async def move(activity: DesktopObjectAction, request: web.Request, mongo_client: mongo.Mongo, sub: str,
               volume_id: str, bucket_id: str, id_: str, key: str, target_volume_id: str, target_bucket_id,
               target_key_parent: str, type_: type[S3Object]) -> web.Response:
    target_key = join(target_key_parent, split(key)[1])
    return await _move_rename(activity, request, mongo_client, sub, volume_id, bucket_id, id_, key, type_,
                              target_bucket_id, target_key, target_volume_id)


async def rename(activity: DesktopObjectAction, request: web.Request, mongo_client: mongo.Mongo, sub: str,
                 volume_id: str, bucket_id: str, id_: str, old_key: str, s3_object:
                 S3Object, type_: type[S3Object]) -> web.Response:
    if not s3_object.key:
        return response.status_bad_request(f'Invalid project key {s3_object.key}')
    if old_key != s3_object.key:
        if bucket_id != s3_object.bucket_id:
            return response.status_bad_request(f"The project's bucket id was {s3_object.bucket_id} but the URL's bucket id was {bucket_id}")

    return await _move_rename(activity, request, mongo_client, sub, volume_id, bucket_id, id_, old_key, type_,
                            bucket_id, s3_object.key, volume_id)


async def _move_rename(activity: DesktopObjectAction, request: web.Request, mongo_client: mongo.Mongo,
                       sub: str, volume_id: str, bucket_id: str, id_: str, key: str, type_: type[S3Object],
                       target_bucket_id: str, target_key: str, new_volume_id: str) -> web.Response:
    """
    :param target_key: the folder/file to move or rename appended to a target path.
    """
    activity.old_object_id = id_
    activity.old_object_uri = f'volumes/{volume_id}/buckets/{bucket_id}/awss3projects/{id_}'
    activity.old_object_type_name = type_.get_type_name()
    activity.old_volume_id = volume_id
    async with aws.S3ClientContext(request=request, volume_id=volume_id) as s3_client:
        try:
            target_id = encode_key(target_key)
            versioned = await awsservicelib.get_latest_object_version(s3_client, bucket_id, key)
            processed_keys: set[str] = set()
            async def move_completed(source_bucket_id: str, source_key_: str, source_version: str | None, target_bucket_id: str, target_key_: str, target_version: str | None):
                path = source_key_
                target_key__ = target_key_
                metadata_ = await mongo_client.get_admin_nondesktop_object(MONGODB_AWS_S3_FOLDER_METADATA_COLLECTION,
                                                                                    {'bucket_id': source_bucket_id,
                                                                                    'encoded_key': encode_key(path),
                                                                                    '$or': [{'deleted': False}, {'deleted': {'$exists': False}}]})
                while path:
                    if path not in processed_keys:
                        if versioned:
                            if metadata_ is not None:
                                metadata_['deleted'] = False
                                metadata_['version'] = target_version
                                metadata_['encoded_key'] = encode_key(target_key__)
                                metadata_['volume_id'] = new_volume_id
                                metadata_['bucket_id'] = target_bucket_id
                                if not (parent_encoded_key := encode_key(parent(target_key__))):
                                    parent_encoded_key = 'root'
                                metadata_['parent_encoded_key'] = parent_encoded_key
                                await mongo_client.update_admin_nondesktop_object(metadata_, MONGODB_AWS_S3_FOLDER_METADATA_COLLECTION)
                        else:
                            await mongo_client.delete_admin(MONGODB_AWS_S3_FOLDER_METADATA_COLLECTION,
                                                            mongoattributes={'bucket_id': source_bucket_id,
                                                                            'encoded_key': encode_key(path),
                                                                            'deleted': False})
                            if metadata_ is not None:
                                new_metadata: dict[str, Any] = {}
                                new_metadata['bucket_id'] = target_bucket_id
                                new_metadata['encoded_key'] = encode_key(target_key__)
                                if not (parent_encoded_key := encode_key(parent(target_key__))):
                                    parent_encoded_key = 'root'
                                new_metadata['parent_encoded_key'] = parent_encoded_key
                                new_metadata['deleted'] = False
                                new_metadata['volume_id'] = new_volume_id
                                new_metadata['version'] = target_version
                                new_metadata['actual_object_type_name'] = metadata_['actual_object_type_name']

                                await mongo_client.insert_admin_nondesktop_object(new_metadata,
                                                                                MONGODB_AWS_S3_FOLDER_METADATA_COLLECTION)
                        processed_keys.add(path)
                    path = parent(path)
                    target_key__ = parent(target_key__)
                    if len(path) < len(target_key):
                        break
                    else:
                        metadata_ = await mongo_client.get_admin_nondesktop_object(MONGODB_AWS_S3_FOLDER_METADATA_COLLECTION,
                                                                                {'bucket_id': source_bucket_id,
                                                                                    'encoded_key': encode_key(path),
                                                                                    '$or': [{'deleted': False}, {'deleted': {'$exists': False}}]})
            await move_object(s3_client=s3_client, source_bucket_id=bucket_id, source_key=key,
                    target_bucket_id=target_bucket_id, target_key=target_key,
                    move_completed_cb=move_completed)
            request.app[HEA_CACHE].pop((sub, volume_id, bucket_id, None, 'actual'), None)
            request.app[HEA_CACHE].pop((sub, volume_id, bucket_id, id_, 'actual'), None)
            if not (folder_id := encode_key(parent(key))):
                folder_id = 'root'
            request.app[HEA_CACHE].pop((sub, volume_id, bucket_id, folder_id, None, 'items'), None)
            request.app[HEA_CACHE].pop((sub, volume_id, bucket_id, folder_id, id_, 'items'), None)
            if not (target_id_parent := encode_key(parent(target_key))):
                target_id_parent = 'root'
            request.app[HEA_CACHE].pop((sub, new_volume_id, target_bucket_id, target_id_parent, None, 'items'), None)

            activity.new_volume_id = new_volume_id
            activity.new_object_type_name = activity.old_object_type_name
            activity.new_object_id = target_id
            activity.new_object_uri = f'volumes/{volume_id}/buckets/{target_bucket_id}/awss3projects/{activity.new_object_id}'
            return response.status_no_content()
        except BotoClientError as e:
            raise awsservicelib.handle_client_error(e)
        except ValueError as e:
            raise response.status_internal_error(str(e))


async def copy(request: web.Request, mongo_client: mongo.Mongo, target_key: str, new_volume_id: str,
               status_location: str | None = None) -> web.Response:
    """
    :param target_key: the folder/file to move or rename appended to a target path.
    :param status_location: if provided, will cause the response to be 303 with this location in the Location header,
    and the copy will be performed asynchronously. Otherwise, the copy will happen synchronously with a 201 response
    success status code or an error status.
    """

    try:
        processed_keys: set[str] = set()
        async def copy_completed(source_bucket_id: str, source_key_: str, target_bucket_id: str, target_key_: str):
            path = source_key_
            target_key__ = target_key_
            metadata_ = await mongo_client.get_admin_nondesktop_object(MONGODB_AWS_S3_FOLDER_METADATA_COLLECTION,
                                                                                {'bucket_id': source_bucket_id,
                                                                                'encoded_key': encode_key(path),
                                                                                '$or': [{'deleted': False}, {'deleted': {'$exists': False}}]})
            while path:
                if path not in processed_keys:
                    if metadata_ is not None:
                        new_metadata: dict[str, Any] = {}
                        new_metadata['bucket_id'] = target_bucket_id
                        new_metadata['encoded_key'] = encode_key(target_key__)
                        if not (parent_encoded_key := encode_key(parent(target_key__))):
                            parent_encoded_key = 'root'
                        new_metadata['parent_encoded_key'] = parent_encoded_key
                        new_metadata['deleted'] = False
                        new_metadata['volume_id'] = new_volume_id
                        new_metadata['actual_object_type_name'] = metadata_['actual_object_type_name']

                        await mongo_client.insert_admin_nondesktop_object(new_metadata,
                                                                        MONGODB_AWS_S3_FOLDER_METADATA_COLLECTION)
                    processed_keys.add(path)
                path = parent(path)
                target_key__ = parent(target_key__)
                if len(path) < len(target_key):
                    break
                else:
                    metadata_ = await mongo_client.get_admin_nondesktop_object(MONGODB_AWS_S3_FOLDER_METADATA_COLLECTION,
                                                                            {'bucket_id': source_bucket_id,
                                                                                'encoded_key': encode_key(path),
                                                                                '$or': [{'deleted': False}, {'deleted': {'$exists': False}}]})
        async def publish_desktop_object_and_clear_cache(app: web.Application, desktop_object: DesktopObject,
                                                    appproperty_=HEA_MESSAGE_BROKER_PUBLISHER):
            if isinstance(desktop_object, Activity):
                await clear_target_in_cache(request)
            await publish_desktop_object(app, desktop_object, appproperty_)

        if status_location:
            return await awsservicelib.copy_object_async(request, status_location,
                                                        activity_cb=publish_desktop_object_and_clear_cache,
                                                        copy_object_completed_cb=copy_completed)
        else:
            return await awsservicelib.copy_object(request, activity_cb=publish_desktop_object_and_clear_cache,
                                                   copy_object_completed_cb=copy_completed)
    except BotoClientError as e:
        raise awsservicelib.handle_client_error(e)
    except ValueError as e:
        raise response.status_internal_error(str(e))
