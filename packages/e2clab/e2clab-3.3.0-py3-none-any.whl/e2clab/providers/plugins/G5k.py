from typing import Dict, Optional, Tuple

import enoslib as en
from enoslib.config import config_context
from enoslib.infra.enos_g5k.g5k_api_utils import get_cluster_site
from enoslib.objects import Host

import e2clab.constants.default as default
from e2clab.config import InfrastructureConfig
from e2clab.constants.layers_services import (
    CLUSTER,
    ENV_NAME,
    ENVIRONMENT,
    FIREWALL_RULES,
    G5K,
    IPV,
    JOB_NAME,
    JOB_TYPE,
    KEY_NAME,
    MONITOR,
    MONITORING_NETWORK_ROLE,
    MONITORING_SERVICE_ROLE,
    MONITORING_SVC,
    MONITORING_SVC_NETWORK,
    MONITORING_SVC_NETWORK_PRIVATE,
    NAME,
    PORTS,
    PROVENANCE_SERVICE_ROLE,
    PROVENANCE_SVC,
    QUANTITY,
    RESERVATION,
    ROLES,
    ROLES_MONITORING,
    SERVERS,
    SERVICES,
    WALLTIME,
)
from e2clab.log import get_logger
from e2clab.managers import Managers
from e2clab.providers import Provider, ProviderConfig

KAVLAN_GLOBAL = "kavlan-global"
KAVLAN = "kavlan"

logger = get_logger(__name__, ["G5K"])


