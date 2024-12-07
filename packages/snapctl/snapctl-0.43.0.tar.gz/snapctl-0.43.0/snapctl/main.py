"""
    SnapCTL entrypoint
"""
import configparser
import os
from sys import platform
from typing import Union
import typer
import pyfiglet

from snapctl.commands.byosnap import ByoSnap
from snapctl.commands.byogs import ByoGs
from snapctl.commands.game import Game
from snapctl.commands.generate import Generate
from snapctl.commands.snapend import Snapend
from snapctl.config.constants import COMPANY_NAME, API_KEY, URL_KEY, CONFIG_FILE_MAC, \
    CONFIG_FILE_WIN, DEFAULT_PROFILE, VERSION, SNAPCTL_SUCCESS, CONFIG_PATH_KEY, \
    SNAPCTL_CONFIGURATION_INCORRECT
from snapctl.config.endpoints import END_POINTS
from snapctl.config.hashes import PROTOS_TYPES, SERVICE_IDS, \
    SNAPEND_MANIFEST_TYPES, SDK_TYPES
from snapctl.utils.echo import error, success, info
from snapctl.utils.helper import validate_api_key

######### Globals #########


def draw_ascii_text():
    """
      Draws the ascii text for Snapser
    """
    ascii_text = pyfiglet.figlet_format(COMPANY_NAME)
    typer.echo(ascii_text)


app = typer.Typer(
    help=draw_ascii_text(),
    context_settings={
        "help_option_names": ["-h", "--help"]
    }
)


######### HELPER METHODS #########


def extract_config(extract_key: str, profile: Union[str, None] = None) -> object:
    """
      Extracts the API Key from the environment variable and if not present from the config file
    """
    result = {
        'location': '',
        'value': None
    }
    # Option 1 - Get the API Key from the environment variable
    env_api_key = os.getenv(extract_key)
    if env_api_key is not None:
        result['location'] = 'environment-variable'
        result['value'] = env_api_key
        return result
    encoding: Union[str, None] = "utf-8-sig" if platform == 'win32' else None
    # Option 2 - Get the API Key from CONFIG PATH environment variable
    config_file_path: Union[str, None] = os.getenv(CONFIG_PATH_KEY)
    # Option 3 - Get the API Key from the hardcoded config file we look for
    if config_file_path is None:
        if platform == 'win32':
            config_file_path = os.path.expandvars(CONFIG_FILE_WIN)
        else:
            config_file_path = os.path.expanduser(CONFIG_FILE_MAC)
    result['location'] = f'{config_file_path}'
    if os.path.isfile(config_file_path):
        config = configparser.ConfigParser()
        config.read(config_file_path, encoding=encoding)
        config_profile: str = DEFAULT_PROFILE
        if profile is not None and profile != '' and profile != DEFAULT_PROFILE:
            result['location'] = f'"{config_file_path}:profile {profile}"'
            config_profile = f'profile {profile}'
            info(
                'Trying to extract API KEY from ' +
                f'{config_file_path}:profile {profile}"'
            )
        result['value'] = config.get(
            config_profile, extract_key, fallback=None, raw=True
        )
    else:
        info(
            f'Config file on platform {platform} not found at {config_file_path}')
    return result


def get_base_url(api_key: Union[str, None]) -> str:
    """
        Returns the base url based on the api_key
    """
    # Check if the user has a URL override
    url_key_obj = extract_config(URL_KEY, None)
    if url_key_obj['value'] is not None:
        return url_key_obj['value']
    # If there was no override then we use the default
    if api_key is None:
        return ''
    if api_key.startswith('dev_'):
        return END_POINTS['DEV']
    if api_key.startswith('devtwo_'):
        return END_POINTS['DEV_TWO']
    if api_key.startswith('playtest_'):
        return END_POINTS['PLAYTEST']
    return END_POINTS['PROD']


def validate_command_context(
        ctx: typer.Context,
):
    """
      Validator to confirm if the context has been set properly
    """
    if ctx.obj['api_key'] is None or ctx.obj['base_url'] == '':
        error("Snapctl Configuration Incorrect. Unable to extract API Key",
              SNAPCTL_CONFIGURATION_INCORRECT)
        raise typer.Exit(code=SNAPCTL_CONFIGURATION_INCORRECT)

######### CALLBACKS #########


