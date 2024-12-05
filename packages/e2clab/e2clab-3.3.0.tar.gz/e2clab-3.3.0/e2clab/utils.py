from pathlib import Path
from typing import Union

import yaml

from e2clab.constants import ENV_AUTO_PREFIX, WORKFLOW_TASKS, Command, ConfFiles
from e2clab.errors import E2clabFileError
from e2clab.log import get_logger
from e2clab.schemas import is_valid_conf

logger = get_logger(__name__, ["UTILS"])


def is_valid_setup(
    scenario_dir: Path,
    artifacts_dir: Union[Path, None],
    command: Command,
    is_app_conf: bool = False,
) -> bool:
    """Checks if E2cLab configuration files follow the right schema.

    Args:
        scenario_dir (Path):
            Path to folder containing experiment configuration files
        artifacts_dir (Union[Path, None]):
            Path to folder containing experiment artifacts
        command (Command):
            E2clab command you intend to run (e.g. 'network' or 'layer-services')
        is_app_conf (bool, optional):
            Are we going to use an 'app_conf' parameter. Defaults to False.

    Returns:
        bool: Validity of the experiment setup
    """

    is_valid = True

    # CHECK SCENARIO_DIR
    if not scenario_dir.exists():
        logger.error(f"Scenario dir path does not exist: {scenario_dir}")
        return False

    # CHECK IF CONFIG FILES EXIST AND ARE VALID IN SCENARIO_DIR
    if command == Command.LYR_SVC or command == Command.DEPLOY:
        res = validate_conf(
            conf_file=scenario_dir / ConfFiles.LAYERS_SERVICES, type="layers_services"
        )
        is_valid = res and is_valid

    if command == Command.NETWORK or command == Command.DEPLOY:
        res = validate_conf(conf_file=scenario_dir / ConfFiles.NETWORK, type="network")
        is_valid = res and is_valid

    if (
        command == Command.WORKFLOW
        or command == Command.DEPLOY
        or command == Command.FINALIZE
    ):
        res = validate_conf(
            conf_file=scenario_dir / ConfFiles.WORKFLOW, type="workflow"
        )
        is_valid = res and is_valid

        # CHECK "workflow_env.yaml"
        if is_app_conf:
            res = validate_conf(
                conf_file=scenario_dir / ConfFiles.WORKFLOW_ENV, type="workflow_env"
            )
            is_valid = res and is_valid

    # CHECK ARTIFACTS_DIR
    if artifacts_dir is not None and not artifacts_dir.exists():
        logger.error(f"Artifact path does not exist: {artifacts_dir}")
        return False

    return is_valid


def is_valid_task(task: str) -> bool:
    is_valid = True
    if task.lower() not in WORKFLOW_TASKS:
        logger.error(
            f"Task {task.lower()} is not valid, "
            "choose one of the following [prepare, launch, finalize]"
        )
        is_valid = False
    return is_valid


def load_yaml_file(file: Path) -> dict[str, str]:
    """Loads an E2clab yaml configuration file

    Args:
        file (Path): Yaml configuration file

    Raises:
        E2clabFileError: if file does not exist
        E2clabFileError: if there is a yaml syntax error
        E2clabFileError: if there is any other unexpected error

    Returns:
        dict[str, str]: python object containing configuration description
    """
    try:
        with open(file, "r") as f:
            content = yaml.safe_load(f)
            return content
    except FileNotFoundError as e:
        raise E2clabFileError(file, "File does not exist") from e
    except yaml.YAMLError as e:
        raise E2clabFileError(file, "Yaml syntax error in file") from e
    except Exception as e:
        raise E2clabFileError(file, "Unknown error") from e


def validate_conf(conf_file: Path, type: str) -> bool:
    """Validate if the configuration file follows the right syntax

    Args:
        conf_file (Path): path to the file
        type (str): "layers_services" | "network" | "workflow" | "workflow_env"

    Returns:
        bool: is the configuration valid
    """
    try:
        conf = load_yaml_file(conf_file)
    except E2clabFileError as e:
        logger.error(e)
        return False
    return is_valid_conf(conf, type)


def write_dot_param(file, envname: str, value, comment: bool = False):
    """Writes a dotfile parameter to the file

    Args:
        file (file buffer): file to write to
        envname (str): E2Clab parameter envame without prefix
        value (Any): value to set
        comment (bool, optional): comment the line to write. Defaults to False.
    """
    line = f"{ENV_AUTO_PREFIX}_{envname}={value}\n"
    if comment:
        line = "# " + line
    file.write(line)
