from jsonschema import Draft7Validator

from e2clab.constants.workflow import (
    DEPENDS_ON,
    GROUPING,
    GROUPING_LIST_USER,
    PREFIX,
    SERV_SELECT,
    TARGET,
    TASKS,
)

task_schema: dict = {
    "description": "Ansible task definition.",
    "type": "array",
}

workflow_schema_tasks: dict = {TASK: task_schema for TASK in TASKS}

# TODO: finish workflow schema
depends_on_schema = {
    "description": "Description of hosts interconnections",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            SERV_SELECT: {
                "description": "",
                "type": "string",
            },
            GROUPING: {
                "description": "Grouping strategy between hosts, defaults: round_robin",
                "type": "string",
                "enum": GROUPING_LIST_USER,
            },
            PREFIX: {
                "description": "Prefix to access linked hosts parameters",
                "type": "string",
            },
        },
        "required": [SERV_SELECT, PREFIX],
    },
}

SCHEMA: dict = {
    "description": "Non-described properties will be passed to ansible in a play.",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            TARGET: {
                "description": "hosts description on which to execute workflow",
                "type": "string",
            },
            DEPENDS_ON: {"$ref": "#/definitions/depends_on"},
            **workflow_schema_tasks,
        },
        "required": [TARGET],
        # "additionalProperties": False,
    },
    "definitions": {"depends_on": depends_on_schema},
}

WorkflowValidator: Draft7Validator = Draft7Validator(SCHEMA)
