from pathlib import Path
from typing import Iterable, Optional

import enoslib as en
from enoslib.objects import Host
from enoslib.service.service import Service

from e2clab.constants.layers_services import DFA_CONTAINER_NAME, PROVENANCE_SVC_PORT
from e2clab.log import get_logger

logger = get_logger(__name__, ["PROVENANCE"])


class Provenance(Service):
    def __init__(
        self, host: Host, agent: Iterable[Host], dataflow_spec: str, parallelism: int
    ):
        self.host = host
        self.dataflow_spec = dataflow_spec
        self.agent = agent
        self.parallelism = parallelism

    def deploy(self):
        """
        Deploys the provenance stack:
            dfanalyzer container + mqtt-sn broker + translator
        and prepare agents
        """
        # install docker
        logger.debug(f"Provenance host type : {type(self.host)}")
        registry_opts = dict(type="external", ip="docker-cache.grid5000.fr", port=80)
        d = en.Docker(
            agent=[self.host],
            registry_opts=registry_opts,
            bind_var_docker="/tmp/docker",
        )
        d.deploy()
        # PROVENANCE SERVICE
        _is_ipv6 = False
        _ip = en.run(
            "ip -6 addr show scope global | awk '/inet6/{print $2}'", roles=self.host
        )[0].stdout
        _is_ipv6 = True if "/" in _ip else False
        if not _is_ipv6:
            _ip = en.run(
                "ip -4 addr show scope global | awk '/inet/{print $2}'", roles=self.host
            )[0].stdout
        provenance_service_ip_address = _ip.split("/")[0] if "/" in _ip else None

        parent_dir = Path(__file__).parent
        with en.actions(roles=self.host) as a:
            # DfAnalyzer container
            a.docker_container(
                name=DFA_CONTAINER_NAME,
                image="vitorss/dataflow_analyzer",
                restart="yes",
                restart_policy="always",
                published_ports=f"{PROVENANCE_SVC_PORT}:{PROVENANCE_SVC_PORT}",
                command="bash -c "
                "'cd dfanalyzer/applications/dfanalyzer/ && "
                "./start-dfanalyzer.sh'",
            )
            # install MQTT-SN broker
            a.git(
                repo="https://github.com/eclipse/mosquitto.rsmb.git",
                dest="~/mosquitto.rsmb/",
                force=True,
            )
            a.shell("cd ~/mosquitto.rsmb/rsmb/src/ && make")
            # install MQTT-SN client
            a.git(
                repo="https://github.com/luanguimaraesla/mqttsn.git",
                dest="~/mqttsn/",
                force=True,
            )
            a.shell("pip3 install -U -e mqttsn/")
            # install DfAnalyzer python lib
            a.git(
                repo="https://gitlab.com/ssvitor/dataflow_analyzer.git",
                dest="~/dataflow_analyzer/",
                force=True,
            )
            a.shell(
                "cp -rf dataflow_analyzer/library/dfa-lib-python . "
                "&& rm -rf dataflow_analyzer/"
            )
            a.shell("pip3 install -e dfa-lib-python/")
            # Enforce the dataflow file provided by users
            a.copy(src=self.dataflow_spec, dest="/tmp/dataflow-specification.py")
            a.shell(
                "export DFA_URL=http://localhost:22000 && "
                "python /tmp/dataflow-specification.py &"
            )
            # Start MQTT-SN broker
            a.copy(
                src=f"{parent_dir}/config.conf",
                dest="~/mosquitto.rsmb/rsmb/src/config.conf",
            )
            a.shell(
                chdir="~/mosquitto.rsmb/rsmb/src/", cmd="./broker_mqtts config.conf &"
            )
            if _is_ipv6:
                a.copy(
                    src=f"{parent_dir}/client_mqttsn_v6.py",
                    dest="~/mqttsn/src/mqttsn/client.py",
                )
            # Start translator
            a.copy(src=f"{parent_dir}/translator.py", dest="/tmp/translator.py")
            # parallelize translator
            for p in range(1, self.parallelism + 1):
                a.shell(
                    f"nohup python3 /tmp/translator.py "
                    f"--topic_id {p} --log /tmp/translator-{p}.log &"
                )

        # PROVENANCE AGENTS
        with en.actions(roles=self.agent) as a:
            # install MQTT-SN client
            a.git(
                repo="https://github.com/luanguimaraesla/mqttsn.git",
                dest="~/mqttsn/",
                force=True,
            )
            a.shell("pip3 install -U -e mqttsn/")
            # install ProvLight python lib
            a.git(
                repo="https://gitlab.inria.fr/provlight/provlight",
                dest="~/provlight/",
                force=True,
            )
            a.shell("pip3 install -e provlight/")
            if _is_ipv6:
                a.copy(
                    src=f"{parent_dir}/client_mqttsn_v6.py",
                    dest="~/mqttsn/src/mqttsn/client.py",
                )
            a.shell(
                f"echo 'export PROVLIGHT_SERVER_URL={provenance_service_ip_address}' "
                f">> ~/.bashrc"
            )
        # parallelize broker topic (roundrobin on clients)
        _topic = 1
        for h in self.agent:
            en.run(
                f"echo 'export PROVLIGHT_SERVER_TOPIC={_topic}' >> ~/.bashrc", roles=h
            )
            _topic = 1 if _topic == self.parallelism else _topic + 1

    def backup(self, backup_dir: Optional[str] = None):
        """
        Dumps provenance database.
        """
        with en.actions(roles=self.host) as a:
            a.shell(
                "docker exec -it dfanalyzer msqldump --database=dataflow_analyzer "
                ">/tmp/provenance_database.sql"
            )
            a.fetch(
                src="/tmp/provenance_database.sql",
                dest=backup_dir,
                validate_checksum="no",
            )
            for p in range(1, self.parallelism + 1):
                a.fetch(src=f"/tmp/translator-{p}.log", dest=backup_dir)

    def destroy(self):
        """
        Destroys the provenance stack:
            dfanalyzer container + mqtt-sn broker + translator
        """
        with en.actions(roles=self.host) as a:
            a.shell(
                f"docker container stop {DFA_CONTAINER_NAME} && "
                f"docker container rm {DFA_CONTAINER_NAME}"
            )
            a.shell(
                "kill -9 `ps -ef | grep -v grep | grep -w translator.py | "
                "awk '{print $2}'`"
            )
            a.shell("killall broker_mqtts")
