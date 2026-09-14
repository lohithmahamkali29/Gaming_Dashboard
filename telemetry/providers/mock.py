import math
import time

from .base import TelemetryProvider, TelemetrySnapshot


class MockTelemetryProvider(TelemetryProvider):
    def read(self, rig):
        elapsed = time.monotonic()
        phase = elapsed % 75
        lap = int(elapsed // 75) + 1
        return TelemetrySnapshot(
            speed=145 + 35 * math.sin(elapsed / 3),
            rpm=int(6500 + 1200 * math.sin(elapsed / 2)),
            throttle=0.5 + 0.5 * math.sin(elapsed / 2.5),
            brake=max(0, math.sin(elapsed / 2.5 + 2.2)),
            position=phase / 75,
            lap=lap,
            lap_time=phase,
            total_time=elapsed,
        )
