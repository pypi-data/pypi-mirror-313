"""
Utils for dynamic service imports and instanciation
"""

from importlib import import_module
from pathlib import Path
from typing import Type

from e2clab.services import Service
from e2clab.services.errors import E2clabServiceImportError


def get_available_services() -> list[str]:
    current_dir = Path(__file__).resolve().parent
    plugins_dir = current_dir / "plugins"
    # list of plugins available that can be imported
    available_services = [f.stem for f in plugins_dir.glob("*.py")]
    # do not print __init__
    if "__init__" in available_services:
        available_services.remove("__init__")
    return available_services


def load_services(service_list: list[str]) -> dict[str, Type[Service]]:
    """
    Dynamically loads python files containing defined service classes
    and returns class Service definitions in a dictionary.
    """
    for service in service_list:
        try:
            import_module(f"e2clab.services.plugins.{service}")
        except ImportError:
            raise E2clabServiceImportError(service)
    loaded = Service.get_loaded_subservices()
    return {k: loaded[k] for k in service_list}
