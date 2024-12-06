import argparse
from rbt.cloud.v1alpha1.application.application_rbt import Application
from rbt.cloud.v1alpha1.auth.auth_rbt import APIKey
from rbt.v1alpha1.errors_pb2 import (
    PermissionDenied,
    StateAlreadyConstructed,
    StateNotConstructed,
    Unauthenticated,
)
from reboot.aio.aborted import Aborted
from reboot.aio.external import ExternalContext
from reboot.cli import terminal
from reboot.cli.rc import ArgumentParser, SubcommandParser
from reboot.cloud.api_keys import (
    InvalidAPIKeyBearerToken,
    parse_api_key_bearer_token,
)
from reboot.naming import (
    ApplicationName,
    QualifiedApplicationName,
    SpaceName,
    UserId,
    make_qualified_application_name,
)

DEFAULT_REBOOT_CLOUD_URL = "https://cloud.prod1.rbt.cloud:9991"

_API_KEY_FLAG = '--api-key'


def add_cloud_options(subcommand: SubcommandParser, *, api_key_required: bool):
    """Add flags common to all `rbt` commands that interact with the cloud."""
    # TODO: Consider moving these to flags on the `cloud` subcommand using #3845

    subcommand.add_argument(
        '--cloud-url',
        type=str,
        help="the URL of the Reboot cloud API",
        default=DEFAULT_REBOOT_CLOUD_URL,
        non_empty_string=True,
    )
    # TODO: This should probably be read from a file by default.
    subcommand.add_argument(
        _API_KEY_FLAG,
        type=str,
        help="the API key to use to connect to the Reboot Cloud API",
        default=None,
        required=api_key_required,
        non_empty_string=True,
    )


def _application_url(application_id: str, cloud_url: str) -> str:
    """
    Given a cloud URL (e.g. `https://cloud.prod1.rbt.cloud:9991`), returns the
    url for the given application (e.g. `https://a12345.prod1.rbt.cloud:9991`).
    """
    if not (
        cloud_url.startswith("https://") or cloud_url.startswith("http://")
    ):
        terminal.fail(
            f"Cloud URL '{cloud_url}' must have 'https://' or 'http://'."
        )
    protocol, hostname_port = cloud_url.split("://", maxsplit=1)
    if not hostname_port.startswith("cloud."):
        terminal.fail(
            f"Cloud host '{hostname_port}' is missing expected 'cloud.' prefix"
        )
    cell_hostname_port = hostname_port.removeprefix("cloud.")
    return f"{protocol}://{application_id}.{cell_hostname_port}"


def cloud_external_context(args) -> ExternalContext:
    api_key = args.api_key
    if api_key is None:
        terminal.fail(
            f"The {_API_KEY_FLAG} flag must be set in order to "
            "access the Reboot Cloud."
        )
    return ExternalContext(
        name="reboot-cli",
        bearer_token=api_key,
        url=args.cloud_url,
    )


def register_cloud(parser: ArgumentParser):
    """Register the 'cloud' subcommand with the given parser."""

    def _add_common_flags(subcommand: SubcommandParser):
        """Adds flags common to every `rbt cloud` subcommand."""

        add_cloud_options(subcommand, api_key_required=True)

        subcommand.add_argument(
            '--name',
            type=str,
            required=True,
            help="name of the application",
            non_empty_string=True,
        )

    up_subcommand = parser.subcommand('cloud up')
    _add_common_flags(up_subcommand)
    up_subcommand.add_argument(
        '--image-name',
        type=str,
        required=True,
        help='the Docker image name of the application; must be a public image',
        non_empty_string=True,
    )

    down_subcommand = parser.subcommand('cloud down')
    _add_common_flags(down_subcommand)


async def _user_id_from_api_key(api_key: str, cloud_url: str) -> str:
    try:
        api_key_id, api_key_secret = parse_api_key_bearer_token(token=api_key)
    except InvalidAPIKeyBearerToken:
        # Note that we do not log the API key contents; they are a secret, which
        # we don't want to output to a log file (if any).
        terminal.fail(
            "Invalid API key shape (expected: "
            "'XXXXXXXXXX-XXXXXXXXXXXXXXXXXXXX')"
        )

    context = ExternalContext(
        name="user-id-from-api-key",
        url=cloud_url,
        # TODO(rjh): once APIKey reads the bearer token for `Authenticate`, use
        #            that instead of passing `secret` in the proto below.
    )

    try:
        return (
            await APIKey.lookup(api_key_id).Authenticate(
                context,
                secret=api_key_secret,
            )
        ).user_id
    except Aborted as aborted:
        match aborted.error:
            case StateNotConstructed(  # type: ignore[misc]
            ) | PermissionDenied(  # type: ignore[misc]
            ) | Unauthenticated():  # type: ignore[misc]
                # Note that we do not log the API key contents; they
                # are a secret, which we don't want to output to a log
                # file (if any).
                terminal.fail("Invalid API key")
            case _:
                terminal.fail(f"Unexpected error: {aborted}")


