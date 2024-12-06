import signal
import time
from typing import Any, Optional

from src.chronos.timer import ChronosTimer


class DebuggingChronosTimer(ChronosTimer):
    def __enter__(self) -> "DebuggingChronosTimer":
        signal.signal(signal.SIGTSTP, self._pause_timer)  # Capture Ctrl+Z for pausing
        signal.signal(signal.SIGCONT, self._resume_timer)  # Capture resume signal
        super().__enter__()
        return self

    def _pause_timer(self, signum: int, frame: Optional[Any]) -> None:
        print("\nTimer paused. Press Ctrl+Z again to resume.")
        self._running = False
        self._pause_time = time.perf_counter()

    def _resume_timer(self, signum: int, frame: Optional[Any]) -> None:
        print("Timer resumed.")
        self._running = True
        if self.start_time is not None and self._pause_time is not None:
            self.start_time += time.perf_counter() - self._pause_time
        else:
            raise ValueError(
                "Cannot resume the timer as it was not properly initialized or paused."
            )
