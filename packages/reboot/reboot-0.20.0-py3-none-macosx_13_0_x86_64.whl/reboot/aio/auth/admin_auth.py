import grpc
from log.log import get_logger
from reboot.aio.headers import AUTHORIZATION_HEADER
from reboot.aio.secrets import SecretNotFoundException, Secrets
from reboot.run_environments import running_rbt_dev
from reboot.settings import ADMIN_SECRET_NAME

logger = get_logger(__name__)


def auth_metadata_from_metadata(
    grpc_context: grpc.aio.ServicerContext
) -> tuple:
    """Helper to extract only the authorization metadata from a gRPC context.

    The context might and will contain other metadata that we should be careful
    with blindly duplicating, such as our own routing headers but also request
    id headers.
    """
    for key, value in grpc_context.invocation_metadata():
        if key == AUTHORIZATION_HEADER:
            return ((key, value),)
    return ()


class AdminAuthMixin:
    """Mixin that is used to provide a helper for checking that a request
    contains the necessary admin credentials.

    We use a mixin over a free standing function to avoid a global `Secrets` object.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__secrets = Secrets()

    async def ensure_admin_auth_or_fail(
        self,
        grpc_context: grpc.aio.ServicerContext,
    ) -> None:
        """Ensure that the request contains the necessary admin credentials.

        If the request does not contain the necessary credentials, the request
        is aborted; an exception is raised and propagated.
        """
        if running_rbt_dev():
            # In rbt dev mode, no admin secret needs to be specified - all calls
            # are assumed to be from the admin (and any specified secret is
            # ignored).
            return

        bearer_token: str
        try:
            metadata: dict[str, str] = dict(grpc_context.invocation_metadata())
            bearer_token = metadata[AUTHORIZATION_HEADER].removeprefix(
                'Bearer '
            )
        except KeyError:
            await grpc_context.abort(
                code=grpc.StatusCode.UNAUTHENTICATED,
                details='Missing bearer token',
            )
            # mypy doesn't have type information for grpc, and so doesn't know
            # that `abort` never returns.
            raise AssertionError
        except Exception as e:
            logger.error(
                "Unknown `%s` while extracting bearer token: %s",
                type(e),
                e,
            )
            raise

        admin_secret: str
        try:
            admin_secret = (await
                            self.__secrets.get(ADMIN_SECRET_NAME)).decode()
        except SecretNotFoundException:
            logger.warning(
                "Admin secret '%s' not found. "
                "Please check your configured secrets and try again",
                ADMIN_SECRET_NAME,
            )

            await grpc_context.abort(
                code=grpc.StatusCode.UNAUTHENTICATED,
                details='No admin secret configured - API disabled',
            )

            raise AssertionError  # For `mypy`.

        if bearer_token != admin_secret:
            await grpc_context.abort(
                code=grpc.StatusCode.PERMISSION_DENIED,
                details='Invalid bearer token',
            )
