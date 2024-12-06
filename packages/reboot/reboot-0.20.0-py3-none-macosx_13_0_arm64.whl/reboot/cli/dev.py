import aiofiles.os
import argparse
import asyncio
import functools
import grpc
import json
import os
import random
import reboot.aio.tracing
import shutil
import sys
import termios
import tty
from colorama import Fore
from grpc_health.v1 import health_pb2, health_pb2_grpc
from pathlib import Path
from reboot.aio.backoff import Backoff
from reboot.aio.contexts import EffectValidation
# We import the whole `terminal` module (as opposed to the methods it contains)
# to allow us to mock these methods out in tests.
from reboot.cli import terminal
from reboot.cli.cloud import add_cloud_options
from reboot.cli.directories import (
    add_working_directory_options,
    dot_rbt_dev_directory,
    use_working_directory,
)
from reboot.cli.monkeys import monkeys, no_chaos_monkeys
from reboot.cli.protoc import protoc_direct
# We won't mock the classes in `rc`, so it's safe to import those directly.
from reboot.cli.rc import (
    ArgumentParser,
    ArgumentParserFactory,
    BaseTransformer,
    SubcommandParser,
    TransformerError,
)
from reboot.cli.subprocesses import Subprocesses
from reboot.cli.watch import watch
from reboot.controller.exceptions import InputError
from reboot.controller.plan_makers import validate_num_consensuses
from reboot.settings import (
    DEFAULT_SECURE_PORT,
    DOCS_BASE_URL,
    ENVOY_PROXY_IMAGE,
    ENVVAR_LOCAL_ENVOY_MODE,
    ENVVAR_LOCAL_ENVOY_USE_TLS,
    ENVVAR_RBT_CLOUD_API_KEY,
    ENVVAR_RBT_CLOUD_URL,
    ENVVAR_RBT_DEV,
    ENVVAR_RBT_EFFECT_VALIDATION,
    ENVVAR_RBT_FROM_NODEJS,
    ENVVAR_RBT_NAME,
    ENVVAR_RBT_NODEJS,
    ENVVAR_RBT_PARTITIONS,
    ENVVAR_RBT_SECRETS_DIRECTORY,
    ENVVAR_RBT_STATE_DIRECTORY,
    ENVVAR_REBOOT_LOCAL_ENVOY,
    ENVVAR_REBOOT_LOCAL_ENVOY_PORT,
)
from typing import Any, Awaitable, Callable, Optional


class EnvTransformer(BaseTransformer):

    def transform(self, value: str):
        if '=' not in value:
            raise TransformerError(
                f"Invalid flag '--env={value}': must be in the form "
                "'--env=KEY=VALUE'"
            )
        return value.split('=', 1)


def add_application_options(subcommand: SubcommandParser) -> None:
    """Helper that adds options used to run Reboot applications."""
    subcommand.add_argument(
        "--env",
        type=str,
        repeatable=True,
        transformer=EnvTransformer(),
        help=
        "sets any specified environment variables before running the application; "
        "'ENV' should be of the form 'KEY=VALUE'",
    )

    subcommand.add_argument(
        '--python',
        type=bool,
        default=False,
        help="whether or not to launch the application by "
        "passing it as an argument to 'python'",
    )

    subcommand.add_argument(
        '--nodejs',
        type=bool,
        default=False,
        help="whether or not to launch the application by "
        "passing it as an argument to 'node'",
    )

    subcommand.add_argument(
        "--secrets-directory",
        type=Path,
        default=None,
        help=(
            "a directory to use to override the default source (environment variables) of Secrets; "
            "in the Reboot Cloud, Secrets are written using `rbt cloud secret write`; "
            f"see {DOCS_BASE_URL}/develop/secrets for more information."
        ),
    )

    subcommand.add_argument(
        '--application',
        type=str,  # TODO: consider argparse.FileType('e')
        help='path to application to execute',
        required=True,
        non_empty_string=True,
    )


def register_dev(parser: ArgumentParser):
    _register_dev_run(parser)
    _register_dev_expunge(parser)