class G5kConfig(ProviderConfig):
    def __init__(self, data: dict) -> None:
        super().__init__(data)

        # Parsing data, define default values
        self.job_name = self.env.get(JOB_NAME, default.JOB_NAME)
        self.walltime = self.env.get(WALLTIME, default.WALLTIME)
        self.reservation = self.env.get(RESERVATION, None)
        self.job_type = self.env.get(JOB_TYPE, default.JOB_TYPE)
        self.env_name = self.env.get(ENV_NAME, None)
        self.cluster = self.env.get(CLUSTER, None)
        self.keyfile = self.env.get(KEY_NAME, default.SSH_KEYFILE)
        self.monitor = self.env.get(MONITOR, None)

    def init(self, optimization_id: Optional[int] = None) -> None:
        """Initialize G5k configuration

        Args:
            optimization_id (Optional[int], optional): Optimization_ID.
                Defaults to None.
        """
        self.check_cluster()

        self.job_name = self.opt_job_id(self.job_name, optimization_id)

        self.config = en.G5kConf.from_settings(
            job_type=self.job_type,
            env_name=self.env_name,
            job_name=self.job_name,
            reservation=self.reservation,
            walltime=self.walltime,
            key=self.keyfile,
            monitor=self.monitor,
        )
        self.cluster_list = self._search_clusters_at_service_level()
        self.prod_network = self._create_production_network_for_clusters(
            self.cluster_list
        )

        for network in self.prod_network.values():
            self.config.add_network_conf(network)

    def config_provenance(self) -> None:
        """Configure provenance service setup

        Args:
            prod_network (dict): production network
        """
        provenance_config = self.get_manager_conf(Managers.PROVENANCE)
        if provenance_config:
            self.provenance_provider = True
            self._configure_provenance(provenance_config)

    def config_monitoring(self) -> None:
        """Configure Monitoring"""
        clusters_to_monitor = self._check_monitoring_request()
        monitoring_config = self.get_manager_conf(Managers.MONITORING)
        self.monit_private_net = False
        if monitoring_config:
            self.monitoring_provider = True
            self._configure_monitoring(monitoring_config, clusters_to_monitor)

    def config_resources(self) -> None:
        """Add computing resources for services"""
        for layer in self.layers:
            for service in layer[SERVICES]:
                add_cluser, add_servers = self.check_service_mapping(service)
                if add_cluser is None:
                    add_cluser = self.cluster

                roles = self.get_service_roles(layer[NAME], service)

                if add_servers:
                    for cluster, servers in self._separate_servers_per_cluster(
                        add_servers
                    ).items():
                        primary_network = self.prod_network[get_cluster_site(cluster)]
                        secondary_networks = self._get_secondary_networks()
                        self.config.add_machine(
                            roles=roles,
                            servers=servers,
                            primary_network=primary_network,
                            secondary_networks=secondary_networks,
                        )
                else:
                    nodes = service.get(QUANTITY, default.NODE_QUANTITY)
                    primary_network = self.prod_network[get_cluster_site(add_cluser)]
                    secondary_networks = self._get_secondary_networks()
                    self.config.add_machine(
                        roles=roles,
                        cluster=add_cluser,
                        nodes=nodes,
                        primary_network=primary_network,
                        secondary_networks=secondary_networks,
                    )

    def finalize(self) -> Tuple[en.G5k, bool, bool]:
        self.config = self.config.finalize()
        logger.debug(f"Provider conf = {self.config.to_dict()}")
        provider = en.G5k(self.config)
        return provider, self.monitoring_provider, self.provenance_provider

    def _check_monitoring_request(self) -> list[str]:
        """Get clusters to monitor

        Returns:
            list[str]: list of clusters
        """
        clusters_to_monitor: set[str] = set()
        for layer in self.layers:
            for service in layer[SERVICES]:
                service_roles = service.get(ROLES, [])
                if ROLES_MONITORING in service_roles:
                    roles = self._get_service_clusters(service)
                    clusters_to_monitor = clusters_to_monitor.union(set(roles))
        return list(clusters_to_monitor)

    def _configure_monitoring(
        self, monitoring_config: dict, clusters_to_monitor: list[str]
    ) -> None:
        """Parsing and configuring monitoring function

        Args:
            monitoring_config (dict): monitoring configuration
        """

        # Monitoring network
        # 1 monitoring network[kavlan,kavlan-global]
        # 1 production network
        # TODO: check schema and add a default value ?
        if monitoring_config[MONITORING_SVC_NETWORK] == MONITORING_SVC_NETWORK_PRIVATE:
            self.monit_private_net = True

        # TODO: Enforce to have one of those in the schema
        monitoring_cluster = monitoring_config.get(CLUSTER, None)
        monitoring_servers = monitoring_config.get(SERVERS, None)
        if monitoring_cluster is None and monitoring_servers is None:
            raise KeyError("No cluster or servers in monitoring ?")

        # Priority to servers definition
        if monitoring_servers:
            monitoring_servers = [monitoring_servers[0]]
            monitoring_cluster = self._get_clusters_from_servers(monitoring_servers)[0]
        monitoring_site = get_cluster_site(monitoring_cluster)

        if self.monit_private_net and len(clusters_to_monitor) > 0:
            self.monit_network = self._create_monitoring_network(
                monitoring_cluster, clusters_to_monitor
            )
            self.config.add_network_conf(self.monit_network)
        # Create a production network (type="prod")
        if monitoring_site not in self.prod_network:
            self.prod_network.update(
                self._create_production_network_for_clusters([monitoring_cluster])
            )
            self.config.add_network_conf(self.prod_network[monitoring_site])

        roles = [G5K, MONITORING_SERVICE_ROLE]
        primary_network = self.prod_network[monitoring_site]
        secondary_networks = [self.monit_network] if self.monit_private_net else None
        # Add resources
        if monitoring_servers:
            # SERVERS defined case
            self.config.add_machine(
                roles=roles,
                servers=monitoring_servers,
                primary_network=primary_network,
                secondary_networks=secondary_networks,
            )
        else:
            # CLUSTER defined case
            self.config.add_machine(
                roles=roles,
                cluster=monitoring_cluster,
                primary_network=primary_network,
                secondary_networks=secondary_networks,
                nodes=1,
            )

    def _configure_provenance(self, provenance_config: dict) -> None:
        """Parse configuration and add necessary machines

        Args:
            provenance_config (dict): provenance configuration
        """
        _provenance_cluster = provenance_config.get(CLUSTER, None)
        if not _provenance_cluster:
            # SERVERS exists if not CLUSTER per schema 'provenance_schema'
            _provenance_servers = [provenance_config[SERVERS][0]]
            _provenance_cluster = self._get_clusters_from_servers(_provenance_servers)[
                0
            ]

        # Manage network
        cluster_provenance = get_cluster_site(_provenance_cluster)
        if cluster_provenance not in self.prod_network:
            self.prod_network.update(
                self._create_production_network_for_clusters([_provenance_cluster])
            )
            self.config.add_network_conf(self.prod_network[cluster_provenance])

        _primary_prod_network = self.prod_network[cluster_provenance]
        # Priority to the SERVERS
        if SERVERS in provenance_config:
            self.config.add_machine(
                roles=[G5K, PROVENANCE_SERVICE_ROLE],
                servers=_provenance_servers,
                primary_network=_primary_prod_network,
            )
        else:
            self.config.add_machine(
                roles=[G5K, PROVENANCE_SERVICE_ROLE],
                cluster=_provenance_cluster,
                primary_network=_primary_prod_network,
            )

    def _get_secondary_networks(self):
        if self.monit_private_net:
            return [self.monit_network]
        else:
            return None

    def _separate_servers_per_cluster(self, servers: list[str]) -> dict[str, list[str]]:
        servers_per_cluster: dict[str, list[str]] = {}
        clusters = self._get_clusters_from_servers(servers)
        for cluster in clusters:
            servers_per_cluster.update({cluster: []})
            for server in servers:
                if cluster in server:
                    servers_per_cluster[cluster].append(server)
        return servers_per_cluster

    def _create_monitoring_network(
        self, monitoring_cluster: str, clusters_to_monitor: list[str]
    ) -> en.G5kNetworkConf:
        """Configure monitoring network

        Args:
            monitoring_cluster (str): cluster to host monitoring manager
            clusters_to_monitor (list[str]): clusters to monitor

        Returns:
            en.G5kNetworkConf: network configuration
        """
        _clusters = set(clusters_to_monitor)
        _clusters.add(monitoring_cluster)
        monit_network_clusters = list(_clusters)
        sites = self._get_sites_from_clusters(monit_network_clusters)
        main_site = get_cluster_site(monitoring_cluster)
        if len(sites) > 1:
            network_type = KAVLAN_GLOBAL
        else:
            network_type = KAVLAN
        id = f"monitoring_network_{main_site}"
        return en.G5kNetworkConf(
            id=id, type=network_type, roles=[MONITORING_NETWORK_ROLE], site=main_site
        )

    @staticmethod
    def _create_production_network_for_clusters(
        clusters: list[str],
    ) -> Dict[str, en.G5kClusterConf]:
        """Creates site-level networks for clusters."""
        networks = {}
        for cluster in clusters:
            _site = get_cluster_site(cluster)
            if _site not in networks:
                networks[_site] = en.G5kNetworkConf(
                    id=f"network_{_site}",
                    type="prod",
                    roles=[f"my_{_site}_network"],
                    site=_site,
                )
        return networks

    def _search_clusters_at_service_level(self):
        """Searches the clusters a Service belongs to"""
        clusters = set([])
        for layer in self.layers:
            for service in layer[SERVICES]:
                service_clusters = set(self._get_service_clusters(service))
                clusters = clusters.union(service_clusters)
        return list(clusters)

    def _get_service_clusters(self, service_conf: dict) -> list[str]:
        """Get G5k clusters associated with service

        Args:
            service_conf (dict): Service configuration

        Returns:
            list[str]: list of clusters
        """
        clusters = []
        s_cluster = service_conf.get(CLUSTER, None)
        s_servers = service_conf.get(SERVERS, None)
        if s_servers:
            server_clusers = self._get_clusters_from_servers(s_servers)
            for c in server_clusers:
                if c not in clusters:
                    clusters.append(c)
        elif s_cluster is not None and s_cluster not in clusters:
            clusters.append(s_cluster)
        elif self.cluster and self.cluster not in clusters:
            clusters.append(self.cluster)
        # TODO: check
        assert len(clusters) != 0
        return clusters

    @staticmethod
    def _get_sites_from_clusters(clusters: list[str]) -> list[str]:
        """return list of sites from clusters

        Args:
            clusters (list[str]): list of clusters

        Returns:
            list[str]: list of sites
        """
        sites = set()
        for cluster in clusters:
            sites.add(get_cluster_site(cluster))
        return list(sites)


