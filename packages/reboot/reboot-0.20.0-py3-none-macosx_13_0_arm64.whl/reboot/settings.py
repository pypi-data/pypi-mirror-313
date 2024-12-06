# The settings below must match their equivalents, if applicable, in:
# * reboot/settings.h
# * <possibly other languages by the time you read this>

# gRPC max message size to transmit large state data.
MAX_SIDECAR_GRPC_MESSAGE_LENGTH_BYTES = 100 * 1024 * 1024

# gRPC max response size (our limit; gRPC doesn't specify a limit normally).
# See: https://github.com/reboot-dev/mono/issues/3944
MAX_GRPC_RESPONSE_SIZE_BYTES = 4 * 1024 * 1024

DOCS_BASE_URL = "https://docs.reboot.dev"

# The path to the directory where Reboot state is stored.
REBOOT_STATE_DIRECTORY = '/var/run/reboot/state'

# The name of the admin secret that is used to authenticate admin requests,
# e.g., for inspect.
ADMIN_SECRET_NAME = 'rbt-admin-secret'

# The names of environment variables that are present both in `rbt dev run` and
# in Kubernetes.
#
# TODO: The API key should likely be provided by a file in production, to allow
# for rotation.
ENVVAR_RBT_CLOUD_API_KEY = 'RBT_CLOUD_API_KEY'
ENVVAR_RBT_CLOUD_URL = 'RBT_CLOUD_URL'

# The names of environment variables that are only present when running in `rbt
# dev run`.
ENVVAR_RBT_DEV = 'RBT_DEV'
ENVVAR_RBT_SERVE = 'RBT_SERVE'
ENVVAR_RBT_NAME = 'RBT_NAME'
ENVVAR_RBT_EFFECT_VALIDATION = 'RBT_EFFECT_VALIDATION'
ENVVAR_RBT_SECRETS_DIRECTORY = 'RBT_SECRETS_DIRECTORY'
ENVVAR_RBT_STATE_DIRECTORY = 'RBT_STATE_DIRECTORY'
ENVVAR_RBT_NODEJS = 'RBT_NODEJS'
ENVVAR_RBT_PARTITIONS = 'RBT_PARTITIONS'

# Environment variable indicating that `rbt` is being invoked from
# Node.js.
ENVVAR_RBT_FROM_NODEJS = 'RBT_FROM_NODEJS'

# The names of environment variables that are only present when configuring a
# local Envoy.
ENVVAR_REBOOT_LOCAL_ENVOY = 'REBOOT_LOCAL_ENVOY'
ENVVAR_REBOOT_LOCAL_ENVOY_PORT = 'REBOOT_LOCAL_ENVOY_PORT'

# The name of an environment variable that indicates that we are
# running from within `node`. Not to be confused with
# `ENVVAR_RBT_NODEJS` which implies the `--nodejs` flag was set when
# using `rbt`.
ENVVAR_REBOOT_NODEJS = 'REBOOT_NODEJS'

# Name of an environment variable that indicates whether or not to use
# .js extensions in generated React files.
ENVVAR_REBOOT_REACT_EXTENSIONLESS = 'REBOOT_REACT_EXTENSIONLESS'

# Name of an environment variable that indicates whether or not to use
# .js extensions in generated Node.js files.
ENVVAR_REBOOT_NODEJS_EXTENSIONLESS = 'REBOOT_NODEJS_EXTENSIONLESS'

# The name of an environment variable that's only present when running on
# Kubernetes.
ENVVAR_KUBERNETES_SERVICE_HOST = 'KUBERNETES_SERVICE_HOST'

# When we set up servers we often need to listen on every addressable
# interface on the local machine. This is especially important in some
# circumstances where networks may be rather convoluted, e.g., when we
# have local Docker containers.
EVERY_LOCAL_NETWORK_ADDRESS = '0.0.0.0'
ONLY_LOCALHOST_NETWORK_ADDRESS = '127.0.0.1'

# Ports that Reboot is, by default, reachable on for gRPC and HTTP traffic
# from clients running outside the Reboot cluster. These are the ports that
# users will use in their configuration/code when they choose how to connect to
# a Reboot cluster.
#
# Note that these are defaults; some environments may override these settings.
# Furthermore, many environments may only have one of these ports exposed.
#
# The insecure port serves unencrypted traffic. The secure port serves traffic
# that uses TLS.
DEFAULT_INSECURE_PORT = 9990
DEFAULT_SECURE_PORT = 9991

# Normally, application IDs are not very human-readable - they're hashes derived
# from a human-readable name. However, we choose a hardcoded human-readable ID
# here, for two reasons:
# 1. We want a human-readable endpoint for the Reboot Cloud; e.g.:
#      cloud.some-cluster.rbt.cloud
# 2. If we need to debug a Kubernetes cluster, we're likely to need to interact
#    with the cloud app. Giving it a human-readable ID makes that easier.
CLOUD_APPLICATION_ID = "cloud"
CLOUD_USER_ID = "cloud"
CLOUD_SPACE_NAME = "cloud"

# The length bounds of user inputs that will be encoded into headers. The
# values are chosen to be larger than any value we've observed in reasonable use
# cases, but small enough that the gRPC maximum metadata size (8 KiB, see [1])
# will not be exceeded.
#   [1]: https://grpc.io/docs/guides/metadata/#be-aware)
MIN_ACTOR_ID_LENGTH = 1
MAX_ACTOR_ID_LENGTH = 128
MAX_IDEMPOTENCY_KEY_LENGTH = 128
MAX_BEARER_TOKEN_LENGTH = 4096

# The suffix given to sidecar state directories.
SIDECAR_SUFFIX = "-sidecar"

# Local envoy specific environment variables that impact how it gets
# configured.
ENVOY_VERSION = '1.30.2'
ENVOY_PROXY_IMAGE = f'envoyproxy/envoy:v{ENVOY_VERSION}'

ENVVAR_LOCAL_ENVOY_USE_TLS = 'REBOOT_LOCAL_ENVOY_USE_TLS'
ENVVAR_LOCAL_ENVOY_TLS_CERTIFICATE_PATH = 'REBOOT_LOCAL_ENVOY_TLS_CERTIFICATE_PATH'
ENVVAR_LOCAL_ENVOY_TLS_KEY_PATH = 'REBOOT_LOCAL_ENVOY_TLS_KEY_PATH'

# The name of the environment variable, which should be set by 'rbt serve' or
# 'rbt dev run', that contains the mode in which the Envoy should run
# (executable/docker).
ENVVAR_LOCAL_ENVOY_MODE = 'REBOOT_LOCAL_ENVOY_MODE'
ENVVAR_LOCAL_ENVOY_DEBUG = 'REBOOT_LOCAL_ENVOY_DEBUG'

# Whether or not signal manipulation is available.
ENVVAR_SIGNALS_AVAILABLE = 'REBOOT_SIGNALS_AVAILABLE'

# Args for launching a nodejs based consensus.
ENVVAR_NODEJS_CONSENSUS = 'REBOOT_NODEJS_CONSENSUS'
ENVVAR_NODEJS_CONSENSUS_BASE64_ARGS = 'REBOOT_NODEJS_CONSENSUS_BASE64_ARGS'

# An environment variable that's only set when running in the Resemble Cloud.
ENVVAR_REBOOT_CLOUD_VERSION = 'REBOOT_CLOUD_VERSION'
