from jsonschema import Draft7Validator

import e2clab.constants.default as default
from e2clab.constants import SUPPORTED_ENVIRONMENTS
from e2clab.constants.layers_services import (
    CHAMELEON_CLOUD,
    CHAMELEON_EDGE,
    CLUSTER,
    ENV,
    ENV_NAME,
    ENVIRONMENT,
    FIREWALL_RULES,
    G5K,
    IMAGE,
    IOT_LAB,
    JOB_NAME,
    JOB_TYPE,
    KEY_NAME,
    LAYERS,
    MONITOR,
    NAME,
    QUANTITY,
    RC_FILE,
    REPEAT,
    RESERVATION,
    ROLES,
    SERVERS,
    SERVICES,
    WALLTIME,
)
from e2clab.managers import Managers

walltime_schema: dict = {
    "description": "Walltime for our experiment, in format hh:mm:ss",
    "type": "string",
    "pattern": r"^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$",
}

service_schema: dict = {
    "descritpion": "E2clab service, other properties are service metedata",
    "type": "object",
    "properties": {
        NAME: {
            "description": (
                "Name of the service. "
                "If the name matches a user-defined service name, "
                "this service will be deployed. "
            ),
            "type": "string",
        },
        QUANTITY: {
            "description": "Number of nodes the service will be deployed on",
            "type": "number",
        },
        ROLES: {
            "type": "array",
        },
        REPEAT: {
            "description": (
                "Number of times the service definition will be duplicated."
            ),
            "type": "number",
        },
        ENV: {
            "description": "Service metadata.",
            "type": "object",
        },
        ENVIRONMENT: {
            "description": (
                "Environment on which the service will be deployed."
                "If set, you can specify other environment-specific properties"
                "from the environment you chose"
            ),
            "type": "string",
            "enum": SUPPORTED_ENVIRONMENTS,
        },
        SERVERS: {
            "description": "Server to deploy services, overwrites cluster definition",
            # "type": "array", can be array or string it seems
            "examples": [
                "chifflot-7.lille.grid5000.fr",
                "chifflot-8.lille.grid5000.fr",
            ],
        },
        # Other properties are service metadata, to configure per service.
    },
    "required": [NAME],
}

service_list: dict = {
    "description": "Description of the service to be deployed on our layer.",
    "type": "array",
    "items": service_schema,
}

job_name_schema: dict = {
    "description": "Name of the job on the testbed",
    "type": "string",
    "default": default.JOB_NAME,
}

# see _provider_g5k in G5k.py
g5k_schema: dict = {
    "type": "object",
    "properties": {
        JOB_NAME: job_name_schema,
        WALLTIME: walltime_schema,
        RESERVATION: {
            "description": "reservation date in YYYY-mm-dd HH:MM:SS format",
            "type": "string",
            "pattern": r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",
        },
        JOB_TYPE: {
            "description": "OAR job type",
            "type": "array",
            "default": default.JOB_TYPE,
        },
        ENV_NAME: {
            "description": "The kadeploy3 environment to use (deploy only)",
            "type": "string",
        },
        CLUSTER: {"description": "Which G5k cluster to use", "type": "string"},
        KEY_NAME: {
            "description": "SSH public key to use",
            "type": "string",
            "default": default.SSH_KEYFILE,
        },
        FIREWALL_RULES: {
            "description": "G5k firewall rules",
            "type": "array",
        },
        MONITOR: {
            "description": "Activate on demand metrics (e.g.`prom_.*`)",
            "type": "string",
        },
    },
}

# see _provider_iotlab in Iotlab.py
iotlab_schema: dict = {
    "type": "object",
    "properties": {
        JOB_NAME: job_name_schema,
        WALLTIME: walltime_schema,
        CLUSTER: {
            "description": "Iotlab cluster to use",
            "type": "string",
            "default": default.IOTLAB_CLUSTER,
        },
    },
}