def _register_dev_run(parser: ArgumentParser):
    add_working_directory_options(parser.subcommand('dev run'))

    add_application_options(parser.subcommand('dev run'))

    parser.subcommand('dev run').add_argument(
        '--name',
        type=str,
        help=(
            "name of application; state will be persisted using this name in "
            "the `.rbt` state directory"
        ),
        non_empty_string=True,
    )

    parser.subcommand('dev run').add_argument(
        '--background-command',
        type=str,
        repeatable=True,
        help=
        'command(s) to execute in the background (multiple instances of this '
        'flag are supported)',
    )

    parser.subcommand('dev run').add_argument(
        '--partitions',
        type=int,
        help='the number of partitioned serving processes to spawn',
        # The goal in this case is to minimize the performance impact in `dev`,
        # while still having a small amount of partitioning to help shake out
        # bugs.
        default=2,
    )

    parser.subcommand('dev run').add_argument(
        '--local-envoy',
        type=bool,
        default=True,
        help='whether or not to bring up a local Envoy',
    )

    parser.subcommand('dev run').add_argument(
        '--local-envoy-port',
        type=int,
        help=f'port for local Envoy; defaults to {DEFAULT_LOCAL_ENVOY_PORT}',
    )

    parser.subcommand('dev run').add_argument(
        '--watch',
        type=str,
        repeatable=True,
        help=
        'path to watch; multiple instances are allowed; globbing is supported',
    )

    parser.subcommand('dev run').add_argument(
        '--chaos',
        type=bool,
        default=True,
        help='whether or not to randomly induce failures',
    )

    parser.subcommand('dev run').add_argument(
        '--effect-validation',
        type=str,
        default="quiet",
        help=(
            'whether to validate effects in development mode; '
            f'see {DOCS_BASE_URL}/develop/side_effects for more '
            'information.'
        ),
        non_empty_string=True,
    )

    parser.subcommand('dev run').add_argument(
        "--protoc-watch",
        type=bool,
        default=True,
        help="also run `rbt protoc --watch` in the background if true, taking "
        "'protoc' arguments from the '.rbtrc' file, which must be present",
    )

    parser.subcommand('dev run').add_argument(
        '--transpile',
        type=str,
        help="command to run _before_ trying to run the application to compile "
        "TypeScript files, e.g., 'npx tsc'",
        default=None,
        non_empty_string=True,
    )

    parser.subcommand('dev run').add_argument(
        "--use-localhost-direct",
        type=bool,
        default=False,
        help=argparse.SUPPRESS,
    )

    parser.subcommand('dev run').add_argument(
        "--terminate-after-health-check",
        type=bool,
        help=argparse.SUPPRESS,
    )

    # The `dev` command does not require an API key, since not everyone will
    # have access to secrets on day one.
    add_cloud_options(parser.subcommand('dev run'), api_key_required=False)


def _register_dev_expunge(parser: ArgumentParser):
    parser.subcommand('dev expunge').add_argument(
        '--name',
        type=str,
        help=(
            "name of the application to expunge; will remove this "
            "application's state from the `.rbt` state directory"
        ),
        required=True,
        non_empty_string=True,
    )

    parser.subcommand('dev expunge').add_argument(
        '--yes',
        type=bool,
        default=False,
        help="skip the confirmation prompt",
    )


async def _run_background_command(
    background_command: str,
    *,
    verbose: bool,
    print_as: Optional[str] = None,
    subprocesses: Subprocesses,
):
    # TODO: Align this with the global `terminal.is_verbose` boolean. We always
    # want error output in case of failure, but we might only want streamed output
    # if `is_verbose`.
    if verbose:
        terminal.info(
            f"Running background command '{print_as or background_command}'"
        )

    async with subprocesses.shell(background_command) as process:
        await process.wait()

        if process.returncode != 0:
            terminal.fail(
                f"Failed to run background command '{background_command}', "
                f"exited with status {process.returncode}"
            )
        elif verbose:
            terminal.warn(
                f"Background command '{background_command}' exited without errors"
            )


@reboot.aio.tracing.asynccontextmanager_span(set_status_on_exception=False)
async def _run(
    application,
    *,
    env: dict[str, str],
    launcher: str,
    subprocesses: Subprocesses,
    application_started_event: asyncio.Event,
):
    """Helper for running the application with an optional launcher."""
    args = [launcher, application]

    async with subprocesses.exec(*args, env=env) as process:
        application_started_event.set()
        yield process

    # As control is returned back to us, it means the application is no longer
    # running. We clear the event in preparation for the next run.
    application_started_event.clear()


def try_and_become_child_subreaper_on_linux():
    if sys.platform == 'linux':
        # The 'pyprctl' module is available on Linux only.
        import pyprctl
        try:
            pyprctl.set_child_subreaper(True)
        except:
            terminal.warn(
                "Failed to become child subreaper, we'll do our "
                "best to ensure all created processes are terminated"
            )
            pass