def default_context_callback(ctx: typer.Context):
    """
      Common Callback to set the main app context
      This gets called on every command right at the start
    """
    # info("In default callback")
    # Ensure ctx object is instantiated
    ctx.ensure_object(dict)
    # Extract the api_key
    api_key_obj = extract_config(API_KEY, None)
    ctx.obj['version'] = VERSION
    ctx.obj['api_key'] = api_key_obj['value']
    ctx.obj['api_key_location'] = api_key_obj['location']
    ctx.obj['profile'] = DEFAULT_PROFILE
    ctx.obj['base_url'] = get_base_url(api_key_obj['value'])


def api_key_context_callback(
        ctx: typer.Context,
        api_key: Union[str, None] = None
):
    """
      Callback to set the context for the api_key
      This gets called only if the user has added a --api-key override
    """
    if api_key is None:
        return None
    # info("In API Key callback")
    # Ensure ctx object is instantiated
    ctx.ensure_object(dict)
    ctx.obj['version'] = VERSION
    ctx.obj['api_key'] = api_key
    ctx.obj['api_key_location'] = 'command-line-argument'
    ctx.obj['base_url'] = get_base_url(api_key)


def profile_context_callback(
        ctx: typer.Context,
        profile: Union[str, None] = None
):
    """
      Callback to set the context for the profile
      This gets called only if the user has added a --profile override
    """
    # Its important to early return if user has already entered API Key via command line
    if profile is None or ctx.obj['api_key_location'] == 'command-line-argument':
        return None
    # info("In Profile Callback")
    # Ensure ctx object is instantiated
    ctx.ensure_object(dict)
    api_key_obj = extract_config(API_KEY, profile)
    # if api_key_obj['value'] is None and profile is not None and profile != '':
    #     conf_file = ''
    #     if platform == 'win32':
    #         conf_file = os.path.expandvars(CONFIG_FILE_WIN)
    #     else:
    #         conf_file = os.path.expanduser(CONFIG_FILE_MAC)
    #     error(
    #         f'Invalid profile input {profile}. '
    #         f'Please check your snap config file at {conf_file}'
    #     )
    ctx.obj['version'] = VERSION
    ctx.obj['api_key'] = api_key_obj['value']
    ctx.obj['api_key_location'] = api_key_obj['location']
    ctx.obj['profile'] = profile if profile else DEFAULT_PROFILE
    ctx.obj['base_url'] = get_base_url(api_key_obj['value'])


# Presently in typer this is the only way we can expose the `--version`
def version_callback(value: bool = True):
    """
        Prints the version and exits
    """
    if value:
        success(f"Snapctl version: {VERSION}")
        raise typer.Exit(code=SNAPCTL_SUCCESS)


@app.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(
        None, "--version", "-v",
        help="Get the Snapctl version.",
        callback=version_callback
    ),
):
    """
    Snapser CLI Tool
    """
    default_context_callback(ctx)

######### TYPER COMMANDS #########


@app.command()
def validate(
    ctx: typer.Context,
    api_key: Union[str, None] = typer.Option(
        None, "--api-key", help="API Key override.", callback=api_key_context_callback
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=profile_context_callback
    ),
) -> None:
    """
    Validate your Snapctl setup
    """
    validate_command_context(ctx)
    validate_api_key(ctx.obj['base_url'], ctx.obj['api_key'])
    success("Setup is valid")
    raise typer.Exit(code=SNAPCTL_SUCCESS)


