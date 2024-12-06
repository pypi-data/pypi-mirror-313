import rbt.v1alpha1.errors_pb2
from abc import ABC, abstractmethod
from google.protobuf.message import Message
from reboot.aio.contexts import ReaderContext
from typing import Generic, Optional, TypeAlias, TypeVar

StateType = TypeVar('StateType', bound=Message)
RequestTypes = TypeVar('RequestTypes', bound=Message)


class Authorizer(ABC, Generic[StateType, RequestTypes]):
    """Abstract base class for general Servicer Authorizers.

    A Servicer's authorizer is used to determine whether a given call to a
    Servicer's methods should be allowed or not.
    """

    # A value of `False` will be translated into a `PermissionDenied` error.
    Decision: TypeAlias = (
        rbt.v1alpha1.errors_pb2.Unauthenticated |
        rbt.v1alpha1.errors_pb2.PermissionDenied | rbt.v1alpha1.errors_pb2.Ok
    )

    @abstractmethod
    async def authorize(
        self,
        *,
        method_name: str,
        context: ReaderContext,
        state: Optional[StateType] = None,
        request: Optional[RequestTypes] = None,
    ) -> Decision:
        """Determine whether a call to a the method @method_name should be
        allowed.

        :param method_name: The name of the method being called.
        :param context: A reader context to enable calling other services.
        :param state: The state where and when available.
        :param request: The request object to the servicer method being called.

        Returns:
            `rbt.v1alpha1.errors_pb2.Ok()` if the call should be allowed,
            `rbt.v1alpha1.errors_pb2.Unauthenticated()` or
            `rbt.v1alpha1.errors_pb2.PermissionDenied()` otherwise.
        """
        raise NotImplementedError


class AllowAllIfAuthenticated(Authorizer[Message, Message]):
    """An authorizer that allows all requests if the caller is authenticated."""

    async def authorize(
        self,
        *,
        method_name: str,
        context: ReaderContext,
        state: Optional[Message] = None,
        request: Optional[Message] = None,
    ) -> Authorizer.Decision:
        if context.auth is None:
            return rbt.v1alpha1.errors_pb2.Unauthenticated()

        return rbt.v1alpha1.errors_pb2.Ok()