async def check_docker_status(subprocesses: Subprocesses):
    """Checks if Docker is running and can use the Envoy proxy image. Downloads
    that image if necessary."""
    async with subprocesses.exec(
        'docker',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    ) as process:
        stdout, _ = await process.communicate()
        if process.returncode != 0:
            terminal.fail(
                f"Could not use Docker:\n"
                "\n"
                f"{stdout.decode() if stdout is not None else '<no output>'}"
            )

    # The '-q' flag returns only the image ID, so if stdout is empty
    # then the image is not downloaded.
    async with subprocesses.exec(
        'docker',
        'images',
        '-q',
        ENVOY_PROXY_IMAGE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    ) as process:
        stdout, _ = await process.communicate()

        if process.returncode != 0:
            terminal.fail(
                f"Could not use Docker; 'docker images -q {ENVOY_PROXY_IMAGE}' failed with output:\n"
                "\n"
                f"{stdout.decode() if stdout is not None else '<no output>'}"
            )
        elif stdout is None or stdout == b'':
            # Empty output means the image is not downloaded because
            # 'docker' didn't find a match for the image name.
            terminal.info(
                f"Pulling Envoy proxy image '{ENVOY_PROXY_IMAGE}'..."
            )
            async with subprocesses.exec(
                'docker',
                'pull',
                ENVOY_PROXY_IMAGE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            ) as process:
                stdout, _ = await process.communicate()
                if process.returncode != 0:
                    terminal.fail(
                        f"Could not use Docker; 'docker pull {ENVOY_PROXY_IMAGE}' failed with output:\n"
                        "\n"
                        f"{stdout.decode() if stdout is not None else '<no output>'}"
                    )


async def _check_local_envoy_status(
    *,
    port: int,
    terminate_after_health_check: bool,
    application_started_event: asyncio.Event,
    use_localhost_direct: bool,
) -> None:
    """Checks if the application is up and running.
    Optionally exits as soon as the health check has passed.
    """
    # Wait until application is running with starting health check.
    await application_started_event.wait()

    # If we've been asked to use `localhost.direct` we use the 'dev'
    # subdomain as a workaround on a gRPC bug that produces log
    # message error about not matching the entry (*.localhost.direct)
    # in the certificate. See
    # https://github.com/reboot-dev/mono/issues/2305
    #
    # We also want to print out 'dev.localhost.direct' so that our
    # users copy that to also avoid getting the log message error from
    # their gRPC or Reboot calls.
    address = (
        f'dev.localhost.direct:{port}'
        if use_localhost_direct else f'127.0.0.1:{port}'
    )

    protocol = "https" if use_localhost_direct else "http"

    backoff = Backoff(
        initial_backoff_seconds=0.01,
        max_backoff_seconds=1,
        backoff_multiplier=1.01,
    )
    was_application_serving = False
    while True:
        try:
            async with (
                grpc.aio.secure_channel(
                    address,
                    grpc.ssl_channel_credentials(),
                ) if use_localhost_direct else grpc.aio.insecure_channel(
                    address,
                )
            ) as channel:
                response = await health_pb2_grpc.HealthStub(channel).Check(
                    health_pb2.HealthCheckRequest()
                )

                is_application_serving = (
                    response.status == health_pb2.HealthCheckResponse.SERVING
                )

        except grpc.aio.AioRpcError:
            is_application_serving = False

        if is_application_serving:
            backoff.clear()

        if (
            is_application_serving != was_application_serving and
            application_started_event.is_set()
        ):
            was_application_serving = is_application_serving

            if is_application_serving:
                terminal.info("Application is serving traffic ...\n")
                terminal.info(
                    f"  Your API is available at {address}\n"
                    "\n"
                    f"  You can use '{protocol}://{address}' as the `url` for an `ExternalContext`\n"
                    "\n"
                    f"  You can inspect your state at {protocol}://{address}/__/inspect\n",
                    color=Fore.WHITE,
                )
                if terminate_after_health_check:
                    # TODO: `initializer`s run asynchronously, but can cause the application
                    # to fail to start up, even after the health check has passed. We sleep a
                    # fixed amount of time after the healthcheck to try to catch those cases.
                    await asyncio.sleep(10)
                    return
            else:
                terminal.warn("Application stopped serving traffic\n")

        if is_application_serving:
            # Once an application is known to be serving traffic, we can take it
            # a little easier on the health checks. That saves us from spamming
            # Envoy logs, if nothing else.
            await asyncio.sleep(1)
        else:
            await backoff()


async def _cancel_all(tasks: list[asyncio.Task]) -> None:
    if not tasks:
        return

    for task in tasks:
        task.cancel()

    await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)


async def _wait_for_first_completed(
    arg0: asyncio.Task[Any], *args: asyncio.Task[Any] | None
) -> set[asyncio.Task[Any]]:
    """Return the first of the given tasks to complete."""
    completed, _ = await asyncio.wait(
        [arg0, *(arg for arg in args if arg is not None)],
        return_when=asyncio.FIRST_COMPLETED
    )
    return completed


def protoc_parser_if_protoc_watch(
    dev_args,
    dev_parser: ArgumentParser,
    parser_factory: ArgumentParserFactory,
) -> Optional[ArgumentParser]:
    """Check whether we can run `rbt protoc --watch` without further
    user-specified arguments. That depends on whether the user has
    specified the necessary arguments in an `.rbtrc`.

    If so, returns the `rbt protoc` ArgumentParser to use.
    """
    if not dev_args.protoc_watch:
        return None
    if dev_parser.dot_rc is None:
        terminal.fail(
            "The '--protoc-watch' flag was specified (or set by default), but "
            "no '.rbtrc' file was found. Add an '.rbtrc' file containing "
            "the necessary arguments to run 'rbt protoc' to use 'rbt dev "
            "run --protoc-watch', or pass '--no-protoc-watch'."
        )

    return parser_factory(['rbt', 'protoc'])


