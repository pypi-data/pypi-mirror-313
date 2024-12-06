"""
Kwollect monitoring manager
"""

import csv
from pathlib import Path
from typing import Hashable, Optional

import pytz
from enoslib.infra.enos_g5k.g5k_api_utils import get_api_client
from grid5000 import Grid5000Error

import e2clab.constants.default as default
from e2clab.constants import WORKFLOW_TASKS, Environment
from e2clab.errors import E2clabError
from e2clab.log import get_logger
from e2clab.managers.manager import Manager
from e2clab.probe import Record, TaskProbe

METRICS = "metrics"
STEP = "step"

START = "start"
END = "end"

ALL = "all"

API_TZ = pytz.timezone("Europe/Paris")

STEP_OPTIONS = [*WORKFLOW_TASKS, "launch"]


class MonitoringKwollectManager(Manager):
    """
    Kwollect monitoring manager class
    """

    logger = get_logger(__name__, ["KWOLLECT"])

    SCHEMA = {
        "$schema": "https://json-schema.org/draft/2019-09/schema",
        "type": "object",
        "title": "Grid5000 kwollect monitoring Schema",
        "properties": {
            METRICS: {
                "description": "Metrics to pull from job, '[all]' to pull all metrics",
                "type": "array",
                "items": {"type": "string"},
            },
            STEP: {
                "description": "Workflow step to monitor",
                "type": "string",
                "enum": STEP_OPTIONS,
                "default": default.KWOLLECT_STEP,
            },
            START: {
                "description": (
                    f"Workflow step to start monitor at. Mandatory if '{END}' is set"
                ),
                "type": "string",
                "enum": STEP_OPTIONS,
            },
            END: {
                "description": "Workflow step to end monitor at",
                "type": "string",
                "enum": STEP_OPTIONS,
            },
        },
        "required": [METRICS],
        "dependencies": {END: [START]},
        "allOf": [
            {
                "if": {"required": [STEP]},
                "then": {
                    "not": {
                        "anyOf": [
                            {"required": [START]},
                            {"required": [END]},
                        ]
                    }
                },
            }
        ],
    }

    CONFIG_KEY = "kwollect"
    SERVICE_ROLE = None  # Not useful
    # Not needed ? Do we take the whole job ?
    ROLE = "k_monitor"

    def create_service(self):
        # No service to create
        pass

    def _deploy(self):
        self.g5k_client = get_api_client()
        self.jobs = self.provider.get_jobs()
        for job in self.jobs:
            site = job.site
            id = job.uid
            dash_addr = self._get_viz_address(site)
            self.logger.info(
                f"Access kwollect metric dashboard for job {id}: {dash_addr}"
            )

    def _backup(self, output_dir: Path):
        # output dir
        kwollect_output_dir = (
            output_dir / default.MONITORING_DATA / default.MONITORING_KWOLLECT_DATA
        )
        kwollect_output_dir.mkdir(exist_ok=True, parents=True)

        # metrics
        metrics = self._get_metrics_str()

        # probe
        try:
            start_str, end_str = self._get_timestamp_str()
        except E2clabError as e:
            self.logger.warning(f"Could not backup kwollect data : {e}")
            return

        for job in self.jobs:
            kwargs = {
                "metrics": metrics,
                "start_time": start_str,
            }
            if end_str:
                kwargs["end_time"] = end_str

            if metrics == ALL:
                kwargs.pop("metrics")

            site = job.site
            nodes_str = self._filter_site_nodes(site)
            if nodes_str:
                kwargs["nodes"] = nodes_str
            else:
                oarjobid = job.uid
                kwargs["job_id"] = oarjobid

            self.logger.debug(
                f"Pulling kwollect data from {site} API with kwargs: {kwargs}"
            )

            # API call
            try:
                metrics_list = self.g5k_client.sites[site].metrics.list(**kwargs)
            except Grid5000Error as e:
                self.logger.error(f"Failed API call to {site} site")
                self.logger.error(e)
                continue
            if len(metrics_list) > 0:
                # TODO: add more comprehensive naming
                self._dump_metrics(
                    metrics_list=metrics_list,
                    output_dir=kwollect_output_dir,
                    filename=site,
                )
            else:
                self.logger.info(f"No metrics data found for Grid'5000 '{site}' site")

    def _destroy(self):
        # Nothing to do
        pass

    def get_environment(self) -> Environment:
        """This manager only works for Grid5000"""
        return Environment.G5K

    def _get_metrics_str(self) -> str:
        m_list = self.config.get(METRICS, [ALL])
        if ALL in m_list:
            return ALL
        else:
            return ",".join(m_list)

    def _get_timestamp_str(self) -> tuple[str, Optional[str]]:
        """Parsing configuration for start and end timestamp

        Returns:
            tuple[str, Optional[str]]: end timestamp may be None
        """
        task_probe = TaskProbe.get_probe()

        def _get_record(rec_name: Hashable) -> Record:
            rec = task_probe.get_task_record(rec_name)
            if rec is None:
                raise E2clabError(f"Failed to get timing record for {rec_name}")
            return rec

        start = None
        end = None
        if STEP in self.config:
            step = self.config[STEP]

            rec = _get_record(step)

            start = rec.start
            end = rec.end

        elif START in self.config:
            step = self.config[START]

            rec = _get_record(step)
            start = rec.start

            if END in self.config:
                step = self.config[END]

                rec = _get_record(step)
                end = rec.end
        else:
            rec = _get_record(default.KWOLLECT_STEP)
            start = rec.start
            end = rec.end

        if start is None:
            raise E2clabError("No start time found for kwollect monitoring")

        start_str = start.astimezone(API_TZ).isoformat()
        end_str = end.astimezone(API_TZ).isoformat() if end else None

        return start_str, end_str

    def _filter_site_nodes(self, site: str) -> Optional[str]:
        nodes = []
        for agent in self.agent:
            addr = agent.address
            if site in addr and "grid5000" in addr:
                nodes.append(addr.split(".")[0])

        if len(nodes) > 0:
            return ",".join(nodes)
        else:
            return None

    def _get_viz_address(self, site: str) -> str:
        """Returns address to dashboard"""
        addr = f"https://api.grid5000.fr/stable/sites/{site}/metrics/dashboard"
        return addr

    @staticmethod
    def _dump_metrics(metrics_list, output_dir: Path, filename: str) -> None:
        """Dump Kwollect API metrics to CSV

        Args:
            metrics (_type_): List of metrics records
            output_dir (Path): Dir to output
            filename (str): name of the file
        """
        metrics_csv = list(map(lambda m: m.to_dict(), metrics_list))
        keys = metrics_csv[0].keys()
        out_file = output_dir / f"{filename}.csv"
        with open(out_file, "w") as out:
            dict_writer = csv.DictWriter(out, keys)
            dict_writer.writeheader()
            dict_writer.writerows(metrics_csv)
