from typing import Optional, Tuple

import enoslib as en
from enoslib.infra.enos_chameleonedge.configuration import Container

import e2clab.constants.default as default
from e2clab.config import InfrastructureConfig
from e2clab.constants.layers_services import (
    CC_DEVICE_PROFILES,
    CC_EXPOSED_PORTS,
    CC_START,
    CC_START_TIMEOUT,
    CHAMELEON_EDGE,
    CLUSTER,
    CONTAINERS,
    IMAGE,
    JOB_NAME,
    NAME,
    RC_FILE,
    SERVICES,
    WALLTIME,
)
from e2clab.log import get_logger
from e2clab.providers import Provider, ProviderConfig

logger = get_logger(__name__, ["CHAM_EDGE"])


class CEConfig(ProviderConfig):
    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.job_name = self.env.get(JOB_NAME, default.JOB_NAME)
        self.walltime = self.env.get(WALLTIME, default.WALLTIME)
        self.rc_file = self.env.get(RC_FILE, None)
        self.image = self.env.get(IMAGE, default.CHIEDGE_IMAGE)
        self.cluster = self.env.get(CLUSTER, default.CHAMELEON_EDGE_CLUSTER)

    def init(self, optimization_id: Optional[int] = None) -> None:
        """Initialize provider config

        Args:
            optimization_id (Optional[int], optional): Optimization_ID.
                Defaults to None.
        """
        self.job_name = self.opt_job_id(self.job_name, optimization_id)

        self.config = en.ChameleonEdgeConf.from_settings(
            lease_name=self.job_name, walltime=self.walltime, rc_file=self.rc_file
        )

    def config_monitoring(self):
        # Not defined for ChiEdge
        pass

    def config_provenance(self):
        # Not defined for Chiedge
        pass

    def config_resources(self):
        for layer in self.layers:
            for service in layer[SERVICES]:
                add_cluster, add_server = self.check_service_mapping(service)
                roles = self.get_service_roles(layer[NAME], service)
                containers = service[CONTAINERS].copy()
                # Check only one container configuration
                for cont_conf in containers:
                    container = Container(
                        name=cont_conf.pop(NAME, default.CONTAINER_NAME),
                        image=cont_conf.pop(IMAGE, self.image),
                        exposed_ports=cont_conf.pop(CC_EXPOSED_PORTS, None),
                        start=cont_conf.pop(CC_START, True),
                        start_timeout=cont_conf.pop(CC_START_TIMEOUT, None),
                        device_profiles=cont_conf.pop(CC_DEVICE_PROFILES, None),
                        **cont_conf,
                    )
                if add_cluster is None:
                    add_cluster = self.cluster
                if add_server is not None:
                    self.config.add_machine(
                        roles=roles, device_name=add_server, container=container
                    )
                else:
                    quantity = self.get_service_quantity(service)
                    self.config.add_machine(
                        roles=roles,
                        machine_name=add_cluster,
                        container=container,
                        count=quantity,
                    )

    def finalize(self) -> Tuple[en.ChameleonEdge, bool, bool]:
        self.config = self.config.finalize()
        logger.debug(f"Provider conf = {self.config.to_dict()}")
        provider = en.ChameleonEdge(self.config)
        return provider, self.monitoring_provider, self.provenance_provider


class Chameleonedge(Provider):
    """
    The provider to use when deploying on Chameleon Edge.
    """

    def __init__(
        self, infra_config: InfrastructureConfig, optimization_id: Optional[int] = None
    ):
        super().__init__(infra_config, optimization_id)
        self.infra_config.refine_to_environment(CHAMELEON_EDGE)
        self.config = CEConfig(self.infra_config)

    def init(self):
        """
        Take ownership over some Chameleon Edge resources (compute).
        :return: roles, networks
        """
        self.provider = self._provider_chameleonedge(
            optimization_id=self.optimization_id
        )

        roles, networks = self.provider.init()
        # en.wait_for(roles)  # FIXME: Is it needed?

        # roles = en.sync_info(roles, networks)

        if None in (roles):
            raise ValueError(f"Failed to get resources from: {CHAMELEON_EDGE}.")

        self.roles = roles
        self.networks = networks
        self.log_roles_networks(CHAMELEON_EDGE)

        return roles, networks

    def destroy(self):
        self.provider.destroy()

    def _provider_chameleonedge(
        self, optimization_id: Optional[int] = None
    ) -> en.ChameleonEdge:
        self.config.init(optimization_id=optimization_id)
        self.config.config_provenance()
        self.config.config_monitoring()
        self.config.config_resources()
        provider, monitoring_provider, provenance_provider = self.config.finalize()
        self.monitoring_provider = monitoring_provider
        self.provenance_provider = provenance_provider
        return provider
