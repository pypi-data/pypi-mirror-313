import multiprocessing
import os
import reboot.aio.tracing
import threading
import unittest
import uuid
from log.log import get_logger
from pathlib import Path
from reboot.aio.auth.token_verifiers import TokenVerifier
from reboot.aio.contexts import EffectValidation
from reboot.aio.external import ExternalContext
from reboot.aio.internals.channel_manager import _ChannelManager
from reboot.aio.once import Once
from reboot.aio.placement import PlanOnlyPlacementClient
from reboot.aio.resolvers import DirectResolver
from reboot.aio.servicers import Serviceable, Servicer
from reboot.aio.tracing import function_span
from reboot.aio.types import ApplicationId, ConsensusId, ServiceName, StateRef
from reboot.controller.application_config import ApplicationConfig
from reboot.controller.application_config_trackers import (
    LocalApplicationConfigTracker,
)
from reboot.controller.config_extractor import LocalConfigExtractor
from reboot.controller.consensus_managers import LocalConsensusManager
from reboot.controller.consensuses import Consensus
from reboot.controller.placement_planner import PlacementPlanner
from reboot.run_environments import on_cloud
from reboot.settings import ENVVAR_LOCAL_ENVOY_MODE, ENVVAR_LOCAL_ENVOY_USE_TLS
from typing import Any, Optional
from unittest import mock

logger = get_logger(__name__)

# Picked so that we don't get a huge amount of load on the system, but are
# more likely to discover any multi-consensus-related bugs in unit tests.
#
# Note that this number does NOT influence the number of partitions in a Reboot
# Cloud deployment, since it gets its `ApplicationConfig` from elsewhere. It may
# still follow `reboot.controller.plan_makers.DEFAULT_NUM_PARTITIONS`.
DEFAULT_NUM_PARTITIONS = 4


def _initialize_multiprocessing_start_method():
    # We don't want any threads to be running when we try and spawn
    # the forkserver via `multiprocessing.set_start_method()`, but we
    # make an exception (for now) when we're getting called through
    # from nodejs as those threads *must* be created in order to call
    # into us in the first place.
    #
    # See 'reboot/nodejs/python.py'.
    if threading.active_count() > 1 and os.environ.get(
        'REBOOT_NODEJS_EVENT_LOOP_THREAD',
        'false',
    ).lower() != 'true':
        raise RuntimeError(
            'Reboot must be initialized before creating any threads'
        )

    multiprocessing_start_method = multiprocessing.get_start_method(
        allow_none=True
    )

    if multiprocessing_start_method is None:
        # We want to use 'forkserver', which should be set before any
        # threads are created, so that users _can_ use threads in
        # their tests and we will be able to reliably fork without
        # worrying about any gotchas due to forking a multi-threaded
        # process.
        multiprocessing.set_start_method('forkserver')
    elif multiprocessing_start_method != 'forkserver':
        raise RuntimeError(
            f"Reboot requires the 'forkserver' start method but you "
            f"appear to have configured '{multiprocessing_start_method}'"
        )


# We're using a global here because we only want to initialize the
# multiprocessing start method once per process.
_initialize_multiprocessing_start_method_once = Once(
    _initialize_multiprocessing_start_method
)


def assert_called_twice_with(
    testcase: unittest.IsolatedAsyncioTestCase,
    mock_obj: mock.Mock,
    *args: Any,
    **kwargs: Any,
) -> None:
    """Asserts that the given mock received exactly two calls, and that they had
    the given arguments.

    This is a useful alternative to `Mock.assert_called_once_with` in the presence
    of effect validation, which will frequently trigger two identical calls to a mock.
    """
    call = mock.call(*args, **kwargs)
    mock_obj.assert_has_calls([call, call])
    testcase.assertEquals(mock_obj.call_count, 2)


