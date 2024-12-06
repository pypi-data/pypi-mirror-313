# HEA Server AWS Accounts Microservice
[Research Informatics Shared Resource](https://risr.hci.utah.edu), [Huntsman Cancer Institute](https://hci.utah.edu),
Salt Lake City, UT

The HEA Server AWS Accounts Microservice is It manages the AWS account information details.

## Version 1.5.1
* Performance improvements.

## Version 1.5.0
* Added support for Python 3.12.

## Version 1.4.0
* Removed integration tests because they all overlapped with the unit tests.
* Accept the data query parameter for get requests for a speed boost.

## Version 1.3.9
* Dependency upgrades for compatibility with heaserver-keychain 1.5.0.

## Version 1.3.8
* Fixed another /accounts regression when no account ids are passed as query parameters.

## Version 1.3.7
* Stop returning all accounts with an accessible volume; only return the requested accounts.

## Version 1.3.6
* When retrieving /accounts, skip volumes with a null account_id. Fixes crash retrieving accounts.

## Version 1.3.5
* Pull /accounts from volume data rather than trying to get account info from AWS. Helps with performance for users who
have access to lots of accounts.

## Version 1.3.4
* Caching optimizations.

## Version 1.3.3
* Fixed new bucket link.

## Version 1.3.2
* Fixed a caching issue when listing accounts.
* Additional input validation.

## Version 1.3.1
* Avoid timeouts loading accounts, which sporadically caused accounts not to be returned.

## Version 1.3.0
* Present accurate account permissions.
* Added caching for getting accounts list.

## Version 1.2.0
* New /accounts endpoint that returns heaobject.account.AccountView objects.

## Version 1.1.3
* Another attempt at fixing the crash regression.

## Version 1.1.2
* Fixed crash regression.

## Version 1.1.1
* Fixed new bucket form submission.

## Version 1.1.0
* Removed the PUT and DELETE account calls because neither works.

## Version 1.0.8
* Addressed occasional slowdown getting one account.

## Version 1.0.7
* Addressed occasional slowdown getting accounts.

## Version 1.0.6
* Display type display name in properties card, and return the type display name from GET calls.

## Version 1.0.5
* Improved performance getting accounts.

## Version 1.0.4
* Corrected caching issue.

## Version 1.0.3
* Improved error handling when the user lacks authorization for some AWS account information.

## Version 1.0.2
* Avoid a 500 error when retrieving accounts when attempting to access a suspended account.
* AWS account info requests return more complete information.
* Omit shares from the properties template.

## Version 1.0.1
* Improved performance.

## Version 1
Initial release.

## Runtime requirements
* Python 3.10 or 3.11.

## Development environment

### Build requirements
* Any development environment is fine.
* On Windows, you also will need:
    * Build Tools for Visual Studio 2019, found at https://visualstudio.microsoft.com/downloads/. Select the C++ tools.
    * git, found at https://git-scm.com/download/win.
* On Mac, Xcode or the command line developer tools is required, found in the Apple Store app.
* Python 3.10, 3.11, or 3.12: Download and install it from https://www.python.org, and select the options to install for all
users and add Python to your environment variables. The install for all users option will help keep you from
accidentally installing packages into your Python installation's site-packages directory instead of to your virtualenv
environment, described below.
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

### Testing using Swagger
Run `python ./run-swaggerui.py` and open up http://locahost:8080/docs in your web browser to get a UI for making REST
API calls.

### Versioning
Use semantic versioning as described in
https://packaging.python.org/guides/distributing-packages-using-setuptools/#choosing-a-versioning-scheme. In addition,
while development is underway, the version should be the next version number suffixed by `.dev`.

### Version tags in git
Version tags should follow the format `heaserver-awsaccounts-<version>`, for example, `heaserver-awsaccounts-1.0.0`.

### Uploading to an index server
The following instructions assume separate stable and staging indexes. Numbered releases, including alphas and betas, go
into the stable index. Snapshots of works in progress go into the staging index. Thus, use staging to upload numbered
releases, verify the uploaded packages, and then upload to stable.

From the project's root directory:
1. For numbered releases, remove `.dev` from the version number in setup.py, tag it in git to indicate a release,
and commit to version control. Skip this step for developer snapshot releases.
2. Run `python setup.py clean --all sdist bdist_wheel` to create the artifacts.
3. Run `twine upload -r <repository> dist/<wheel-filename> dist/<tarball-filename>` to upload to the
 repository. The repository name has to be defined in a twine configuration file such as `$HOME/.pypirc`.
4. For numbered releases, increment the version number in setup.py, append `.dev` to it, and commit to version
control with a commit message like, "Prepare for next development iteration."
