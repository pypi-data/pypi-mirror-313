"""
E2clab logging module
"""

import logging
from pathlib import Path
from typing import Tuple

from enoslib import set_config
from rich.logging import RichHandler

import e2clab.constants.default as default


class E2clabLogger(logging.LoggerAdapter):
    """
    Custom logger adapter to add prefixes to E2clab logs for better readability.
    """

    def process(self, msg, kwargs):
        prefix = default.LOG_E2CLAB_PREFIX
        extra_tags = self.extra["tags"]
        if extra_tags is not None:
            prefix = ",".join([prefix, *self.extra["tags"]])
        return f"[{prefix}] {msg}", kwargs


def get_logger(name, tags=None) -> E2clabLogger:
    """
    Returns a E2clab logger
    """
    if tags is None:
        tags = None
    logger = E2clabLogger(logging.getLogger(name), dict(tags=tags))
    return logger


def init_logging(
    level=logging.INFO,
    enable_enoslib: bool = True,
    mute_ansible: bool = False,
    file_handler: bool = True,
    file_path: Path = Path("./"),
    **kwargs,
):
    """
    Initiates the global loggers for :
        - E2clab
        - EnOSlib
    Sets terminal and file handler for root logger.
    """
    default_kwargs = dict(
        show_time=False,
        rich_tracebacks=True,
    )

    default_kwargs.update(**kwargs)

    # Setup global parent logger for e2clab
    e2c_logger = logging.getLogger("e2clab")
    e2c_logger.setLevel(level=level)

    rich_handler = RichHandler(**default_kwargs)
    rich_formatter = logging.Formatter("%(message)s")
    rich_handler.setFormatter(rich_formatter)

    # If we want to see logs from EnOSlib, we need to setup the logger
    # We don't use the enoslib.init_logging method as it directly setups
    # the root logger and gives us less fine-tuning.
    if enable_enoslib:
        en_logger = logging.getLogger("enoslib")
        en_logger.setLevel(level=level)

    if mute_ansible:
        set_config(ansible_stdout="noop")

    # Setup the root logger for terminal and file output
    root_logger = logging.getLogger()
    root_logger.addHandler(rich_handler)

    if file_handler:
        config_file_logger(file_path)


def config_file_logger(
    file_path: Path = Path("./"),
) -> Tuple[Path, Path]:
    """Configures the file loggers

    Args:
        file_path (Path, optional): Dir to output the logging files.
            Defaults to Path("./").

    Returns:
        log_file (Path): Path to logging file.
        error_file (Path): Path to error file.
    """
    # Get root logger
    root_logger = logging.getLogger()
    # Get pre-configured level of e2clab logger
    level = logging.getLogger("e2clab").level

    # Remove previous file handlers
    for hdlr in reversed(root_logger.handlers):
        if isinstance(hdlr, logging.FileHandler):
            root_logger.removeHandler(hdlr)

    FILE_FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_formatter = logging.Formatter(FILE_FORMATTER)
    # Overwrites logging file by default
    log_file = file_path / default.LOG_INFO_FILENAME
    log_file = log_file.resolve().as_posix()
    file_handler_info = logging.FileHandler(log_file, default.LOG_WRITING_MODE)
    file_handler_info.setLevel(level=level)
    file_handler_info.setFormatter(file_formatter)

    error_file = file_path / default.LOG_ERR_FILENAME
    error_file = error_file.resolve().as_posix()
    file_handler_error = logging.FileHandler(error_file, default.LOG_WRITING_MODE)
    file_handler_error.setLevel(level=logging.ERROR)
    file_handler_error.setFormatter(file_formatter)

    root_logger.addHandler(file_handler_info)
    root_logger.addHandler(file_handler_error)

    return log_file, error_file
