"""Layers Services file definitions"""

# TODO: Eventually only use the Enum
G5K = "g5k"
IOT_LAB = "iotlab"
CHAMELEON_CLOUD = "chameleoncloud"
CHAMELEON_EDGE = "chameleonedge"

ENVIRONMENT = "environment"
LAYERS = "layers"
PROVENANCE_SVC = "provenance"
MONITORING_SVC = "monitoring"
MONITORING_IOT_SVC = "monitoring_iotlab"

VALID_LAYERS_SERVICES_KEYS = [
    ENVIRONMENT,
    LAYERS,
    PROVENANCE_SVC,
    MONITORING_SVC,
    MONITORING_IOT_SVC,
]

DEFAULT_SERVICE_NAME = "Default"
KEY_NAME = "ssh_key"
FIREWALL_RULES = "firewall_rules"
PORTS = "ports"
CLUSTER = "cluster"
SERVERS = "servers"
JOB_TYPE_DEPLOY = "deploy"
JOB_NAME = "job_name"
JOB_TYPE = "job_type"
QUEUE = "queue"
WALLTIME = "walltime"
RESERVATION = "reservation"
ENV_NAME = "env_name"
QUANTITY = "quantity"
MONITOR = "monitor"
SERVICES = "services"
NAME = "name"
IMAGE = "image"
ARCHI = "archi"
ROLES = "roles"
ENV = "env"
KEY_NAME = "key_name"
REPEAT = "repeat"
RC_FILE = "rc_file"
IPV = "ipv"
IPV_VERSIONS = [4, 6]
CONTAINERS = "containers"
PROFILE = "profile"

# Config / Service / Infra
ID = "_id"
SERVICE_ID = "service_id"
LAYER_NAME = "layer_name"
LAYER_ID = "layer_id"
SERVICE_PLUGIN_NAME = "service_plugin_name"

# ChameleonCloud
CC_EXPOSED_PORTS = "exposed_ports"
CC_START = "start"
CC_START_TIMEOUT = "start_timeout"
CC_DEVICE_PROFILES = "device_profiles"

# Provenance
PROVENANCE_SVC_PARALLELISM = "parallelism"
PROVENANCE_SERVICE_ROLE = "provenance_service"
PROVENANCE_SVC_PORT = "22000"
PROVENANCE_SVC_PROVIDER = "provider"
PROVENANCE_SVC_DATAFLOW_SPEC = "dataflow_spec"
DFA_CONTAINER_NAME = "dfanalyzer"

# Monitoring
MONITORING_SVC_PROVIDER = "provider"
MONITORING_SVC_PORT = "3000"
MONITORING_SVC_TYPE = "type"
MONITORING_SVC_TIG = "tig"
MONITORING_SVC_TPG = "tpg"
MONITORING_SVC_DSTAT = "dstat"
MONITORING_SVC_NETWORK = "network"
MONITORING_SVC_NETWORK_PRIVATE = "private"
MONITORING_SVC_NETWORK_SHARED = "shared"
MONITORING_SVC_AGENT_CONF = "agent_conf"
MONITORING_REMOTE_WORKING_DIR = "monitoring_remote_working_dir"
MONITORING_NETWORK_ROLE = "my_monitoring_network"
MONITORING_NETWORK_ROLE_IP = MONITORING_NETWORK_ROLE + "_ip"
MONITORING_SERVICE_ROLE = "monitoring_service"

DSTAT_OPTIONS = "options"
DSTAT_DEFAULT_OPTS = "-m -c -n"


# IotLab monitoring
MONITORING_IOT_ARCHI = ["a8", "m3", "custom"]
MONITORING_IOT_PROFILES = "profiles"
MONITORING_IOT_CURRENT = "current"
MONITORING_IOT_POWER = "power"
MONITORING_IOT_VOLTAGE = "voltage"
MONITORING_IOT_PERIOD = "period"
MONITORING_IOT_PERIOD_VALS = [140, 204, 332, 588, 1100, 2116, 4156, 8244]
MONITORING_IOT_AVERAGE = "average"
MONITORING_IOT_AVERAGE_VALS = [1, 4, 16, 64, 128, 256, 512, 1024]

ROLES_MONITORING = "monitoring"
ROLES_PROVENANCE = "provenance"
