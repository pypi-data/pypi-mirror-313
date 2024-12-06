"""
Main experiment class to manage steps of the experimental workflows:
- Infrastructure
- Networking
- Workflow execution
"""

import subprocess
import time
from pathlib import Path
from typing import Optional
from uuid import UUID

import questionary
import yaml
from enoslib import Host, Roles

import e2clab.constants.default as default
from e2clab.app import App
from e2clab.constants import ConfFiles, Environment, WorkflowTasks
from e2clab.constants.layers_services import (
    LAYERS,
    MONITORING_SERVICE_ROLE,
    MONITORING_SVC,
    MONITORING_SVC_PORT,
    MONITORING_SVC_PROVIDER,
    NAME,
    PROVENANCE_SERVICE_ROLE,
    PROVENANCE_SVC_PORT,
    ROLES_MONITORING,
    SERVICES,
)
from e2clab.errors import E2clabError
from e2clab.infra import Infrastructure
from e2clab.log import config_file_logger, get_logger
from e2clab.network import Network
from e2clab.probe import TaskProbe


class Experiment:
    def __init__(
        self,
        scenario_dir: Path,
        artifacts_dir: Path,
        repeat: Optional[int] = None,
        app_conf_list: list[str] = [],
        optimization_config=None,
        optimization_id: Optional[UUID] = None,
    ) -> None:
        self.id = time.strftime("%Y%m%d-%H%M%S")
        self.scenario_dir = scenario_dir.resolve()
        self.artifacts_dir = artifacts_dir.resolve()

        # 'Deploy' related
        self.app_conf_list = app_conf_list
        self.repeat = repeat

        # 'Optimization' related
        self.optimization_id = optimization_id
        self.optimization_config = optimization_config

        self.logger = get_logger(__name__, ["EXP"])

        # Experiment components
        self.infra: Optional[Infrastructure] = None
        self.net: Optional[Network] = None
        self.app: Optional[App] = None

        # Probing execution timestamp
        self.probe = TaskProbe()

    def __setstate__(self, state):
        """Ran when unpickling"""
        self.__dict__.update(state)
        # re-configure loggers
        config_file_logger(self.experiment_dir)

    def initiate(self) -> None:
        # TODO: THIS DOESNT HAVE TO BE DEFINED HERE OR HAVE THIS VALUE ?
        self.monitoring_remote_working_dir = (
            f"/builds/monitoring-{self.id}-{self.scenario_dir.stem}"
        )
        # FILE USED BY USERS TO DEPLOY THEIR APPLICATIONS
        self.experiment_dir = Path(f"{self.scenario_dir}/{self.id}")
        self.experiment_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Experiment directory is: {self.experiment_dir}")
        # Outputing e2clab logs into experiment dir
        log_file, error_file = config_file_logger(self.experiment_dir)
        self.logger.info(f"Logging file at {log_file}")
        self.logger.info(f"Error file at {error_file}")

        self.layers_services_val_file = (
            self.experiment_dir / default.LAYERS_SERVICES_VALIDATE_FILE
        )

    def infrastructure(self) -> int:
        """
        Deploy experiment infrastructure
        """
        self.logger.info("Deploying experiment inrastructure")

        conf_file = self.scenario_dir / ConfFiles.LAYERS_SERVICES

        # Infrastructure
        self.logger.debug("Init infrastructure")
        self.infra = Infrastructure(conf_file, self.optimization_id)
        self.logger.debug("Preparing infrastructure")
        self.infra.prepare()
        self.logger.debug("Deploying infrastructure")
        roles, networks = self.infra.deploy(
            artifacts_dir=self.artifacts_dir,
            remote_working_dir=self.monitoring_remote_working_dir,
        )
        self.logger.info("Experiment infrastructure deployed")

        self.probe.set_start("infra")

        self.roles = roles
        self.networks = networks

        # Generate Layers Services validate file
        # application_parameters(app_param_dir, self.infra.roles, self.infra.config)
        self._dump_application_parameters()

        return self.id

    def network(self) -> None:
        """
        Deploy experiment network emulation
        """
        if not self.infra:
            raise E2clabError(
                "Cannot deploy a network without a deployed infrastructure"
            )

        self.logger.info("Deploying experiment network")

        conf_file = self.scenario_dir / ConfFiles.NETWORK

        # Network
        self.logger.debug("Init network")
        self.net = Network(conf_file, self.roles, self.networks)
        self.logger.debug("Preparing network")
        self.net.prepare()
        self.logger.debug("Deploying network")
        self.net.deploy()
        self.logger.debug("Validating network")
        self.net.validate(self.experiment_dir)

        self.logger.info("Experiment network deployed")

    def application(self, task: WorkflowTasks, app_conf: Optional[str] = None) -> None:
        """
        Enforce workflow definition
        """
        if not self.infra:
            raise E2clabError("Cannot run a workflow without a deployed infrastructure")

        env_conf = None

        if app_conf:
            env_conf = self.scenario_dir / ConfFiles.WORKFLOW_ENV

        conf_file = self.scenario_dir / ConfFiles.WORKFLOW

        self.app = App(
            config=conf_file,
            experiment_dir=self.experiment_dir,
            scenario_dir=self.scenario_dir,
            artifacts_dir=self.artifacts_dir,
            roles=self.roles,
            all_serv_extra_inf=self.infra.all_serv_extra_inf,
            app_conf=app_conf,
            env_config=env_conf,
            optimization_config=self.optimization_config,
        )

        # Enforce task
        self.logger.info(f"Enforcing workflow:{task.value}")
        self.run_task(task=task, current_repeat=self.repeat)
        self.logger.info(f"Done enforcing workflow:{task.value}")

    def run_task(self, task: WorkflowTasks, current_repeat: Optional[int] = None):
        """Wrapper for application run_task"""
        if not self.app:
            raise E2clabError("Failed initializing App")
        self.probe.set_start(record_name=task.value)
        self.app.run_task(task=task, current_repeat=current_repeat)
        self.probe.set_end(record_name=task.value)

    def finalize(self, app_conf: Optional[str] = None, destroy: bool = False) -> None:
        """
        Finalize experiment
        """
        if not self.infra or not self.app:
            raise E2clabError(
                "Cannot finalize an experiment without "
                "an infrastructure or before running 'workflow'"
            )

        # TODO: find a more elegant way to do this output dir thing
        output_dir = self.experiment_dir
        if app_conf:
            output_dir = self.experiment_dir / app_conf

        self.logger.info("Finalizing experiment")
        self.logger.info("Running workflow 'finalize'")
        self.run_task(WorkflowTasks.FINALIZE, current_repeat=self.repeat)
        self.logger.info("Finalizing layers and services")
        self.infra.finalize(output_dir=output_dir)
        self.logger.info("Done finalizing experiment")

        if destroy:
            self.logger.info("Destroying after successful finish")
            self.destroy()

    def deploy(
        self, duration: int, is_prepare: bool = True, destroy_on_finish: bool = False
    ) -> None:
        """
        Deploy E2Clab experiment
        """

        self.logger.info("Starting experiment deployment")
        self.initiate()
        self.infrastructure()
        self.network()

        self.logger.debug(f"[APPLICATION CONF LIST]: {self.app_conf_list}")

        self.logger.info("Starting experiment deployment")
        if self.app_conf_list:
            for app_conf in self.app_conf_list:
                self.logger.info(f"Running experiment configuration '{app_conf}'")
                is_prepare = self._run_deploy(duration, is_prepare, app_conf)
        else:
            is_prepare = self._run_deploy(duration, is_prepare, None)

        self.logger.info("Done experiment deployment")

        if destroy_on_finish:
            self.logger.info("Destroying after successful deploy")
            self.destroy()

    def _run_deploy(
        self, duration: int, is_prepare: bool, app_conf: Optional[str] = None
    ):
        if is_prepare:
            # No app_conf during prepare stage
            self.application(WorkflowTasks.PREPARE)
            # We prepare our deployment only once
            is_prepare = False
        self.application(WorkflowTasks.LAUNCH, app_conf)

        self.logger.info(f"Waiting for duration: {duration} seconds")
        self.probe.set_start("wait")

        time.sleep(duration)

        self.probe.set_end("wait")
        self.logger.info(f"Stopping experiment after {duration} seconds")

        self.finalize(app_conf=app_conf)
        return is_prepare

    def destroy(self) -> None:
        """
        Release (free) computing resources, e.g. kill G5k oar jobs
        """
        if not self.infra:
            raise E2clabError(
                "Can't destroy an uninstantiated infrastructure."
                "Have you run `e2clab layers_services` ?"
            )
        self.logger.info("Destroying provider computing resource")
        self.infra.destroy()
        self.logger.info("Destroyed computing resources")

        self.probe.set_end("infra")

    def ssh(
        self,
        forward: Optional[bool] = False,
        local_port: Optional[int] = None,
        remote_port: Optional[int] = None,
    ) -> None:
        """Runs a subprocess to ssh to selected remote host"""
        host = self._ask_ssh_host()
        ssh_target = f"{host.user}@{host.address}"
        identity = host.keyfile
        port = host.port
        command = ["ssh", ssh_target]
        # is we want to run ssh tunnelling
        if forward and local_port and remote_port:
            command += ["-NL", f"{local_port}:localhost:{remote_port}"]
        if port is not None:
            command += ["-p", str(port)]
        if identity is not None:
            command += ["-i", str(identity)]
        self.logger.debug(f"SSH COMMAND : {command}")
        try:
            if forward:
                self.logger.info(f"Access localhost:{local_port}")
            else:
                self.logger.info(f"Accessing {host.address}")
            subprocess.run(command)
        except Exception as e:
            self.logger.error(f"Failed to connect: {e}")

    def get_output_dir(self) -> None:
        """Prints experiment directory to stdout"""
        print(self.get_exp_dir())

    def get_exp_id(self) -> str:
        return self.id

    def get_exp_dir(self) -> Path:
        return self.experiment_dir

    # TODO: refactor using managers to return information
    def _dump_application_parameters(self) -> None:
        """
        Generates a file with a list of User-Defined Services to be used by the user in
        the network.yaml and workflow.yaml configuration files.
        """
        user_roles = self._get_filtered_user_roles()

        role_data = {}
        with open(self.layers_services_val_file, "w") as f:
            if MONITORING_SERVICE_ROLE in user_roles:
                yaml.dump(
                    "* * * * * * * Monitoring Service (started during workflow "
                    "'launch' step)",
                    f,
                )
                monitoring_node = user_roles.pop(MONITORING_SERVICE_ROLE)[0].address
                yaml.dump(f"Available at: http://localhost:{MONITORING_SVC_PORT}", f)
                _access = (
                    f"Access from your local machine: "
                    f"ssh -NL {MONITORING_SVC_PORT}:localhost:{MONITORING_SVC_PORT}"
                )
                if (
                    self.infra.config[MONITORING_SVC][MONITORING_SVC_PROVIDER]
                    == Environment.CHAMELEON_CLOUD.value
                ):
                    yaml.dump(f"{_access} cc@<FLOATING_IP>", f)
                else:
                    yaml.dump(f"{_access} {monitoring_node}", f)
                yaml.dump("username: admin / password: admin", f)

            if PROVENANCE_SERVICE_ROLE in user_roles:
                yaml.dump("* * * * * * * Provenance Service", f)
                provenance_node = user_roles.pop(PROVENANCE_SERVICE_ROLE)[0].address
                yaml.dump(f"Available at: http://localhost:{PROVENANCE_SVC_PORT}", f)
                _access = (
                    f"Access from your local machine: "
                    f"ssh -NL {PROVENANCE_SVC_PORT}:localhost:{PROVENANCE_SVC_PORT}"
                )
                yaml.dump(f"{_access} {provenance_node}", f)

            yaml.dump(
                "* * * * * * * Configure network.yaml and workflow.yaml using the "
                "information below!",
                f,
            )

            for layer in self.infra.config[LAYERS]:
                roles = []
                for role in sorted(user_roles):
                    # filter roles per layer name
                    if len(role.split(".")) > 1 and role.split(".")[0] == layer[NAME]:
                        hosts = []
                        for host in user_roles[role]:
                            hosts.append(host.address)
                        roles.append({role: hosts})
                role_data.update({layer[NAME]: roles})

            yaml.dump(role_data, f)

    def _get_filtered_user_roles(self) -> Roles:
        """Returns user-used roles"""
        user_roles = self.roles.copy()
        # remove roles not needed by the users
        if ROLES_MONITORING in user_roles:
            user_roles.pop(ROLES_MONITORING)
        for layer in self.infra.config[LAYERS]:
            for service in layer[SERVICES]:
                if service["_id"] in user_roles:
                    user_roles.pop(service["_id"])
                if service[NAME] in user_roles:
                    user_roles.pop(service[NAME])
        return user_roles

    def _get_ssh_user_roles_data(self) -> dict[str, Roles]:
        user_roles = self._get_filtered_user_roles()
        data = {}
        for layer_name in self.infra.config.get_layer_names():
            roles_layer = Roles({})
            for role in user_roles:
                s = role.split(".")
                if len(s) > 1 and s[0] == layer_name:
                    roles_layer.update({role: user_roles[role]})
            data.update({layer_name: roles_layer})
        return data

    def _ask_ssh_host(self) -> Host:
        """Queries user for host to ssh to

        Returns:
            Host: host to ssh to
        """
        data_ssh_roles = self._get_ssh_user_roles_data()
        self.logger.debug(f"SSH roles: {data_ssh_roles}")

        layer_answer = questionary.select(
            "Select layer to ssh to", choices=data_ssh_roles.keys()
        ).ask()

        roles_answer = questionary.select(
            "Select host to ssh to", choices=data_ssh_roles[layer_answer]
        ).ask()

        host: Host = data_ssh_roles[layer_answer][roles_answer][0]
        return host
