import asyncio
import colorama
import os
import sys
import traceback
import uuid
from log.log import get_logger
from pathlib import Path
from reboot.aio.auth.token_verifiers import TokenVerifier
from reboot.aio.external import ExternalContext
from reboot.aio.idempotency import IdempotencyRequiredError
from reboot.aio.servers import (
    InitializerError,
    InstantiateError,
    Server,
    run_application_initializer,
)
from reboot.aio.servicers import Serviceable, Servicer
from reboot.aio.tests import Reboot
from reboot.aio.tracing import function_span
from reboot.cli import terminal
from reboot.consensus.service_descriptor_validator import ProtoValidationError
from reboot.consensus.sidecar import SidecarServerFailed
from reboot.controller.consensus_managers import run_nodejs_consensus_process
from reboot.controller.exceptions import InputError
from reboot.controller.settings import USER_CONTAINER_GRPC_PORT
from reboot.run_environments import (
    InvalidRunEnvironment,
    RunEnvironment,
    RunSettings,
    TypescriptEnvironment,
    _detect_run_settings,
)
from reboot.settings import (
    DEFAULT_SECURE_PORT,
    ENVVAR_RBT_NAME,
    ENVVAR_RBT_PARTITIONS,
    ENVVAR_RBT_STATE_DIRECTORY,
    ENVVAR_REBOOT_LOCAL_ENVOY,
    ENVVAR_REBOOT_LOCAL_ENVOY_PORT,
    ENVVAR_REBOOT_NODEJS,
)
from typing import Awaitable, Callable, NoReturn, Optional

logger = get_logger(__name__)


def _handle_unknown_exception(
    exception: Exception,
    stack_trace: Optional[str] = None,
    with_contact_info: bool = True,
) -> None:
    """Pretty print stack trace and error message for an unknown exception. This
    includes informing the user how to best get in touch with us.
    """
    # When we are running this code within `node` we might want to log
    # things differently. For example, if we already have some logging in
    # our TypeScript code these logs may be redundant. Or we want to avoid
    # printing stack traces as those are Python specific.
    NODEJS: bool = os.environ.get(
        ENVVAR_REBOOT_NODEJS,
        "false",
    ).lower() == "true"

    if not NODEJS:
        if stack_trace is None:
            stack_trace = ''.join(traceback.format_exception(exception))

        # Emulate `traceback.print_exc()` by printing the
        # error to `sys.stderr`.
        print(stack_trace, file=sys.stderr)

    terminal.error(
        f'Caught unexpected `{type(exception).__name__}`: {exception}\n'
        '\n',
    )

    if not with_contact_info:
        return

    terminal.warn(
        'Please report this error, including any stack trace above, \n'
        'to the kind folks at Reboot - they\'ll be happy to help you out!\n'
        'You can get in touch via Discord: https://discord.gg/cRbdcS94Nr\n'
        '\n'
    )


def _handle_input_error(input_error: InputError) -> None:
    """Handle an input error."""
    # Special cases of a `causing_exception` to indicate that a
    # user has done something they should not.
    if isinstance(input_error, ProtoValidationError):
        terminal.error(input_error.reason)
        for validation_error in input_error.validation_errors:
            terminal.error(f'  - {validation_error}')
        terminal.error('\n')

    elif isinstance(input_error.causing_exception, SidecarServerFailed):
        if (
            'Failed to instantiate service'
            in str(input_error.causing_exception) and
            '/LOCK:' in str(input_error.causing_exception)
        ):
            terminal.error(
                '\n'
                "Sidecar server failed to start."
                '\n',
            )
            terminal.warn(
                'Did you start another instance of `rbt dev run` '
                'in another terminal?'
                '\n'
            )

    else:
        # TODO: ideally we can treat all "input errors" as implying
        # they come from bad user input, aka user bugs. Unfortunately
        # we have not always correctly used `InputError` that way,
        # instead we have constructed `InputError`'s lots of places
        # that might not actually be _user_ bugs. Thus, we need to
        # explicitly check which of the `InputError`'s we consider to
        # be _user_ bugs vs which ones are definitely _our_ bugs so
        # that we only output contact information when we think it is
        # _our_ bug.
        with_contact_info = not isinstance(
            input_error, (
                InitializerError,
                InstantiateError,
                IdempotencyRequiredError,
            )
        )

        _handle_unknown_exception(
            input_error,
            input_error.stack_trace,
            with_contact_info,
        )


