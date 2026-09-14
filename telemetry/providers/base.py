from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class TelemetrySnapshot:
    speed: float = 0
    rpm: int = 0
    throttle: float = 0
    brake: float = 0
    position: float = 0
    lap: int = 0
    lap_time: float = 0
    total_time: float = 0
    extra: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self):
        return {
            'speed': round(self.speed, 1),
            'rpm': self.rpm,
            'throttle': round(self.throttle, 3),
            'brake': round(self.brake, 3),
            'position': round(self.position, 3),
            'lap': self.lap,
            'lap_time': round(self.lap_time, 3),
            'total_time': round(self.total_time, 3),
            **self.extra,
        }


class TelemetryProvider(ABC):
    @abstractmethod
    def read(self, rig):
        raise NotImplementedError

    def close(self):
        return None
