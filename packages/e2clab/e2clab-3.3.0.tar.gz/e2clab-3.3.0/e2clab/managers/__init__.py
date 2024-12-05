from enum import Enum

from .manager import Manager
from .monitoring import MonitoringManager
from .monitoring_iot import MonitoringIoTManager
from .monitoring_kwollect import MonitoringKwollectManager
from .provenance import ProvenanceManager


class Managers(Enum):
    PROVENANCE = ProvenanceManager
    MONITORING = MonitoringManager
    MONITORING_IOT = MonitoringIoTManager
    KWOLLECT = MonitoringKwollectManager


__all__ = ["Manager", "Managers"]
