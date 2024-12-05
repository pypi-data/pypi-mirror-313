"""
Monitoring manager module
"""

from enum import Enum
from ipaddress import IPv4Network, IPv6Network
from pathlib import Path
from typing import Optional

from enoslib import Dstat, TIGMonitoring, TPGMonitoring

import e2clab.constants.default as default

from ..constants import SUPPORTED_ENVIRONMENTS, Environment
from ..constants.layers_services import (
    CLUSTER,
    DSTAT_OPTIONS,
    IPV,
    IPV_VERSIONS,
    MONITORING_NETWORK_ROLE,
    MONITORING_SERVICE_ROLE,
    MONITORING_SVC,
    MONITORING_SVC_AGENT_CONF,
    MONITORING_SVC_DSTAT,
    MONITORING_SVC_NETWORK,
    MONITORING_SVC_NETWORK_PRIVATE,
    MONITORING_SVC_NETWORK_SHARED,
    MONITORING_SVC_PORT,
    MONITORING_SVC_PROVIDER,
    MONITORING_SVC_TIG,
    MONITORING_SVC_TPG,
    MONITORING_SVC_TYPE,
    ROLES_MONITORING,
    SERVERS,
)
from ..log import get_logger
from .manager import Manager


class MonitoringType(Enum):
    TPG = TPGMonitoring
    TIG = TIGMonitoring
    DSTAT = Dstat


