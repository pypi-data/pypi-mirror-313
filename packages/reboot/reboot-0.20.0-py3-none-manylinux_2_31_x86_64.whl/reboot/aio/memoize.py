import log.log
import pickle
import sys
import uuid
from datetime import datetime
from reboot.aio.auth.app_internal_auth import AppInternalAuth
from reboot.aio.contexts import (
    EffectValidation,
    ReaderContext,
    WorkflowContext,
    WriterContext,
    _log_message_for_effect_validation,
    retry_reactively_until,
)
from reboot.aio.types import assert_type
from reboot.memoize.v1.memoize_rbt import (
    FailRequest,
    FailResponse,
    Memoize,
    ResetRequest,
    ResetResponse,
    StartRequest,
    StartResponse,
    StatusRequest,
    StatusResponse,
    StoreRequest,
    StoreResponse,
)
from reboot.settings import DOCS_BASE_URL
from typing import Awaitable, Callable, Optional, TypeVar, overload

T = TypeVar('T')

logger = log.log.get_logger(__name__)

# Dictionary 'idempotency alias': 'timestamp' to keep track of when we
# last explained effect validation for a memoized block given the
# specified idempotency alias. By using the helper
# `_log_message_for_effect_validation` we'll log a message on the
# first invocation of 'idempotency alias' as well as after some time
# so that the user is not inundated with log messages.
_has_ever_explained_effect_validation: dict[str, datetime] = {}


class AtMostOnceFailedBeforeCompleting(Exception):
    """Raised for any repeat attempts at performing an "at most once"
    operation that was started but didn't complete.
    """
    pass


async def memoize(
    idempotency_alias: str,
    context: WorkflowContext,
    callable: Callable[[], Awaitable[T]],
    *,
    type_t: type[T],
    at_most_once: bool,
    retryable_exceptions: Optional[list[type[Exception]]] = None,
    # TODO: idempotency_lifetime: Optional[...] = None,
) -> T:
    """Memoizes the result of running `callable`, only attempting to do so
    once if `at_most_once=True`.

    NOTE: this is the Python wrapper for `reboot.memoize.v1` and as
    such uses `pickle` to serialize the result of calling `callable`
    which therefore must be pickle-able.
    """
    assert_type(context, [WorkflowContext])

    assert context.task_id is not None

    # First make sure we've constructed the state by calling the
    # writer `Reset`, but idempotently so we only do it the first
    # time.
    #
    # TODO(benh): colocate with `context.state_ref` for performance.
    memoize = Memoize.lookup(
        str(uuid.uuid5(context.task_id, idempotency_alias)),
    )

    await memoize.idempotently(
        f'{idempotency_alias} initial reset',
    ).Reset(context)

    status = await memoize.Status(context)

    if at_most_once and status.started and not status.stored:
        raise AtMostOnceFailedBeforeCompleting(
            status.failure if status.failed else (
                '... it looks like an external failure occurred (e.g., '
                'the machine failed, your container was rescheduled, etc) '
                'while your code was executing'
            )
        )
    elif status.stored:
        t = pickle.loads(status.data)
        if type(t) is not type_t:
            raise TypeError(
                f"Stored result of type '{type(t).__name__}' from 'callable' "
                f"is not of expected type '{type_t.__name__}'; have you changed "
                "the 'type' that you expect after having stored a result?"
            )
        return t

    # Only need to call `Start` for "at most once" semantics.
    if at_most_once:
        assert not status.started
        await memoize.unidempotently().Start(context)

    try:

        async def callable_validating_effects():
            """Helper to re-run `callable` if this is not "at most once" and we
            are validating effects.
            """
            t = await callable()

            if (
                at_most_once or
                context._effect_validation == EffectValidation.DISABLED
            ):
                return t

            # Effect validation is enabled, and this callable needs to
            # retry: compose a message, log it, and then raise.
            message = (
                f"Re-running block with idempotency alias '{idempotency_alias}' "
                f"to validate effects. See {DOCS_BASE_URL}/develop/side_effects "
                "for more information."
            )

            _log_message_for_effect_validation(
                effect_validation=context._effect_validation,
                identifier=idempotency_alias,
                timestamps=_has_ever_explained_effect_validation,
                logger=logger,
                message=message,
            )

            # Reset the context since it is an `IdempotencyManager` so
            # we can re-execute `callable` as though it is being
            # retried from scratch.
            context.reset()

            # TODO: check if `t` is different (we don't do this for
            # other effect validation so we're also not doing it now).

            return await callable()

        t = await callable_validating_effects()

    except BaseException as exception:
        if at_most_once and retryable_exceptions is not None and any(
            isinstance(exception, retryable_exception)
            for retryable_exception in retryable_exceptions
        ):
            # Only need to reset for "at most once" semantics.
            #
            # NOTE: it's possible that we won't be able to call
            # `Reset` before we fail and even though this "at most
            # once" could be retried it won't be. But the same is true
            # if we failed before we even called `callable` above!
            # While we're eliminating the possibility of trying to
            # call `callable` more than once, we are not ensuring it
            # is called at least once.
            await memoize.unidempotently().Reset(context)
        elif at_most_once:
            # Attempt to store information about the failure for
            # easier debugging in the future.
            failure = f'{type(exception).__name__}'

            message = f'{exception}'

            if len(message) > 0:
                failure += f': {message}'

            await memoize.idempotently(f'{idempotency_alias} fail').Fail(
                context,
                failure=failure,
            )

        raise
    else:
        # TODO(benh): retry just this part in the event of retryable
        # errors so that we aren't the cause of raising
        # `AtMostOnceFailedBeforeCompleting`.
        await memoize.idempotently(f'{idempotency_alias} store').Store(
            context,
            data=pickle.dumps(t),
        )

        # NOTE: we validate _after_ we have stored in the event that
        # the user just passed an incorrect `validate` they can simply
        # fix that and everything else will just work. Worst case
        # scenario, they can change the idempotency alias/key so that
        # the callable is re-executed.
        #
        # This is technically not required as we'll check the type
        # when we return an already memoized result, but this helps
        # find bugs sooner.
        if type(t) is not type_t:
            raise TypeError(
                f"Result of type '{type(t).__name__}' from 'callable' is "
                f"not of expected type '{type_t.__name__}'; "
                "did you specify an incorrect 'type'?"
            )

        return t


