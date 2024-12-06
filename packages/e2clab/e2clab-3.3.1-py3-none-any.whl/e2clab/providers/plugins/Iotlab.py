from typing import Optional, Tuple

import enoslib as en
from enoslib.infra.enos_iotlab.configuration import ConsumptionConfiguration

import e2clab.constants.default as default
from e2clab.config import InfrastructureConfig
from e2clab.constants.layers_services import (
    ARCHI,
    CLUSTER,
    IMAGE,
    IOT_LAB,
    JOB_NAME,
    MONITORING_IOT_AVERAGE,
    MONITORING_IOT_CURRENT,
    MONITORING_IOT_PERIOD,
    MONITORING_IOT_POWER,
    MONITORING_IOT_PROFILES,
    MONITORING_IOT_VOLTAGE,
    NAME,
    PROFILE,
    QUANTITY,
    SERVICES,
    WALLTIME,
)
from e2clab.log import get_logger
from e2clab.managers import Managers
from e2clab.providers import Provider, ProviderConfig

logger = get_logger(__name__, ["IOTLAB"])


class Iotlab(Provider):
    """
    The provider to use when deploying on FIT IoT LAB.
    """

    def __init__(
        self, infra_config: InfrastructureConfig, optimization_id: Optional[int] = None
    ):
        super().__init__(infra_config, optimization_id)
        self.infra_config.refine_to_environment(IOT_LAB)
        self.config = IotlabConfig(self.infra_config)

    def init(self):
        """
        Take ownership over some FIT IoT LAB resources (compute and networks).
        :return: roles, networks
        """
        self.provider = self._provider_iotlab(self.optimization_id)

        roles, networks = self.provider.init()
        en.wait_for(roles)

        roles = en.sync_info(roles, networks)

        if None in (roles, networks):
            raise ValueError(f"Failed to get resources from: {IOT_LAB}.")

        self.roles = roles
        self.networks = networks
        self.log_roles_networks(IOT_LAB)

        return roles, networks

    def destroy(self):
        self.provider.destroy()

    def _provider_iotlab(self, optimization_id: Optional[int] = None) -> en.Iotlab:
        self.config.init(optimization_id=optimization_id)
        self.config.config_provenance()
        self.config.config_monitoring()
        self.config.config_resources()
        provider, monitoring_provider, provenance_provider = self.config.finalize()
        self.monitoring_provider = monitoring_provider
        self.provenance_provider = provenance_provider
        return provider


class IotlabConfig(ProviderConfig):
    def __init__(self, data: dict) -> None:
        super().__init__(data)

        self.job_name = self.env.get(JOB_NAME, default.JOB_NAME)
        self.walltime = self.env.get(WALLTIME, default.WALLTIME)
        self.cluster = self.env.get(CLUSTER, default.IOTLAB_CLUSTER)

    def init(self, optimization_id: Optional[int] = None):
        self.job_name = self.opt_job_id(self.job_name, optimization_id)

        self.config = en.IotlabConf.from_settings(
            job_name=self.job_name, walltime=self.walltime
        )

    def config_monitoring(self) -> None:
        """Configure provider config for monitoring"""
        monitoring_conf = self.get_manager_conf(Managers.MONITORING_IOT)
        # FIT Iotlab monitoring is not "standard"
        # hence no monitoring provider = True
        if monitoring_conf:
            self._configure_monitoring(monitoring_conf)

    def _configure_monitoring(self, monitoring_conf: dict) -> None:
        for profile in monitoring_conf[MONITORING_IOT_PROFILES]:
            # period and average existance and compliance validated by schema
            period = profile.get(MONITORING_IOT_PERIOD, default.IOT_PERIOD_VAL)
            average = profile.get(MONITORING_IOT_AVERAGE, default.IOT_AVERAGE_VAL)
            current = profile.get(MONITORING_IOT_CURRENT, False)
            power = profile.get(MONITORING_IOT_POWER, False)
            voltage = profile.get(MONITORING_IOT_VOLTAGE, False)
            self.config.add_profile(
                name=profile[NAME],
                archi=profile[ARCHI],
                consumption=ConsumptionConfiguration(
                    current=current,
                    power=power,
                    voltage=voltage,
                    period=period,
                    average=average,
                ),
            )

    def config_provenance(self) -> None:
        pass

    def config_resources(self) -> None:
        for layer in self.layers:
            for service in layer[SERVICES]:
                roles = self.get_service_roles(layer[NAME], service)
                image = service.get(IMAGE, None)
                profile = service.get(PROFILE, None)
                # TODO: Review this
                if not self.monitoring_provider:
                    self.monitoring_provider = True if PROFILE in service else False
                add_cluster, add_servers = self.check_service_mapping(service)
                if add_servers is not None:
                    self.config.add_machine(
                        roles=roles, hostname=add_servers, image=image, profile=profile
                    )
                else:
                    if add_cluster is None:
                        add_cluster = self.cluster
                    archi = service[ARCHI]
                    quantity = service.get(QUANTITY, default.NODE_QUANTITY)
                    self.config.add_machine(
                        roles=roles,
                        archi=archi,
                        site=add_cluster,
                        number=quantity,
                        image=image,
                        profile=profile,
                    )

    def finalize(self) -> Tuple[en.Iotlab, bool, bool]:
        self.config = self.config.finalize()
        logger.debug(f"Provider conf = {self.config.to_dict()}")
        provider = en.Iotlab(self.config)
        return provider, self.monitoring_provider, self.provenance_provider
