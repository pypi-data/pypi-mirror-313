"""
  BYOSnap CLI commands
"""
import base64
from binascii import Error as BinasciiError
import json
import os
import re
import time
import subprocess
import platform as sys_platform
from sys import platform
from typing import Union, List
import requests
from requests.exceptions import RequestException

from rich.progress import Progress, SpinnerColumn, TextColumn
from snapctl.commands.snapend import Snapend
from snapctl.config.constants import SERVER_CALL_TIMEOUT
from snapctl.config.constants import HTTP_ERROR_SERVICE_VERSION_EXISTS, \
    HTTP_ERROR_TAG_NOT_AVAILABLE, HTTP_ERROR_ADD_ON_NOT_ENABLED, SNAPCTL_INPUT_ERROR, \
    SNAPCTL_BYOSNAP_DEPENDENCY_MISSING, SNAPCTL_BYOSNAP_ECR_LOGIN_ERROR, \
    SNAPCTL_BYOSNAP_BUILD_ERROR, SNAPCTL_BYOSNAP_TAG_ERROR, SNAPCTL_BYOSNAP_PUBLISH_IMAGE_ERROR, \
    SNAPCTL_BYOSNAP_PUBLISH_IMAGE_DUPLICATE_TAG_ERROR, \
    SNAPCTL_BYOSNAP_CREATE_DUPLICATE_NAME_ERROR, SNAPCTL_BYOSNAP_CREATE_PERMISSION_ERROR, \
    SNAPCTL_BYOSNAP_CREATE_ERROR, SNAPCTL_BYOSNAP_PUBLISH_VERSION_DUPLICATE_TAG_ERROR, \
    SNAPCTL_BYOSNAP_PUBLISH_VERSION_ERROR, HTTP_ERROR_SERVICE_IN_USE, \
    SNAPCTL_BYOSNAP_UPDATE_VERSION_ERROR, SNAPCTL_BYOSNAP_UPDATE_VERSION_SERVICE_IN_USE_ERROR, \
    SNAPCTL_BYOSNAP_UPDATE_VERSION_TAG_ERROR, SNAPCTL_BYOSNAP_NOT_FOUND, \
    HTTP_ERROR_RESOURCE_NOT_FOUND
from snapctl.utils.echo import info, warning
from snapctl.utils.helper import get_composite_token, snapctl_error, snapctl_success, \
    check_dockerfile_architecture


