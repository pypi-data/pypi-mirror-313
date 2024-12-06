from __future__ import annotations

import log.log
from google.protobuf.empty_pb2 import Empty
from rbt.std.collections.v1.sorted_map_rbt import (
    Entry,
    GetRequest,
    GetResponse,
    InsertRequest,
    InsertResponse,
    InvalidRangeError,
    RangeRequest,
    RangeResponse,
    RemoveRequest,
    RemoveResponse,
    SortedMap,
)
from reboot.aio.auth.app_internal_auth import AppInternalAuth
from reboot.aio.contexts import ReaderContext, WriterContext

logger = log.log.get_logger(__name__)


class SortedMapServicer(AppInternalAuth, SortedMap.Servicer):

    async def Insert(
        self,
        # TODO: Once https://github.com/reboot-dev/mono/issues/2918 is fixed
        # this method should become a Transaction, which will be a backwards
        # compatible change.
        context: WriterContext,
        state: SortedMap.State,
        request: InsertRequest,
    ) -> InsertResponse:
        context._colocated_upserts = list(request.entries.items())

        return InsertResponse()

    async def Remove(
        self,
        # TODO: Once https://github.com/reboot-dev/mono/issues/2918 is fixed
        # this method should become a Transaction, which will be a backwards
        # compatible change.
        context: WriterContext,
        state: SortedMap.State,
        request: RemoveRequest,
    ) -> RemoveResponse:
        context._colocated_upserts = list((k, None) for k in request.keys)

        return RemoveResponse()

    async def Range(
        self,
        context: ReaderContext,
        state: Empty,
        request: RangeRequest,
    ) -> RangeResponse:
        if request.limit == 0:
            raise SortedMap.RangeAborted(
                InvalidRangeError(
                    message="Range requires a non-zero `limit` value."
                )
            )
        if request.HasField('start_key') and request.HasField('end_key'):
            if request.start_key >= request.end_key:
                raise SortedMap.RangeAborted(
                    InvalidRangeError(
                        message=(
                            "Range requires `end_key` to be larger than "
                            f"`start_key`; got start_key='{request.start_key}' "
                            f"and end_key='{request.end_key}'"
                        )
                    )
                )

        assert self._middleware is not None

        page = await self._middleware._state_manager.colocated_range(
            context,
            start=(
                request.start_key if request.HasField('start_key') else None
            ),
            end=(request.end_key if request.HasField('end_key') else None),
            limit=request.limit,
        )

        return RangeResponse(entries=[Entry(key=k, value=v) for k, v in page])

    async def Get(
        self,
        context: ReaderContext,
        state: Empty,
        request: GetRequest,
    ) -> GetResponse:
        # Implemented essentially the same as `Range`, but with the `end_key`
        # set to the smallest possible value after `start_key`.
        #
        # TODO: optimize this by using a point-lookup all the way down to the
        #       storage sidecar?
        assert self._middleware is not None

        page = await self._middleware._state_manager.colocated_range(
            context,
            start=request.key,
            # Add a one-byte to the end of the key to create the smallest
            # possible key after `start_key`. The one-byte is the correct answer
            # here because the zero-byte is forbidden in keys (see
            # `StateRef.from_id`). Since `end` is exclusive, this ensures that
            # we will only ever get exactly `start_key` in our result set.
            end=request.key + b'\x01'.decode('ascii'),
            limit=1,
        )

        assert len(page) <= 1

        if len(page) == 0:
            return GetResponse()  # Leaving 'value' unset means "not found".

        _, value = page[0]
        return GetResponse(value=value)


def servicers():
    return [SortedMapServicer]