async def induce_chaos() -> Optional[int]:
    """Helper that allows inducing chaos via pressing keys 0-9."""

    def read(future: asyncio.Future[Optional[int]]):
        value = sys.stdin.read(1)
        if value == '0':
            # No delay, restart app immediately.
            future.set_result(None)
        elif value in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            # Delay restarting app by the 2 raised to the power of the
            # key pressed, e.g., if '3' was pressed we'll wait 8
            # seconds, if '4' is pressed we'll wait 16 seconds, if '9'
            # was pressed we'll wait 512 seconds (almost 10 minutes).
            future.set_result(2**int(value))

    future: asyncio.Future[Optional[int]] = asyncio.Future()

    # Add an async file descriptor reader to our running event
    # loop so that we know when a key has been pressed.
    loop = asyncio.get_running_loop()

    sys_stdin_fd = sys.stdin.fileno()

    loop.add_reader(sys_stdin_fd, read, future)

    try:
        return await future
    finally:
        loop.remove_reader(sys_stdin_fd)


DEFAULT_LOCAL_ENVOY_PORT: int = DEFAULT_SECURE_PORT


def _check_common_args(args):
    if args.python and args.nodejs:
        terminal.fail(
            "Only one of '--python' or '--nodejs' should be specified."
        )
    elif not args.python and not args.nodejs:
        terminal.fail("One of '--python' or '--nodejs' must be specified.")


@reboot.aio.tracing.function_span()
async def dev_run(
    args,
    *,
    parser: ArgumentParser,
    parser_factory: ArgumentParserFactory,
) -> int:
    """Implementation of the 'dev run' subcommand."""

    _check_common_args(args)

    # We don't expect developers to have Envoy installed
    # on their own machines, so we pull and run it as a
    # Docker container, unless specified otherwise via the
    # `ENVVAR_LOCAL_ENVOY_MODE` env variable, which
    # we at least use to run nodejs examples on macOS
    # GitHub runners since they don't have Docker.
    local_envoy_mode = os.environ.get(ENVVAR_LOCAL_ENVOY_MODE, 'docker')
    os.environ[ENVVAR_LOCAL_ENVOY_MODE] = local_envoy_mode

    if args.use_localhost_direct:
        # We ask for TLS without specifying a specific certificate,
        # which means Envoy will use the one for `localhost.direct`.
        os.environ[ENVVAR_LOCAL_ENVOY_USE_TLS] = 'True'
    else:
        os.environ[ENVVAR_LOCAL_ENVOY_USE_TLS] = 'False'

    if parser.dot_rc is not None:
        while True:
            async with watch([parser.dot_rc]) as rc_file_event_task:
                return_code = await _dev_run(
                    args,
                    parser=parser,
                    parser_factory=parser_factory,
                    rc_file_event_task=rc_file_event_task,
                )
            if return_code is not None:
                return return_code

            terminal.info(
                '\n'
                f'{parser.dot_rc_filename} modified; restarting ... '
                '\n'
            )
            args, _ = parser.parse_args()
    else:
        return_code = await _dev_run(
            args,
            parser=parser,
            parser_factory=parser_factory,
            rc_file_event_task=None,
        )
        assert return_code is not None, "Should not have requested re-running: no `rc_file_event_task` was set."
        return return_code


@reboot.aio.tracing.function_span()
async def _dev_run(
    args,
    *,
    parser: ArgumentParser,
    parser_factory: ArgumentParserFactory,
    rc_file_event_task: Optional[asyncio.Task],
) -> Optional[int]:
    """Changes the working directory, and executes other preparation that needs
    cleanup when the dev loop exits.

    Has the same return semantics as `__dev_run`.
    """

    # Determine the working directory and move into it.
    with use_working_directory(args, parser, verbose=True):

        # If on Linux try and become a child subreaper so that we can
        # properly clean up all processes descendant from us!
        try_and_become_child_subreaper_on_linux()

        # Prepare to run background tasks and to potentially adjust terminal
        # settings, both of which need cleanup on exit.
        background_command_tasks: list[asyncio.Task] = []

        # In some environments, e.g., CI, we don't have a tty, nor do
        # we need one as we're not expecting to read from stdin.
        # 'sys.stdin.isatty()' returns True even if it is called from a
        # '.sh' script, which blocks the execution of
        # 'rbt dev run --terminate-after-health-check'.
        use_tty = sys.stdin.isatty(
        ) and args.terminate_after_health_check is not True

        # Save the old tty settings so we can set them back to that
        # when exiting.
        sys_stdin_fd = sys.stdin.fileno()
        old_tty_settings = termios.tcgetattr(sys_stdin_fd) if use_tty else None
        try:
            # Set the tty to not echo key strokes back to the terminal
            # and also remove buffering so we can read a single key
            # stroke at a time (yes, `tty.setcbreak()` does all that!)
            if use_tty:
                tty.setcbreak(sys_stdin_fd)

            # Then execute the dev loop.
            return await __dev_run(
                args,
                parser=parser,
                parser_factory=parser_factory,
                rc_file_event_task=rc_file_event_task,
                background_command_tasks=background_command_tasks,
            )
        finally:
            await _cancel_all(background_command_tasks)
            # Reset the terminal to old settings, i.e., make key
            # strokes be echoed, etc.
            if old_tty_settings is not None:
                try:
                    termios.tcsetattr(
                        sys_stdin_fd, termios.TCSADRAIN, old_tty_settings
                    )
                except:
                    # TODO: figure out why when running a `nodejs`
                    # application trying to "reset" TTY settings
                    # raises. Initial experimentation has shown that
                    # `sys.stdin` is still open and valid. Perhaps
                    # `node` itself is doing some form of "reset"?
                    pass


