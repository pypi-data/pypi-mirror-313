# HEA Server AWS S3 Bucket Folders Microservice
[Research Informatics Shared Resource](https://risr.hci.utah.edu), [Huntsman Cancer Institute](https://healthcare.utah.edu/huntsmancancerinstitute/),
Salt Lake City, UT

The HEA Server AWS S3 Bucket Folders Microservice manages folders in AWS S3 buckets.

## Version 1.8.1
* Fixed bug where copy fails if the target folder contains an object with a name that is a prefix of the object to be copied.
* Performance improvements.

## Version 1.8.0
* Added support for python 3.12.
* Improved performance of getting projects.

## Version 1.7.1
* Fixed regression causing move to fail.

## Version 1.7.0
* Removed integration tests that overlap with the unit tests.
* Accept the data query parameter for get requests for a speed boost.

## Version 1.6.1
* Dependency upgrades for compatibility with heaserver-keychain 1.5.0.
* Fixed wrong readOnly status for a trash item's size attribute in unit test.

## Version 1.6.0
* Make metadata follow objects during moves, copies, renames, and trash restores.
* Clear cache properly after deleting and restoring objects.
* Clear cache properly after moves, copies, and renames.
* Merged trash microservice.

## Version 1.5.6
* Fixed regression causing the service to crash when the user closes their browser in the middle of a download.

## Version 1.5.5
* Only resort to asynchronous get-items call when the call has taken longer than 30 seconds to come back.
* Use cache when retrieving file desktop objects.
* Fixed caching issue when moving a file from the root of a bucket.
* Reimplemented download to work with aiohttp 3.10.

## Version 1.5.4
* Fixed stale cache when converting a folder to a project.
* Permissions calculation speedup.
* Fixed stale cache when archiving a file.

## Version 1.5.3
* Fixed stale cache when copying a file to the root of a bucket.

## Version 1.5.2
* Fixed file renaming regression.

## Version 1.5.1
* Caching optimizations.

## Version 1.5.0
* Support mode and access_token query parameters when getting a file object.

## Version 1.4.1
* Improved permission denied messages.

## Version 1.4.0
* Present accurate file permissions.

## Version 1.3.0
* Merged the AWS S3 files microservice into this one.
* Fixed caching bugs affecting web client object explorer refresh.
* Avoid timeouts loading objects, which sporadically caused objects not to be returned.

## Version 1.2.2
* Prevent failed content downloads from hanging the microservice.

## Version 1.2.1
* Install setuptools first during installation.
* Correct issue where some users lost access to folder and folder items because the user lacked permissions in AWS to simulate permissions. Instead, such users will appear to receive full permission for everything, which was the behavior prior to version 1.2.0. As before, AWS will still reject requests that users lack permission for.

## Version 1.2.0
* Present accurate bucket permissions.

## Version 1.1.6
* Minor bug fixes.

## Version 1.1.5
* Made a project's unarchive restore duration required in the unarchive card.

## Version 1.1.4
* Made a folder's unarchive restore duration required in the unarchive card.

## Version 1.1.3
* Fixed potential issue preventing the service from updating temporary credentials.

## Version 1.1.2
* Fixed new folder form submission.

## Version 1.1.1
* Display type display name in properties card, and return the type display name from GET calls.

## Version 1.1.0
* Pass folder and project permissions back to clients.

## Version 1.0.13
* Changed presented bucket owner to system|aws.
* Omitted shares from the properties template.

## Version 1.0.12
* Improved upload desktop object action message.

## Version 1.0.11
* Improved performance.

## Version 1.0.10
* Support getting the content of a folder as a zip file when the folder has files > 2GiB in size.

## Version 1.0.9
* Prevent zip file corruption when getting the content of a folder.

## Version 1.0.8
* Addressed issue where downloads start failing for all users if one user interrupts their download.

## Version 1.0.7
* Addressed potential failures to connect to other CORE Browser microservices.

## Version 1.0.6
* Addressed potential exception while unarchiving objects.
* Addressed issue preventing copying and moving folders containing unarchived objects.
* Improved error message when attempting to copy or move a folder with archived objects.

## Version 1.0.5
* Improved validation for downloading objects and generating presigned URLs.

## Version 1.0.4
* Improved performance.
* Allow unarchived S3 objects to be downloaded.

## Version 1.0.3
* Fixed project downloading.

## Version 1.0.2
* Fixed project copy and move causing 404 error.

## Version 1.0.1
* Improved performance.
* Corrected issue copying, moving, and renaming folders and projects containing archived objects.
* Corrected error opening a project with an archived README.*.
* Skip archived objects when downloading a folder or project.

## Version 1
Initial release.

## Runtime requirements
* Python 3.10, 3.11, or 3.12.

## Development environment

### Build requirements
* Any development environment is fine.
* On Windows, you also will need:
    * Build Tools for Visual Studio 2019, found at https://visualstudio.microsoft.com/downloads/. Select the C++ tools.
    * git, found at https://git-scm.com/download/win.
* On Mac, Xcode or the command line developer tools is required, found in the Apple Store app.
* Python 3.10, 3.11, or 3.12: Download and install Python from https://www.python.org, and select the options to
install for all users and add Python to your environment variables. The install for all users option will help keep you
from accidentally installing packages into your Python installation's site-packages directory instead of to your
virtualenv environment, described below.
* Create a virtualenv environment using the `python -m venv <venv_directory>` command, substituting `<venv_directory>`
with the directory name of your virtual environment. Run `source <venv_directory>/bin/activate` (or `<venv_directory>/Scripts/activate` on Windows) to activate the virtual
environment. You will need to activate the virtualenv every time before starting work, or your IDE may be able to do
this for you automatically. **Note that PyCharm will do this for you, but you have to create a new Terminal panel
after you newly configure a project with your virtualenv.**
* From the project's root directory, and using the activated virtualenv, run `pip install wheel` followed by
  `pip install -r requirements_dev.txt`. **Do NOT run `python setup.py develop`. It will break your environment.**

### Running tests
Run tests with the `pytest` command from the project root directory. To improve performance, run tests in multiple
processes with `pytest -n auto`.

### Running integration tests
* Install Docker
* On Windows, install pywin32 version >= 223 from https://github.com/mhammond/pywin32/releases. In your venv, make sure that
`include-system-site-packages` is set to `true`.
* A compatible heaserver-registry Docker image must be available.
* Run tests with the `pytest integrationtests` command from the project root directory.

### Trying out the APIs
This microservice has Swagger3/OpenAPI support so that you can quickly test the APIs in a web browser. Do the following:
* Install Docker, if it is not installed already.
* Have a heaserver-registry docker image in your Docker cache. You can generate one using the Dockerfile in the
  heaserver-registry project.
* Run the `run-swaggerui.py` file in your terminal. This file contains some test objects that are loaded into a MongoDB
  Docker container.
* Go to http://127.0.0.1:8080/docs in your web browser.

Once `run-swaggerui.py` is running, you can also access the APIs via `curl` or other tool. For example, in Windows
PowerShell, execute:
```
Invoke-RestMethod -Uri http://localhost:8080/awss3folders/root/items -Method GET -Headers @{'accept' = 'application/json'}`
```
In MacOS or Linux, the equivalent command is:
```
curl -X GET http://localhost:8080/awss3folders/root/items -H 'accept: application/json'
```

### Packaging and releasing this project
See the [RELEASING.md](RELEASING.md) file for details.