# see _provider_chameleoncloud in Chameleoncloud.py
chameleon_cloud_schema: dict = {
    "type": "object",
    "properties": {
        JOB_NAME: job_name_schema,
        WALLTIME: walltime_schema,
        RC_FILE: {
            "description": "Openstack environment rc file path",
            "type": "string",
        },
        KEY_NAME: {
            "description": "SSH pub key",
            "type": "string",
        },
        IMAGE: {
            "description": "Cloud image to use",
            "type": "string",
            "default": default.CHICLOUD_IMAGE,
        },
        CLUSTER: {
            "descruption": "Chameleon cloud machine flavour to use",
            "type": "string",
        },
    },
}

# see _provider_chameleonedge in Chameleonedge.py
chameleon_edge_schema: dict = {
    "type": "object",
    "properties": {
        JOB_NAME: job_name_schema,
        WALLTIME: walltime_schema,
        RC_FILE: {
            "description": "Openstack environment rc file path",
            "type": "string",
        },
        KEY_NAME: {
            "description": "SSH pub key",
            "type": "string",
        },
        IMAGE: {
            "description": "Chameleon edge image to use",
            "type": "string",
            "default": default.CHIEDGE_IMAGE,
        },
        CLUSTER: {
            "description": "Chameleon edge machine flavour to use",
            "type": "string",
            "default": default.CHAMELEON_EDGE_CLUSTER,
        },
    },
}

common_prov_properties: dict = {
    JOB_NAME: job_name_schema,
    WALLTIME: walltime_schema,
    CLUSTER: {"description": "Which cluster to deploy on", "type": "string"},
}


"""
    Main layers_services.yml schema
"""

env_schema = {
    "description": "Definition of experiment environments",
    "type": "object",
    "properties": {
        # Common provider properties can be defined at the top level
        **common_prov_properties,
        JOB_NAME: {
            "description": "Name of our experiment",
            "type": "string",
        },
        G5K: {
            "description": "Grid5000 configuration",
            "$ref": f"#/definitions/{G5K}",
        },
        IOT_LAB: {
            "description": "FIT IoT-LAB configuration",
            "$ref": f"#/definitions/{IOT_LAB}",
        },
        CHAMELEON_CLOUD: {
            "description": "ChameleonCloud configuration",
            "$ref": f"#/definitions/{CHAMELEON_CLOUD}",
        },
        CHAMELEON_EDGE: {
            "description": "ChameleonEdge configuration",
            "$ref": f"#/definitions/{CHAMELEON_EDGE}",
        },
    },
    "required": [],
    "anyOf": [
        {"required": [prov]} for prov in SUPPORTED_ENVIRONMENTS
    ],  # Need at least one environment
}

# Main jsonschema

SCHEMA: dict = {
    "description": "Experiment Layers & Services description",
    "type": "object",
    "properties": {
        ENVIRONMENT: {"$ref": "#/definitions/environment"},
        LAYERS: {
            "description": "Experiment layers definition.",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    NAME: {
                        "description": "Name of the layer, e.g. edge, fog, cloud...",
                        "type": "string",
                    },
                    SERVICES: {"$ref": "#/definitions/service_list"},
                },
                "required": [
                    NAME,
                    SERVICES,
                ],  # Need at least one layer with one service
            },
        },
    },
    "required": [LAYERS, ENVIRONMENT],
    "additionalProperties": False,  # Only defined properties are allowed
    "definitions": {
        "service_list": service_list,
        "environment": env_schema,
        G5K: g5k_schema,
        IOT_LAB: iotlab_schema,
        CHAMELEON_CLOUD: chameleon_cloud_schema,
        CHAMELEON_EDGE: chameleon_edge_schema,
    },
}

# Add managers schemas
for manager in Managers:
    manager_class = manager.value
    SCHEMA["properties"].update(
        {
            manager_class.get_config_key(): {
                "$ref": f"#/definitions/{manager_class.__name__}"
            }
        }
    )
    SCHEMA["definitions"].update(
        {f"{manager_class.__name__}": manager_class.get_schema()}
    )

LayersServicesValidator: Draft7Validator = Draft7Validator(SCHEMA)
ServiceValidator: Draft7Validator = Draft7Validator(service_schema)
