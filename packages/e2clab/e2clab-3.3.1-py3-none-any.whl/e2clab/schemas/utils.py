import jsonschema

from e2clab.log import get_logger
from e2clab.schemas.layers_services_schema import LayersServicesValidator
from e2clab.schemas.network_schema import NetworkValidator
from e2clab.schemas.workflow_env_schema import WorkflowEnvValidator
from e2clab.schemas.workflow_schema import WorkflowValidator

logger = get_logger(__name__, ["SCHEMA"])


def is_valid_conf(conf: dict[str:str], conf_type: str) -> bool:
    """Confronts the configuration to the configuration schemas

    Args:
        conf (yaml dump): yaml dump of the configuration file
        conf_type (str): type of configuration

    Returns:
        bool
    """
    is_valid = True
    # TODO: Use enums for schema keys
    schemas = {
        "layers_services": LayersServicesValidator,
        "network": NetworkValidator,
        "workflow": WorkflowValidator,
        "workflow_env": WorkflowEnvValidator,
    }
    try:
        schemas[conf_type].validate(conf)
    except KeyError as e:
        names = list(schemas.keys())
        logger.exception(f"Invalid configuration name : {e}\nValid names : {names}")
        is_valid = False
    except jsonschema.ValidationError as e:
        logger.error(f"Invalid {conf_type} configuration : {e.message}")
        is_valid = False
    return is_valid
