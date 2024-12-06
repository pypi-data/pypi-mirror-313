"""
Default global parameters

Those parameters dictate the default behaviour of experiments

The purpose of this module is to group experiment-level parameters
that are going to be configurable via a config file in the future
"""

import os
from pathlib import Path
from typing import Any

from e2clab.constants.layers_services import (
    JOB_TYPE_DEPLOY,
    MONITORING_IOT_AVERAGE_VALS,
    MONITORING_IOT_PERIOD_VALS,
)

from . import ENV_AUTO_PREFIX, WorkflowTasks


def prefix(value: str):
    return ENV_AUTO_PREFIX + "_" + value


def load_def(value: str, default: Any):
    """Loads value from environment

    Args:
        value (str): environment variable: E2C_<value>
        default (Any): default return value

    Returns:
        Any: return value
    """
    env = os.environ
    return env.get(prefix(value), default)


# Cluster
G5K_CLUSTER = load_def("G5K_CLUSER", "paradoxe")
IOTLAB_CLUSTER = load_def("IOTLAB_CLUSTER", "saclay")
CHAMELEON_CLOUD_CLUSTER = load_def("CHAMELEON_CLOUD_CLUSTER", "gpu_rtx_6000")
CHAMELEON_EDGE_CLUSTER = load_def("CHAMELEON_EDGE_CLUSTER", "jetson-nano")
# Experiment
JOB_NAME = load_def("JOB_NAME", "E2Clab")
WALLTIME = load_def("WALLTIME", "01:00:00")
# Id
SSH_KEYFILE = load_def("SSH_KEYFILE", str(Path.home() / ".ssh" / "id_rsa.pub"))
# Services
NODE_QUANTITY = load_def("NODE_QUANTITY", 1)
# Providers
G5K_ENV_NAME = load_def("G5K_ENV_NAME", "debian11-x64-big")
CHICLOUD_IMAGE = load_def("CHICLOUD_IMAGE", "CC-Ubuntu20.04")
CHIEDGE_IMAGE = load_def("CHIEDGE_IMAGE", "ubuntu")
# Logging
LOG_E2CLAB_PREFIX = load_def("LOG_E2CLAB_PREFIX", "E2C")
LOG_WRITING_MODE = load_def("LOG_WRITING_MODE", "a+")
LOG_INFO_FILENAME = load_def("LOG_INFO_FILENAME", "e2clab.log")
LOG_ERR_FILENAME = load_def("LOG_ERR_FILENAME", "e2clab.err")
# G5k
JOB_TYPE = [load_def("JOB_TYPE", JOB_TYPE_DEPLOY)]
# ChameleonEdge
# Default container name
CONTAINER_NAME = load_def("CONTAINER_NAME", "mycontainer")
# Validate files/dir
LAYERS_SERVICES_VALIDATE_FILE = load_def(
    "LAYERS_SERVICES_VALIDATE_FILE", "layers_services-validate.yaml"
)
NET_VALIDATE_DIR = load_def("NET_VALIDATE_DIR", "network-validate")
WORKFLOW_VALIDATE_FILE = load_def("WORKFLOW_VALIDATE_FILE", "workflow-validate.out")
# Output folders
PROVENANCE_DATA = load_def("PROVENANCE_DATA", "provenance-data")
MONITORING_DATA = load_def("MONITORING_DATA", "monitoring-data")
MONITORING_IOT_DATA = load_def("MONITORING_IOT_DATA", "iotlab-data")
MONITORING_KWOLLECT_DATA = load_def("MONITORING_KWOLLECT_DATA", "kwollect-data")
# Workflow_env
WORKFLOW_ENV_PREFIX = load_def("WORKFLOW_ENV_PREFIX", "env_")
# Monitoring IOT
IOT_PERIOD_VAL = load_def("IOT_PERIOD_VAL", MONITORING_IOT_PERIOD_VALS[-1])
IOT_AVERAGE_VAL = load_def("IOT_AVERAGE_VAL", MONITORING_IOT_AVERAGE_VALS[1])
# Kwollect monitoring
KWOLLECT_STEP = load_def("KWOLLECT_STEP", WorkflowTasks.LAUNCH.value)
# Provenance
PARALLELISM: int = load_def("PARALLELISM", 1)
DATAFLOW_SPEC: str = load_def("DATAFLOW_SPEC", "")
# Monitoring
DSTAT_OPTS: str = load_def("DSTAT_OPTIONS", "-m -c -n")
