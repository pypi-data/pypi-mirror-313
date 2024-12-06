import aiofiles.os
import argparse
import asyncio
import glob
import os
import reboot.aio.tracing
import sys
from collections import defaultdict
from importlib import resources
from pathlib import Path
from reboot.cli import terminal
from reboot.cli.directories import (
    add_working_directory_options,
    chdir,
    compute_working_directory,
    dot_rbt_directory,
    get_absolute_path_from_path,
    is_on_path,
    use_working_directory,
)
from reboot.cli.rc import ArgumentParser
from reboot.cli.subprocesses import Subprocesses
from reboot.settings import (
    DOCS_BASE_URL,
    ENVVAR_RBT_FROM_NODEJS,
    ENVVAR_REBOOT_NODEJS_EXTENSIONLESS,
    ENVVAR_REBOOT_REACT_EXTENSIONLESS,
)
from typing import Optional, Tuple

REBOOT_SPECIFIC_PLUGINS = ['python', 'react', 'nodejs']
REBOOT_EXPERIMENTAL_PLUGINS = ['nodejs']

# Dictionary from out path to list of sufficient plugins (it's a list
# since in some cases more than one plugin may be sufficient).
PLUGINS_SUFFICIENT_FOR_EXPLICIT_OUT_FLAGS = {
    '--python_out': ['python'],
    '--grpc_python_out': ['python'],
    '--reboot_python_out': ['python'],
    '--mypy_out': ['python'],
    '--es_out': ['react', 'nodejs'],
    '--reboot_react_out': ['react'],
    '--reboot_nodejs_out': ['nodejs'],
}

# Specify all possible flags for supported languages, in a priority order.
OUTPUT_FLAGS_BY_LANGUAGE = {
    "python":
        [
            "--reboot_python_out",
            "--python_out",
            "--grpc_python_out",
            "--mypy_out",
        ],
    "react": [
        "--reboot_react_out",
        "--es_out",
    ],
    "nodejs": [
        "--reboot_nodejs_out",
        "--es_out",
    ],
}

PROTOC_PLUGIN_BY_LANGUAGE = {
    "python": "protoc-gen-reboot_python",
    "react": "protoc-gen-reboot_react",
    "nodejs": "protoc-gen-reboot_nodejs",
}

BOILERPLATE_SUPPORTED_LANGUAGES = ['python', 'nodejs']

BOILERPLATE_PLUGIN_BY_LANGUAGE = {
    "python": "protoc-gen-reboot_python_boilerplate",
    "nodejs": "protoc-gen-reboot_nodejs_boilerplate"
}

OUTPUT_BOILERPLATE_FLAG_BY_LANGUAGE = {
    "python": "--reboot_python_boilerplate_out",
    "nodejs": "--reboot_nodejs_boilerplate_out"
}


def register_protoc(parser: ArgumentParser):
    add_working_directory_options(parser.subcommand('protoc'))

    parser.subcommand('protoc').add_argument(
        '--python',
        type=str,
        default=None,
        help="output directory in which `protoc` will generate Python files",
    )

    parser.subcommand('protoc').add_argument(
        '--react',
        type=str,
        default=None,
        help="output directory in which `protoc` will generate React files",
    )

    parser.subcommand('protoc').add_argument(
        '--react-extensionless',
        type=bool,
        default=True,
        help="don't generate .js extensions for imports in React files",
    )

    parser.subcommand('protoc').add_argument(
        '--nodejs',
        type=str,
        default=None,
        # Don't output the '--nodejs' flag in the help message, as we don't
        # officially support it yet.
        help=argparse.SUPPRESS,
    )

    parser.subcommand('protoc').add_argument(
        '--nodejs-extensionless',
        type=bool,
        default=True,
        help="don't generate .js extensions for imports in Node.js files",
    )

    parser.subcommand('protoc').add_argument(
        '--boilerplate',
        type=str,
        help="generate a fill-in-the-blanks boilerplate at the specified path.",
    )

    parser.subcommand('protoc').add_argument(
        'proto_directories',
        type=str,
        help="proto directory(s) which will (1) be included as import paths "
        "and (2) be recursively searched for '.proto' files to compile",
        repeatable=True,
        required=True,
    )