class MonitoringManager(Manager):
    """
    Monitoring manager class
    """

    logger = get_logger(__name__, ["MONITORING"])

    SCHEMA = {
        "description": "Definition of the monitoring capabilities",
        "type": "object",
        "properties": {
            MONITORING_SVC_TYPE: {
                "description": "Type of monitoring deployed on experiment",
                "type": "string",
                "enum": [
                    MONITORING_SVC_DSTAT,
                    MONITORING_SVC_TPG,
                    MONITORING_SVC_TIG,
                ],
            },
            MONITORING_SVC_PROVIDER: {
                "description": "Dedicated machine hosting InfluxDB and Grafana",
                "type": "string",
                "enum": SUPPORTED_ENVIRONMENTS,
            },
            CLUSTER: {
                "description": "Cluster on which to deploy the machine",
                "type": "string",
            },
            SERVERS: {
                "description": (
                    f"Optional if {CLUSTER} defined. "
                    "Machine on which to deploy the machine"
                ),
                "type": "array",
            },
            MONITORING_SVC_NETWORK: {
                "description": (
                    "Define network for the monitoring service. "
                    # "'public' -> a new network is created' "
                    # "'private' -> 2 NICs is needed on the server."
                ),
                "type": "string",
                "enum": [
                    MONITORING_SVC_NETWORK_SHARED,
                    MONITORING_SVC_NETWORK_PRIVATE,
                ],
            },
            MONITORING_SVC_AGENT_CONF: {
                "description": "Config file in 'artifacts_dir' for the monitor agent",
                "type": "string",
            },
            DSTAT_OPTIONS: {
                "description": "Dstat monitoring options",
                "type": "string",
                "default": default.DSTAT_OPTS,
            },
            IPV: {
                "description": "Type of network the monitoring provider will use.",
                "type": "number",
                "enum": IPV_VERSIONS,
            },
        },
        "required": [MONITORING_SVC_TYPE],  # , MONITORING_SVC_PROVIDER],
    }
    CONFIG_KEY = MONITORING_SVC
    SERVICE_ROLE = MONITORING_SERVICE_ROLE
    ROLE = ROLES_MONITORING

    def create_service(self):
        filtered_nets = self._get_nets(self.networks, IPv6Network)
        if not filtered_nets:
            filtered_nets = self._get_nets(self.networks, IPv4Network)

        if MONITORING_NETWORK_ROLE in self.networks.keys():
            monitor_networks = self.networks[MONITORING_NETWORK_ROLE]
        else:
            monitor_networks = filtered_nets
        monitoring_type = self._get_monitoring_type()
        if monitoring_type == MonitoringType.DSTAT:
            self.logger.debug("Monitoring type : DSTAT")
            monit = monitoring_type.value(
                nodes=self.agent, options=self._get_dstat_options()
            )
        elif monitoring_type == MonitoringType.TIG:
            self.logger.debug("Monitoring type : TIG")
            agent_conf = self._get_agent_conf()
            monit = monitoring_type.value(
                collector=self.host,
                ui=self.host,
                agent=self.agent,
                remote_working_dir=self.meta["remote_working_dir"],
                networks=monitor_networks,
                agent_conf=agent_conf,
            )
        elif monitoring_type == MonitoringType.TPG:
            self.logger.debug("Monitoring type : TPG")
            monit = monitoring_type.value(
                collector=self.host,
                ui=self.host,
                agent=self.agent,
                remote_working_dir=self.meta["remote_working_dir"],
                networks=monitor_networks,
            )
        return monit

    @property
    def schema(self):
        return self.SCHEMA

    @property
    def config_key(self):
        return self.CONFIG_KEY

    @property
    def service_role(self):
        return self.SERVICE_ROLE

    @property
    def role(self):
        return self.ROLE

    def _deploy(self):
        self.logger.info("Deploying...")
        self.service.deploy()
        self.logger.info("Done deploying")

    def _backup(self, output_dir: Path):
        monit_output_dir = output_dir / default.MONITORING_DATA
        self.logger.info(f"Backing up monitoring data in {monit_output_dir}...")
        self.service.backup(backup_dir=monit_output_dir)
        self.logger.info("Backup done")

    def _destroy(self):
        self.logger.info("Destroying...")
        self.service.destroy()
        self.logger.info("Done destroying")

    def get_environment(self) -> Optional[Environment]:
        provider = self.config.get(MONITORING_SVC_PROVIDER)
        if provider:
            return Environment(provider)
        else:
            return None

    def get_extra_info(self) -> dict:
        """Returns monitoring information

        Returns:
            Tuple[str, dict]: monitoring_type, monitoring_extra_info
        """
        monitoring_extra_info = {}
        _monitoring_type = self._get_monitoring_type()
        if None not in (self.host, self.agent, self.networks):
            if _monitoring_type in (
                MonitoringType.TIG,
                MonitoringType.TPG,
            ):
                ui_address = self.host.address
                monitoring_extra_info = {
                    MONITORING_SERVICE_ROLE: {
                        "__address__": f"{ui_address}",
                        "url": f"http://{ui_address}:{MONITORING_SVC_PORT}",
                    }
                }

        return monitoring_extra_info

    def _get_monitoring_type(self) -> MonitoringType:
        # See schema for input format
        type: str = self.config.get(MONITORING_SVC_TYPE)
        return MonitoringType[type.upper()]

    def _get_dstat_options(self) -> str:
        try:
            opt = self.config[DSTAT_OPTIONS]
        except KeyError:
            self.logger.info(f"DSTAT options defaulting to: {default.DSTAT_OPTS}")
            return default.DSTAT_OPTS
        return str(opt)

    def _get_monitoring_agent_conf(self) -> Optional[str]:
        return self.config.get(MONITORING_SVC_AGENT_CONF, None)

    def _get_agent_conf(self) -> Optional[Path]:
        agent_conf = None
        agent_conf_filename = self._get_monitoring_agent_conf()
        if agent_conf_filename:
            agent_conf_file = self.artifacts_dir / agent_conf_filename
            if agent_conf_file.exists():
                agent_conf = agent_conf_file
            else:
                self.logger.warning(
                    f"Monitoring agent conf {agent_conf_file} does not exist"
                )

        return agent_conf

    def _get_nets(self, networks, net_type):
        """Aux method to filter networs from roles"""
        return [
            n
            for net_list in networks.values()
            for n in net_list
            if isinstance(n.network, net_type)
        ]