class Reboot:

    def __init__(
        self,
        *,
        application_name: Optional[str] = None,
        state_directory: Optional[Path] = None,
    ):
        """
        state_directory: directory below which applications will store state.
        """
        global _initialize_multiprocessing_start_method_once
        global _initialize_tracing_once

        _initialize_multiprocessing_start_method_once()

        # Multiprocessing must have started before tracing starts, because tracing
        # spawns threads.
        reboot.aio.tracing.start(process_name=application_name or "Reboot")

        self._running_service_names: set[str] = set()
        self._consensus_manager = LocalConsensusManager(state_directory)
        self._config_tracker = LocalApplicationConfigTracker()
        self._config_extractor = LocalConfigExtractor()

        self._placement_planner = PlacementPlanner(
            self._config_tracker,
            self._consensus_manager,
            # Let the PlacementPlanner choose its own port locally, in
            # case we are running multiple PlacementPlanners on the
            # same host (for example, running multiple unit tests in
            # parallel).
            '127.0.0.1:0'
        )

        self._consensus_manager.register_placement_planner_address(
            self._placement_planner.address()
        )

        self._placement_client = PlanOnlyPlacementClient(
            self._placement_planner.address()
        )
        self._resolver = DirectResolver(self._placement_client)
        self._channel_manager = _ChannelManager(
            self._resolver,
            # Not using a secure channel, since this will all be localhost
            # traffic that does not flow through the gateway, which is the
            # only place we do `localhost.direct` SSL termination.
            secure=False,
        )

    async def start(self):
        await self._placement_planner.start()
        await self._placement_client.start()
        await self._resolver.start()

    def create_external_context(
        self,
        *,
        name: str,
        bearer_token: Optional[str] = None,
        idempotency_seed: Optional[uuid.UUID] = None,
        idempotency_required: bool = False,
        idempotency_required_reason: Optional[str] = None,
        use_internal_api_key_from: Optional[ApplicationId] = None,
    ) -> ExternalContext:
        """ Create an `ExternalContext` for use in tests.

        use_internal_api_key_from: When set, the context is being used to
          represent a client internal to the application: essentially, to mock
          traffic from another servicer in the same application. A
          per-application secret will be set as the bearer_token (which must not
          also be set).
        """
        if use_internal_api_key_from is not None:
            if bearer_token is not None:
                raise ValueError(
                    "At most one of `use_internal_api_key_from` and `bearer_token` may be set."
                )
            bearer_token = self._consensus_manager.app_internal_api_key_secret(
                use_internal_api_key_from
            )
            if bearer_token is None:
                raise ValueError(
                    f"Unknown application: {use_internal_api_key_from}"
                )
        return ExternalContext(
            name=name,
            channel_manager=self._channel_manager,
            bearer_token=bearer_token,
            idempotency_seed=idempotency_seed,
            idempotency_required=idempotency_required,
            idempotency_required_reason=idempotency_required_reason,
        )

    @function_span()
    async def up(
        self,
        *,
        servicers: Optional[list[type[Servicer]]] = None,
        # A legacy gRPC servicer type can't be more specific than `type`,
        # because legacy gRPC servicers (as generated by the gRPC `protoc`
        # plugin) do not share any common base class other than `object`.
        legacy_grpc_servicers: Optional[list[type]] = None,
        token_verifier: Optional[TokenVerifier] = None,
        config: Optional[ApplicationConfig] = None,
        in_process: bool = False,
        local_envoy: bool = False,
        local_envoy_port: int = 0,
        name: Optional[str] = None,
        effect_validation: Optional[EffectValidation] = None,
        partitions: Optional[int] = None,
    ) -> ApplicationConfig:
        """Bring up a collection of servicers, or an already brought up
        instance identifiable via its ApplicationConfig.

        in_process: If False, bring up Reboot in a separate process - to
        prevent user-facing log spam from gRPC. gRPC has an issue
        [#25364](https://github.com/grpc/grpc/issues/25364), open since Feb
        2021, that logs errant BlockingIOErrors if gRPC is in a multi-process
        Python context. If True, servicers are brought up in the current
        process and users will have to know to just ignore BlockingIOErrors.

        local_envoy: If True, bring up a LocalEnvoy proxy for our Reboot
        services.

        local_envoy_port: port on which to connect to Envoy,
        defaults to 0 (picked dynamically by the OS).

        name: name to use to override the default (randomly generated)
        deployment name.

        effect_validation: sets EffectValidation for these servicers. By default,
        effect validation is:
          1. Enabled in unit tests, but controllable by this argument.
          2. Enabled in `rbt dev run`, but controllable via the
             `--effect-validation` flag.
          3. Disabled in production.

        partitions: the number of logical partitions (also known as "shards")
          of state machines to create. Must be stable for one application over
          time.
        """
        # There should be no code path where this is run on kubernetes.
        assert not on_cloud()

        if local_envoy:
            # 'Reboot' is part of 'Application', which users will call to run
            # the backend, so we don't want to override the environment variable
            # if it's already set by 'rbt dev run' or 'rbt serve'.
            if os.environ.get(ENVVAR_LOCAL_ENVOY_MODE) is None:
                # We don't expect developers to have Envoy installed
                # on their own machines, so when running unit tests we
                # pull it as a Docker container.
                os.environ[ENVVAR_LOCAL_ENVOY_MODE] = 'docker'
            if os.environ.get(ENVVAR_LOCAL_ENVOY_USE_TLS) is None:
                # We ask for TLS without specifying a specific certificate,
                # which means Envoy will use the one for `localhost.direct`.
                os.environ[ENVVAR_LOCAL_ENVOY_USE_TLS] = 'True'

        if servicers is None and legacy_grpc_servicers is None and config is None:
            raise ValueError(
                "One of 'servicers', 'legacy_grpc_servicers', or 'config' must "
                "be passed"
            )

        if servicers is not None and len(servicers) == 0:
            raise ValueError("'servicers' can't be an empty list")

        if config is not None:
            if servicers is not None or legacy_grpc_servicers is not None:
                raise ValueError(
                    "Only pass one of ('servicers' and/or 'legacy_grpc_servicers') "
                    "or 'config'"
                )
            elif name is not None:
                raise ValueError(
                    "Passing 'name' is not valid when passing 'config'"
                )
            elif partitions is not None:
                raise ValueError(
                    "Passing 'partitions' is not valid when passing 'config'"
                )

            # Is there already a consensus running with the name associated with
            # this config? Updating a running config is not allowed.
            running_configs = await self._config_tracker.get_application_configs(
            )
            if config.application_id() in running_configs:
                raise ValueError(
                    f"Config '{config.application_id()}' is already running. "
                    "Updating a running config in dev mode is not allowed"
                )

            # This is a new config. We just need to check that it doesn't
            # conflict with any servicers already running.
            # NOTE: For now we do not support multiple applications using the same
            # servicers when not running on Kubernetes.
            for service_name in config.spec.service_names:
                if service_name in self._running_service_names:
                    raise ValueError(
                        f"A servicer for '{service_name}' "
                        "has already been brought up"
                    )

        serviceables: list[Serviceable] = []
        for servicer in servicers or []:
            serviceables.append(Serviceable.from_servicer_type(servicer))
        for legacy_grpc_servicer in legacy_grpc_servicers or []:
            serviceables.append(
                Serviceable.from_servicer_type(legacy_grpc_servicer)
            )

        # To prevent typos mixing up `servicers` and `serviceables`, delete
        # `servicers` (so that mypy can catch if we accidentally use it).
        del servicers

        if len(serviceables) > 0:
            # NOTE: For now we do not support multiple applications using the
            # same servicers when not running on Kubernetes.
            for serviceable in serviceables:
                for service_name in serviceable.service_names():
                    if service_name in self._running_service_names:
                        raise ValueError(
                            f"A servicer for '{service_name}' "
                            "has already been brought up"
                        )

            self._consensus_manager.register_serviceables(
                serviceables=serviceables,
                token_verifier=token_verifier,
                in_process=in_process,
                local_envoy=local_envoy,
                local_envoy_port=local_envoy_port,
                effect_validation=effect_validation,
            )

            partitions = partitions or DEFAULT_NUM_PARTITIONS
            config = self._config_extractor.config_from_serviceables(
                serviceables,
                # NOTE: Consensuses are exposed to users as partitions.
                consensuses=partitions,
            )

            if name is not None:
                config.metadata.name = name

        assert config is not None

        # This addition will trigger a new plan being made: then, wait for it
        # to have been observed.
        await self._config_tracker.add_config(config)
        await self._wait_for_local_plan_sync()

        self._running_service_names.update(config.spec.service_names)
        return config

    def https_localhost_direct_url(self, path: str = ''):
        return f"https://{self.localhost_direct_endpoint()}{path}"

    def localhost_direct_endpoint(self):
        """Returns the Envoy proxy endpoint."""
        return f'dev.localhost.direct:{self.envoy_port()}'

    def envoy_port(self):
        """Returns the Envoy proxy port."""
        envoy = self._consensus_manager.local_envoy

        if envoy is None:
            raise ValueError(
                "No local Envoy was launched; did you forget to pass "
                "'local_envoy=True'?"
            )

        return envoy.port

    async def _wait_for_local_plan_sync(self) -> None:
        """Waits for our placement client to have seen the most recent plan.

        NOTE: This is not equivalent to having waited for _all_ clients to have
        seen the most recent version, but should be sufficient for most tests.
        """
        plan_version = self._placement_planner.current_version
        assert plan_version is not None
        await self._placement_client.wait_for_version(plan_version)

    async def unique_consensuses(
        self,
        state_ref_1: StateRef,
        state_ref_2: StateRef,
    ) -> tuple[ConsensusId, ConsensusId]:
        """Given two StateRefs, look up their unique owning consensuses.

        Fails if both StateRefs are owned by the same consensus.
        """
        application_configs = await self._config_tracker.get_application_configs(
        )
        if len(application_configs) != 1:
            # TODO: See https://github.com/reboot-dev/mono/issues/3356.
            raise ValueError(
                "Only supported when a single application is running."
            )
        application_id = next(iter(application_configs.keys()))
        consensus_id_1 = self._placement_client.consensus_for_actor(
            application_id,
            state_ref_1,
        )
        consensus_id_2 = self._placement_client.consensus_for_actor(
            application_id,
            state_ref_2,
        )
        assert consensus_id_1 != consensus_id_2, (
            f"{state_ref_1=} and {state_ref_2=} are hosted by the same consensus: "
            f"{consensus_id_1}"
        )
        return consensus_id_1, consensus_id_2

    async def consensus_stop(self, consensus_id: ConsensusId) -> Consensus:
        return await self._consensus_manager.consensus_stop(consensus_id)

    async def consensus_start(self, consensus: Consensus) -> None:
        # Restart the consensus.
        await self._consensus_manager.consensus_start(consensus)
        # TODO: We need to poke the ConfigTracker to tell the
        # PlacementPlanner to make a new plan after a consensus has changed
        # addresses. See https://github.com/reboot-dev/mono/issues/3356
        # about removing some of this complexity for local runs.
        await self._config_tracker.refresh()
        await self._wait_for_local_plan_sync()

    async def stop(self) -> None:
        """Bring down all servicers and shut down the Reboot instance such
        that no more servicers can be brought up. """
        try:
            await self.down()
        finally:
            try:
                await self._resolver.stop()
            finally:
                await self._placement_planner.stop()

    async def down(self, config: Optional[ApplicationConfig] = None) -> None:
        """Bring down either a single config or everything that has been
        brought up.
        """
        if config is None:
            # Delete all configs so that the PlacementPlanner will bring down
            # all consensuses.
            await self._config_tracker.delete_all_configs()
            await self._wait_for_local_plan_sync()
            self._running_service_names = set()
        else:
            # Get services the resolver currently knows about.
            services: list[ServiceName] = list(
                self._resolver.application_id_by_service_name().keys()
            )

            for service_name in config.spec.service_names:
                # Remove all the services we expect to be brought down.
                services.remove(service_name)

                # Proactively remove each service name so that while we wait for
                # the config to be deleted and the resolver to get the updated
                # plan any concurrent calls into this instance will raise.
                self._running_service_names.remove(service_name)

            await self._config_tracker.delete_config(config)
            await self._wait_for_local_plan_sync()
