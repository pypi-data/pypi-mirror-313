from typing import List, Optional

from src.chronos.base_timer import BaseChronosTimer


class DistributedChronosTimer(BaseChronosTimer):
    def __init__(self, name: Optional[str] = None, default_unit: str = "seconds") -> None:
        super().__init__(name=name, default_unit=default_unit)
        self._external_timings: List[float] = []

    def __enter__(self) -> "DistributedChronosTimer":
        super().__enter__()
        return self

    def add_timing(self, elapsed_time: float) -> None:
        self._external_timings.append(elapsed_time)

    def get_total_time(self, unit: str = "seconds") -> float:
        if self.elapsed is None:
            raise RuntimeError("Timer has not finished yet.")
        total_elapsed = self.elapsed + sum(self._external_timings)
        return self._convert_time(total_elapsed, unit)