@app.command()
def byogs(
    ctx: typer.Context,
    # Required fields
    subcommand: str = typer.Argument(
        ..., help="BYOGs Subcommands: " + ", ".join(ByoGs.SUBCOMMANDS) + "."
    ),
    # sid: str = typer.Argument(
    #     ByoGs.SID,  help="Game Server Id. Should start with byogs"
    # ),
    # publish, publish-image and publish-version
    tag: str = typer.Option(
        None, "--tag",
        help="(req: build, push, publish) Tag for your snap"
    ),
    # publish and publish-image
    path: Union[str, None] = typer.Option(
        None, "--path", help="(req: build, publish) Path to your snap code"
    ),
    resources_path: Union[str, None] = typer.Option(
        None, "--resources-path", help="(optional: publish) Path to resources such as your Dockerfile, swagger.json or README.md"
    ),
    docker_file: str = typer.Option(
        "Dockerfile", help="(optional: publish) Dockerfile name to use"
    ),
    skip_build: bool = typer.Option(
        False, "--skip-build", help="(optional: publish) Skip the build step. You have to pass the image tag you used during the build step."
    ),
    snapend_id: str = typer.Option(
        None, "--snapend-id",
        help=("(req: sync) Snapend Id.")
    ),
    fleet_names: str = typer.Option(
        None, "--fleet-names",
        help=("(req: sync) Comma separated fleet names.")
    ),
    blocking: bool = typer.Option(
        False, "--blocking",
        help=(
            "(optional: update) Set to true if you want to wait for the update to complete "
            "before returning."
        )
    ),
    # overrides
    api_key: Union[str, None] = typer.Option(
        None, "--api-key", help="API Key override.", callback=api_key_context_callback
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=profile_context_callback
    ),
) -> None:
    """
      Bring your own game server commands
    """
    validate_command_context(ctx)
    byogs_obj: ByoGs = ByoGs(
        subcommand=subcommand,
        base_url=ctx.obj['base_url'],
        api_key=ctx.obj['api_key'],
        tag=tag,
        path=path,
        resources_path=resources_path,
        dockerfile=docker_file,
        skip_build=skip_build,
        snapend_id=snapend_id,
        fleet_names=fleet_names,
        blocking=blocking
    )
    getattr(byogs_obj, subcommand.replace('-', '_'))()
    success(f"BYOGs {subcommand} complete")
    raise typer.Exit(code=SNAPCTL_SUCCESS)


@app.command()
def byosnap(
    ctx: typer.Context,
    # Required fields
    subcommand: str = typer.Argument(
        ..., help="BYOSnap Subcommands: " + ", ".join(ByoSnap.SUBCOMMANDS) + "."
    ),
    sid: str = typer.Argument(..., help="Snap Id. Should start with byosnap-"),
    # create
    name: str = typer.Option(
        None, "--name", help="(req: create) Name for your snap."
    ),
    desc: str = typer.Option(
        None, "--desc", help="(req: create) Description for your snap"
    ),
    platform_type: str = typer.Option(
        None, "--platform",
        help="(req: create) Platform for your snap - " + \
        ", ".join(ByoSnap.PLATFORMS) + "."
    ),
    language: str = typer.Option(
        None, "--language",
        help="(req: create) Language of your snap - " + \
        ", ".join(ByoSnap.LANGUAGES) + "."
    ),
    # publish-image and publish-version
    tag: str = typer.Option(
        None, "--tag", help=(
            "(req: publish-image, publish-version, sync) Tag for your snap"
        )
    ),
    # publish-image
    path: Union[str, None] = typer.Option(
        None, "--path", help="(req: publish-image, sync) Path to your snap code"
    ),
    resources_path: Union[str, None] = typer.Option(
        None, "--resources-path", help="(optional: publish-image, sync; req: upload-docs) Path to resources such as your Dockerfile, swagger.json or README.md"
    ),
    docker_file: str = typer.Option(
        "Dockerfile", help="(optional: publish) Dockerfile name to use"
    ),
    # publish-version
    prefix: str = typer.Option(
        '/v1', "--prefix", help="(req: publish-version) URL Prefix for your snap"
    ),
    version: Union[str, None] = typer.Option(
        None, "--version",
        help="(req: publish-version) Snap version. Should start with v. Example vX.X.X"
    ),
    http_port: Union[str, None] = typer.Option(
        None, "--http-port", help="(req: publish-version) Ingress HTTP port version"
    ),
    byosnap_profile: Union[str, None] = typer.Option(
        None, "--byosnap-profile", help=(
            "(req: publish-version) Path to your byosnap-profile JSON file. You can generate a base version of this file using the `snapctl generate profile --category byosnap --out-path <output_path>` command."
        )
    ),
    skip_build: bool = typer.Option(
        False, "--skip-build", help="(optional: publish-image, sync) Skip the build step. You have to pass the image tag you used during the build step."
    ),
    readiness_path: str = typer.Option(
        None, "--readiness-path", help="(req: publish-version) Readiness path for your snap"
    ),
    readiness_delay: int = typer.Option(
        None, "--readiness-delay", help="(req: publish-version) Delay before readiness check"
    ),
    # sync
    snapend_id: str = typer.Option(
        None, "--snapend-id",
        help=("(req: sync) Snapend Id. NOTE: Development Snapends only.")
    ),
    blocking: bool = typer.Option(
        False, "--blocking",
        help=(
            "(optional: sync) Set to true if you want to wait for the update to complete "
            "before returning."
        )
    ),
    # overrides
    api_key: Union[str, None] = typer.Option(
        None, "--api-key", help="API Key override.", callback=api_key_context_callback
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=profile_context_callback
    ),
) -> None:
    """
      Bring your own snap commands
    """
    validate_command_context(ctx)
    byosnap_obj: ByoSnap = ByoSnap(
        subcommand=subcommand,
        base_url=ctx.obj['base_url'],
        api_key=ctx.obj['api_key'],
        sid=sid,
        name=name,
        desc=desc,
        platform_type=platform_type,
        language=language,
        tag=tag,
        path=path,
        resources_path=resources_path,
        dockerfile=docker_file,
        prefix=prefix,
        version=version,
        http_port=http_port,
        byosnap_profile=byosnap_profile,
        skip_build=skip_build,
        readiness_path=readiness_path,
        readiness_delay=readiness_delay,
        snapend_id=snapend_id,
        blocking=blocking
    )
    getattr(byosnap_obj, subcommand.replace('-', '_'))()
    success(f"BYOSnap {subcommand} complete")
    raise typer.Exit(code=SNAPCTL_SUCCESS)


