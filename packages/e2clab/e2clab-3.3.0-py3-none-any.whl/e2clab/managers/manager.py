"""
Base module for manager interface definition
"""

from abc import ABC, abstractmethod
from copy import deepcopy
from pathlib import Path
from typing import Any, Optional, Union

from enoslib import Host, Networks, Roles
from enoslib.service.service import Service as EnService
from jsonschema import Draft7Validator, ValidationError

from ..constants import Environment
from ..errors import E2clabConfigError, E2clabError
from ..log import get_logger


class Manager(ABC):
    """Abstract class for manager implementations"""

    logger = get_logger(__name__, ["MANAGER"])

    SCHEMA: dict[str, Any] = {}
    CONFIG_KEY: str = ""

    SERVICE_ROLE: Optional[str] = ""
    ROLE: Optional[str] = ""

    def __init__(
        self,
        # This is a Manager-specific config, not the whole infra config
        # TODO: define new typing
        config: Union[dict, list],
    ):
        # Prevent unwanted side effects
        self.config = deepcopy(config)
        if not self._validate_config(self.config):
            raise E2clabConfigError

        self.host: Optional[Host] = None
        # Iterable[Host] ?
        self.agent: Roles = Roles()
        self.networks: Optional[Networks] = None
        self.artifacts_dir: Optional[Path] = None
        self.provider = None
        self.meta: dict = {}
        self.service: Optional[EnService] = None

    def init(
        self,
        roles: Optional[Roles] = None,
        networks: Optional[Networks] = None,
        artifacts_dir: Optional[Path] = None,
        # TODO: fix this mess
        # Can't import due to cyclical imports through layers_config
        # provider: Optional[Provider] = None,
        # Weird stuff, only needed for iotlab monitoring to have consistent api
        provider=None,
        meta: dict = {},
    ):
        if roles:
            if len(roles[self.service_role]) > 0:
                self.host = roles[self.service_role][0]
            else:
                self.host = None
            self.agent = roles[self.role]
        self.networks = networks
        self.artifacts_dir = artifacts_dir
        self.provider = provider
        # Implementation-specific info
        self.meta = meta
        # We want the create service to parse info from the config
        self.service = self.create_service()

    @abstractmethod
    def create_service(self) -> EnService:
        """Initiates Manager service

        Returns:
            EnService: Manager service
        """
        pass

    @abstractmethod
    def _deploy(self):
        # Hook function for service deployment
        pass

    def deploy(self):
        """Deploy manager service"""
        try:
            self._deploy()
        except Exception as e:
            self.logger.error(f"Failed deploying {self.__class__.__name__}: {e}")
            raise E2clabError

    @abstractmethod
    def _backup(self, output_dir: Path):
        # Hook function for service backup
        pass

    def backup(self, output_dir: Path):
        """Backup manager service"""
        try:
            self._backup(output_dir=output_dir)
        except Exception as e:
            self.logger.error(f"Failed backup {self.__class__.__name__}: {e}")
            raise E2clabError

    @abstractmethod
    def _destroy(self):
        # Hook function for service destroy
        pass

    def destroy(self):
        """Destroy manager service"""
        try:
            self._destroy()
        except Exception as e:
            self.logger.error(f"Failed destroying {self.__class__.__name__}: {e}")
            raise E2clabError

    @abstractmethod
    def get_environment(self) -> Environment:
        pass

    @classmethod
    def get_schema(cls):
        return cls.SCHEMA

    @classmethod
    def get_config_key(cls):
        return cls.CONFIG_KEY

    @classmethod
    def get_service_role(cls):
        return cls.SERVICE_ROLE

    @classmethod
    def get_role(cls):
        return cls.ROLE

    @property
    def schema(self) -> dict:
        """Example implementation

        Returns:
            dict: config jsonschema
        """
        return self.SCHEMA

    @property
    def config_key(self) -> str:
        """Example implementation

        Returns:
            str: configuration key for layers_services
        """
        return self.CONFIG_KEY

    @property
    def service_role(self) -> Optional[str]:
        """Example implementation

        Returns:
            str: service role
        """
        return self.SERVICE_ROLE

    @property
    def role(self) -> Optional[str]:
        """Example implementation

        Returns:
            str: agent roles
        """
        return self.ROLE

    def get_extra_info(self) -> dict:
        return {}

    def _validate_config(self, config) -> bool:
        is_valid = True
        _validator = Draft7Validator(self.schema)
        try:
            _validator.validate(config)
        except ValidationError as e:
            is_valid = False
            self.logger.error(
                f"Invalid configuration for {self.__class__.__name__}: {e.message}"
            )
        return is_valid
