import asyncio
import grpc
from asyncio import Queue
from google.protobuf import json_format, struct_pb2
from rbt.v1alpha1 import sidecar_pb2
from rbt.v1alpha1.admin import export_import_pb2_grpc
from rbt.v1alpha1.admin.export_import_pb2 import (
    ExportImportItem,
    ExportRequest,
    ImportResponse,
    ListConsensusesRequest,
    ListConsensusesResponse,
)
from reboot.admin.export_import_converters import ExportImportItemConverters
from reboot.aio.auth.admin_auth import (
    AdminAuthMixin,
    auth_metadata_from_metadata,
)
from reboot.aio.internals.channel_manager import _ChannelManager
from reboot.aio.internals.middleware import Middleware
from reboot.aio.placement import PlacementClient
from reboot.aio.state_managers import StateManager
from reboot.aio.types import (
    ApplicationId,
    ConsensusId,
    StateRef,
    StateTypeName,
)
from reboot.consensus.sidecar import (
    SORTED_MAP_ENTRY_TYPE_NAME,
    SORTED_MAP_TYPE_NAME,
)
from typing import AsyncIterator, Optional


class ExportImportServicer(
    AdminAuthMixin,
    export_import_pb2_grpc.ExportImportServicer,
):

    def __init__(
        self,
        application_id: ApplicationId,
        consensus_id: ConsensusId,
        state_manager: StateManager,
        placement_client: PlacementClient,
        channel_manager: _ChannelManager,
        serializers: ExportImportItemConverters,
        middleware_by_state_type_name: dict[StateTypeName, Middleware],
    ):
        super().__init__()

        self._application_id = application_id
        self._consensus_id = consensus_id
        self._state_manager = state_manager
        self._placement_client = placement_client
        self._channel_manager = channel_manager
        self._serializers = serializers
        self._middleware_by_state_type_name = middleware_by_state_type_name

    def add_to_server(self, server: grpc.aio.Server) -> None:
        export_import_pb2_grpc.add_ExportImportServicer_to_server(self, server)

    async def ListConsensuses(
        self,
        request: ListConsensusesRequest,
        grpc_context: grpc.aio.ServicerContext,
    ) -> ListConsensusesResponse:
        await self.ensure_admin_auth_or_fail(grpc_context)

        return ListConsensusesResponse(
            consensus_ids=self._placement_client.known_consensuses(
                self._application_id
            ),
        )

    async def Export(
        self,
        request: ExportRequest,
        grpc_context: grpc.aio.ServicerContext,
    ) -> AsyncIterator[ExportImportItem]:
        await self.ensure_admin_auth_or_fail(grpc_context)

        if request.consensus_id != self._consensus_id:
            await grpc_context.abort(
                grpc.StatusCode.NOT_FOUND,
                "This process does not host that consensus.",
            )
            raise RuntimeError('This code is unreachable')

        # If SORTED_MAP_TYPE_NAME is installed, additionally export
        # SORTED_MAP_ENTRY_TYPE_NAME (see #2983). We use a list here rather
        # than a set so that we export in a determinstic order.
        state_types = list(self._serializers.state_types)
        if SORTED_MAP_TYPE_NAME in state_types:
            state_types.append(SORTED_MAP_ENTRY_TYPE_NAME)

        for state_type_name in state_types:
            async for item in self._state_manager.export_items(
                state_type_name
            ):
                active_field_name = item.WhichOneof("item")
                if active_field_name == "actor":
                    if state_type_name == SORTED_MAP_ENTRY_TYPE_NAME:
                        yield ExportImportItem(
                            state_type=state_type_name,
                            state_ref=item.actor.state_ref,
                            sorted_map_entry=item.actor.state,
                        )
                    else:
                        state = self._serializers.state_to_struct(
                            item.actor.state,
                            state_type_name,
                        )
                        yield ExportImportItem(
                            state_type=state_type_name,
                            state_ref=item.actor.state_ref,
                            state=state,
                        )
                elif active_field_name == "task":
                    yield ExportImportItem(
                        state_type=state_type_name,
                        state_ref=item.task.task_id.state_ref,
                        task=json_format.ParseDict(
                            json_format.MessageToDict(
                                item.task,
                                preserving_proto_field_name=True,
                            ),
                            struct_pb2.Struct(),
                        ),
                    )
                else:
                    assert active_field_name == "idempotent_mutation"
                    yield ExportImportItem(
                        state_type=state_type_name,
                        state_ref=item.idempotent_mutation.state_ref,
                        idempotent_mutation=json_format.ParseDict(
                            json_format.MessageToDict(
                                item.idempotent_mutation,
                                preserving_proto_field_name=True,
                            ),
                            struct_pb2.Struct(),
                        ),
                    )

    async def Import(
        self,
        requests: AsyncIterator[ExportImportItem],
        grpc_context: grpc.aio.ServicerContext,
    ) -> ImportResponse:
        await self.ensure_admin_auth_or_fail(grpc_context)

        tasks = []
        queues_by_consensus: dict[ConsensusId,
                                  Queue[Optional[ExportImportItem]]] = {}

        async def _remote_iterator(
            requests: Queue[Optional[ExportImportItem]],
        ) -> AsyncIterator[ExportImportItem]:
            while True:
                request = await requests.get()
                if request is None:
                    return
                yield request

        async def _task(
            consensus_id: ConsensusId,
            states: Queue[Optional[ExportImportItem]],
        ) -> None:
            if consensus_id != self._consensus_id:
                channel = self._channel_manager.get_channel_to(
                    self._placement_client.address_for_consensus(consensus_id)
                )
                export_import = export_import_pb2_grpc.ExportImportStub(
                    channel
                )
                await export_import.Import(
                    _remote_iterator(states),
                    metadata=auth_metadata_from_metadata(grpc_context),
                )
                return

            while True:
                item = await states.get()
                if item is None:
                    return

                state_type_name = StateTypeName(item.state_type)
                state_ref = StateRef(item.state_ref)

                active_field_name = item.WhichOneof("item")
                if active_field_name == "state":
                    await self._state_manager.import_actor(
                        state_type_name,
                        state_ref,
                        self._serializers.state_from_struct(
                            item.state,
                            state_type_name,
                        ),
                    )
                elif active_field_name == "sorted_map_entry":
                    await self._state_manager.import_sorted_map_entry(
                        state_type_name,
                        state_ref,
                        item.sorted_map_entry,
                        self._serializers,
                    )
                elif active_field_name == "task":
                    middleware = self._middleware_by_state_type_name.get(
                        state_type_name
                    )
                    if middleware is None:
                        raise ValueError(
                            "Unrecognized state type: {item.state_type!r}"
                        )
                    await self._state_manager.import_task(
                        state_type_name,
                        state_ref,
                        json_format.ParseDict(
                            json_format.MessageToDict(
                                item.task,
                                preserving_proto_field_name=True,
                            ), sidecar_pb2.Task()
                        ),
                        middleware,
                    )
                else:
                    assert active_field_name == "idempotent_mutation"
                    await self._state_manager.import_idempotent_mutation(
                        state_type_name,
                        state_ref,
                        json_format.ParseDict(
                            json_format.MessageToDict(
                                item.idempotent_mutation,
                                preserving_proto_field_name=True,
                            ), sidecar_pb2.IdempotentMutation()
                        ),
                    )

        # Route each request to a per-consensus Queue, with a Task that will drain it
        # to the appropriate destination.
        async for request in requests:
            consensus_id = self._placement_client.consensus_for_actor(
                self._application_id,
                StateRef(request.state_ref),
            )
            queue = queues_by_consensus.get(consensus_id)
            if queue is None:
                queue = Queue(maxsize=128)
                queues_by_consensus[consensus_id] = queue
                tasks.append(asyncio.create_task(_task(consensus_id, queue)))

            await queue.put(request)

        # And a sentinel value to each queue, and gather the tasks to wait for
        # them to flush to their destinations.
        await asyncio.gather(
            *(queue.put(None) for queue in queues_by_consensus.values()),
        )
        await asyncio.gather(*tasks)

        return ImportResponse()