IsFile = bool


async def _check_or_install_npm_packages(
    subprocesses: Subprocesses,
    package_names: list[Tuple[str, IsFile]],
):
    # Check and see if we've already installed a package and if not install it,
    # unless we are not installing the package from a file, in that case we
    # assume that we are installing a 'dev' version and we install it.
    #
    # We redirect stdout/stderr to a pipe and only print it out if any of our
    # commands fail.
    for package_name, is_file in package_names:
        async with subprocesses.shell(
            f'npm list {package_name}',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        ) as process:
            stdout, _ = await process.communicate()

            if process.returncode != 0 or is_file:
                async with subprocesses.shell(
                    f'npm install {package_name}',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT,
                ) as process:
                    stdout, _ = await process.communicate()

                    if process.returncode != 0:
                        terminal.fail(
                            "\n"
                            f"Failed to install '{package_name}':\n"
                            f"{stdout.decode() if stdout is not None else '<no output>'}"
                            "\n"
                            "Please report this bug to the maintainers."
                        )


async def ensure_protoc_gen_es(
    args,
    parser: ArgumentParser,
    subprocesses: Subprocesses,
):
    """Helper to ensure we have 'protoc-gen-es' and its dependencies
    installed.

    We install these in the '.rbt' directory, by placing an empty
    'package.json' file and then running 'npm install' as
    necessary. This approach makes it so that we don't have to bundle
    'protoc-gen-es' as part of our pip package.
    """
    if not is_on_path('npm'):
        terminal.fail(
            "We require 'npm' and couldn't find it on your PATH. "
            "Is it installed?"
        )

    if not is_on_path('node'):
        terminal.fail(
            "We require 'node' and couldn't find it on your PATH. "
            "Is it installed?"
        )

    dot_rbt = dot_rbt_directory(args, parser)
    await aiofiles.os.makedirs(dot_rbt, exist_ok=True)

    # TODO: Changing directory like this is not concurrency safe.
    with chdir(dot_rbt):
        if (
            not await aiofiles.os.path.isfile('package.json') or
            await aiofiles.os.path.getsize('package.json') == 0
        ):
            with open('package.json', 'w') as file:
                file.write('{ "type": "module" }')

        await _check_or_install_npm_packages(
            subprocesses,
            [
                # NOTE: these versions should match with what we're
                # using in all of our 'package.json' files!
                ('@bufbuild/protoplugin@1.3.2', False),
                ('@bufbuild/protoc-gen-es@1.3.2', False),
                ('@bufbuild/protobuf@1.3.2', False),
            ]
        )

    env_path = os.environ.get("PATH", "")

    if env_path != "":
        env_path += os.pathsep

    env_path += os.path.join(
        dot_rbt_directory(args, parser),
        'node_modules',
        '.bin',
    )

    os.environ["PATH"] = env_path

    env_node_path = os.environ.get("NODE_PATH", "")

    if env_node_path != "":
        env_node_path += os.pathsep

    env_node_path += os.path.join(
        dot_rbt_directory(args, parser),
        'node_modules',
    )

    os.environ["NODE_PATH"] = env_node_path


LanguageName = str
OutputPath = str
FlagName = str


async def get_output_paths_and_languages(
    args,
) -> dict[LanguageName, OutputPath]:
    """Get the output paths for each language that we are generating code for.
    We'll return a dictionary where the key is the language and the value is
    an output path.
    """

    output_by_language: dict[LanguageName, OutputPath] = {}

    if args.python is not None:
        output_by_language['python'] = args.python
    if args.react is not None:
        output_by_language['react'] = args.react
    if args.nodejs is not None:
        output_by_language['nodejs'] = args.nodejs

    return output_by_language