@overload
async def at_most_once(
    idempotency_alias: str,
    context: WorkflowContext,
    callable: Callable[[], Awaitable[None]],
    *,
    type: type = type(None),
    retryable_exceptions: Optional[list[type[Exception]]] = None,
    # TODO: idempotency_lifetime: Optional[...] = None,
) -> None:
    ...


@overload
async def at_most_once(
    idempotency_alias: str,
    context: WorkflowContext,
    callable: Callable[[], Awaitable[T]],
    *,
    type: type[T],
    retryable_exceptions: Optional[list[type[Exception]]] = None,
    # TODO: idempotency_lifetime: Optional[...] = None,
) -> T:
    ...


async def at_most_once(
    idempotency_alias: str,
    context: WorkflowContext,
    callable: Callable[[], Awaitable[T]],
    *,
    type: type = type(None),
    retryable_exceptions: Optional[list[type[Exception]]] = None,
    # TODO: idempotency_lifetime: Optional[...] = None,
) -> T:
    """Attempts to run and memoize the result of calling `callable` but
    only once.

    NOTE: this is the Python wrapper for `reboot.memoize.v1` and as
    such uses `pickle` to serialize the result of calling `callable`
    which therefore must be pickle-able.
    """
    try:
        return await memoize(
            idempotency_alias,
            context,
            callable,
            type_t=type,
            at_most_once=True,
            retryable_exceptions=retryable_exceptions,
        )
    except:
        print(
            "Caught exception within `at_most_once` which will now forever "
            "more raise `AtMostOnceFailedBeforeCompleting`; "
            "to propagate failures return a value instead!",
            file=sys.stderr,
        )
        raise


@overload
async def at_least_once(
    idempotency_alias: str,
    context: WorkflowContext,
    callable: Callable[[], Awaitable[None]],
    *,
    type: type = type(None),
    # TODO: idempotency_lifetime: Optional[...] = None,
) -> None:
    ...


@overload
async def at_least_once(
    idempotency_alias: str,
    context: WorkflowContext,
    callable: Callable[[], Awaitable[T]],
    *,
    type: type[T],
    # TODO: idempotency_lifetime: Optional[...] = None,
) -> T:
    ...


async def at_least_once(
    idempotency_alias: str,
    context: WorkflowContext,
    callable: Callable[[], Awaitable[T]],
    *,
    type: type = type(None),
    # TODO: idempotency_lifetime: Optional[...] = None,
) -> T:
    """Attempts to run and memoize the result of calling `callable` while
    supporting retrying as many times as necessary until `callable`
    succeeds.

    NOTE: this is the Python wrapper for `reboot.memoize.v1` and as
    such uses `pickle` to serialize the result of calling `callable`
    which therefore must be pickle-able.
    """
    return await memoize(
        idempotency_alias,
        context,
        callable,
        type_t=type,
        at_most_once=False,
    )


@overload
async def until(
    idempotency_alias: str,
    context: WorkflowContext,
    callable: Callable[[], Awaitable[bool]],
    *,
    type: type = bool,
    # TODO: idempotency_lifetime: Optional[...] = None,
) -> bool:
    ...


@overload
async def until(
    idempotency_alias: str,
    context: WorkflowContext,
    callable: Callable[[], Awaitable[T]],
    *,
    type: type[T],
    # TODO: idempotency_lifetime: Optional[...] = None,
) -> T:
    ...


async def until(
    idempotency_alias: str,
    context: WorkflowContext,
    callable: Callable[[], Awaitable[T]],
    *,
    type: type = bool,
    # TODO: idempotency_lifetime: Optional[...] = None,
) -> T:
    """Attempts to reactively run `callable` "until" it returns a non
    `False` result we memoize.
    """

    async def converge():
        return await retry_reactively_until(context, callable)

    return await at_least_once(
        idempotency_alias,
        context,
        converge,
        type=type,
    )


class MemoizeServicer(AppInternalAuth, Memoize.Servicer):

    async def Reset(
        self,
        context: WriterContext,
        state: Memoize.State,
        request: ResetRequest,
    ) -> ResetResponse:
        assert not state.stored
        state.CopyFrom(Memoize.State())
        return ResetResponse()

    async def Status(
        self,
        context: ReaderContext,
        state: Memoize.State,
        request: StatusRequest,
    ) -> StatusResponse:
        return StatusResponse(
            started=state.started,
            stored=state.stored,
            failed=state.failed,
            data=state.data,
            failure=state.failure,
        )

    async def Start(
        self,
        context: WriterContext,
        state: Memoize.State,
        request: StartRequest,
    ) -> StartResponse:
        assert not state.started
        state.started = True
        return StartResponse()

    async def Store(
        self,
        context: WriterContext,
        state: Memoize.State,
        request: StoreRequest,
    ) -> StoreResponse:
        assert not state.stored
        state.stored = True
        state.data = request.data
        return StoreResponse()

    async def Fail(
        self,
        context: WriterContext,
        state: Memoize.State,
        request: FailRequest,
    ) -> FailResponse:
        assert not state.stored
        state.failed = True
        state.failure = request.failure
        return FailResponse()


def servicers():
    return [MemoizeServicer]