async def _maybe_create_application(
    qualified_application_name: QualifiedApplicationName,
    cloud_url: str,
    api_key: str,
) -> None:
    """
    Creates the Application with the given `qualified_application_name` if it
    doesn't exist yet.
    """
    # Use a separate context for `Create()`, since that call is allowed to fail
    # and will then leave its context unable to continue due to idempotency
    # uncertainty.
    context = ExternalContext(
        name="cloud-up-create-application",
        url=cloud_url,
        bearer_token=api_key,
    )
    try:
        await Application.construct(
            id=qualified_application_name,
        ).Create(
            context,
        )
    except Aborted as aborted:
        match aborted.error:
            case StateAlreadyConstructed():  # type: ignore[misc]
                # That's OK; we just want the application to exist!
                pass
            case _:
                # Unexpected error, propagate it.
                raise


def _make_qualified_application_name(
    user_id: UserId,
    application_name: ApplicationName,
) -> QualifiedApplicationName:
    # During Alpha, the name of the space is always the same as the name of the
    # application.
    space_name: SpaceName = application_name
    return make_qualified_application_name(
        user_id, space_name, application_name
    )


async def _parse_common_cloud_args(
    args: argparse.Namespace
) -> tuple[str, str]:

    user_id = await _user_id_from_api_key(
        api_key=args.api_key,
        cloud_url=args.cloud_url,
    )

    qualified_application_name = _make_qualified_application_name(
        user_id=user_id,
        application_name=args.name,
    )

    return user_id, qualified_application_name


async def cloud_up(args: argparse.Namespace) -> None:
    """Implementation of the 'cloud up' subcommand."""

    user_id, qualified_application_name = await _parse_common_cloud_args(args)

    context = ExternalContext(
        name="cloud-up",
        url=args.cloud_url,
        bearer_token=args.api_key,
    )

    try:
        await _maybe_create_application(
            qualified_application_name=qualified_application_name,
            cloud_url=args.cloud_url,
            api_key=args.api_key,
        )
        application = Application.lookup(qualified_application_name)

        up_response = await application.Up(
            context,
            container_image_name=args.image_name,
        )
    except Aborted as aborted:
        # While `InvalidInputError` is declared for `Up()`, it is not
        # expected here as we'll fail earlier if `args.image_name` is
        # missing or invalid. And there aren't any declared errors for
        # `Create()`, so any error is unexpected. Most notably,
        # `PermissionDenied` can't happen, since the application we're
        # attempting to `Up()` is by definition owned by the user.
        terminal.fail(f"Unexpected error: {aborted}")

    application_id = up_response.application_id
    terminal.info(
        f"Application '{args.name}' starting; your application will be "
        "available at:\n\n"
        f"  {_application_url(application_id, args.cloud_url)}"
        "\n"
    )

    # TODO(rjh): once the Cloud waits to resolve `up_response.up_task_id` until
    #            the application has completed deployment, await the completion
    #            of `up_response.up_task_id` here, and tell the user when their
    #            application is in fact up and running.


async def cloud_down(args: argparse.Namespace) -> None:
    """Implementation of the 'cloud down' subcommand."""

    user_id, qualified_application_name = await _parse_common_cloud_args(args)

    context = ExternalContext(
        name="cloud-down",
        url=args.cloud_url,
        bearer_token=args.api_key,
    )

    try:
        await Application.lookup(qualified_application_name).Down(context)
    except Aborted as aborted:
        match aborted.error:
            case StateNotConstructed():  # type: ignore[misc]
                terminal.fail(
                    f"User '{user_id}' does not have an application named "
                    f"'{args.name}'"
                )
            case _:
                # There are no other expected errors for
                # `Down()`. Most notably, `PermissionDenied` can't
                # happen, since the application we're attempting to
                # `Down()` is by definition owned by the user.
                terminal.fail(f"Unexpected error: {aborted}")

    terminal.info(
        f"Success. Your application '{args.name}' is being terminated."
    )

    # TODO(rjh): once the CLoud waits to resolve `down_response.down_task_id`
    #            until the application has terminated, await the completion of
    #            `down_response.down_task_id` here, and tell the user when their
    #            application has in fact terminated.