@app.command()
def game(
    ctx: typer.Context,
    # Required fields
    subcommand: str = typer.Argument(
        ..., help="Game Subcommands: " + ", ".join(Game.SUBCOMMANDS) + "."
    ),
    # name
    name: str = typer.Option(
        None, "--name",
        help=("(req: create) Name of your game: ")
    ),
    # overrides
    api_key: Union[str, None] = typer.Option(
        None, "--api-key", help="API Key override.", callback=api_key_context_callback
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=profile_context_callback
    ),
) -> None:
    """
      Game commands
    """
    validate_command_context(ctx)
    game_obj: Game = Game(
        subcommand=subcommand,
        base_url=ctx.obj['base_url'],
        api_key=ctx.obj['api_key'],
        name=name
    )
    getattr(game_obj, subcommand.replace('-', '_'))()
    success(f"Game {subcommand} complete")
    raise typer.Exit(code=SNAPCTL_SUCCESS)


@app.command()
def generate(
    ctx: typer.Context,
    # Required fields
    subcommand: str = typer.Argument(
        ..., help=(
            "Generate Subcommands: " + \
            ", ".join(Generate.SUBCOMMANDS) + "." + " "
            "Deprecation Notice: " + \
            ",".join(Generate.DEPRECATED_SOON_SUBCOMMANDS) + \
            " will be deprecated soon. "
            "Use `snapctl generate profile --category byosnap --out-path <output_path>` command instead."
        )
    ),
    category: Union[str, None] = typer.Option(
        None, "--category",
        help=(
            "(req: profile, token) (profile: " +
            ", ".join(Generate.CATEGORIES['profile']) +
            ") (token: " + ", ".join(Generate.CATEGORIES['credentials']) + ')'
        )
    ),
    # byosnap-profile, profile
    out_path: Union[str, None] = typer.Option(
        None, "--out-path", help=(
            "(req: byosnap-profile, profile, token) Path to output the byosnap profile"
        )
    ),
    # overrides
    api_key: Union[str, None] = typer.Option(
        None, "--api-key", help="API Key override.", callback=api_key_context_callback
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=profile_context_callback
    ),
) -> None:
    """
      Generate files to be used by other commands
    """
    validate_command_context(ctx)
    generate_obj: Generate = Generate(
        subcommand=subcommand,
        base_url=ctx.obj['base_url'],
        api_key=ctx.obj['api_key'],
        category=category,
        out_path=out_path
    )
    getattr(generate_obj, subcommand.replace('-', '_'))()
    success(f"Generate {subcommand} complete")
    raise typer.Exit(code=SNAPCTL_SUCCESS)


