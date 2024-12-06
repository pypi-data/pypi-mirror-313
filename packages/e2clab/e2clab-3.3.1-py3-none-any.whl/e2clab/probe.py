"""
Probe singletons module
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Hashable, Optional

from e2clab.log import get_logger


@dataclass
class Record:
    start: Optional[datetime] = None
    end: Optional[datetime] = None


class TaskProbe:
    """
    Pickle-resistant implementation of a singleton

    Not an issue as un-pickling is done at the beginning of an e2clab process
    """

    _instance = None

    def __init__(self) -> None:
        self.logger = get_logger(__name__, ["PROBE"])

        self._records: dict[Hashable, Record] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __setstate__(self, state):
        """
        Ran when unpickling an instance
        """
        self.__dict__.update(state)
        # restore unpickled probe as singleton
        type(self)._instance = self

    def set_start(self, record_name: Hashable) -> None:
        self._check_record(record_name)
        timestmp = self._get_now()
        self._records[record_name].start = timestmp

        self.logger.debug(f"Set start timestamp for {record_name}")

    def set_end(self, record_name: Hashable) -> None:
        self._check_record(record_name)
        timestmp = self._get_now()
        self._records[record_name].end = timestmp

        self.logger.debug(f"Set end timestamp for {record_name}")

    @staticmethod
    def _get_now() -> datetime:
        return datetime.now().astimezone()

    def _check_record(self, record_name: Hashable):
        """Init record if doesn't exist"""
        if record_name not in self._records:
            self._records[record_name] = Record()

    def get_task_record(self, record_name: Hashable):
        return self._records.get(record_name, None)

    def get_records(self) -> dict[Hashable, Record]:
        return self._records

    @classmethod
    def get_probe(cls):
        """Get timestamp probe object (singleton)"""
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
