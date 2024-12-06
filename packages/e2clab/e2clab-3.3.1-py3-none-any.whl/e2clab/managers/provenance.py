"""
Provenance manager module
"""

from pathlib import Path

import e2clab.constants.default as default

from ..constants import SUPPORTED_ENVIRONMENTS, Environment
from ..constants.layers_services import (
    CLUSTER,
    IPV,
    IPV_VERSIONS,
    PROVENANCE_SERVICE_ROLE,
    PROVENANCE_SVC,
    PROVENANCE_SVC_DATAFLOW_SPEC,
    PROVENANCE_SVC_PARALLELISM,
    PROVENANCE_SVC_PORT,
    PROVENANCE_SVC_PROVIDER,
    ROLES_PROVENANCE,
    SERVERS,
)
from ..log import get_logger
from ..services import Provenance
from .manager import Manager


class ProvenanceManager(Manager):
    """Provenance manager"""

    logger = get_logger(__name__, ["PROVENANCE_MANAGER"])

    SCHEMA = {
        "description": "Definition of the provenance data capture capabilities",
        "type": "object",
        "properties": {
            PROVENANCE_SVC_PROVIDER: {
                "description": "Testbed to deploy the provenance service: G5k only",
                "type": "string",
                "enum": SUPPORTED_ENVIRONMENTS,
            },
            CLUSTER: {
                "description": "Cluster where the provenence server will be running",
                "type": "string",
            },
            SERVERS: {
                "description": "Machine where the provenance server will be running",
                "type": "array",
                "maxItems": 1,
                "items": {"type": "string"},
            },
            PROVENANCE_SVC_DATAFLOW_SPEC: {
                "description": "User-defined dataflow specifications",
                "type": "string",
                "default": default.DATAFLOW_SPEC,
            },
            IPV: {
                "description": "IP network version to transmit provenance data",
                "type": "number",
                "enum": IPV_VERSIONS,
                "default": 4,
            },
            PROVENANCE_SVC_PARALLELISM: {
                "description": "Parallelizes the prov data translator and broker topic",
                "type": "number",
                "default": default.PARALLELISM,
            },
        },
        "oneOf": [
            {
                "required": [
                    PROVENANCE_SVC_PROVIDER,
                    CLUSTER,
                    PROVENANCE_SVC_DATAFLOW_SPEC,
                ]
            },
            {
                "required": [
                    PROVENANCE_SVC_PROVIDER,
                    SERVERS,
                    PROVENANCE_SVC_DATAFLOW_SPEC,
                ]
            },
        ],
    }

    CONFIG_KEY = PROVENANCE_SVC
    SERVICE_ROLE = PROVENANCE_SERVICE_ROLE
    ROLE = ROLES_PROVENANCE

    # Abstract classes definitions
    def create_service(self) -> Provenance:
        dataflow_file_spec = self._get_dataflow_spec()
        dataflow_file_path = self.artifacts_dir / dataflow_file_spec
        if not dataflow_file_path.exists():
            self.logger.warning(f"Dataflow file: {dataflow_file_path}, does not exist.")
        provenance = Provenance(
            host=self.host,
            agent=self.agent,
            dataflow_spec=str(dataflow_file_path),
            parallelism=self._get_parallelism(),
        )
        return provenance

    def _deploy(self) -> None:
        self.logger.info("Deploying...")
        self.service.deploy()
        self.logger.info("Done deploying...")

    def _backup(self, output_dir: Path):
        prov_out_dir = output_dir / default.PROVENANCE_DATA
        self.logger.info(f"Backing up provenance data in {prov_out_dir} ...")
        self.service.backup(backup_dir=prov_out_dir)
        self.logger.info("Backup done")

    def _destroy(self):
        self.logger.info("Destroying...")
        self.service.destroy()
        self.logger.info("Done destroying")

    def get_environment(self) -> Environment:
        # Provenance_svc_provider can't be none due to schema
        return Environment(self.config.get(PROVENANCE_SVC_PROVIDER))

    def get_extra_info(self) -> dict:
        """Returns provenance extra information

        Returns:
            dict: provenance_extra_info
        """
        ui_address = self.host.address
        _provenance_extra_info = {
            PROVENANCE_SERVICE_ROLE: {
                "__address__": f"{ui_address}",
                "url": f"http://{ui_address}:{PROVENANCE_SVC_PORT}",
            }
        }
        return _provenance_extra_info

    # Config parsing
    def _get_parallelism(self) -> int:
        return int(self.config.get(PROVENANCE_SVC_PARALLELISM, default.PARALLELISM))

    def _get_dataflow_spec(self) -> str:
        return str(self.config.get(PROVENANCE_SVC_DATAFLOW_SPEC, default.DATAFLOW_SPEC))
