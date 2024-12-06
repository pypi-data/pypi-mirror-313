import grpc.aio
import uuid
from google.protobuf.message import Message
from kubernetes_utils.kubernetes_client import EnhancedKubernetesClient
from kubernetes_utils.retry import Retry, retry_unless_pods_have_failed
from reboot.aio.idempotency import IdempotencyManager
from reboot.aio.internals.channel_manager import (
    LegacyGrpcChannel,
    _ChannelManager,
)
from reboot.aio.internals.contextvars import Servicing, _servicing
from reboot.aio.resolvers import StaticResolver
from typing import Optional, TypeVar
from urllib.parse import urlparse

ResponseT = TypeVar('ResponseT', bound='Message')


class ExternalContext(IdempotencyManager):
    """Abstraction for making RPCs to one or more reboot states from
    _outside_ of Reboot.
    """

    def __init__(
        self,
        *,
        name: str,
        gateway: None = None,  # Deprecated. Use `url` instead.
        secure_channel: None = None, # Deprecated. Use `url` instead.
        url: Optional[str] = None,
        channel_manager: Optional[_ChannelManager] = None,
        bearer_token: Optional[str] = None,
        idempotency_seed: Optional[uuid.UUID] = None,
        idempotency_required: bool = False,
        idempotency_required_reason: Optional[str] = None,
    ):
        if gateway is not None or secure_channel is not None:
            raise ValueError(
                "'gateway' and 'secure_channel' have been removed; use 'url' "
                "instead"
            )

        super().__init__(
            seed=idempotency_seed,
            required=idempotency_required,
            required_reason=idempotency_required_reason,
        )

        if _servicing.get() is Servicing.YES:
            raise RuntimeError(
                'Can not construct an ExternalContext from within a servicer'
            )

        if url is not None:
            if channel_manager is not None:
                raise ValueError(
                    "ExternalContext should be constructed via _one of_ "
                    "'url' or 'channel_manager', not both"
                )

            scheme, address, path, params, query, fragment = urlparse(url)

            if scheme == '' and address == '':
                # Rewrite the URL so that we can extract address vs path.
                url = f'//{url}'
                scheme, address, path, params, query, fragment = urlparse(url)

            if path != '':
                raise ValueError(
                    f"ExternalContext is not expecting a URL with a path, got '{url}'"
                )

            if params != '':
                raise ValueError(
                    f"ExternalContext is not expecting a URL with path parameters, , got '{url}'"
                )

            if query != '':
                raise ValueError(
                    f"ExternalContext is not expecting a URL with a query component, , got '{url}'"
                )

            if fragment != '':
                raise ValueError(
                    f"ExternalContext is not expecting a URL with a fragment identifier, got '{url}'"
                )

            if scheme == '':
                raise ValueError(
                    "ExternalContext expects a URL including an explicit "
                    "'http' or 'https'"
                )

            if scheme != '' and scheme not in ['http', 'https']:
                raise ValueError(
                    "ExternalContext expects a URL with either an "
                    f"'http' or https' scheme but found '{scheme}'"
                )

            channel_manager = _ChannelManager(
                resolver=StaticResolver(address if address != '' else path),
                secure=scheme == 'https',
            )
        elif channel_manager is None:
            raise ValueError(
                "ExternalContext should be constructed by passing either "
                "a 'url' or a 'channel_manager'"
            )

        self._name = name
        self._channel_manager = channel_manager
        self._bearer_token = bearer_token

    @property
    def name(self) -> str:
        return self._name

    @property
    def channel_manager(self) -> _ChannelManager:
        """Return channel manager.
        """
        return self._channel_manager

    @property
    def bearer_token(self) -> Optional[str]:
        return self._bearer_token

    def legacy_grpc_channel(self) -> grpc.aio.Channel:
        """Get a gRPC channel that can connect to any Reboot-hosted legacy
        gRPC service. Simply use this channel to create a Stub and call it, no
        address required."""
        return LegacyGrpcChannel(self._channel_manager)


async def retry_context_unless_pods_have_failed(
    *,
    name: str,
    k8s_client: EnhancedKubernetesClient,
    pods: list[tuple[str, list[str]]],
    exceptions: list[type[BaseException]],
    url: Optional[str] = None,
    treat_not_found_as_failed: bool = False,
    max_backoff_seconds: int = 3,
):
    """Wrapper around `retry_unless_pods_have_failed(...)`.

    :param name: name of the external context.

    :param url: optional URL of the Reboot application.

    See other parameters described in `retry_unless_pods_have_failed(...)`.

    Example:

    async for retry in retry_context_unless_pods_have_failed(...):
        with retry() as context:
            foo = Foo('some-key')
            response = await foo.SomeMethod(context)
    """
    context = ExternalContext(name=name, url=url)

    async for retry in retry_unless_pods_have_failed(
        retry=Retry(context),
        k8s_client=k8s_client,
        pods=pods,
        exceptions=exceptions,
        treat_not_found_as_failed=treat_not_found_as_failed,
        max_backoff_seconds=max_backoff_seconds,
    ):
        yield retry
