"""
Utils for dynamisc imports and instanciation
"""

from importlib import import_module
from pathlib import Path
from typing import Type

from e2clab.constants import Environment
from e2clab.providers import Provider
from e2clab.providers.errors import E2clabProviderImportError


def get_available_providers() -> list[Environment]:
    current_dir = Path(__file__).resolve().parent
    plugins_dir = current_dir / "plugins"
    # list of available modules
    filename_list = [f.stem for f in plugins_dir.glob("*.py")]
    # do not print __init__
    if "__init__" in filename_list:
        filename_list.remove("__init__")
    # TODO: move class definition to lower case module
    available_services = [Environment(f.lower()) for f in filename_list]
    return available_services


def load_providers(
    environment_list: list[Environment],
) -> dict[Environment, Type[Provider]]:
    """
    Dynamically loads python files containing defined service classes
    and returns requested Provider class definitions in a dictionary.
    """
    for environment in environment_list:
        # TODO: move class definition to lower case module
        provider_module = environment.value.capitalize()
        try:
            import_module(f"e2clab.providers.plugins.{provider_module}")
        except ImportError:
            raise E2clabProviderImportError(provider_module)
    _loaded = Provider.get_loaded_providers()
    loaded_providers = {}
    for name, prov in _loaded.items():
        env = Environment(name.lower())
        if env in environment_list:
            loaded_providers[env] = prov
    return loaded_providers
