import json
import logging
import threading
import time
from typing import Dict, Optional, Union


class BaseChronosTimer:
    UNITS = {
        "milliseconds": 1000,
        "seconds": 1,
        "minutes": 1 / 60,
        "hours": 1 / 3600,
        "days": 1 / 86400,
    }

    def __init__(
        self,
        name: Optional[str] = None,
        log_file: Optional[str] = None,
        threshold: Optional[float] = None,
        interval: Optional[float] = None,
        default_unit: str = "seconds",
    ) -> None:
        if default_unit not in self.UNITS:
            raise ValueError(f"Invalid default_unit. Must be one of {list(self.UNITS.keys())}.")

        self.name: Optional[str] = name
        self.log_file: Optional[str] = log_file
        self.threshold: Optional[float] = threshold
        self.interval: Optional[float] = interval
        self.default_unit: str = default_unit
        self.start_time: Optional[float] = None
        self.elapsed: Optional[float] = None
        self._running: bool = False
        self._thread: Optional[threading.Thread] = None

        if log_file:
            logging.basicConfig(filename=log_file, level=logging.INFO)

    def __enter__(self) -> "BaseChronosTimer":
        self.start_time = time.perf_counter()
        if self.interval:
            self._start_progress_reporting()
        return self

    def __exit__(
        self, exc_type: Optional[type], exc_value: Optional[Exception], traceback: Optional[object]
    ) -> None:
        if self.start_time is None:
            raise RuntimeError("Timer was never started.")
        self.elapsed = time.perf_counter() - self.start_time
        self._stop_progress_reporting()
        self._print_and_log()
        self._check_threshold()

    def _start_progress_reporting(self) -> None:
        if self.interval is None:
            raise ValueError("Interval must be set to enable progress reporting.")
        self._running = True
        self._thread = threading.Thread(target=self._report_progress)
        self._thread.start()

    def _stop_progress_reporting(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join()

    def _report_progress(self) -> None:
        if self.start_time is None:
            raise RuntimeError("Timer was never started.")
        while self._running:
            elapsed = time.perf_counter() - self.start_time
            converted = self._convert_time(elapsed, self.default_unit)
            print(
                f"{self.name or 'Task'}: {converted:.2f} {self.default_unit} elapsed...", end="\r"
            )
            if self.interval is None:
                raise ValueError("Interval must be set for progress reporting.")
            time.sleep(self.interval)

    def _convert_time(self, elapsed: float, unit: str) -> float:
        if unit not in self.UNITS:
            raise ValueError(f"Invalid unit. Must be one of {list(self.UNITS.keys())}.")
        return elapsed * self.UNITS[unit]

    def _print_and_log(self) -> None:
        if self.elapsed is None:
            raise RuntimeError("Timer was never stopped.")
        converted = self._convert_time(self.elapsed, self.default_unit)
        message = f"{self.name or 'Task'} completed in {converted:.2f} {self.default_unit}"
        print(message)
        if self.log_file:
            logging.info(message)

    def _check_threshold(self) -> None:
        if (
            self.threshold is not None
            and self.elapsed is not None
            and self.elapsed > self.threshold
        ):
            print(
                f"WARNING: {self.name or 'Task'} exceeded the threshold of {self.threshold:.2f} seconds!"
            )

    def get_elapsed(self, unit: str = "seconds") -> float:
        if self.elapsed is None:
            raise RuntimeError("Timer has not finished yet.")
        return self._convert_time(self.elapsed, unit)

    def to_json(self, unit: str = "seconds") -> str:
        return json.dumps(self.to_dict(unit))

    def to_dict(self, unit: str = "seconds") -> Dict[str, Union[str, float]]:
        return {
            "task": self.name or "Unnamed Task",
            "elapsed": self.get_elapsed(unit),
            "unit": unit,
        }
