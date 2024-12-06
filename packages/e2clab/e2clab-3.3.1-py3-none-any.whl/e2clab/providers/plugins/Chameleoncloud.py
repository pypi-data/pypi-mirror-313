from typing import Optional, Tuple

import enoslib as en

import e2clab.constants.default as default
from e2clab.config import InfrastructureConfig
from e2clab.constants.layers_services import (
    CHAMELEON_CLOUD,
    CLUSTER,
    IMAGE,
    JOB_NAME,
    KEY_NAME,
    MONITORING_SERVICE_ROLE,
    NAME,
    RC_FILE,
    SERVICES,
    WALLTIME,
)
from e2clab.log import get_logger
from e2clab.managers import Managers
from e2clab.providers import Provider, ProviderConfig

logger = get_logger(__name__, ["CC"])


class CCConfig(ProviderConfig):
    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.job_name = self.env.get(JOB_NAME, default.JOB_NAME)
        self.walltime = self.env.get(WALLTIME, default.WALLTIME)
        self.rc_file = self.env.get(RC_FILE, None)
        self.key_name = self.env.get(KEY_NAME, None)
        self.image = self.env.get(IMAGE, default.CHICLOUD_IMAGE)
        self.cluster = self.env.get(CLUSTER, None)

    def init(self, optimization_id: Optional[int] = None) -> None:
        """Initialize provider config

        Args:
            optimization_id (Optional[int], optional): Optimization_ID.
                Defaults to None.
        """
        self.check_cluster()

        self.job_name = self.opt_job_id(self.job_name, optimization_id)

        self.config = en.CBMConf.from_settings(
            lease_name=self.job_name,
            walltime=self.walltime,
            rc_file=self.rc_file,
            key_name=self.key_name,
            image=self.image,
        )

    def config_monitoring(self) -> None:
        """Configure provider config for monitoring"""
        monitoring_conf = self.get_manager_conf(Managers.MONITORING)
        self.monitoring_provider = False
        if monitoring_conf:
            self.monitoring_provider = True
            self._configure_monitoring(monitoring_config=monitoring_conf)

    def config_provenance(self):
        # CC not configured for provenance management
        pass

    def _configure_monitoring(self, monitoring_config: dict) -> None:
        """Add Chameleon node as monitoring provider: 1 machine[ui, collector]

        Args:
            config (en.CBMConf): provider configuration
            monitoring_config (dict): experiment monitoring configuration
        """
        # Cluster existence validated by schema
        _cluster = monitoring_config[CLUSTER]
        self.config.add_machine(
            roles=[MONITORING_SERVICE_ROLE],
            flavour=_cluster,
            number=1,
        )

    def config_resources(self) -> None:
        """Add machines for services"""
        for layer in self.layers:
            for service in layer[SERVICES]:
                add_cluster, add_server = self.check_service_mapping(service)
                if not add_cluster:
                    add_cluster = self.cluster
                roles = self.get_service_roles(layer[NAME], service)
                quantity = self.get_service_quantity(service)
                self.config.add_machine(
                    roles=roles, flavour=add_cluster, number=quantity
                )

    def finalize(self) -> Tuple[en.CBM, bool, bool]:
        self.config = self.config.finalize()
        logger.debug(f"Provider conf = {self.config.to_dict()}")
        provider = en.CBM(self.config)
        return provider, self.monitoring_provider, self.provenance_provider


class Chameleoncloud(Provider):
    """
    The provider to use when deploying on Chameleon Cloud.
    """

    def __init__(
        self, infra_config: InfrastructureConfig, optimization_id: Optional[int] = None
    ):
        super().__init__(infra_config, optimization_id)
        infra_config.refine_to_environment(CHAMELEON_CLOUD)
        self.config = CCConfig(infra_config)

    def init(self) -> Tuple[en.Roles, en.Networks]:
        """
        Take ownership over some Chameleon Cloud resources (compute and networks).
        :return: roles, networks
        """
        self.provider = self._provider_chameleoncloud(self.optimization_id)

        roles, networks = self.provider.init()

        roles = en.sync_info(roles, networks)

        self.roles = roles
        self.networks = networks

        if None in (roles, networks):
            raise ValueError(f"Failed to get resources from: {CHAMELEON_CLOUD}.")

        self.log_roles_networks(CHAMELEON_CLOUD)

        return roles, networks

    def destroy(self):
        self.provider.destroy()

    def _provider_chameleoncloud(self, optimization_id: Optional[int] = None) -> en.CBM:
        self.config.init(optimization_id=optimization_id)
        self.config.config_provenance()
        self.config.config_monitoring()
        self.config.config_resources()
        provider, monitoring_provider, provenance_provider = self.config.finalize()
        self.monitoring_provider = monitoring_provider
        self.provenance_provider = provenance_provider
        return provider