class ByoSnap:
    """
      CLI commands exposed for a BYOSnap
    """
    ID_PREFIX = 'byosnap-'
    SUBCOMMANDS = [
        'create', 'publish-image', 'publish-version', 'upload-docs', 'update-version',
        'sync'
    ]
    PLATFORMS = ['linux/arm64', 'linux/amd64']
    LANGUAGES = ['go', 'python', 'ruby', 'c#', 'c++', 'rust', 'java', 'node']
    DEFAULT_BUILD_PLATFORM = 'linux/arm64'
    SID_CHARACTER_LIMIT = 47
    TAG_CHARACTER_LIMIT = 80
    VALID_CPU_MARKS = [100, 250, 500, 750, 1000, 1500, 2000, 3000]
    VALID_MEMORY_MARKS = [0.125, 0.25, 0.5, 1, 2, 3, 4]
    MAX_READINESS_TIMEOUT = 30
    MAX_MIN_REPLICAS = 4

    def __init__(
        self, *, subcommand: str, base_url: str, api_key: Union[str, None], sid: str,
        name: Union[str, None] = None, desc: Union[str, None] = None,
        platform_type: Union[str, None] = None, language: Union[str, None] = None,
        tag: Union[str, None] = None, path: Union[str, None] = None,
        resources_path: Union[str, None] = None,  dockerfile: Union[str, None] = None,
        prefix: Union[str, None] = None, version: Union[str, None] = None,
        http_port: Union[int, None] = None,
        byosnap_profile: Union[str, None] = None, skip_build: bool = False,
        readiness_path: Union[str, None] = None, readiness_delay: Union[int, None] = None,
        snapend_id: Union[str, None] = None, blocking: bool = False
    ) -> None:
        self.subcommand: str = subcommand
        self.base_url: str = base_url
        self.api_key: Union[str, None] = api_key
        self.sid: str = sid
        self.name: str = name
        self.desc: str = desc
        self.platform_type: str = platform_type
        self.language: str = language
        if subcommand != 'create':
            self.token: Union[str, None] = get_composite_token(
                base_url, api_key,
                'byosnap', {'service_id': sid}
            )
        else:
            self.token: Union[str, None] = None
        self.token_parts: Union[list, None] = ByoSnap._get_token_values(
            self.token) if self.token is not None else None
        self.tag: Union[str, None] = tag
        self.path: Union[str, None] = path
        self.resources_path: Union[str, None] = resources_path
        self.dockerfile: str = dockerfile
        self.prefix: str = prefix
        self.version: Union[str, None] = version
        self.http_port: Union[int, None] = http_port
        self.byosnap_profile: Union[str, None] = byosnap_profile
        self.skip_build: bool = skip_build
        self.readiness_path: Union[str, None] = readiness_path
        self.readiness_delay: Union[int, None] = readiness_delay
        self.snapend_id: Union[str, None] = snapend_id
        self.blocking: bool = blocking
        # Validate the input
        self.validate_input()

    # Protected methods
    @staticmethod
    def _get_token_values(token: str) -> Union[None, List]:
        """
          Method to break open the token
        """
        try:
            input_token = base64.b64decode(token).decode('ascii')
            parts = input_token.split('|')
            # url|web_app_token|service_id|ecr_repo_url|ecr_repo_username|ecr_repo_token
            # url = self.token_parts[0]
            # web_app_token = self.token_parts[1]
            # service_id = self.token_parts[2]
            # ecr_repo_url = self.token_parts[3]
            # ecr_repo_username = self.token_parts[4]
            # ecr_repo_token = self.token_parts[5]
            # platform = self.token_parts[6]
            if len(parts) >= 3:
                return parts
        except BinasciiError:
            pass
        return None

    def _check_dependencies(self) -> None:
        """
          Check application dependencies
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Checking dependencies...', total=None)
        try:
            # Check dependencies
            result = subprocess.run([
                "docker", "info"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
            if not result.returncode:
                return snapctl_success(
                    message='BYOSnap dependencies verified',
                    progress=progress, no_exit=True)
        except subprocess.CalledProcessError:
            snapctl_error(
                message='Snapctl Exception',
                code=SNAPCTL_BYOSNAP_DEPENDENCY_MISSING, progress=progress)
        finally:
            progress.stop()
        snapctl_error(
            message='Docker not running. Please start docker.',
            code=SNAPCTL_BYOSNAP_DEPENDENCY_MISSING, progress=progress)

    def _docker_login(self) -> None:
        """
          Docker Login
        """
        ecr_repo_url = self.token_parts[0]
        ecr_repo_username = self.token_parts[1]
        ecr_repo_token = self.token_parts[2]
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Logging into Snapser Image Registry...', total=None)
        try:
            # Login to Snapser Registry
            if platform == 'win32':
                response = subprocess.run([
                    'docker', 'login', '--username', ecr_repo_username,
                    '--password', ecr_repo_token, ecr_repo_url
                ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
            else:
                response = subprocess.run([
                    f'echo "{ecr_repo_token}" | docker login ' +
                    f'--username {ecr_repo_username} --password-stdin {ecr_repo_url}'
                ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
            if not response.returncode:
                return snapctl_success(
                    message='BYOSnap ECR login successful',
                    progress=progress, no_exit=True)
        except subprocess.CalledProcessError:
            snapctl_error(
                message='Snapctl Exception',
                code=SNAPCTL_BYOSNAP_ECR_LOGIN_ERROR, progress=progress)
        finally:
            progress.stop()
        snapctl_error(
            message='BYOSnap ECR login failure',
            code=SNAPCTL_BYOSNAP_ECR_LOGIN_ERROR, progress=progress)

    def _docker_build(self) -> None:
        # Get the data
        # image_tag = f'{self.sid}.{self.tag}'
        build_platform = ByoSnap.DEFAULT_BUILD_PLATFORM
        if len(self.token_parts) == 4:
            build_platform = self.token_parts[3]
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Building your snap...', total=None)
        try:
            # Build your snap
            if self.resources_path:
                base_path = self.resources_path
            else:
                base_path = self.path
            docker_file_path = os.path.join(base_path, self.dockerfile)

            # Warning check for architecture specific commands
            info(f'Building on system architecture {sys_platform.machine()}')
            check_response = check_dockerfile_architecture(
                docker_file_path, sys_platform.machine())
            if check_response['error']:
                warning(check_response['message'])
            # Build the image
            if platform == "win32":
                response = subprocess.run([
                    # f"docker build --no-cache -t {tag} {path}"
                    'docker', 'build', '--platform', build_platform, '-t', self.tag,
                    '-f', docker_file_path,  self.path
                ], shell=True, check=False)
                # stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            else:
                response = subprocess.run([
                    # f"docker build --no-cache -t {tag} {path}"
                    "docker build --platform " +
                    f"{build_platform} -t {self.tag} " +
                    f"-f {docker_file_path} {self.path}"
                ], shell=True, check=False)
                # stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            if not response.returncode:
                return snapctl_success(
                    message='BYOSnap build successful', progress=progress, no_exit=True)
        except subprocess.CalledProcessError:
            snapctl_error(
                message='Snapctl Exception',
                code=SNAPCTL_BYOSNAP_BUILD_ERROR, progress=progress)
        finally:
            progress.stop()
        snapctl_error(
            message='BYOSnap build failure',
            code=SNAPCTL_BYOSNAP_BUILD_ERROR, progress=progress)

    def _docker_tag(self) -> None:
        # Get the data
        ecr_repo_url = self.token_parts[0]
        image_tag = f'{self.sid}.{self.tag}'
        full_ecr_repo_url = f'{ecr_repo_url}:{image_tag}'
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Tagging your snap...', total=None)
        try:
            # Tag the repo
            if platform == "win32":
                response = subprocess.run([
                    'docker', 'tag', self.tag, full_ecr_repo_url
                ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
            else:
                response = subprocess.run([
                    f"docker tag {self.tag} {full_ecr_repo_url}"
                ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
            if not response.returncode:
                return snapctl_success(
                    message='BYOSnap tag successful', progress=progress, no_exit=True)
        except subprocess.CalledProcessError:
            snapctl_error(
                message='Snapctl Exception',
                code=SNAPCTL_BYOSNAP_TAG_ERROR, progress=progress)
        finally:
            progress.stop()
        snapctl_error(
            message='BYOSnap tag failure',
            code=SNAPCTL_BYOSNAP_TAG_ERROR, progress=progress)

    def _docker_push(self) -> bool:
        """
          Push the Snap image
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(description='Pushing your snap...', total=None)
        try:
            # Push the image
            ecr_repo_url = self.token_parts[0]
            image_tag = f'{self.sid}.{self.tag}'
            full_ecr_repo_url = f'{ecr_repo_url}:{image_tag}'
            if platform == "win32":
                response = subprocess.run([
                    'docker', 'push', full_ecr_repo_url
                ], shell=True, check=False)
                # stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            else:
                response = subprocess.run([
                    f"docker push {full_ecr_repo_url}"
                ], shell=True, check=False)
                # stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            if not response.returncode:
                return snapctl_success(
                    message='BYOSnap upload successful', progress=progress, no_exit=True)
        except subprocess.CalledProcessError:
            snapctl_error(
                message='Snapctl Exception',
                code=SNAPCTL_BYOSNAP_PUBLISH_IMAGE_ERROR, progress=progress)
        finally:
            progress.stop()
        snapctl_error(
            message='BYOSnap upload failure. Duplicate image error.',
            code=SNAPCTL_BYOSNAP_PUBLISH_IMAGE_DUPLICATE_TAG_ERROR, progress=progress)

    def _validate_byosnap_profile(self) -> None:
        """
          Validate the BYOSnap profile
        """
        if not self.byosnap_profile:
            snapctl_error(
                message="Missing BYOSnap profile path", code=SNAPCTL_INPUT_ERROR)
        if not os.path.isfile(self.byosnap_profile):
            snapctl_error(
                message="Unable to find BYOSnap profile " +
                f"JSON at path {self.byosnap_profile}",
                code=SNAPCTL_INPUT_ERROR
            )
        profile_data = None
        with open(self.byosnap_profile, 'rb') as file:
            try:
                profile_data = json.load(file)
            except json.JSONDecodeError:
                pass
        if not profile_data:
            snapctl_error(
                message='Invalid BYOSnap profile JSON. Please check the JSON structure',
                code=SNAPCTL_INPUT_ERROR
            )
        if 'dev_template' not in profile_data or \
            'stage_template' not in profile_data or \
                'prod_template' not in profile_data:
            snapctl_error(
                message='Invalid BYOSnap profile JSON. Please check the JSON structure',
                code=SNAPCTL_INPUT_ERROR
            )
        for profile in ['dev_template', 'stage_template', 'prod_template']:
            # Currently, not checking for 'min_replicas' not in profile_data[profile]
            if 'cpu' not in profile_data[profile] or \
                'memory' not in profile_data[profile] or \
                    'cmd' not in profile_data[profile] or \
                    'args' not in profile_data[profile] or \
                    'env_params' not in profile_data[profile]:
                snapctl_error(
                    message='Invalid BYOSnap profile JSON. Please check the JSON structure',
                    code=SNAPCTL_INPUT_ERROR
                )
            if profile_data[profile]['cpu'] not in ByoSnap.VALID_CPU_MARKS:
                snapctl_error(
                    message='Invalid CPU value in BYOSnap profile. Valid values are' +
                    f'{", ".join(map(str, ByoSnap.VALID_CPU_MARKS))}',
                    code=SNAPCTL_INPUT_ERROR
                )
            if profile_data[profile]['memory'] not in ByoSnap.VALID_MEMORY_MARKS:
                snapctl_error(
                    message='Invalid Memory value in BYOSnap profile. Valid values are ' +
                    f'{", ".join(map(str, ByoSnap.VALID_MEMORY_MARKS))}',
                    code=SNAPCTL_INPUT_ERROR
                )
            if 'min_replicas' in profile_data[profile] and \
                (not isinstance(profile_data[profile]['min_replicas'], int) or
                    int(profile_data[profile]['min_replicas']) < 0 or
                 int(profile_data[profile]['min_replicas']) > ByoSnap.MAX_MIN_REPLICAS):
                snapctl_error(
                    message='Invalid Min Replicas value in BYOSnap profile. ' +
                    'Minimum replicas should be between 0 and ' +
                    f'{ByoSnap.MAX_MIN_REPLICAS}',
                    code=SNAPCTL_INPUT_ERROR
                )

    def _clean_slate(self) -> None:
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Cleaning cache and initializing...', total=None)
        try:
            # Specific ECR repository URL to check against
            ecr_domain = self.token_parts[0].split('/')[0]
            # Perform the Docker logout
            if platform == "win32":
                logout_response = subprocess.run(['docker', 'logout', ecr_domain],
                                                 shell=True, check=False)
            else:
                logout_response = subprocess.run([
                    f"docker logout {ecr_domain}"
                ], shell=True, check=False)
            if not logout_response.returncode:
                return snapctl_success(
                    message='Cleanup complete.', progress=progress, no_exit=True)
        except subprocess.CalledProcessError:
            warning('Unable to initialize with a clean slate.')
        finally:
            progress.stop()

    # Public methods

    # Validator
    def validate_input(self) -> None:
        """
          Validator
        """
        # Check API Key and Base URL
        if not self.api_key or self.base_url == '':
            snapctl_error(
                message="Missing API Key.", code=SNAPCTL_INPUT_ERROR)
        # Check subcommand
        if not self.subcommand in ByoSnap.SUBCOMMANDS:
            snapctl_error(
                message="Invalid command. Valid commands are " +
                f"{', '.join(ByoSnap.SUBCOMMANDS)}.",
                code=SNAPCTL_INPUT_ERROR
            )
        # Validate the SID
        if not self.sid.startswith(ByoSnap.ID_PREFIX):
            snapctl_error(
                message="Invalid Snap ID. Valid Snap IDs start with " +
                f"{ByoSnap.ID_PREFIX}.",
                code=SNAPCTL_INPUT_ERROR
            )
        if len(self.sid) > ByoSnap.SID_CHARACTER_LIMIT:
            snapctl_error(
                message="Invalid Snap ID. Snap ID should be less than " +
                f"{ByoSnap.SID_CHARACTER_LIMIT} characters",
                code=SNAPCTL_INPUT_ERROR
            )
        # Validation for subcommands
        if self.subcommand == 'create':
            if self.name == '':
                snapctl_error(message="Missing name", code=SNAPCTL_INPUT_ERROR)
            if not self.language:
                snapctl_error(message="Missing language",
                              code=SNAPCTL_INPUT_ERROR)
            if self.language not in ByoSnap.LANGUAGES:
                snapctl_error(
                    message="Invalid language. Valid languages are " +
                    f"{', '.join(ByoSnap.LANGUAGES)}.",
                    code=SNAPCTL_INPUT_ERROR
                )
            if self.platform_type not in ByoSnap.PLATFORMS:
                snapctl_error(
                    message="Invalid platform. Valid platforms are " +
                    f"{', '.join(ByoSnap.PLATFORMS)}.",
                    code=SNAPCTL_INPUT_ERROR
                )
            return
        # Now validate all other commands Check the token
        if self.token_parts is None:
            snapctl_error('Invalid token. Please reach out to your support team.',
                          SNAPCTL_INPUT_ERROR)
        if self.subcommand in ['publish-image']:
            if not self.tag:
                snapctl_error(
                    "Missing required parameter: tag", SNAPCTL_INPUT_ERROR)
            if len(self.tag.split()) > 1 or \
                    len(self.tag) > ByoSnap.TAG_CHARACTER_LIMIT:
                snapctl_error(
                    "Tag should be a single word with maximum of " +
                    f"{ByoSnap.TAG_CHARACTER_LIMIT} characters",
                    SNAPCTL_INPUT_ERROR
                )
            if not self.skip_build and not self.path:
                snapctl_error("Missing required parameter: path",
                              SNAPCTL_INPUT_ERROR)
            # Check path
            if self.resources_path:
                docker_file_path = \
                    f"{self.resources_path}/{self.dockerfile}"
            else:
                docker_file_path = f"{self.path}/{self.dockerfile}"
            if not self.skip_build and not os.path.isfile(docker_file_path):
                snapctl_error(
                    "Unable to find " +
                    f"{self.dockerfile} at path {docker_file_path}",
                    SNAPCTL_INPUT_ERROR)
        # elif self.subcommand == 'push':
        #     if not self.tag:
        #         error("Missing required parameter: tag", SNAPCTL_INPUT_ERROR)
        #         raise typer.Exit(code=SNAPCTL_INPUT_ERROR)
        elif self.subcommand == 'upload-docs':
            if self.path is None and self.resources_path is None:
                snapctl_error(
                    "Missing one of: path or resources-path parameter", SNAPCTL_INPUT_ERROR)
        elif self.subcommand == 'publish-version':
            if not self.tag:
                snapctl_error(
                    "Missing required parameter: tag", SNAPCTL_INPUT_ERROR)
            if len(self.tag.split()) > 1 or \
                    len(self.tag) > ByoSnap.TAG_CHARACTER_LIMIT:
                snapctl_error(
                    "Tag should be a single word with maximum of " +
                    f"{ByoSnap.TAG_CHARACTER_LIMIT} characters",
                    SNAPCTL_INPUT_ERROR
                )
            if not self.prefix or self.prefix == '':
                snapctl_error("Missing prefix", SNAPCTL_INPUT_ERROR)
            if not self.prefix.startswith('/'):
                snapctl_error("Prefix should start with a forward slash (/)",
                              SNAPCTL_INPUT_ERROR)
            if self.prefix.endswith('/'):
                snapctl_error("Prefix should not end with a forward slash (/)",
                              SNAPCTL_INPUT_ERROR)
            if not self.version:
                snapctl_error("Missing version", SNAPCTL_INPUT_ERROR)
            pattern = r'^v\d+\.\d+\.\d+$'
            if not re.match(pattern, self.version):
                snapctl_error("Version should be in the format vX.X.X",
                              SNAPCTL_INPUT_ERROR)
            if not self.http_port:
                snapctl_error("Missing Ingress HTTP Port",
                              SNAPCTL_INPUT_ERROR)
            if not self.http_port.isdigit():
                snapctl_error("Ingress HTTP Port should be a number",
                              SNAPCTL_INPUT_ERROR)
            if self.readiness_path is not None:
                if self.readiness_path.strip() == '':
                    snapctl_error("Readiness path cannot be empty",
                                  SNAPCTL_INPUT_ERROR)
                if not self.readiness_path.strip().startswith('/'):
                    snapctl_error("Readiness path has to start with /",
                                  SNAPCTL_INPUT_ERROR)
            if self.readiness_delay is not None:
                if self.readiness_delay < 0 or \
                        self.readiness_delay > ByoSnap.MAX_READINESS_TIMEOUT:
                    snapctl_error(
                        "Readiness delay should be between 0 " +
                        f"and {ByoSnap.MAX_READINESS_TIMEOUT}", SNAPCTL_INPUT_ERROR)
            # Check byosnap_profile path
            self._validate_byosnap_profile()
        elif self.subcommand == 'update-version':
            if not self.version:
                snapctl_error(message="Missing version",
                              code=SNAPCTL_INPUT_ERROR)
            pattern = r'^v\d+\.\d+\.\d+$'
            if not re.match(pattern, self.version):
                snapctl_error(
                    message="Version should be in the format vX.X.X",
                    code=SNAPCTL_INPUT_ERROR)
            if not self.tag:
                snapctl_error(
                    message="Missing required parameter: tag", code=SNAPCTL_INPUT_ERROR)
            if len(self.tag.split()) > 1 or \
                    len(self.tag) > ByoSnap.TAG_CHARACTER_LIMIT:
                snapctl_error(
                    message="Tag should be a single word with maximum of " +
                    f"{ByoSnap.TAG_CHARACTER_LIMIT} characters",
                    code=SNAPCTL_INPUT_ERROR
                )
        elif self.subcommand == 'sync':
            if not self.version:
                snapctl_error(message="Missing version",
                              code=SNAPCTL_INPUT_ERROR)
            pattern = r'^v\d+\.\d+\.\d+$'
            if not re.match(pattern, self.version):
                snapctl_error(message="Version should be in the format vX.X.X",
                              code=SNAPCTL_INPUT_ERROR)
            if not self.tag:
                snapctl_error(
                    message="Missing required parameter: tag", code=SNAPCTL_INPUT_ERROR)
            if len(self.tag.split()) > 1 or \
                    len(self.tag) > ByoSnap.TAG_CHARACTER_LIMIT:
                snapctl_error(
                    message="Tag should be a single word with maximum of " +
                    f"{ByoSnap.TAG_CHARACTER_LIMIT} characters",
                    code=SNAPCTL_INPUT_ERROR
                )
            if not self.skip_build and not self.path:
                snapctl_error(
                    message="Missing required parameter: path",
                    code=SNAPCTL_INPUT_ERROR)
            # Check path
            if self.resources_path:
                docker_file_path = \
                    f"{self.resources_path}/{self.dockerfile}"
            else:
                docker_file_path = f"{self.path}/{self.dockerfile}"
            if not self.skip_build and not os.path.isfile(docker_file_path):
                snapctl_error(
                    message="Unable to find " +
                    f"{self.dockerfile} at path {docker_file_path}",
                    code=SNAPCTL_INPUT_ERROR)
    # CRUD methods

    def build(self) -> None:
        """
          Build the image
          1. Check Dependencies
          2. Login to Snapser Registry
          3. Build your snap
        """
        self._check_dependencies()
        self._docker_build()

    def push(self) -> bool:
        """
          Tag the image
          1. Check Dependencies
          2. Login to Snapser Registry
          3. Tag the snap
          4. Push your snap
        """
        self._check_dependencies()
        self._docker_tag()
        self._clean_slate()
        self._docker_login()
        self._docker_push()

    # Upper echelon commands
    def upload_docs(self, no_exit: bool = False) -> None:
        '''
        Note this step is optional hence we do not raise a typer.Exit
        '''
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Uploading your BYOSnap Docs...', total=None)
        try:
            if self.resources_path:
                base_dir = self.resources_path
            else:
                base_dir = self.path

            swagger_file = os.path.join(base_dir, 'swagger.json')
            readme_file = os.path.join(base_dir, 'README.md')

            # Upload swagger.json
            if os.path.isfile(swagger_file):
                try:
                    with open(swagger_file, "rb") as attachment_file:
                        url = (
                            f"{self.base_url}/v1/snapser-api/byosnaps/"
                            f"{self.sid}/docs/{self.tag}/openapispec"
                        )
                        test_res = requests.post(
                            url, files={"attachment": attachment_file},
                            headers={'api-key': self.api_key},
                            timeout=SERVER_CALL_TIMEOUT
                        )
                        if test_res.ok:
                            snapctl_success(
                                message='Uploaded swagger.json', progress=None, no_exit=True)
                        else:
                            info('Unable to upload your swagger.json')
                except RequestException as e:
                    info(
                        'Exception: Unable to find swagger.json at ' +
                        f'{base_dir} {e}'
                    )
            else:
                info(
                    'No swagger.json found at' +
                    f'{base_dir}. Skipping swagger.json upload'
                )

            # Upload README.md
            if os.path.isfile(readme_file):
                try:
                    with open(readme_file, "rb") as attachment_file:
                        url = (
                            f"{self.base_url}/v1/snapser-api/byosnaps/"
                            f"{self.sid}/docs/{self.tag}/markdown"
                        )
                        test_res = requests.post(
                            url, files={"attachment": attachment_file},
                            headers={'api-key': self.api_key},
                            timeout=SERVER_CALL_TIMEOUT
                        )
                        if test_res.ok:
                            snapctl_success(
                                message='Uploaded README.md', progress=None, no_exit=True)
                        else:
                            info('Unable to upload your README.md')
                except RequestException as e:
                    info(
                        'Exception: Unable to find README.md at ' +
                        f'{base_dir} {str(e)}'
                    )
            else:
                info(
                    'No README.md found at ' +
                    f'{base_dir}. Skipping README.md upload'
                )

            # Upload any snapser-tool-*.json files
            for file_name in os.listdir(base_dir):
                if file_name.startswith("snapser-tool-") and file_name.endswith(".json"):
                    file_path = os.path.join(base_dir, file_name)
                    if os.path.isfile(file_path):
                        try:
                            with open(file_path, "rb") as attachment_file:
                                url = (
                                    f"{self.base_url}/v1/snapser-api/byosnaps/"
                                    f"{self.sid}/docs/{self.tag}/tools"
                                )
                                test_res = requests.post(
                                    url, files={"attachment": attachment_file},
                                    headers={'api-key': self.api_key},
                                    timeout=SERVER_CALL_TIMEOUT
                                )
                                if test_res.ok:
                                    snapctl_success(
                                        message=f'Uploaded tool {file_name}',
                                        progress=None, no_exit=True)
                                else:
                                    info(f'Unable to upload tool {file_name}')
                        except RequestException as e:
                            info('Exception: Unable to upload tool ' +
                                 f'{file_name} {str(e)}')

            # Show success message
            snapctl_success(
                message='Completed the docs uploading process', progress=progress, no_exit=no_exit)
        except RequestException as e:
            info(f'Exception: Unable to upload your API Json {str(e)}')
        finally:
            progress.stop()

    def create(self, no_exit: bool = False) -> None:
        """
          Creating a new snap
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(description='Creating your snap...', total=None)
        try:
            payload = {
                "service_id": self.sid,
                "name": self.name,
                "description": self.desc,
                "platform": self.platform_type,
                "language": self.language,
            }
            res = requests.post(
                f"{self.base_url}/v1/snapser-api/byosnaps",
                json=payload, headers={'api-key': self.api_key},
                timeout=SERVER_CALL_TIMEOUT
            )
            if res.ok:
                return snapctl_success(
                    message='BYOSNAP create successful', progress=progress, no_exit=no_exit)
            response_json = res.json()
            if "api_error_code" in response_json and "message" in response_json:
                if response_json['api_error_code'] == HTTP_ERROR_RESOURCE_NOT_FOUND:
                    snapctl_error(
                        message='BYOSnap not found.',
                        code=SNAPCTL_BYOSNAP_NOT_FOUND, progress=progress
                    )
                if response_json['api_error_code'] == HTTP_ERROR_SERVICE_VERSION_EXISTS:
                    snapctl_error(
                        message=f'BYOSnap {self.name} already exists. ' +
                        'Please use a different name',
                        code=SNAPCTL_BYOSNAP_CREATE_DUPLICATE_NAME_ERROR,
                        progress=progress
                    )
                # elif response_json['api_error_code'] == HTTP_ERROR_TAG_NOT_AVAILABLE:
                #     error('Invalid tag. Please use the correct tag')
                if response_json['api_error_code'] == HTTP_ERROR_ADD_ON_NOT_ENABLED:
                    snapctl_error(
                        message='Missing Add-on. Please enable the add-on via the Snapser Web app.',
                        code=SNAPCTL_BYOSNAP_CREATE_PERMISSION_ERROR,
                        progress=progress
                    )
            snapctl_error(
                message=f'Server error: {json.dumps(response_json, indent=2)}',
                code=SNAPCTL_BYOSNAP_CREATE_ERROR, progress=progress)
        except RequestException as e:
            snapctl_error(
                message=f"Exception: Unable to create your snap {e}",
                code=SNAPCTL_BYOSNAP_CREATE_ERROR, progress=progress)
        finally:
            progress.stop()
        snapctl_error(
            message='Failed to create snap',
            code=SNAPCTL_BYOSNAP_CREATE_ERROR, progress=progress)

    def publish_image(self, no_exit: bool = False) -> None:
        """
          Publish the image
          1. Check Dependencies
          2. Login to Snapser Registry
          3. Build your snap
          4. Tag the repo
          5. Push the image
          6. Upload swagger.json
        """
        self._check_dependencies()
        if not self.skip_build:
            self._docker_build()
        else:
            info('--skip-build set. Skipping the build step.')
        self._docker_tag()
        self._clean_slate()
        self._docker_login()
        self._docker_push()
        if self.path is not None or self.resources_path is not None:
            self.upload_docs(no_exit=True)
        snapctl_success(
            message='BYOSNAP publish successful', no_exit=no_exit)

    def publish_version(self, no_exit: bool = False) -> None:
        """
          Publish the version
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Publishing your snap...', total=None)
        try:
            profile_data = {}
            profile_data['dev_template'] = None
            profile_data['stage_template'] = None
            profile_data['prod_template'] = None
            with open(self.byosnap_profile, 'rb') as file:
                profile_data = json.load(file)
            payload = {
                "version": self.version,
                "image_tag": self.tag,
                "base_url": f"{self.prefix}/{self.sid}",
                "http_port": self.http_port,
                "readiness_probe_config": {
                    "path": self.readiness_path,
                    "initial_delay_seconds": self.readiness_delay
                },
                "dev_template": profile_data['dev_template'],
                "stage_template": profile_data['stage_template'],
                "prod_template": profile_data['prod_template']
            }
            res = requests.post(
                f"{self.base_url}/v1/snapser-api/byosnaps/{self.sid}/versions",
                json=payload, headers={'api-key': self.api_key},
                timeout=SERVER_CALL_TIMEOUT
            )
            if res.ok:
                return snapctl_success(
                    message='BYOSNAP publish version successful',
                    progress=progress, no_exit=no_exit)
            response_json = res.json()
            if "api_error_code" in response_json:
                if response_json['api_error_code'] == HTTP_ERROR_RESOURCE_NOT_FOUND:
                    snapctl_error(
                        message='BYOSnap not found.',
                        code=SNAPCTL_BYOSNAP_NOT_FOUND, progress=progress
                    )
                if response_json['api_error_code'] == HTTP_ERROR_SERVICE_VERSION_EXISTS:
                    snapctl_error(
                        message='Version already exists. Please update your version and try again',
                        code=SNAPCTL_BYOSNAP_PUBLISH_IMAGE_DUPLICATE_TAG_ERROR,
                        progress=progress
                    )
                if response_json['api_error_code'] == HTTP_ERROR_TAG_NOT_AVAILABLE:
                    snapctl_error(
                        message='Invalid tag. Please use the correct tag.',
                        code=SNAPCTL_BYOSNAP_PUBLISH_VERSION_DUPLICATE_TAG_ERROR,
                        progress=progress)
            snapctl_error(
                message=f'Server error: {json.dumps(response_json, indent=2)}',
                code=SNAPCTL_BYOSNAP_PUBLISH_VERSION_ERROR, progress=progress)
        except RequestException as e:
            snapctl_error(
                message='Exception: Unable to publish a ' +
                f'version for your snap. Exception: {e}',
                code=SNAPCTL_BYOSNAP_PUBLISH_VERSION_ERROR, progress=progress)
        finally:
            progress.stop()
        snapctl_error(
            message='Failed to publish version',
            code=SNAPCTL_BYOSNAP_PUBLISH_VERSION_ERROR, progress=progress)

    def update_version(self, no_exit: bool = False) -> None:
        """
          Update the byosnap version
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Updating your Byosnap...', total=None)
        try:
            payload = {
                'image_tag': self.tag,
            }
            res = requests.patch(
                f"{self.base_url}/v1/snapser-api/byosnaps/{self.sid}/versions/{self.version}",
                json=payload, headers={'api-key': self.api_key},
                timeout=SERVER_CALL_TIMEOUT
            )
            if res.ok:
                return snapctl_success(
                    message='BYOSNAP update version successful',
                    progress=progress, no_exit=no_exit)
            response_json = res.json()
            if "api_error_code" in response_json:
                if response_json['api_error_code'] == HTTP_ERROR_RESOURCE_NOT_FOUND:
                    snapctl_error(
                        message='BYOSnap not found.',
                        code=SNAPCTL_BYOSNAP_NOT_FOUND, progress=progress
                    )
                if response_json['api_error_code'] == HTTP_ERROR_SERVICE_IN_USE:
                    snapctl_error(
                        message='Version already in use in a staging or production snapend. ' +
                        'Please publish an unused version and start using that instead.',
                        code=SNAPCTL_BYOSNAP_UPDATE_VERSION_SERVICE_IN_USE_ERROR,
                        progress=progress
                    )
                if response_json['api_error_code'] == HTTP_ERROR_TAG_NOT_AVAILABLE:
                    snapctl_error(
                        message='Invalid tag. Please use the correct tag.',
                        code=SNAPCTL_BYOSNAP_UPDATE_VERSION_TAG_ERROR, progress=progress)
            snapctl_error(
                message=f'Server error: {json.dumps(response_json, indent=2)}',
                code=SNAPCTL_BYOSNAP_UPDATE_VERSION_ERROR, progress=progress)
        except RequestException as e:
            snapctl_error(
                message='Exception: Unable to update a ' +
                f'version for your snap. Exception: {e}',
                code=SNAPCTL_BYOSNAP_UPDATE_VERSION_ERROR, progress=progress)
        finally:
            progress.stop()
        snapctl_error(
            message='Failed to update version',
            code=SNAPCTL_BYOSNAP_UPDATE_VERSION_ERROR, progress=progress)

    def sync(self) -> None:
        '''
        Sync the snap
        '''
        try:
            self.tag = f'{self.tag}-{int(time.time())}'
            self.publish_image(no_exit=True)
            self.update_version(no_exit=True)
            byosnap_list: str = f"{self.sid}:{self.version}"
            snapend = Snapend(
                subcommand='update', base_url=self.base_url, api_key=self.api_key,
                snapend_id=self.snapend_id, byosnaps=byosnap_list, blocking=self.blocking
            )
            snapend.update(no_exit=True)
            return snapctl_success(message='BYOSNAP sync successful')
        except RequestException as e:
            snapctl_error(
                message='Exception: Unable to update a ' +
                f' version for your snap. Exception: {e}',
                code=SNAPCTL_BYOSNAP_UPDATE_VERSION_ERROR)
