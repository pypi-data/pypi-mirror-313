"""
Constants module
Defined for all managers in config
Default paramters in the default module
"""

from enum import Enum
from pathlib import Path

from . import layers_services

PATH_ROOT_E2CLAB = Path(__file__).parent.parent.resolve()
PATH_SERVICES_PLUGINS = PATH_ROOT_E2CLAB / "services" / "plugins"


class ConfFiles:
    LAYERS_SERVICES = "layers_services.yaml"
    NETWORK = "network.yaml"
    WORKFLOW = "workflow.yaml"
    WORKFLOW_ENV = "workflow_env.yaml"


CONF_FILES_LIST = [
    ConfFiles.LAYERS_SERVICES,
    ConfFiles.NETWORK,
    ConfFiles.WORKFLOW,
    ConfFiles.WORKFLOW_ENV,
]

"""
    Environments yaml keys
"""


class Environment(Enum):
    G5K: str = "g5k"
    IOT_LAB: str = "iotlab"
    CHAMELEON_CLOUD: str = "chameleoncloud"
    CHAMELEON_EDGE: str = "chameleonedge"


SUPPORTED_ENVIRONMENTS = [e.value for e in Environment]

"""
    CLI constants
"""

ENV_SCENARIO_DIR = "E2C_SCENARIO_DIR"
ENV_ARTIFACTS_DIR = "E2C_ARTIFACTS_DIR"

ENV_AUTO_PREFIX = "E2C"


class Command(Enum):
    DEPLOY: str = "deploy"
    LYR_SVC: str = "layers-services"
    NETWORK: str = "network"
    WORKFLOW: str = "workflow"
    FINALIZE: str = "finalize"


COMMAND_RUN_LIST = [e.value for e in Command]

"""
    Workflow tasks
"""


class WorkflowTasks(Enum):
    PREPARE: str = "prepare"
    LAUNCH: str = "launch"
    FINALIZE: str = "finalize"


WORKFLOW_TASKS = [e.value for e in WorkflowTasks]


"""
    Managers
"""


class ManagerSvcs(Enum):
    PROVENANCE: str = layers_services.PROVENANCE_SVC
    MONITORING: str = layers_services.MONITORING_SVC
    MONITORING_IOT: str = layers_services.MONITORING_IOT_SVC


class MonitoringType(Enum):
    TIG: str = layers_services.MONITORING_SVC_TIG
    TPG: str = layers_services.MONITORING_SVC_TPG
    DSTAT: str = layers_services.MONITORING_SVC_DSTAT
