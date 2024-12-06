#!/usr/bin/env python3
import os
import reboot.aio.tracing
from dataclasses import dataclass
from reboot.cli import terminal
from reboot.protoc_gen_reboot_generic import (
    BaseClient,
    BaseFile,
    BaseMethod,
    BaseMethodOptions,
    BaseService,
    BaseState,
    PluginSpecificData,
    ProtoType,
    UserProtoError,
)
from reboot.protoc_gen_reboot_typescript import TypescriptRebootProtocPlugin
from reboot.settings import ENVVAR_REBOOT_REACT_EXTENSIONLESS
from typing import Sequence

ReactType = str


@dataclass
class ReactMethodOptions(BaseMethodOptions):
    errors: dict[ProtoType, ReactType]


@dataclass
class ReactMethod(BaseMethod):
    options: ReactMethodOptions
    input_type: ReactType
    output_type: ReactType


@dataclass
class ReactService(BaseService):
    methods: Sequence[ReactMethod]


@dataclass
class ReactState(BaseState):
    services: Sequence[ReactService]


@dataclass
class ReactClient(BaseClient):
    services: Sequence[ReactService]


@dataclass
class ReactFile(BaseFile):
    # Dictionary where the key is the relative path to the
    # file and the value is the unique name of the file.
    imports: dict[str, str]
    # The name of the ES module, which contains the generated protobuf
    # messages ("*_pb.js").
    pb_name: str
    # Set of messages that are used in the file and should be imported from
    # '@bufbuild/protobuf'.
    google_protobuf_used_messages: set[str]
    # Whether or not to emit .js extensions.
    react_extensionless: bool


class ReactRebootProtocPlugin(TypescriptRebootProtocPlugin):

    @staticmethod
    def plugin_specific_data() -> PluginSpecificData:
        return PluginSpecificData(
            template_filename="reboot_react.ts.j2",
            output_filename_suffix="_rbt_react.ts",
            supported_features=[
                "reader",
                "writer",
                "transaction",
                "error",
                "streaming",
                "workflow",
            ],
        )

    def _react_services(self, file: BaseFile,
                        services: Sequence[BaseService]) -> list[ReactService]:
        state_names = [state.proto.name for state in file.states]
        return [
            ReactService(
                proto=service.proto,
                options=service.options,
                methods=[
                    ReactMethod(
                        proto=method.proto,
                        options=ReactMethodOptions(
                            proto=method.options.proto,
                            errors=self._analyze_errors(
                                method.proto._descriptor,
                                state_names=state_names,
                            ),
                        ),
                        input_type=self._typescript_type_from_proto_type(
                            message=method.proto._descriptor.input_type,
                            file=file.proto._descriptor,
                            state_names=state_names,
                            messages_and_enums=file.proto.messages_and_enums,
                        ),
                        output_type=self._typescript_type_from_proto_type(
                            message=method.proto._descriptor.output_type,
                            file=file.proto._descriptor,
                            state_names=state_names,
                            messages_and_enums=file.proto.messages_and_enums,
                        ),
                    ) for method in service.methods
                ],
            ) for service in services
        ]

    def _react_states(
        self,
        file: BaseFile,
        states: Sequence[BaseState],
    ) -> list[ReactState]:
        return [
            ReactState(
                proto=state.proto,
                services=self._react_services(file, state.services),
            ) for state in states
        ]

    def _react_clients(
        self,
        file: BaseFile,
        clients: Sequence[BaseClient],
    ) -> list[ReactClient]:
        return [
            ReactClient(
                proto=client.proto,
                services=self._react_services(file, client.services),
                state=client.state,
            ) for client in clients
        ]

    def add_language_dependent_data(self, file: BaseFile) -> BaseFile:
        react_file: BaseFile = ReactFile(
            proto=file.proto,
            legacy_grpc_services=file.legacy_grpc_services,
            states=self._react_states(file, file.states),
            clients=self._react_clients(file, file.clients),
            reboot_version=file.reboot_version,
            imports=self._analyze_imports(file.proto._descriptor),
            pb_name=self._pb_file_name(file.proto._descriptor),
            google_protobuf_used_messages=self._google_protobuf_messages(
                file.proto._descriptor
            ),
            react_extensionless=os.environ.get(
                ENVVAR_REBOOT_REACT_EXTENSIONLESS, "false"
            ).lower() == "true",
        )

        return react_file


# This is a separate function (rather than just being in `__main__`) so that we
# can refer to it as a `script` in our `pyproject.rbt.toml` file.
@reboot.aio.tracing.main_span("protoc_gen_reboot_react")
def main():
    try:
        ReactRebootProtocPlugin.execute()
    except UserProtoError as error:
        terminal.fail(str(error))


if __name__ == '__main__':
    main()