@reboot.aio.tracing.function_span()
async def __dev_run(
    args,
    *,
    parser: ArgumentParser,
    parser_factory: ArgumentParserFactory,
    rc_file_event_task: Optional[asyncio.Task],
    background_command_tasks: list[asyncio.Task],
) -> Optional[int]:
    """Runs until:
      * the given `rc_file_event_task` triggers (returns None)
      * the health check passes, and `--terminate-on-health-check` is set (returns 0)
      * an exception is raised
    """
    # Use `Subprocesses` to manage all of our subprocesses for us.
    subprocesses = Subprocesses()

    application = os.path.abspath(args.application)
    application_started_event = asyncio.Event()

    # Run background tasks.
    for background_command in args.background_command or []:
        background_command_tasks.append(
            asyncio.create_task(
                _run_background_command(
                    background_command,
                    verbose=True,
                    subprocesses=subprocesses,
                ),
                name=f'_run_background_command(...) in {__name__}',
            )
        )

    # Boolean indicating whether or not user would like us to do
    # transpilation for them automatically.
    auto_transpilation = Path(application).suffix == '.ts'

    # If `--protoc-watch` is enabled, prepare to invoke protoc as part of our loop.
    proto_globs = []
    needs_proto_compile = False
    protoc_python_directory: Optional[str] = None
    proto_compile: Optional[Callable[[], Awaitable[int]]] = None

    protoc_parser: Optional[ArgumentParser] = protoc_parser_if_protoc_watch(
        args,
        parser,
        parser_factory,
    )

    if protoc_parser is not None:
        try:
            protoc_args, protoc_argv_after_dash_dash = protoc_parser.parse_args(
            )
        except SystemExit:
            # Trying to catch 'sys.exit()' from top level 'protoc' parser.
            terminal.fail(
                "Failed to run 'rbt protoc' as part of 'rbt dev run' with "
                "'--protoc-watch' flag set.\n"
                "Edit the '.rbtrc' file to set the necessary arguments to run "
                "'rbt protoc', or pass '--no-protoc-watch'."
            )

        if args.transpile is not None:
            if 'react' not in protoc_args or 'nodejs' not in protoc_args:
                terminal.fail(
                    "You must pass either '--react' or '--nodejs' to 'rbt protoc' to use '--transpile'."
                )
            if auto_transpilation:
                terminal.fail(
                    "You can not pass '--transpile' when passing a '.ts' file to '--application' as that implies you want us to do the transpilation for you."
                )

        if auto_transpilation:
            rbt_from_nodejs = os.environ.get(
                ENVVAR_RBT_FROM_NODEJS,
                "false",
            ).lower() == "true"

            if not rbt_from_nodejs:
                terminal.fail(
                    "Expecting to be invoked from Node.js in order to do transpilation of your TypeScript code for you."
                )

            # NOTE: this isn't a technical requirement, but requiring
            # '--name' simplifies being able to tell people where to
            # find their transpiled code in the event that something
            # isn't working.
            if args.name is None:
                terminal.fail(
                    "You must pass '--name' for us to do transpilation of your TypeScript code for you."
                )

        protoc_python_directory = protoc_args.python
        proto_globs = [
            f"{pd}/**/*.proto" for pd in protoc_args.proto_directories
        ]
        needs_proto_compile = True
        proto_compile = functools.partial(
            protoc_direct,
            protoc_args,
            protoc_argv_after_dash_dash,
            protoc_parser,
            subprocesses,
        )

    # Set all the environment variables that
    # 'reboot.aio.Application' will be looking for.
    #
    # We make a copy of the environment so that we don't change
    # our environment variables which might cause an issue.
    env = os.environ.copy()

    env[ENVVAR_RBT_DEV] = 'true'

    if args.name is not None:
        env[ENVVAR_RBT_NAME] = args.name
        # Use a state directory specific to the application name. For some
        # applications there may be multiple consensuses, each with their own
        # subdirectory.
        env[ENVVAR_RBT_STATE_DIRECTORY] = str(
            dot_rbt_dev_directory(args, parser) / args.name
        )

    if args.secrets_directory is not None:
        env[ENVVAR_RBT_SECRETS_DIRECTORY] = args.secrets_directory

    health_check_task: Optional[asyncio.Task] = None
    if args.local_envoy:
        # Check if Docker is running and can access the Envoy proxy image.
        # Fail otherwise.
        if os.environ[ENVVAR_LOCAL_ENVOY_MODE] == 'docker':
            await check_docker_status(subprocesses)
        env[ENVVAR_REBOOT_LOCAL_ENVOY] = 'true'

        health_check_task = asyncio.create_task(
            _check_local_envoy_status(
                port=args.local_envoy_port or DEFAULT_LOCAL_ENVOY_PORT,
                terminate_after_health_check=args.terminate_after_health_check
                or False,
                application_started_event=application_started_event,
                use_localhost_direct=args.use_localhost_direct,
            ),
            name=f'_check_local_envoy_status(...) in {__name__}',
        )
        background_command_tasks.append(health_check_task)
    else:
        env[ENVVAR_REBOOT_LOCAL_ENVOY] = 'false'

    env[ENVVAR_REBOOT_LOCAL_ENVOY_PORT] = str(
        args.local_envoy_port or DEFAULT_LOCAL_ENVOY_PORT
    )

    try:
        validate_num_consensuses(args.partitions, "partitions")
    except InputError as e:
        terminal.fail(f"Invalid `--partitions` value: {e}")
    env[ENVVAR_RBT_PARTITIONS] = str(args.partitions)

    if args.nodejs:
        env[ENVVAR_RBT_NODEJS] = 'true'

        # Also pass the `--enable-source-maps` option to `node` so
        # that we get better debugging experience with stacks.
        if "NODE_OPTIONS" in env:
            env["NODE_OPTIONS"] += " --enable-source-maps"
        else:
            env["NODE_OPTIONS"] = "--enable-source-maps"

        # Also set env to 'development' unless it's already been set
        # as this will make sure that (a) Node.js will consume a
        # `.env.development` and (b) it will do module resolution the
        # same way that we do via `esbuild` since we set `conditions:
        # ["development"]` (see reboot/nodejs/rbt-esbuild.ts).
        if "NODE_ENV" not in env:
            env["NODE_ENV"] = "development"

    try:
        # TODO: In Python 3.12, can use `choice in Enum`.
        EffectValidation[args.effect_validation.upper()]
    except KeyError:
        options = ', '.join(e.name.lower() for e in EffectValidation)
        terminal.fail(
            f"Unexpected value for --effect-validation: `{args.effect_validation}`. "
            f"Legal values are: {options}"
        )
    env[ENVVAR_RBT_EFFECT_VALIDATION] = args.effect_validation.upper()

    if args.api_key is not None:
        env[ENVVAR_RBT_CLOUD_API_KEY] = args.api_key
    env[ENVVAR_RBT_CLOUD_URL] = args.cloud_url

    # Also include all environment variables from '--env='.
    for (key, value) in args.env or []:
        env[key] = value

    # If 'PYTHONPATH' is not explicitly set, we'll set it to the
    # specified generated code directory.
    if 'PYTHONPATH' not in env and protoc_python_directory is not None:
        env['PYTHONPATH'] = protoc_python_directory

    if not args.chaos:
        # When running with '--terminate-after-health-check', we
        # would love to be consistent in the output we produce to be able to
        # test it.
        no_chaos_monkey = no_chaos_monkeys[
            0] if args.terminate_after_health_check else random.choice(
                no_chaos_monkeys
            )
        terminal.warn(
            '\n' + no_chaos_monkey + '\n'
            'You Have Disabled Chaos Monkey! (see --chaos)\n'
            '\n'
            'Only You (And Chaos Monkey) Can Prevent Bugs!'
            '\n'
        )

    # Bool used to steer the printing. i.e., are we starting or restarting
    # the application?
    first_start = True

    # Optional delay, used for inducing chaos with a delay.
    delay: Optional[int] = None

    # Variables used for auto transpiling and bundling TypeScript if
    # given a `.ts` file.
    ts_input_paths: list[str] = []
    bundle_directory: Optional[Path] = None

    def bundle_file():
        assert auto_transpilation
        assert bundle_directory is not None
        return bundle_directory / 'bundle.js'

    while True:
        if delay is not None:
            await asyncio.sleep(delay)
            delay = None

        # Determine the appropriate verb.
        start_verb = "Starting" if first_start else "Restarting"
        if args.name is None:
            terminal.warn(
                f'{start_verb} an ANONYMOUS application; to reuse state '
                'across application restarts use --name'
                '\n'
            )
        else:
            terminal.info(
                f'{start_verb} application with name "{args.name}"...'
                '\n'
            )
        first_start = False

        async with watch(proto_globs) as protos_event_task:

            if needs_proto_compile:
                assert proto_compile is not None
                if await proto_compile() != 0:
                    # Failed to compile: wait for a relevant input to have changed.
                    terminal.warn(
                        '\n'
                        'Protoc compilation failed '
                        '... waiting for modification'
                        '\n'
                    )
                    completed = await _wait_for_first_completed(
                        protos_event_task,
                        rc_file_event_task,
                    )
                    if rc_file_event_task in completed:
                        return None
                    terminal.info(
                        '\n'
                        'Application modified; restarting ... '
                        '\n'
                    )
                    continue

                # Else, successfully compiled.
                needs_proto_compile = False

            # NOTE: we don't want to watch `application` yet as it
            # might be getting generated if we're using `transpile`.
            async with watch(args.watch or []) as watch_event_task:

                # Transpile TypeScript if requested.
                if args.transpile is not None:
                    terminal.info(
                        f'Transpiling TypeScript with `{args.transpile}` ...'
                        '\n',
                    )
                    async with subprocesses.shell(
                        f'{args.transpile}'
                    ) as process:
                        await process.wait()
                        if process.returncode != 0:
                            terminal.warn(
                                f'`{args.transpile}` failed with exit status {process.returncode} '
                                '... waiting for modification'
                                '\n'
                            )
                            completed = await _wait_for_first_completed(
                                watch_event_task,
                                protos_event_task,
                                rc_file_event_task,
                            )
                            if rc_file_event_task in completed:
                                return None
                            if protos_event_task in completed:
                                needs_proto_compile = True
                            terminal.info(
                                '\n'
                                'Application modified; restarting ... '
                                '\n'
                            )
                            continue

                if auto_transpilation:
                    # TODO: ensure `esbuild` is on PATH (should be
                    # because we have validated `rbt_from_nodejs`.
                    async with subprocesses.shell(
                        f'rbt-esbuild {application} {args.name}',
                        stdout=asyncio.subprocess.PIPE,
                    ) as process:
                        stdout, _ = await process.communicate()

                        if process.returncode != 0:
                            if len(ts_input_paths) == 0:
                                terminal.fail(
                                    '\n'
                                    'Transpilation failed, please fix the errors above and re-run `rbt dev`'
                                )

                            terminal.warn(
                                '\n'
                                'Transpilation failed ... waiting for modification\n'
                                '\n'
                            )

                            # Watch all previously watched files for
                            # changes as we don't know which file
                            # might have add the transpilation issue.
                            async with watch(
                                ts_input_paths
                            ) as application_event_task:
                                completed = await _wait_for_first_completed(
                                    application_event_task,
                                    watch_event_task,
                                    protos_event_task,
                                    rc_file_event_task,
                                )

                                if application_event_task in completed:
                                    return None
                                if rc_file_event_task in completed:
                                    return None
                                if protos_event_task in completed:
                                    needs_proto_compile = True

                                terminal.info(
                                    '\n'
                                    'Application modified; restarting ... '
                                    '\n'
                                )
                                continue

                        bundle_directory = Path(stdout.decode().strip())

                        assert bundle_directory != ""

                        # Now add all the input files that we need to
                        # watch, starting from an empty list.
                        ts_input_paths.clear()
                        metafile = bundle_directory / 'meta.json'
                        with open(str(metafile), 'r') as file:
                            meta = json.load(file)
                            for input in meta['inputs']:
                                ts_input_paths.append(os.path.abspath(input))

                        # TODO: if we want to rebuild when external
                        # modules change, such as `@reboot-dev/reboot`
                        # we'd need to explicitly add them to watch
                        # because they will be marked as 'external' when
                        # calling `esbuild` and thus it is not in the
                        # `metafile`.

                def have_rc_file_or_protos_or_watch_event():
                    """Helper for checking if we have an event that may warrant returning
                    or continuing the outer loop."""
                    return (
                        rc_file_event_task is not None and
                        rc_file_event_task.done()
                    ) or (
                        protos_event_task is not None and
                        protos_event_task.done()
                    ) or (
                        watch_event_task is not None and
                        watch_event_task.done()
                    )

                # It's possible that the application may get deleted
                # and then (re)created by a build system so rather
                # than fail if we can't find it we'll retry but print
                # out a warning every ~5 seconds (which corresponds
                # to ~10 retries since we sleep for 0.5 seconds
                # between each retry).
                retries = 0
                while (
                    not await aiofiles.os.path.isfile(application) and
                    not have_rc_file_or_protos_or_watch_event()
                ):
                    if retries != 0 and retries % 10 == 0:
                        terminal.warn(
                            f"Missing application at '{application}' "
                            "(is it being rebuilt?)"
                        )
                    retries += 1
                    await asyncio.sleep(0.5)

                # While waiting for a missing application it's
                # possible an event fired that might be responsible
                # for creating the application, e.g., running `tsc`.
                if (
                    rc_file_event_task is not None and
                    rc_file_event_task.done()
                ):
                    return None
                elif (
                    protos_event_task is not None and protos_event_task.done()
                ):
                    needs_proto_compile = True
                    continue
                elif (
                    watch_event_task is not None and watch_event_task.done()
                ):
                    continue

                if not await aiofiles.os.path.isfile(application):
                    terminal.fail(f"Missing application at '{application}'")

                launcher: Optional[str] = None
                if args.python:
                    launcher = sys.executable
                else:
                    launcher = 'node'

                # TODO(benh): catch just failure to create the subprocess
                # so that we can either try again or just listen for a
                # modified event and then try again.
                async with watch(
                    [application] if not auto_transpilation else ts_input_paths
                ) as application_event_task, _run(
                    application
                    if not auto_transpilation else str(bundle_file()),
                    env=env,
                    launcher=launcher,
                    subprocesses=subprocesses,
                    application_started_event=application_started_event,
                ) as process:
                    process_wait_task = asyncio.create_task(
                        process.wait(),
                        name=f'process.wait() in {__name__}',
                    )

                    induce_chaos_task = asyncio.create_task(
                        induce_chaos(),
                        name=f'induce_chaos() in {__name__}',
                    )

                    chaos_task: Optional[asyncio.Task] = None
                    if args.chaos:
                        chaos_task = asyncio.create_task(
                            asyncio.sleep(600),
                            name=f'asyncio.sleep(600) in {__name__}',
                        )

                    completed = await _wait_for_first_completed(
                        application_event_task,
                        watch_event_task,
                        protos_event_task,
                        process_wait_task,
                        induce_chaos_task,
                        health_check_task,
                        chaos_task,
                        rc_file_event_task,
                    )

                    # Cancel tasks regardless of what completed
                    # first as we won't ever wait on them.
                    induce_chaos_task.cancel()
                    if chaos_task:
                        chaos_task.cancel()

                    if rc_file_event_task in completed:
                        return None
                    elif process_wait_task in completed:
                        message = (
                            'Application exited unexpectedly '
                            f'(with exit status {process_wait_task.result()})'
                        )
                        if args.terminate_after_health_check:
                            terminal.fail(message)
                        terminal.warn(
                            '\n'
                            f'{message} ... waiting for modification'
                            '\n'
                        )
                        # NOTE: we'll wait for a file system event
                        # below to signal a modification!
                    elif (
                        (induce_chaos_task in completed) or
                        (args.chaos and chaos_task in completed)
                    ):
                        terminal.warn(
                            '\n'
                            'Chaos Monkey Is Restarting Your Application'
                            '\n' + random.choice(monkeys) + '\n'
                            '... disable via --no-chaos if you must'
                            '\n'
                            '\n'
                        )
                        if induce_chaos_task in completed:
                            delay = await induce_chaos_task
                        continue
                    elif health_check_task in completed:
                        # The health check passed, and we were asked to exit
                        # after a health check (otherwise the health check task
                        # continues to run more health checks).
                        return 0

                    # Wait for a watch task to fire.
                    # TODO: If:
                    # 1. user changes a file they asked us to watch,
                    #    causing this wait to return
                    # 2. proto files then additionally change before we
                    #    re-enter the proto watch above
                    # ... then we would miss that event.
                    # See https://github.com/reboot-dev/mono/issues/2940
                    completed = await _wait_for_first_completed(
                        application_event_task,
                        watch_event_task,
                        protos_event_task,
                        rc_file_event_task,
                    )
                    if rc_file_event_task in completed:
                        return None
                    if protos_event_task in completed:
                        needs_proto_compile = True

                    terminal.info(
                        '\n'
                        'Application modified; restarting ... '
                        '\n'
                    )


async def dev_expunge(
    args: argparse.Namespace,
    parser: ArgumentParser,
) -> None:
    """
    Delete the sidecar state directory for the application with the given name.
    """

    def ask_for_confirmation(question: str) -> bool:
        yes_answers = ['y', 'yes']
        terminal.info(question)
        answer = input()
        return answer.lower() in yes_answers

    dot_rbt_dev = dot_rbt_dev_directory(args, parser)
    if args.yes is False:
        terminal.info(f"About to expunge '{args.name}' from '{dot_rbt_dev}'")
        if not ask_for_confirmation("Do you want to continue? [y/n]:"):
            terminal.fail("Expunge cancelled")

    application_directory = dot_rbt_dev / args.name
    try:
        shutil.rmtree(application_directory)
        terminal.info(f"Application '{args.name}' has been expunged")
    except FileNotFoundError:
        terminal.fail(
            f"Could not find application with name '{args.name}' (looked in "
            f"'{application_directory}'); did not expunge"
        )
