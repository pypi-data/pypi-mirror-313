from __future__ import annotations

import log.log
import reboot.aio.auth.token_verifiers
from google.protobuf.message import Message
from rbt.v1alpha1.errors_pb2 import Ok, PermissionDenied, Unauthenticated
from reboot.aio.auth import Auth, authorizers, token_verifiers
from reboot.aio.contexts import ReaderContext
from reboot.run_environments import on_cloud
from typing import Optional

logger = log.log.get_logger(__name__)

_APP_INTERNAL_API_KEY_VERIFIED = 'APP_INTERNAL_API_KEY_VERIFIED'


class AppInternalAuth:
    """A Servicer mixin which only allows other Servicers in the same app."""

    def __init__(self):
        super().__init__()

        # TODO: We are currently checking for kubernetes as proxy for checking
        # for cloud.
        if on_cloud():
            logger.warning(
                "App-internal traffic identification is not yet supported on the cloud!",
            )

    def token_verifier(
        self,
    ) -> Optional[reboot.aio.auth.token_verifiers.TokenVerifier]:
        return TokenVerifier()

    def authorizer(self) -> Optional[authorizers.Authorizer]:
        return Authorizer()


class TokenVerifier(token_verifiers.TokenVerifier):

    async def verify_token(
        self,
        context: ReaderContext,
        token: str,
    ) -> Optional[Auth]:
        if token == context._app_internal_api_key_secret:
            return Auth(
                # No user ID, the secret _is_ the API key.
                user_id=None,
                properties={_APP_INTERNAL_API_KEY_VERIFIED: True},
            )
        else:
            return None


class Authorizer(authorizers.Authorizer[Message, Message]):

    async def authorize(
        self,
        *,
        method_name: str,
        context: ReaderContext,
        state: Optional[Message] = None,
        request: Optional[Message] = None,
    ) -> authorizers.Authorizer.Decision:
        if context.auth is None:
            return Unauthenticated()
        if _APP_INTERNAL_API_KEY_VERIFIED in context.auth.properties:
            return Ok()

        return PermissionDenied()
