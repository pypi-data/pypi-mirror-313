"""
This file defines all functions and utilities needded to enforce the 'workflow'
of our experiment
"""

import copy
from pathlib import Path
from typing import Optional, Tuple, Type

from enoslib import Networks, Roles

from e2clab.config import InfrastructureConfig
from e2clab.constants import Environment
from e2clab.constants.layers_services import ID, SERVICE_PLUGIN_NAME
from e2clab.errors import E2clabError
from e2clab.log import get_logger
from e2clab.providers import Provider, get_available_providers, load_providers
from e2clab.services import Service, get_available_services, load_services
from e2clab.utils import load_yaml_file

from .managers import Manager, Managers


class Infrastructure:
    """
    Enforce Layers & Services definitions
    a.k.a. Layers & Services manager
    """

    def __init__(self, config: Path, optimization_id: Optional[str] = None) -> None:
        """Create a new experiment architecture

        Args:
            config (Path): Path to 'layers_services.yaml' file
            optimization_id (Optional[str], optional): Optimization id. Defaults to None
        """
        self.logger = get_logger(__name__, ["INFRA"])
        self.config = self._load_config(config)
        self.optimization_id: int = optimization_id

        # TODO: check if we can do without this
        # Registering extra information from services
        self.all_serv_extra_inf = {}

    def _load_config(self, config_path: Path) -> InfrastructureConfig:
        c = load_yaml_file(config_path)
        return InfrastructureConfig(c)

    # User Methods

    def prepare(self) -> None:
        """Prepare infrastructure deployment"""
        self.logger.debug("Preparing infrastructure deployment")
        self.prov_to_load = self.config.get_providers_to_load()
        self.serv_to_load = self.config.get_services_to_load()

        self.managers: dict[Managers, Manager] = {}
        for manager in Managers:
            manager_conf = self.config.get_manager_conf(manager)
            if manager_conf:
                self.logger.debug(f"Found {manager.name} manager configuration")
                self.managers[manager] = manager.value(config=manager_conf)

        self.logger.debug(
            f"[AVAILABLE PROVIDERS]: {[e.name for e in get_available_providers()]}"
        )
        self.logger.debug(f"[PROVIDERS TO LOAD] {[e.name for e in self.prov_to_load]}")
        self.logger.debug(f"[AVAILABLE SERVICES]: {get_available_services()}")
        self.logger.debug(f"[SERVICES TO LOAD] {self.serv_to_load}")

    def deploy(
        self, artifacts_dir: Path, remote_working_dir: str
    ) -> Tuple[Roles, Networks]:
        """Deploys infrastructure

        Args:
            artifacts_dir (Path): Path to artifacts of the experiment
            remote_working_dir (str): Directory to output monitoring data
                on remote hosts

        Returns:
            Tuple[Roles, Networks]: Roles and Networks associated
                with the infrastructure
        """
        self.logger.debug("Lodaing providers")
        loaded_providers = self._load_providers()
        self.logger.debug("Creating providers")
        self.providers = self._create_providers(loaded_providers)
        self.logger.debug("Initiate provider resources")
        self.roles, self.networks = self._init_providers_merge_resources()

        self.logger.debug("Loading services")
        loaded_services = self._load_services()
        self.logger.debug("Creating services")
        self._create_services(loaded_services)

        # MANAGERS
        for e_manager, manager in self.managers.items():
            self.logger.debug(f"Init {e_manager.name} manager")
            provider = None
            manager_env = manager.get_environment()
            if manager_env:
                try:
                    provider = self.providers[manager_env]
                except KeyError as e:
                    raise E2clabError(
                        f"Could not find provider {manager_env} for "
                        f"{e_manager.name}: {e}"
                    )

            manager.init(
                roles=self.roles,
                networks=self.networks,
                artifacts_dir=artifacts_dir,
                provider=provider,
                meta={"remote_working_dir": remote_working_dir},
            )

            self.logger.debug(f"Deploying {e_manager.name} manager")

            manager.deploy()
            extra_inf = manager.get_extra_info()
            self.all_serv_extra_inf.update(extra_inf)

        self.logger.debug(f"[SERVICE EXTRA INFO] = {self.all_serv_extra_inf}")
        self.logger.debug(f"[ROLES] = {self.roles}")
        self.logger.debug(f"[ALL NETWORKS] = {self.networks}")

        self.logger.info("Infrastructure deployed !")

        return self.roles, self.networks

    def finalize(self, output_dir: Path):
        """Backup data and destroy manager services

        Args:
            output_dir (Path): Path to output backup data
        """
        for e_manager, manager in self.managers.items():
            self.logger.debug(f"Backup {e_manager.name} manager")
            manager.backup(output_dir=output_dir)
            self.logger.debug(f"Destroying {e_manager.name} manager")
            manager.destroy()

    def destroy(self) -> None:
        """Destroys all providers resources"""
        for environment, provider in self.providers.items():
            self.logger.debug(f"[DESTROYING PROVIDER] {environment.name}")
            provider.destroy()

    # End User Methods

    def _load_providers(self) -> dict[Environment, Type[Provider]]:
        """
        Loads providers
        """
        loaded_providers = load_providers(self.prov_to_load)
        return loaded_providers

    def _create_providers(
        self, loaded_providers: dict[Environment, Type[Provider]]
    ) -> dict[Environment, Provider]:
        providers = {}
        for environment, provider_class in loaded_providers.items():
            providers[environment] = provider_class(
                infra_config=copy.deepcopy(self.config),
                optimization_id=self.optimization_id,
            )

        return providers

    def _init_providers_merge_resources(self) -> Tuple[Roles, Networks]:
        """Init all resources and merges all of them in a Roles and a Networks object
        Also adds global roles "provider_name"

        Returns:
            Tuple[Roles, Networks]: All resources
        """
        # Inspired by the Providers.init() method from enoslib
        roles = Roles()
        networks = Networks()
        for env, provider in self.providers.items():
            _roles, _networks = provider.init()
            roles.extend(_roles)
            roles[env.value.capitalize()] = _roles.all()
            networks.extend(_networks)
            networks[env.value.capitalize()] = _networks.all()
        return roles, networks

    def _load_services(self) -> dict[str, Service]:
        """Loads needed services"""
        loaded_services = load_services(self.serv_to_load)
        return loaded_services

    def _create_services(self, loaded_services: dict[str, Service]):
        """
        Loads services from the infrastructure configuration and deploys them
        """
        for service in self.config.iterate_services():
            service_name = service[SERVICE_PLUGIN_NAME]
            self.logger.debug(f"Creating {service_name}")
            # Get class definition and instantiate
            try:
                class_service = loaded_services[service_name]
            except KeyError:
                self.logger.error(f"Failed importing service: {service_name}")
                raise E2clabError
            # Create service instance
            inst_service: Service = class_service(
                hosts=self.roles[service[ID]],
                service_metadata=service,
            )
            # Deploy
            service_extra_info, service_roles = inst_service._init()
            self.all_serv_extra_inf.update(service_extra_info)
            # TODO: This does nothing ?
            service["metadata"] = service_extra_info
            self.roles.update(service_roles)
            self.logger.debug(f"Done creating {service_name}")