class Application:
    """Entry point for all reboot applications."""

    def __init__(
        self,
        *,
        servicers: Optional[list[type[Servicer]]] = None,
        # A legacy gRPC servicer type can't be more specific than `type`,
        # because legacy gRPC servicers (as generated by the gRPC `protoc`
        # plugin) do not share any common base class other than `object`.
        legacy_grpc_servicers: Optional[list[type]] = None,
        initialize: Optional[Callable[[ExternalContext],
                                      Awaitable[None]]] = None,
        initialize_bearer_token: Optional[str] = None,
        token_verifier: Optional[TokenVerifier] = None,
    ):
        """
        :param servicers: the types of Reboot-powered servicers that this
                          Application will serve.
        :param legacy_grpc_servicers: the types of legacy gRPC servicers (not
                                      using Reboot libraries) that this
                                      Application will serve.

        :param initialize: will be called after the Application's servicers have
                       started for the first time, so that it can perform
                       initialization logic (e.g., creating some well-known
                       actors, loading some data, etc. It must do so in the
                       context of the given ExternalContext.

        :param initialize_bearer_token: a Bearer token that will be used to construct
            the `ExternalContext` passed to `initialize`.

        :param token_verifier: a TokenVerifier that will be used to verify
            authorization bearer tokens passed to the application.

        TODO(benh): update the initialize function to be run in a transaction
        and ensure that the transaction has finished before serving any other
        calls on the servicers.
        """
        # Runtime type checks, in case the type annotation didn't get checked
        # statically.
        for servicer in servicers or []:
            if not isinstance(servicer, type):
                raise ValueError(
                    "The `servicers` parameter contains a "
                    f"'{type(servicer).__name__}' object, but was expecting "
                    f"only classes. Try passing `{type(servicer).__name__}` "
                    f"instead of `{type(servicer).__name__}(...)`"
                )
            if not issubclass(servicer, Servicer):
                raise ValueError(
                    "The `servicers` parameter contains "
                    f"'{servicer.__name__}', which is not a Reboot servicer. "
                    "If it is a legacy gRPC servicer it should be passed in "
                    "via the `legacy_grpc_servicers` parameter instead"
                )
        for servicer in legacy_grpc_servicers or []:
            if not isinstance(servicer, type):
                raise ValueError(
                    "The `legacy_grpc_servicers` parameter contains a "
                    f"'{type(servicer).__name__}' object, but was expecting "
                    f"only classes. Try passing `{type(servicer).__name__}` "
                    f"instead of `{type(servicer).__name__}(...)`"
                )
            if issubclass(servicer, Servicer):
                raise ValueError(
                    "The `legacy_grpc_servicers` parameter contains "
                    f"'{servicer.__name__}', which is a Reboot servicer, not "
                    "a legacy gRPC servicer. It should be passed in via the "
                    "`servicers` parameter instead"
                )

        self._servicers = servicers
        self._legacy_grpc_servicers = legacy_grpc_servicers
        self._initialize = initialize
        self._token_verifier = token_verifier
        self._initialize_bearer_token = initialize_bearer_token

        self._rbt: Optional[Reboot] = None

        self._directory: Optional[Path] = None

        self._run_settings: Optional[RunSettings] = None
        try:
            self._run_settings = _detect_run_settings()
        except InvalidRunEnvironment:
            # Bail out. The user will be given a helpful error message at
            # run-time and the application will exit with a non-0 exit
            # code without a distracting stack trace.
            return

        if self._run_settings.run_environment not in [
            RunEnvironment.RBT_DEV,
            RunEnvironment.RBT_SERVE,
        ] or self._run_settings.typescript_environment == TypescriptEnvironment.NODEJS_CONSENSUS:
            # Only when running as part of `rbt dev run` we need to bring up
            # a Reboot cluster instance in-memory.
            # We don't need to bring up a Reboot cluster instance when running
            # TypeScript, because it will create its own cluster as part of 'reboot_native'.
            return

        self._name: Optional[str] = os.environ.get(ENVVAR_RBT_NAME)
        state_directory: Optional[str] = os.environ.get(
            ENVVAR_RBT_STATE_DIRECTORY
        )
        self._state_directory = (
            None if state_directory is None else Path(state_directory)
        )

        if self._name is not None:
            assert self._state_directory is not None

        # NOTE: we construct a 'Reboot' instance here so that it can
        # perform any process wide initialization as early as possible
        # (e.g., initializing multiprocessing before any threads are
        # created)
        if self._state_directory is not None:
            os.makedirs(self._state_directory, exist_ok=True)
        self._rbt = Reboot(
            application_name=self._name,
            state_directory=self._state_directory,
        )

    @function_span()
    async def _run(self) -> None:
        assert self._rbt is not None
        assert self._run_settings is not None
        await self._rbt.start()
        local_envoy: bool = os.environ.get(
            ENVVAR_REBOOT_LOCAL_ENVOY,
            'false',
        ).lower() == 'true'

        local_envoy_port: int = int(
            os.environ.get(
                ENVVAR_REBOOT_LOCAL_ENVOY_PORT, str(DEFAULT_SECURE_PORT)
            )
        )

        def partition_count() -> int:
            partition_count_str = os.environ.get(
                ENVVAR_RBT_PARTITIONS,
                None,
            )
            assert partition_count_str is not None
            return int(partition_count_str)

        config = await self._rbt.up(
            servicers=self._servicers,
            legacy_grpc_servicers=self._legacy_grpc_servicers,
            token_verifier=self._token_verifier,
            local_envoy=local_envoy,
            local_envoy_port=local_envoy_port,
            name=self._name,
            partitions=partition_count(),
        )

        if self._initialize is not None:
            await run_application_initializer(
                application_id=config.application_id(),
                initialize=self._initialize,
                context=self._rbt.create_external_context(
                    name='initialize',
                    bearer_token=self._initialize_bearer_token,
                    # We pass a `seed` so that we can
                    # re-execute `initialize` idempotently!
                    idempotency_seed=uuid.uuid5(
                        uuid.NAMESPACE_DNS,
                        'anonymous.rbt.dev',
                    ),
                    idempotency_required=True,
                    idempotency_required_reason=
                    'Calls to mutators from within your initialize function must use idempotency',
                )
            )

    async def _run_forever(self) -> NoReturn:
        """Runs the application and returns a status code indicating success
        or failure."""
        assert self._rbt is not None
        try:
            await self._run()

            # Wait forever unless we get cancelled!
            #
            # TODO(benh): have 'rbt.up()' return a tuple of (config,
            # future) so we can watch the future and if that ever
            # fails we should exit and return an error to the user.
            #
            # TODO(benh): also have 'rbt.up()' fail the future that it
            # returns to us if the local envoy that got started
            # happened to fail.
            forever = asyncio.Event()
            await forever.wait()
        finally:
            await self._rbt.stop()

        raise AssertionError("Unreachable")

    async def _run_kubernetes(self) -> NoReturn:
        """Runs a single consensus in a Kubernetes-appropriate way.

        Blocks until cancelled, then returns a status code indicating success
        or failure.
        """

        try:
            server = Server.create_on_k8s(
                serviceables=self._get_serviceables(),
                listen_address=f'0.0.0.0:{USER_CONTAINER_GRPC_PORT}',
                initialize=self._initialize,
                initialize_bearer_token=self._initialize_bearer_token,
                token_verifier=self._token_verifier,
            )
            server_run_task = asyncio.create_task(
                server.run(),
                name=f'server.run() in {__name__}',
            )

        except Exception as e:
            logger.error(f"Unexpected error while starting: {e}")
            # An unexpected error, by definition, is something that we didn't
            # see coming. It may have been caused by the user's code. Help them
            # (and us, if they file a bug report) debug it by printing the stack
            # trace.
            logger.error("Stack trace:", exc_info=True)
            raise SystemExit(1)

        # Wait forever, or at least until the server gets shut down.
        await server_run_task

        raise SystemExit(0)

    def _get_serviceables(self) -> list[Serviceable]:
        """Helper for converting servicers and legacy gRPC servicers into
        serviceables.
        """
        serviceables: list[Serviceable] = []
        for servicer in self._servicers or []:
            serviceables.append(Serviceable.from_servicer_type(servicer))

        for legacy_grpc_servicer in self._legacy_grpc_servicers or []:
            serviceables.append(
                Serviceable.from_servicer_type(legacy_grpc_servicer)
            )

        if len(serviceables) == 0:
            raise ValueError("No servicers were provided to the Application")

        return serviceables

    async def _run_nodejs_consensus(self) -> NoReturn:
        """Runs a single consensus in a nodejs-appropriate way.

        Blocks until cancelled, then raises SystemExit.
        """
        try:
            await run_nodejs_consensus_process(
                self._get_serviceables(),
                self._token_verifier,
            )
        except Exception as e:
            logger.error(f"Unexpected error while starting: {e}")
            # An unexpected error, by definition, is something that we didn't
            # see coming. It may have been caused by the user's code. Help them
            # (and us, if they file a bug report) debug it by printing the stack
            # trace.
            logger.error("Stack trace:", exc_info=True)
            raise SystemExit(1)

        raise SystemExit(0)

    async def run(self) -> NoReturn:
        """Runs the application, and does not return unless the application fails.

        Raises SystemExit in case of failure.
        """

        colorama.init()

        if self._run_settings is None:
            # We can't detect the run environment. Assume that the user is trying to
            # run the application locally, but doing it in a way we don't support.
            # Give a helpful error message pointing them to `rbt dev run`.
            terminal.error(
                "Please use 'rbt dev run' to run your application locally",
            )
            raise SystemExit(1)
        elif self._run_settings.run_environment in [
            RunEnvironment.RBT_DEV,
            RunEnvironment.RBT_SERVE,
        ]:
            if self._run_settings.typescript_environment != TypescriptEnvironment.NODEJS_CONSENSUS:
                try:
                    await self._run_forever()
                except InputError as e:
                    _handle_input_error(e)
                except Exception as e:
                    _handle_unknown_exception(e)

                raise SystemExit(1)
            else:
                await self._run_nodejs_consensus()

        await self._run_kubernetes()