async def protoc(
    args,
    argv_after_dash_dash: list[str],
    parser: ArgumentParser,
) -> int:
    """Invokes `protoc` with the arguments passed to 'rbt protoc'."""
    # Determine the working directory and move into it.
    with use_working_directory(args, parser):
        # Use `Subprocesses` to manage all of our subprocesses for us.
        subprocesses = Subprocesses()

        return await protoc_direct(
            args, argv_after_dash_dash, parser, subprocesses
        )


@reboot.aio.tracing.function_span()
async def protoc_direct(
    args,
    argv_after_dash_dash: list[str],
    parser: ArgumentParser,
    subprocesses: Subprocesses,
) -> int:
    """Invokes `protoc` with the arguments passed to 'rbt protoc', while asserting that
    the working directory is already correct."""

    if Path(os.getcwd()).resolve() != compute_working_directory(args, parser):
        # TODO: Move to a global flag using #3845.
        terminal.fail(
            "The `--working-directory` for `protoc` must match the "
            "`--working-directory` for the current command."
        )

    # As part of `rbt protoc` we invoke `protoc` a number of times with
    # different plugins, some of them may have specific arguments, but at the
    # same time they all share some common arguments. We'll build up the
    # arguments for each plugin separately and then combine them all together at
    # the end to invoke `protoc`.
    common_args: list[str] = ["grpc_tools.protoc"]

    # This list contains a list of specific arguments for each plugin, for
    # example:
    #
    # [
    #   ['--python_out=python_out'],
    #   ['--es_out=es_out', '--es_opt=target=ts]',
    #   ...
    # ]
    all_plugins_args: list[list[str]] = []

    def add_args_to_plugin(plugin_out_flag: str, args: list[str]):
        # Find the list which contains the 'plugin_out_flag' flag, and add
        # 'args' to it.
        for i, plugin_args in enumerate(all_plugins_args):
            if any(arg.startswith(plugin_out_flag) for arg in plugin_args):
                all_plugins_args[i] += args
                return

    # We want to find all Python `site-packages`/`dist-packages` directories
    # that (may) contain a 'rbt/v1alpha1' directory, which is where we'll find
    # our protos.
    #
    # We can look for Python packages like a 'rbt' folder via the `resources`
    # module; the resulting path is a `MultiplexedPath`, since there may be
    # multiple.
    #
    # HOWEVER, the `resources` module does NOT work well when all subpaths of
    # one `rbt/` folder are ALSO present in another `rbt/` folder - e.g. if we
    # have two `rbt/v1alpha1` folders in two separate locations (in two Bazel
    # repos, say), we will get just one of those `rbt/v1alpha1` folders, and
    # thereby maybe only ever see one of the `rbt/` folders too (if there's
    # nothing unique inside it). So instead of looking for `rbt/` (which only
    # contains `v1alpha1/`, which is not unique) we look for its sibling path
    # `reboot/`, which contains a lot of unique names in every place it is
    # present.
    #
    # The paths we get don't contain a `parent` attribute, since there isn't one
    # answer. Instead we use `iterdir()` to get all of the children of all
    # 'reboot' folders, and then dedupe parents-of-the-parents-of-those-children
    # (via the `set`), which gives us the 'rbt' folders' parents' paths.
    reboot_parent_paths: set[str] = set()
    for resource in resources.files('reboot').iterdir():
        with resources.as_file(resource) as path:
            reboot_parent_paths.add(str(path.parent.parent))

    if len(reboot_parent_paths) == 0:
        raise FileNotFoundError(
            "Failed to find 'rbt' resource path. "
            "Please report this bug to the maintainers."
        )

    # Now add these to '--proto_path', so that users don't need to provide
    # their own Reboot protos.
    for reboot_parent_path in reboot_parent_paths:
        common_args.append(f"--proto_path={reboot_parent_path}")

    # User protos may rely on `google.protobuf.*` protos. We
    # conveniently have those files packaged in our Python
    # package; make them available to users, so that users don't
    # need to provide them.
    common_args.append(
        f"--proto_path={resources.files('grpc_tools').joinpath('_proto')}"
    )

    for flag, languages in PLUGINS_SUFFICIENT_FOR_EXPLICIT_OUT_FLAGS.items():
        if any(arg.startswith(flag) for arg in argv_after_dash_dash):
            suggestions = ' or '.join(
                [
                    f"'--{language}'" for language in languages
                    if language not in REBOOT_EXPERIMENTAL_PLUGINS
                ]
            )
            terminal.fail(
                f"{flag} was specified after '--'. Instead, use {suggestions} "
                "to specify the output directory."
            )

    if (
        args.react is not None and args.nodejs is not None and
        args.react == args.nodejs and
        args.nodejs_extensionless != args.react_extensionless
    ):
        terminal.fail(
            "You are generating code for both Node.js and React in the same "
            f"directory (`--nodejs={args.nodejs}` and `--react={args.react}`) "
            "but you have specified different values for "
            f"`--nodejs-extensionless={args.nodejs_extensionless}` and "
            f"`--react-extensionless={args.react_extensionless}`. If you "
            "need the generated code for Node.js and React to be different you "
            "must use different directories."
        )

    output_path_by_language = await get_output_paths_and_languages(args)

    if len(output_path_by_language) == 0:
        official_supported_plugins = [
            plugin for plugin in REBOOT_SPECIFIC_PLUGINS
            if plugin not in REBOOT_EXPERIMENTAL_PLUGINS
        ]

        terminal.fail(
            f"At least one of '{', '.join(official_supported_plugins)}' must be specified."
        )

    languages_to_generate = list(output_path_by_language.keys())

    protoc_plugin_out_flags: dict[FlagName, OutputPath] = {}

    skip_next: bool = False
    for i, arg in enumerate(argv_after_dash_dash):
        if skip_next is True:
            skip_next = False
            continue
        if '=' in arg:
            arg_name, arg_value = arg.split('=')

            if arg_name.endswith('_out'):
                # This means that a user has specified an output path for a
                # some arbitrary plugin and we will invoke it only once and in
                # parallel with the other plugins.

                protoc_plugin_out_flags[arg_name] = arg_value
            else:
                common_args.append(f'{arg_name}={arg_value}')
        else:
            if len(argv_after_dash_dash) - 1 == i:
                terminal.fail(f'Missing value for {arg}, try {arg}=VALUE')

            if arg.endswith('_out'):
                # This means that a user has specified an output path for a
                # some arbitrary plugin and we will invoke it only once and in
                # parallel with the other plugins.

                protoc_plugin_out_flags[arg] = argv_after_dash_dash[i + 1]
            else:
                common_args.append(f'{arg}={argv_after_dash_dash[i + 1]}')

            skip_next = True

    # If `args.react` and `args.nodejs` point to different directories
    # then we have to call `protoc` twice, each with different
    # `--es_out=` arguments (one for the `args.react` directory and
    # one for the `args.nodejs` directory.
    es_out_language: Optional[str] = None

    for language in languages_to_generate:
        if language in BOILERPLATE_SUPPORTED_LANGUAGES and args.boilerplate is not None:
            if await aiofiles.os.path.isfile(args.boilerplate):
                terminal.fail(
                    f"Expecting a directory for '--boilerplate={args.boilerplate}'"
                )
            if not await aiofiles.os.path.isdir(args.boilerplate):
                await aiofiles.os.makedirs(
                    args.boilerplate,
                )
            if not is_on_path(BOILERPLATE_PLUGIN_BY_LANGUAGE[language]):
                raise FileNotFoundError(
                    f"Failed to find '{BOILERPLATE_PLUGIN_BY_LANGUAGE[language]}'. "
                    "Please report this bug to the maintainers."
                )

            all_plugins_args.append(
                [
                    f"{OUTPUT_BOILERPLATE_FLAG_BY_LANGUAGE[language]}={args.boilerplate}"
                ]
            )

        if not is_on_path(PROTOC_PLUGIN_BY_LANGUAGE[language]):
            raise FileNotFoundError(
                f"Failed to find '{PROTOC_PLUGIN_BY_LANGUAGE[language]}'. "
                "Please report this bug to the maintainers."
            )

        # If the directory doesn't exist create it (we checked in
        # `_check_explicitly_specified_out_paths()` that none of
        # the specified out paths were files).
        #
        # This is a _much_ better experience than the error message
        # that `protoc` gives if the directory does not exist.
        if not await aiofiles.os.path.isdir(output_path_by_language[language]):
            await aiofiles.os.makedirs(
                output_path_by_language[language],
                exist_ok=True,
            )

        # This is safe even when multiple languages share one protoc plugin,
        # because in those cases their output path is guaranteed to be the
        # same.
        for flag_name in OUTPUT_FLAGS_BY_LANGUAGE[language]:
            if flag_name == '--es_out':
                if es_out_language is not None:
                    continue
                es_out_language = language

            protoc_plugin_out_flags[flag_name] = output_path_by_language[
                language]

    for flag_name, out in protoc_plugin_out_flags.items():
        all_plugins_args.append([f"{flag_name}={out}"])

    if args.react is not None or args.nodejs is not None:
        rbt_from_nodejs = os.environ.get(
            ENVVAR_RBT_FROM_NODEJS,
            "false",
        ).lower() == "true"

        if not rbt_from_nodejs:
            await ensure_protoc_gen_es(args, parser, subprocesses)

        # If a Python backend, protoc-gen-es should already be on the PATH.
        # The check below should only happen if a Node dev failed to see a
        # missing peerDependency when installing @reboot-dev/reboot.
        if not is_on_path('protoc-gen-es'):
            raise FileNotFoundError(
                "Failed to find binary for 'protoc-gen-es' on PATH. "
                "This is likely because you need to explicitly add "
                "@bufbuild/protoc-gen-es as a dependency of your project."
            )

        protoc_gen_es_with_deps_path: Optional[str] = (
            get_absolute_path_from_path("protoc-gen-es_with_deps")
        )

        if protoc_gen_es_with_deps_path is None:
            raise FileNotFoundError(
                "Failed to find 'protoc-gen-es_with_deps'. "
                "Please report this bug to the maintainers."
            )

        def add_es_opts(
            protoc_gen_es_with_deps_path: str,
            import_extension: str,
            output_path: Optional[str] = None,
        ):
            common_es_opts = [
                # We always want to generate TypeScript so that end users can
                # decide how to convert that to JavaScript.
                "--es_opt=target=ts",
                f"--plugin=protoc-gen-es={protoc_gen_es_with_deps_path}",
                f'--es_opt=import_extension={import_extension}'
            ]

            if output_path is not None:
                # If 'output_path' is not None, that means that we are
                # scheduling a second invocation of `protoc gen es` with
                # different arguments, so we have to store the whole list
                # specific arguments as a separate list.
                common_es_opts = [
                    f'--es_out={output_path}',
                ] + common_es_opts

                all_plugins_args.append(common_es_opts)
            else:
                add_args_to_plugin('--es_out', common_es_opts)

        extensionless = (
            args.nodejs_extensionless
            if es_out_language == "nodejs" else args.react_extensionless
        )

        add_es_opts(
            protoc_gen_es_with_deps_path,
            "none" if extensionless else ".js",
        )

        # Schedule one more invocation of `protoc gen es` if we're
        # generating code for both Node.js and React in different
        # directories.
        if (
            args.react is not None and args.nodejs is not None and
            args.react != args.nodejs
        ):
            extensionless = (
                args.react_extensionless
                if es_out_language == "nodejs" else args.nodejs_extensionless
            )
            output_path = output_path_by_language['react' if es_out_language ==
                                                  'nodejs' else 'nodejs']

            add_es_opts(
                protoc_gen_es_with_deps_path,
                "none" if extensionless else ".js",
                output_path,
            )

    if args.nodejs_extensionless:
        os.environ[ENVVAR_REBOOT_NODEJS_EXTENSIONLESS] = "true"

    if args.react_extensionless:
        os.environ[ENVVAR_REBOOT_REACT_EXTENSIONLESS] = "true"

    # The `mypy` plugin is by default being a little loud for our liking.
    # This can be suppressed by passing the parameter `quiet` to the plugin.
    # https://github.com/nipunn1313/mypy-protobuf/blob/7f4a558c00faf8fac0cd6d7a6d1332d1643cc08c/mypy_protobuf/main.py#L1082
    # Check if we are going to invoke `mypy` and if so, make sure we are
    # also passing `quiet`.

    quiet_arg = '--mypy_opt=quiet'
    if quiet_arg not in common_args:
        add_args_to_plugin('--mypy_out', [quiet_arg])

    # Grab all of the positional '.proto' arguments.
    proto_directories: list[str] = args.proto_directories or []

    protos_by_directory: defaultdict[str, list[str]] = defaultdict(list)

    for proto_directory in proto_directories:
        if not proto_directory.endswith(os.path.sep):
            proto_directory += os.path.sep
        # Expand any directories to be short-form for 'directory/**/*.proto'.
        if not await aiofiles.os.path.isdir(proto_directory):
            terminal.fail(f"Failed to find directory '{proto_directory}'")
        else:
            # Also add any directories given to us as part of the import path.
            common_args.append(f'--proto_path={proto_directory}')

            found_protos = False
            for file in glob.iglob(
                os.path.join(proto_directory, '**', '*.proto'),
                recursive=True,
            ):
                _, extension = os.path.splitext(file)
                if extension == '.proto':
                    found_protos = True
                    protos_by_directory[proto_directory].append(file)

            if not found_protos:
                terminal.fail(
                    f"'{proto_directory}' did not match any '.proto' files"
                )

    proto_files: list[str] = []

    for protos in protos_by_directory.values():
        for file in protos:
            if os.stat(file).st_size == 0:
                terminal.error(
                    f"'{file}' is empty. "
                    f"See {DOCS_BASE_URL}/develop/schema for "
                    "more information on filling out your proto file."
                )
                # Return an error status here to not break the 'rbt dev' loop.
                return 1

        proto_files.extend(protos)

    if not terminal.is_verbose():
        terminal.info(
            'Running `protoc ...` (use --verbose to see full command)'
            '\n'
        )

    @reboot.aio.tracing.function_span()
    async def _invoke_protoc(
        common_args,
        all_plugins_args,
        proto_files,
        subprocesses,
    ) -> int:
        command_list = [
            # Ignore the deprecation warning from `grpc_tools.protoc`.
            'PYTHONWARNINGS=ignore::DeprecationWarning:',
            f'{sys.executable}',
            '-m',
        ]

        protoc_tasks = []

        # Run protoc plugins in parallel.
        for args in all_plugins_args:
            command_list_for_plugin = command_list + common_args + args + proto_files

            if terminal.is_verbose():
                terminal.verbose('protoc')
                # Skip the args from 'command_list' and change
                # 'grpc_tools.protoc' to 'protoc'.
                for arg in command_list_for_plugin[4:]:
                    terminal.verbose(f'  {arg}')

            command = ' '.join(command_list_for_plugin)

            async def __invoke_protoc(command):
                async with subprocesses.shell(
                    command=command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT,
                ) as process:
                    stdout, _ = await process.communicate()

                    # Print if we failed.
                    if process.returncode != 0:
                        # Print the output in the white color.
                        print(
                            f'{stdout.decode() if stdout is not None else "<no output>"}',
                            file=sys.stderr,
                        )
                        terminal.error(
                            f"`protoc` failed with exit status {process.returncode}"
                        )

                    return process.returncode

            protoc_tasks.append(asyncio.create_task(__invoke_protoc(command)))

        result = await asyncio.gather(*protoc_tasks)

        for returncode in result:
            if returncode != 0:
                return returncode

        return 0

    returncode = await _invoke_protoc(
        common_args,
        all_plugins_args,
        proto_files,
        subprocesses,
    )

    return returncode