class G5k(Provider):
    """
    The provider to use when deploying on Grid'5000.
    """

    def __init__(
        self, infra_config: InfrastructureConfig, optimization_id: Optional[int] = None
    ):
        super().__init__(infra_config, optimization_id)
        # Cater data to the providers specifications.
        self.infra_config.refine_to_environment(G5K)
        self.config = G5kConfig(self.infra_config)

    def init(self):
        """
        Take ownership over some Grid'5000 resources (compute and networks).
        :return: roles, networks
        """
        with config_context(g5k_cache=False):
            provider = self._provider_g5k(self.optimization_id)

        self.en_provider = provider

        roles, networks = provider.init()
        en.wait_for(roles)

        # TODO: Rewrite this
        if (
            MONITORING_SVC in self.infra_config
            and IPV in self.infra_config[MONITORING_SVC]
            and self.infra_config[MONITORING_SVC][IPV] == 6
        ) or (
            PROVENANCE_SVC in self.infra_config
            and IPV in self.infra_config[PROVENANCE_SVC]
            and self.infra_config[PROVENANCE_SVC][IPV] == 6
        ):
            roles = en.sync_info(roles, networks)
            _hosts = []
            for h in roles[G5K]:
                _hosts.append(h)
            self.__enable_ipv6_network(_hosts)

        roles = en.sync_info(roles, networks)

        if FIREWALL_RULES in self.infra_config[ENVIRONMENT]:
            self.__apply_firewall_rules(provider, roles)

        if None in (roles, networks):
            raise ValueError(f"Failed to get resources from: {G5K}.")

        self.roles = roles
        self.networks = networks
        self.log_roles_networks(G5K)

        return roles, networks

    def destroy(self):
        self.en_provider.destroy()

    def get_sites(self) -> list[str]:
        return self.en_provider.provider_conf.sites

    def get_jobs(self):
        return self.en_provider.jobs

    def _provider_g5k(self, optimization_id: Optional[int] = None) -> en.G5k:
        self.config.init(optimization_id)
        self.config.config_provenance()
        self.config.config_monitoring()
        self.config.config_resources()
        provider, monitoring_provider, provenance_provider = self.config.finalize()
        self.monitoring_provider = monitoring_provider
        self.provenance_provider = provenance_provider
        return provider

    def __apply_firewall_rules(self, provider, roles):
        """
        Reconfigurable firewall on G5K allows you to open some ports of some of your
        Services.
        Allows connections from other environments (e.g., FIT IoT, Chameleon, etc.)
        to G5K.
        """
        try:
            for fw_rule in self.infra_config[ENVIRONMENT][FIREWALL_RULES]:
                svcs = []
                for scv in fw_rule[SERVICES]:
                    svcs += roles[scv]
                try:
                    provider.fw_create(
                        hosts=svcs, port=fw_rule[PORTS], src_addr=None, proto="tcp+udp"
                    )
                except Exception as e:
                    if "already exists" not in str(e):
                        raise e
        except Exception as e:
            raise e

    def __enable_ipv6_network(self, _hosts):
        for _host in _hosts:
            for routable_nic in self.get_host_routable_nic(_host):
                en.run(f"dhclient -6 {routable_nic}", roles=_host)
                break

    @staticmethod
    def get_host_routable_nic(host: Host):
        routable_nic = []
        for net_device in host.net_devices:
            for _address in net_device.addresses:
                if _address.network and _address.ip.version in [4]:
                    routable_nic.append(str(net_device.name))
                    break
        return routable_nic