@app.command()
def snapend(
    ctx: typer.Context,
    # Required fields
    subcommand: str = typer.Argument(
        ..., help="Snapend Subcommands: " + ", ".join(Snapend.SUBCOMMANDS) + "."
    ),
    # snapend_id: str = typer.Argument(..., help="Snapend Id"),
    snapend_id: str = typer.Option(
        None, "--snapend-id",
        help=("(req: state, update, download) Snapend Id")
    ),
    # enumerate
    game_id: str = typer.Option(
        None, "--game-id",
        help="(req: enumerate, clone) Game Id"
    ),
    # apply, clone
    manifest_path: str = typer.Option(
        None, "--manifest-path",
        help="(req: apply|clone) Path to the manifest file"
    ),
    # download
    category: str = typer.Option(
        None, "--category",
        help=(
            "(req: download) Category of the Download: " +
            ", ".join(Snapend.DOWNLOAD_CATEGORY) + "."
        )
    ),
    sdk_access_type: str = typer.Option(
        'external', "--sdk-access-type",
        help=(
            "(optional: download) Access type of the Download: " +
            "external, internal."
        )
    ),
    sdk_auth_type: str = typer.Option(
        None, "--sdk-auth-type",
        help=(
            "(optional: download) Only applicable for --category sdk --sdk-access-type external "
            "Auth-Types: (" + ", ".join(Snapend.AUTH_TYPES) + ")"
        )
    ),
    platform_type: str = typer.Option(
        None, "--type",
        help=(
            "(req: --category sdk|protos|snapend-manifest --type ) "
            "SDK Types: sdk(" + ", ".join(SDK_TYPES.keys()) +
            ") protos(" + ", ".join(PROTOS_TYPES.keys()) + ")" +
            ") snapend-manifest(" + \
            ", ".join(SNAPEND_MANIFEST_TYPES.keys()) + ")"
        )
    ),
    protos_category: str = typer.Option(
        'messages', "--protos-category",
        help=(
            "(optional: download) Only applicable for --category protos --protos-category"
            "Protos-Category: (" + ", ".join(Snapend.PROTOS_CATEGORY) + ")"
        )
    ),
    snaps: Union[str, None] = typer.Option(
        None, "--snaps",
        help=(
            "(optional: download) Comma separated list of snap ids to customize the "
              "SDKs, protos or admin settings. "
              "snaps(" + ", ".join(SERVICE_IDS)
        )
    ),
    # Clone
    name: Union[str, None] = typer.Option(
        None, "--name", help="(req: clone) Snapend name"),
    env: Union[str, None] = typer.Option(
        None, "--env", help=(
            "(req: clone) Snapend environment"
            "Environments: (" + ", ".join(Snapend.ENV_TYPES) + ")"
        )),
    # Download, Apply, Clone
    out_path: Union[str, None] = typer.Option(
        None, "--out-path", help="(optional: download|apply|clone) Path to save the output file"),
    # update
    byosnaps_list: str = typer.Option(
        None, "--byosnaps",
        help=(
            "(optional: update) Comma separated list of BYOSnap ids and versions. "
            "Eg: service-1:v1.0.0,service-2:v1.0.0"
        )
    ),
    byogs_list: str = typer.Option(
        None, "--byogs",
        help=(
            "(optional: update) Comma separated list of BYOGs fleet name:tags. "
            "Eg: fleet-1:service-1:v1.0.0,fleet-2:service-2:v1.0.0"
        )
    ),
    # create, update, promote, apply, clone
    blocking: bool = typer.Option(
        False, "--blocking",
        help=(
            "(optional: update) Set to true if you want to wait for the update to complete "
            "before returning."
        )
    ),
    # overrides
    api_key: Union[str, None] = typer.Option(
        None, "--api-key", help="API Key override.", callback=api_key_context_callback
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=profile_context_callback
    ),
) -> None:
    """
      Snapend commands
    """
    validate_command_context(ctx)
    snapend_obj: Snapend = Snapend(
        subcommand=subcommand,
        base_url=ctx.obj['base_url'],
        api_key=ctx.obj['api_key'],
        snapend_id=snapend_id,
        # Enumerate, Clone
        game_id=game_id,
        # Clone
        name=name, env=env,
        # Apply, Clone
        manifest_path=manifest_path,
        # Download
        category=category, sdk_access_type=sdk_access_type,
        sdk_auth_type=sdk_auth_type, platform_type=platform_type,
        protos_category=protos_category,
        snaps=snaps,
        # Download, Apply and Clone
        out_path=out_path,
        # Update
        byosnaps=byosnaps_list, byogs=byogs_list, blocking=blocking
    )
    getattr(snapend_obj, subcommand.replace('-', '_'))()
    success(f"Snapend {subcommand} complete")
    raise typer.Exit(code=SNAPCTL_SUCCESS)
