"""
This file defines all functions and utilities needded to enforce
the 'networking' of our experiment
"""

from pathlib import Path
from typing import Iterable

import enoslib as en
from enoslib.infra.enos_chameleonedge.objects import ChameleonDevice

from e2clab.config import NetworkConfig
from e2clab.constants.default import NET_VALIDATE_DIR
from e2clab.constants.layers_services import MONITORING_NETWORK_ROLE
from e2clab.constants.network import DELAY, DST, LOSS, RATE, SRC, SYMMETRIC
from e2clab.log import get_logger
from e2clab.utils import load_yaml_file


class Network:
    """
    Enforce network definition
    a.k.a. Network manager
    """

    def __init__(self, config: Path, roles, networks) -> None:
        """Create a new experiment network emulation

        Args:
            config (Path): Path to 'network.yaml' configuration file
            roles (en.Roles): EnOSlib Roles associated with the experiment
            networks (en.Networks): EnOSlib Networks associated with the experiment
        """
        self.logger = get_logger(__name__, ["NET"])
        self.config = self._load_config(config)
        self.roles = roles
        self.networks = networks

    def _load_config(self, config_path: Path) -> NetworkConfig:
        c = load_yaml_file(config_path)
        return NetworkConfig(c)

    # User Methods

    def prepare(self) -> None:
        # TODO: check that source and dest are correctly setup
        """Prepare network emulation"""
        self.networks_to_em = self._get_filtered_networks()

        self.logger.debug(f"[NETWORK TO EMMULATE] {self.networks_to_em}")

    def deploy(self) -> None:
        """Deploy configured network emulation"""
        self.netems = {}

        networks_confs = self.config.get_networks()
        if networks_confs is None:
            self.logger.info("No network emulation to deploy")
            return

        self.logger.info("Deploying network emulation")

        # TODO: Maybe optimize by re-using the netem instances and building constraints
        for net_config in networks_confs:
            if self._check_edgeChameleonDevice(net_config):
                netem = self._configure_netem(net_config)
            else:
                netem = self._configure_netemhtb(net_config, self.networks_to_em)

            self.logger.debug(f"[NETEM CONFIG] {net_config}")
            self.logger.debug(f"[NETEM] {netem}")

            netem.deploy()

            key = self.config.get_netem_key(net_config)
            self.netems.update({key: netem})

            self.logger.info(f"Network emulation {key} deployed")
        self.logger.info("Done deploying network emulations")

    def validate(self, experiment_dir: Path) -> None:
        """Validate network emmulation deployment

        Args:
            experiment_dir (Path): Path to output validation file
        """
        if self.netems:
            self.logger.info(
                f"Network emulation validation files sotred in {experiment_dir}"
            )
        for key, netem in self.netems.items():
            # Creating dir to store validation files
            netem_validate_dir: Path = experiment_dir / NET_VALIDATE_DIR / key
            netem_validate_dir.mkdir(parents=True, exist_ok=True)

            netem.validate(output_dir=netem_validate_dir)
            self.logger.debug(f"Validated netem {key} in {netem_validate_dir}")

    def destroy(self):
        raise NotImplementedError

    # End User methods

    def _get_filtered_networks(self) -> Iterable[en.Network]:
        networks_to_em = []
        for key, value in self.networks.items():
            # TODO: Mayner also add provenance networks ?
            if key not in [MONITORING_NETWORK_ROLE]:
                networks_to_em.extend(value)
        return networks_to_em

    def _configure_netem(self, net_config: dict) -> en.Netem:
        netem = en.Netem()

        command = ""
        if DELAY in net_config:
            command += f"{DELAY} {net_config[DELAY]} "
        if RATE in net_config:
            command += f"{RATE} {net_config[RATE]} "
        if LOSS in net_config:
            command += f"{LOSS} {net_config[LOSS]} "
        netem = en.Netem()
        netem.add_constraints(
            command,
            en.get_hosts(roles=self.roles, pattern_hosts=net_config[SRC]),
            symmetric=False,
        )
        return netem

    def _configure_netemhtb(
        self, net_config: dict, networks_to_em: Iterable[en.Network]
    ) -> en.NetemHTB:
        netem = en.NetemHTB()

        sym = net_config.get(SYMMETRIC, False)
        delay = net_config.get(DELAY, "")
        rate = net_config.get(RATE, "")
        loss = net_config.get(LOSS, None)

        src = en.get_hosts(roles=self.roles, pattern_hosts=net_config[SRC])
        dest = en.get_hosts(roles=self.roles, pattern_hosts=net_config[DST])

        netem.add_constraints(
            src=src,
            dest=dest,
            delay=delay,
            rate=rate,
            loss=loss,
            symmetric=sym,
            networks=networks_to_em,
        )
        return netem

    def _check_edgeChameleonDevice(self, net_config) -> bool:
        hosts = self.roles[net_config[DST]]
        # hosts = en.get_hosts(roles=self.roles, pattern_hosts=net_config[DST])
        for host in hosts:
            if isinstance(host, ChameleonDevice):
                self.logger.debug(f"Network ChameleonDevice: {host}")
                return True
        return False
