"""
This file defines all functions and utilities needded to enforce the 'workflow'
of our experiment
"""

import copy
import json
import logging
from pathlib import Path
from typing import Optional, Union

from enoslib.api import Results, run_play
from enoslib.enos_inventory import EnosInventory
from enoslib.infra.enos_chameleonedge.objects import ChameleonDevice
from enoslib.objects import Host, Roles
from jinja2 import Template

import e2clab.constants.default as default
from e2clab.config import WorkflowConfig, WorkflowEnvConfig
from e2clab.constants import WorkflowTasks
from e2clab.constants.workflow import (
    DEFAULT_GROUPING,
    DEPENDS_ON,
    GROUPING,
    PREFIX,
    SELF_PREFIX,
    SERV_SELECT,
    TARGET,
    TASK_FINALIZE,
)
from e2clab.errors import E2clabFileError
from e2clab.grouping import get_grouping
from e2clab.log import get_logger
from e2clab.utils import load_yaml_file


class App:
    """
    Enforce workflow definition
    a.k.a. Workflow manager
    """

    def __init__(
        self,
        config: Path,
        experiment_dir: Path,
        scenario_dir: Path,
        artifacts_dir: Path,
        roles: Roles,
        all_serv_extra_inf: dict,
        app_conf: Optional[str] = None,
        env_config: Optional[Path] = None,
        optimization_config: dict[str, any] = None,
    ) -> None:
        """Create an application for the experiment

        Args:
            config (Path): Path to 'workflow.yaml' file
            experiment_dir (Path): Folder for experiment results
            scenario_dir (Path): Path to experiment definition
            artifacts_dir (Path): Path to experiment artifacts
            roles (Roles): EnOSlib.Roles associated with our experiment
            all_serv_extra_inf (dict): Extra information from deployed services
            app_conf (str, optional): Application configuration. Defaults to None.
            env_config (Path, optional): Path to 'workflow_env.yaml'. Defaults to None.
            optimization_config (dict[str, any], optional): Optimization configuration.
                Defaults to None.
        """
        self.logger = get_logger(__name__, ["APP"])
        self.config = self._load_config(config)

        # Relevant directories
        self.experiment_dir = experiment_dir
        self.scenario_dir = scenario_dir
        self.artifacts_dir = artifacts_dir

        # Global Experiment infrastructure Roles
        self.roles = roles
        # Global Experiment services extra information
        self.all_serv_extra_inf = all_serv_extra_inf

        self.app_conf = app_conf
        self.optimization_config = optimization_config

        if not app_conf:
            self.app_dir = self.experiment_dir
        else:
            # If we are running a specific configuration, we output in another dir
            self.app_dir = self.experiment_dir / app_conf
            self.workflow_env = self._load_env_config(env_config)

        # Application directory i.e. where to output
        self.app_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self, config_path: Path) -> WorkflowConfig:
        """Loads yaml 'workflow' file into a WorkflowConfig

        Args:
            config_path (Path): Path to the 'workflow.yaml' file

        Returns:
            WorkflowConfig: E2clab workflow config object
        """
        c = load_yaml_file(config_path)
        return WorkflowConfig(c)

    def _load_env_config(self, env_config_path: Path) -> Union[WorkflowEnvConfig, None]:
        try:
            c = load_yaml_file(env_config_path)
        except E2clabFileError:
            self.logger.warning(
                f"{env_config_path} does not exist, "
                "only adding 'app_conf' parameter to ansible env"
            )
            return WorkflowEnvConfig(dict())
        return WorkflowEnvConfig(c)

    # User methods

    # 'Alias' for app.application()
    def run_task(
        self,
        task: WorkflowTasks,
        current_repeat: Optional[int] = None,
    ) -> None:
        """Run application task

        Args:
            task (str): 'prepare' | 'launch' | 'finalize'
            current_repeat (int, optional): Defaults to None.
        """

        # TODO: propagate enum use to the rest of the module
        task_name = task.value

        # Define our working directory
        self.working_dir = self._prepare_working_dir(task=task_name)
        self.current_repeat = current_repeat
        # Get task run relevant additional ansible variables
        self.ansible_vars = self._vars_to_inject_ansible()

        self.logger.debug(f"[WORKING DIR] {self.working_dir}")
        self.logger.debug(f"[CURRENT REPEAT] {self.current_repeat}")
        self.logger.debug(f"[ANSIBLE VARS] {self.ansible_vars}")

        # filtered_config is a copy
        filtered_config = self.config.get_task_filtered_host_config(task=task_name)

        self.logger.debug(f"[TASK CONFIG] {filtered_config}")

        # Iterate on each hosts defnition
        # TODO: check performance impact and maybe run a single ansible play
        for host_task_conf in filtered_config:
            self.logger.debug(f"[HOST TASK CONF] {host_task_conf}")
            # TODO: manage EnosFailedHostsError
            ansible_play_return, ansible_roles = self._enforce_tasks(host_task_conf)
            self._print_workflow_validate(
                host_conf=host_task_conf,
                roles_validate=ansible_roles,
                task=task_name,
                ret=ansible_play_return,
            )

    # End User Methods

    def _prepare_working_dir(self, task: str) -> Path:
        """Defines the current working directory

        Args:
            task (str): Task from 'workflow.yaml' to inforce

        Returns:
            working_dir (Path): Path to the current working directory
        """
        if task != TASK_FINALIZE:
            working_dir = self.artifacts_dir
        else:
            working_dir = self.app_dir
        return working_dir

    def _enforce_tasks(self, host_task_conf: list[dict]) -> tuple[Results, Roles]:
        # depends_on being a list is already enforced by the workflow schema
        # Enforce tasks on chameleon devices
        # TODO: Workflow validate ?
        cham_conf = copy.deepcopy(host_task_conf)
        self.__enforce_tasks_on_chameleon_device(cham_conf)
        return self.__enforce_tasks_on_hosts(host_task_conf)

    def __enforce_tasks_on_chameleon_device(self, host_task_conf: list[dict]):
        depends_on_list = host_task_conf.pop(DEPENDS_ON, [])
        task_devices = self._filter_chameleon_devices(host_task_conf[TARGET])

        prefixes = []
        for depends in depends_on_list:
            prefixes.append(depends[PREFIX])

        if task_devices:
            self.logger.debug(f"[TASK DEVICES] {task_devices}")
            self.logger.debug(f"[DEPENDS ON LIST] {depends_on_list}")

            prepared_task_devices = self._get_prepared_task_hosts(
                depends_on_list=depends_on_list,
                task_hosts=task_devices,
                host_task_conf=host_task_conf,
                is_device=True,
            )

            role_depends_on = "all"
            host_task_conf[TARGET] = role_depends_on
            ansible_roles = self._get_ansible_roles(
                all_new_hosts=prepared_task_devices, role_depends_on=role_depends_on
            )

            for dev in prepared_task_devices:
                self.logger.debug(f"[DEVICE EXTRA] {dev.extra}")

                for _task in host_task_conf["tasks"]:
                    self.logger.debug(f"[ENFORCING TASK] {_task}")

                    self._enforce_task_on_dev(prefixes, dev, _task)
            return None, ansible_roles
        else:
            return None, None

    def __enforce_tasks_on_hosts(
        self, host_task_conf: list[dict]
    ) -> tuple[Results, Roles]:
        depends_on_list = host_task_conf.pop(DEPENDS_ON, [])
        task_hosts = self._filter_hosts(host_task_conf[TARGET])

        # no task hosts e.g. chameleon devices
        if task_hosts:
            self.logger.debug(f"[TASK HOSTS] {task_hosts}")
            self.logger.debug(f"[DEPENDS ON LIST] {depends_on_list}")
            # prepared_task_hosts refers to 'enoslib.host'
            # with 'prefix (data from other hosts)'
            prepared_task_hosts = self._get_prepared_task_hosts(
                depends_on_list=depends_on_list,
                task_hosts=task_hosts,
                host_task_conf=host_task_conf,
            )
            # self.logger.warning(prepared_task_hosts)
            self.logger.debug(f"[PREPARED_TASK_HOSTS] {prepared_task_hosts}")

            role_depends_on = "all"
            host_task_conf[TARGET] = role_depends_on
            ansible_roles = self._get_ansible_roles(
                all_new_hosts=prepared_task_hosts, role_depends_on=role_depends_on
            )

            # Run ansible task on hosts
            # TODO: Handle exceptions
            ansible_task = host_task_conf

            if self.logger.getEffectiveLevel() < logging.INFO:
                self.logger.debug("Printing hosts extra vars")
                for h in ansible_roles["all"]:
                    self.logger.debug(f"{h.alias} extra vars: {h.extra}")

            ansible_play_return = run_play(
                ansible_task, roles=ansible_roles, extra_vars=self.ansible_vars
            )
            return ansible_play_return, ansible_roles
        else:
            return None, None

    def _get_prepared_task_hosts(
        self,
        depends_on_list: list[dict],
        task_hosts: Union[list[Host], list[ChameleonDevice]],
        host_task_conf: list[dict],
        is_device: bool = False,
    ) -> Union[list[Host], list[ChameleonDevice]]:
        """
        Args:
            depends_on_list (list[dict]): List of "depends_on" configurations
            task_hosts (list[Host]): List of task-relevant EnOSlib hosts
            host_task_conf (list[dict]): Configuration for the tasks hosts
            is_device (bool): Are hosts 'ChameleonDevices'. Defaults to False
        Returns:
            list[Host]: Copy of the tasks hosts with added "extra" variables
        """
        all_new_hosts = []

        if isinstance(task_hosts[0], ChameleonDevice):
            is_device = True

        if is_device:
            # add the "extra" attribute
            task_hosts = self._add_extra_chameleondevice(task_hosts)

        if len(depends_on_list) == 0:
            all_new_hosts = copy.deepcopy(task_hosts)
        else:
            for depends_on in depends_on_list:
                # 'depends_on' adds 'extra' of a Service to the target host
                #   (e.g., -hosts:)
                # Get 'depends_on' services extra information
                # Key existence garenteed by schema validation
                service_selector = depends_on[SERV_SELECT]
                depends_on_service_extra_info = self._filter_service_extra_info(
                    service_selector
                )
                grouping_type = depends_on.get(GROUPING, DEFAULT_GROUPING)
                # WORKFLOW_PREFIX must exist as per schema validation
                prefix = depends_on[PREFIX]
                grouping = get_grouping(
                    grouping_type, task_hosts, prefix, depends_on_service_extra_info
                )
                new_hosts = grouping.distribute()

                # merge data from multiple Services ('depends_on')
                # in the 'extra' attribute of hosts
                if not all_new_hosts:
                    all_new_hosts += new_hosts
                else:
                    self._merge_depends_on(new_hosts, all_new_hosts, prefix)
        # all_new_hosts with '_self' (extra data generated in user-defined service)
        if is_device:
            return self._device_self_extra_info(all_new_hosts)
        else:
            return self._host_self_extra_info(all_new_hosts, host_task_conf)

    def _get_ansible_roles(
        self, all_new_hosts: list[Host], role_depends_on: str
    ) -> Roles:
        """Prepare our enoslib Roles to run the ansible command

        Args:
            all_new_hosts (list[Host]): Hosts with addes extra information
            role_depends_on (str): Role key

        Returns:
            Roles: EnOSlib Roles object
        """
        _roles_validate = Roles({role_depends_on: all_new_hosts})
        return _roles_validate

    def _enforce_task_on_dev(
        self, prefixes: list[str], dev: ChameleonDevice, _task: str
    ):
        """Enforce ansible-like tasks on ChameleonDevices

        Args:
            prefixes (list[str]): List of depends_on prefixes
            dev (ChameleonDevice): Task device
            _task (str): Ansible task. Must be 'copy' | 'shell' | 'fetch'
        """

        # if _task not in WORKFLOW_DEVICE_TASK:
        #     self.logger.warning(
        #       f"Chameleon Device task: {_task} is not in authorized "
        #       )

        if "copy" in _task:
            dev.upload(
                self._build_dev_command_from_ansible(
                    _task["copy"]["src"], self.ansible_vars, dev.extra, prefixes
                ),
                self._build_dev_command_from_ansible(
                    _task["copy"]["dest"], self.ansible_vars, dev.extra, prefixes
                ),
            )
        elif "shell" in _task:
            dev.execute(
                self._build_dev_command_from_ansible(
                    _task["shell"], self.ansible_vars, dev.extra, prefixes
                )
            )
        elif "fetch" in _task:
            dev.download(
                self._build_dev_command_from_ansible(
                    _task["fetch"]["src"], self.ansible_vars, dev.extra, prefixes
                ),
                self._build_dev_command_from_ansible(
                    _task["fetch"]["dest"], self.ansible_vars, dev.extra, prefixes
                ),
            )

    # def _filter_host_per_task(self, task) -> list[dict]:
    #     """
    #         Returns a list of hosts in workflow.yaml (-hosts:)
    #     with a single task [prepare, launch, finalize] defined in task_filter
    #     :param task: prepare, or launch, or finalize
    #     :return: list of hosts in workflow.yaml with task_filter
    #     """
    #     # TODO: Enfore task in WORKFLOW_TASKS
    #     filtered_hosts = []
    #     for host in copy.deepcopy(self.config):
    #         self.logger.debug(host)
    #         # filter task
    #         if task in host:
    #             host["tasks"] = host.pop(task)
    #             # clean all tasks that are not to be executed
    #             for other_task in WORKFLOW_TASKS:
    #                 # if other_task not defined, None is returned
    #                 host.pop(other_task, None)
    #             filtered_hosts.append(host)
    #     return filtered_hosts

    def _filter_chameleon_devices(self, pattern_selector: str):
        """
            Returns hosts as ChameleonDevice or None.
        :param all_service_extra_info: service extra info
        :param patter_selector: host in workflow.yaml
        :return: ChameleonDevice or []
        """
        selected_service_extra_info = self.__filter_using_ansible(pattern_selector)
        # extract the selected_service_extra_info back
        filtered_service_extra_info = {}
        for h in selected_service_extra_info:
            filtered_service_extra_info[h.address] = h.vars["__app_info__"]
        is_chameleon_device = []
        for _h in self.get_hosts_from_roles(
            # self.roles, filtered_service_extra_info.keys()
            hosts_key=filtered_service_extra_info.keys()
        ):
            if isinstance(_h, ChameleonDevice):
                is_chameleon_device.append(_h)
        return is_chameleon_device

    def __filter_using_ansible(self, pattern_selector: str):
        """
            Uses fake Host to use the convenient get_hosts method to pattern match the
            service extra information we want.
        :param patter_selector: pattern (as string) used to filter hosts
        :return: ansible.hosts
        """
        fake_roles = {}
        i = 0
        for key, conf in self.all_serv_extra_inf.items():
            fake_roles[str(i)] = [Host(key, extra={"__app_info__": conf})]
            i += 1
        fake_inventory = EnosInventory(roles=fake_roles)
        return fake_inventory.get_hosts(pattern=pattern_selector.lower())

    def _filter_hosts(self, hosts_selector: str):
        """
        Takes advantage of Ansible's 'pattern' to filter EnOSlib hosts from Roles
        :param roles: EnOSlib roles
        :param all_service_extra_info: service extra info
        :param hosts_selector: pattern (as string) used to filter hosts
        :return: EnOSlib Hosts
        """
        enos_inventory = EnosInventory(roles=self.roles)
        # these are ansible.hosts not enoslib hosts...
        selected_hosts = enos_inventory.get_hosts(pattern=hosts_selector.lower())
        # convert them back to enoslib.host
        hosts_with_app_info = self.get_hosts_from_roles(
            # self.roles, self.all_serv_extra_inf.keys()
            hosts_key=self.all_serv_extra_inf.keys()
        )
        selected_hosts = [
            k
            for h in selected_hosts
            for k in hosts_with_app_info
            if h.address == k.address
        ]
        return selected_hosts

    def get_hosts_from_roles(self, hosts_key: str) -> list[Host]:
        """
        Returns hosts from all roles
        :param hosts_key: role name
        :return: EnOSlib hosts
        """
        hosts = []
        for host_key in hosts_key:
            if host_key in self.roles:
                hosts += self.roles[host_key]
        return hosts

    def _filter_service_extra_info(self, pattern_selector: dict[str]) -> list[dict]:
        """
            Filters Services extra info by `service_key`.
        :param all_service_extra_info: Dict of Service extra info as: e.g.
            {service_key_1: {key: value},...,service_key_n: {key: value}}.
        :param patter_selector: Pattern to get Service extra info.
        :return: List[Dict] with Service values: e.g. [{key: value},...,{key: value}].
        """
        selected_service_extra_info = self.__filter_using_ansible(pattern_selector)
        # self.logger.warning(f"SELECTED {selected_service_extra_info}")
        # extract the selected_service_extra_info back
        selected_service_extra_info = [
            h.vars["__app_info__"] for h in selected_service_extra_info
        ]
        return selected_service_extra_info

    def _merge_depends_on(
        self, new_hosts: list[Host], all_new_hosts: list[Host], prefix: str
    ):
        for new_h in new_hosts:
            for stored_host in all_new_hosts:
                if new_h.address == stored_host.address:
                    if prefix in stored_host.extra:
                        stored_host.extra[prefix].update(new_h.extra[prefix])
                    else:
                        stored_host.extra.update({prefix: new_h.extra[prefix]})

    # TODO: test
    def _host_self_extra_info(self, hosts: list[Host], host_conf) -> list[Host]:
        """
            Adds '_self' attribute in extra info of a Service (enoslib.Host).
        :param roles: Roles (enoslib).
        :param all_service_extra_info: Services extra info.
        :param host: Host from `workflow.yaml`.
        :return: Hosts with `extra` info.
        """
        prefix = SELF_PREFIX
        grouping_type = "address_match"

        # Getting the hosts self extra information
        selected_service_extra_info = self._filter_service_extra_info(
            host_conf["hosts"]
        )

        # TODO: Necessary ?
        hosts = self._add_gateway_in_prefix(hosts, prefix)

        grouping = get_grouping(
            grouping_type, hosts, prefix, selected_service_extra_info
        )
        return grouping.distribute()

    def _device_self_extra_info(
        self, devices: list[ChameleonDevice]
    ) -> list[ChameleonDevice]:
        """
            Adds 'self' attribute in extra info of a Service (enoslib.ChameleonDevice).
        :param all_new_hosts: Chameleon devices.
        :return: ChameleonDevice with `extra` info.
        """
        new_devices = []
        for _device in devices:
            for key, data in self.all_serv_extra_inf.items():
                if _device.address == data["__address__"]:
                    _device_cp = copy.deepcopy(_device)
                    to_inject = {SELF_PREFIX: data}
                    _device_cp.extra.update(to_inject)
                    new_devices.append(_device_cp)
                    break
        return new_devices

    @staticmethod
    def _add_extra_chameleondevice(
        devices: list[ChameleonDevice],
    ) -> list[ChameleonDevice]:
        """
            Adds 'extra' in enoslib.ChameleonDevice.
            Can be removed in the future if we add 'extra: dict'
            in enoslib.ChameleonDevice.

        :param devices: devices as enoslib.ChameleonDevice
        :return: enoslib.ChameleonDevice with 'extra' attribute
        """
        devices_cp = copy.deepcopy(devices)
        for dev in devices_cp:
            if not hasattr(dev, "extra"):
                setattr(dev, "extra", {})
        return devices_cp

    # TODO: Why unused prefixes ?
    def _build_dev_command_from_ansible(
        self,
        raw_command: str,
        extra_vars: dict,
        device_extra: dict,
        prefixes: list[str],
    ) -> str:
        """Build a ChameleonDevice command from an ansible command

        Args:
            raw_command (str): Raw ansible command
            extra_vars (dict): Extra experiment variables e.g. 'working_dir'
            device_extra (dict): Extra device variables e.g. 'depends_on' variables
            prefixes (list[str]): Depends_on prefixes

        Returns:
            str: Executable ChameleonDevice command
        """
        command = self._inject_vars(
            command=raw_command, extra_vars=extra_vars, device_extra=device_extra
        )

        self.logger.debug(f"[DEVICE ANSIBLE RAW COMMAND] {raw_command}")
        self.logger.debug(f"[DEVICE ANSIBLE COMMAND] {command}")

        return command

    @staticmethod
    def _inject_vars(command: str, extra_vars: dict, device_extra: dict) -> str:
        """Injects vars into the device command like ansible with jinja.
        e.g. replaces  Jija template expressions like {{ test }} with the value in
        `extra_vars={test: 123}`: 123

        Args:
            command (str): base command
            extra_vars (dict): extra vars
            device_extra (dict): device extra information

        Returns:
            str: base command with injected vars
        """
        cmd_template = Template(command)
        template_data = {}
        template_data.update(extra_vars)
        template_data.update(device_extra)
        rendered_cmd = cmd_template.render(template_data)
        return rendered_cmd

    # TODO: see if necessary
    def _add_gateway_in_prefix(self, hosts: list[Host], prefix: str) -> list[Host]:
        """
            This is for Chameleon Cloud
            (it uses `gateway` IP to allow Ansible ssh hosts).

        Return a enoslib Host with `gateway` attribute of 'extra' within 'prefix'.
        :param hosts: enoslib Host
        :return: enoslib Host
        """
        hosts_cp = copy.deepcopy(hosts)
        for h in hosts_cp:
            if "gateway" in h.extra:
                h.extra.update({prefix: {"gateway": h.extra["gateway"]}})
        return hosts_cp

    def _vars_to_inject_ansible(self) -> dict[str, str]:
        """All application-level variables to inject in ansible tasks

        Returns:
            dict[str, str]: Key:Value dict
        """
        # ADD EXTRA VARIABLES
        extra_vars = {
            "working_dir": str(self.working_dir),
            "scenario_dir": str(self.scenario_dir),
            "artifacts_dir": str(self.artifacts_dir),
        }
        if self.optimization_config:
            extra_vars.update({"optimization_config": str(self.optimization_config)})
        if self.app_conf:
            # Feeding workflow environment into the ansible commands
            extra_vars.update({"app_conf": self.app_conf})
            extra_vars.update(self.workflow_env.get_env(self.app_conf, {}))
        if self.current_repeat:
            extra_vars.update({"current_repeat": self.current_repeat})
        else:
            extra_vars.update({"current_repeat": 1})
        return extra_vars

    def _print_workflow_validate(self, host_conf, roles_validate, task: str, ret: list):
        # workflow_validate_dir = os.path.join(_exp_dir, WORKFLOW_VALIDATE_FILE)
        workflow_validate_dir = self.app_dir / default.WORKFLOW_VALIDATE_FILE
        with open(workflow_validate_dir, "a+") as f:
            host_names = host_conf["hosts"]
            f.write("# # # HOSTS\n")
            f.write(f"# # # {host_names}\n")
            f.write("# # # ANSIBLE TASK\n")
            f.write(str(host_conf))
            f.write(f"\n\n# {task.upper()}")
            f.write("\n\n# ROLES\n")
            f.write(str(roles_validate))
            f.write("\n\n# EXTRA_VARS\n")
            f.write(str(self.ansible_vars))
            f.write("\n\n# ANSBILE_RETURN\n")
            # f.write(str(ret))
            if ret:
                for r in ret:
                    f.write(json.dumps(r.to_dict()))
                    f.write("\n")
            f.write("\n\n\n\n")
