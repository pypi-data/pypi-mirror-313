"""
Monitoring IoT-Lab module
"""

from pathlib import Path

import e2clab.constants.default as default

from ..constants import Environment
from ..constants.layers_services import (
    ARCHI,
    MONITORING_IOT_ARCHI,
    MONITORING_IOT_AVERAGE,
    MONITORING_IOT_AVERAGE_VALS,
    MONITORING_IOT_CURRENT,
    MONITORING_IOT_PERIOD,
    MONITORING_IOT_PERIOD_VALS,
    MONITORING_IOT_POWER,
    MONITORING_IOT_PROFILES,
    MONITORING_IOT_SVC,
    MONITORING_IOT_VOLTAGE,
    NAME,
)
from ..errors import E2clabError
from ..log import get_logger
from .manager import Manager


class MonitoringIoTManager(Manager):
    """
    Iotlab monitoring does not work like other managers
    but for a consistent API we define this class
    """

    logger = get_logger(__name__, ["MONITORING_IOT"])

    _MONITORING_PROFILE = {
        "description": "https://www.iot-lab.info/testbed/resources/monitoring",
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                NAME: {
                    "description": "Name of the monitoring profile.",
                    "type": "string",
                },
                ARCHI: {
                    "Description": "Type of architecture to monitor.",
                    "type": "string",
                    "enum": MONITORING_IOT_ARCHI,
                },
                MONITORING_IOT_CURRENT: {
                    "description": "Enable current monitoring",
                    "type": "boolean",
                    "default": False,
                },
                MONITORING_IOT_POWER: {
                    "description": "Enable power monitoring",
                    "type": "boolean",
                    "default": False,
                },
                MONITORING_IOT_VOLTAGE: {
                    "description": "Enable voltage monitoring",
                    "type": "boolean",
                    "default": False,
                },
                MONITORING_IOT_PERIOD: {
                    "description": "Sampling period (µs)",
                    "type": "number",
                    "enum": MONITORING_IOT_PERIOD_VALS,
                    "default": default.IOT_PERIOD_VAL,
                },
                MONITORING_IOT_AVERAGE: {
                    "description": "Monitoring samples averaging window.",
                    "type": "number",
                    "enum": MONITORING_IOT_AVERAGE_VALS,
                    "default": default.IOT_AVERAGE_VAL,
                },
            },
            # "required": [NAME, ARCHI, MONITORING_IOT_PERIOD, MONITORING_IOT_AVERAGE],
            "required": [NAME, ARCHI],
        },
    }

    SCHEMA = {
        "description": "FIT IoT-Lab monitoring profiles ",
        "type": "object",
        "properties": {MONITORING_IOT_PROFILES: _MONITORING_PROFILE},
        "required": [MONITORING_IOT_PROFILES],
    }
    CONFIG_KEY = MONITORING_IOT_SVC
    SERVICE_ROLE = None
    ROLE = None

    def create_service(self):
        # No service to create, monitoring delegated to provider
        pass

    def _deploy(self):
        # No deployment, monitoring delegated to provider
        pass

    def _backup(self, output_dir: Path):
        if self.provider is None:
            self.logger.error("Monitoring Iotlab did not find Iotlab provider")
            raise E2clabError
        self.logger.info("Backing up monitoring data...")
        iot_out_dir = output_dir / default.MONITORING_DATA / default.MONITORING_IOT_DATA
        iot_out_dir.mkdir(parents=True, exist_ok=True)
        self.provider.provider.collect_data_experiment(iot_out_dir)
        self.logger.info("Backup done")

    def _destroy(self):
        pass

    def get_environment(self) -> Environment:
        return Environment.IOT_LAB
