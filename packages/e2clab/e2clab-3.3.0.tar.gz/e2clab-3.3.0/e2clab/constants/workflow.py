"""Workflow file constants"""

TARGET = "hosts"
DEPENDS_ON = "depends_on"
SERV_SELECT = "service_selector"
GROUPING = "grouping"
PREFIX = "prefix"
SELF_PREFIX = "_self"

WORKFLOW_GROUPING_LIST = [
    "round_robin",
    "asarray",
    "aggregate",
    # used internally by e2clab, not meant to use for the user
    "address_match",
]

GROUPING_LIST_USER = [
    "round_robin",
    "asarray",
    "aggregate",
    # TODO: Check CCTV example and maybe remove this option
    # CCTV example
    "address_match",
]

DEFAULT_GROUPING = "round_robin"

# TODO: Use the Enum instead
TASK_LAUNCH = "launch"
TASK_PREPARE = "prepare"
TASK_FINALIZE = "finalize"

ANSIBLE_TASKS = "tasks"

TASKS = [TASK_PREPARE, TASK_LAUNCH, TASK_FINALIZE]

WORKFLOW_DEVICE_TASK = ["copy", "shell", "fetch"]
