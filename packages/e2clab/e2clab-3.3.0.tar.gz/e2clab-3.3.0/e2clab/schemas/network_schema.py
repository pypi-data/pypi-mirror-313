from jsonschema import Draft7Validator

from e2clab.constants.network import DELAY, DST, LOSS, NETWORKS, RATE, SRC, SYMMETRIC

SCHEMA: dict = {
    "description": "Experiment Network description",
    "type": "object",
    "properties": {
        NETWORKS: {
            "type": ["array", "null"],
            "items": {"$ref": "#/definitions/network"},
        }
    },
    "required": [NETWORKS],
    "additionalProperties": False,
    "definitions": {
        "network": {
            "title": "Network emulation",
            # "$$target": "#/definitons/network",
            "type": "object",
            "properties": {
                SRC: {
                    "description": "Source layer name",
                    "type": "string",
                },
                DST: {
                    "description": "Destination layer name",
                    "type": "string",
                },
                DELAY: {
                    "description": "The delay to apply",
                    "type": "string",
                    "examples": ["10ms", "1ms"],
                },
                RATE: {
                    "description": "The rate to apply",
                    "type": "string",
                    "examples": ["1gbit", "100mbit"],
                },
                LOSS: {
                    "description": "The percentage of loss",
                    "type": "string",
                    "pattern": r"\d*.?\d*%",
                    "examples": ["1%", "5%"],
                },
                SYMMETRIC: {
                    "description": "True for symmetric rules to be applied",
                    "type": "boolean",
                },
            },
            "required": [SRC, DST],
            "additionalProperties": False,
        }
    },
}

NetworkValidator: Draft7Validator = Draft7Validator(SCHEMA)
