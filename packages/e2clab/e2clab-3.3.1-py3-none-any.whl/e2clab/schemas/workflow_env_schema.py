from jsonschema import Draft7Validator

SCHEMA: dict = {
    "type": "object",
    "additionalProperties": {
        "type": "object",
        "additionalProperties": {
            "type": ["string", "number", "boolean"],
        },
    },
}

WorkflowEnvValidator: Draft7Validator = Draft7Validator(SCHEMA)
