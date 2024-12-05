from pathlib import Path
from typing import Iterable, Optional

import enoslib as en
from enoslib.api import run_ansible
from enoslib.objects import Host, Roles
from enoslib.service.service import Service

from e2clab.log import get_logger

logger = get_logger(__name__, ["FLOWCEPT"])

FILE_PATH = Path(__file__)
PLAYBOOK = "flowcept.yml"

FLOWCEPT_REPO = "https://github.com/ORNL/flowcept.git"

FLOWCEPT_MONGO = "flowcept_mongo"
FLOWCEPT_REDIS = "flowcept_redis"

DEFAULT_BACKUP = Path("flowcept_output")


class Flowcept(Service):
    def __init__(
        self,
        host: Host,
        agent: Iterable[Host],
        agent_flavor: Optional[str] = None,
        backup_dir: Optional[Path] = None,
        extra_vars: Optional[dict] = None,
    ):
        self.host = host
        self.agent = agent
        self.extra_vars = extra_vars if extra_vars else {}

        if agent_flavor:
            self.agent_flavor = f"[{agent_flavor}]"
        else:
            self.agent_flavor = ""
        self.backup_dir = backup_dir if backup_dir is not None else DEFAULT_BACKUP

        self._roles = Roles()
        self._roles.update(flowcept_host=[self.host], flowcept_agent=agent)

        self._playbook = FILE_PATH.parent / PLAYBOOK
        self.extra_vars.update(
            {
                "redis_name": FLOWCEPT_REDIS,
                "mongo_name": FLOWCEPT_MONGO,
                "flowcept_repo": FLOWCEPT_REPO,
                "remote_working_dir": "/tmp/data",
            }
        )

    def deploy(self):
        # Install Docker for flowcept host
        registry_opts = dict(type="external", ip="docker-cache.grid5000.fr", port=80)
        d = en.Docker(
            agent=[self.host],
            registry_opts=registry_opts,
            bind_var_docker="/tmp/docker",
        )
        d.deploy()

        extra_vars = {
            "e2c_action": "deploy",
            "host_address": self.host.address,
            "agent_flavor": "[dask]",
        }
        extra_vars.update(self.extra_vars)
        run_ansible([self._playbook], extra_vars=extra_vars, roles=self._roles)

    def backup(self, backup_dir: Optional[Path] = None):
        if backup_dir:
            self.backup_dir = backup_dir
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        print(str(self.backup_dir))
        self.backup_dir = self.backup_dir.resolve()
        print(str(self.backup_dir))

        extra_vars = {"e2c_action": "backup", "backup_dir": str(self.backup_dir)}
        extra_vars.update(self.extra_vars)
        run_ansible(
            [self._playbook],
            extra_vars=extra_vars,
            # roles=Roles(flowcept_host=self._roles["flowcept_host"]),
            roles=self._roles,
        )

    def destroy(self):
        extra_vars = {"e2c_action": "destroy"}
        extra_vars.update(extra_vars)
        run_ansible([self._playbook], extra_vars=extra_vars, roles=self._roles)
