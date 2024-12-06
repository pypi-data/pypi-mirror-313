import sys
import time

from src.chronos.timer import ChronosTimer


class ChronosTimerWithVisualization(ChronosTimer):
    def _report_progress(self) -> None:
        bar_length = 40
        while self._running:
            if self.start_time is None:
                raise ValueError("Timer has not been started.")
            if self.interval is None:
                raise ValueError("Interval must be set before reporting progress.")

            elapsed = time.perf_counter() - self.start_time
            converted = self._convert_time(elapsed, self.default_unit)
            progress = min(1, elapsed / self.threshold) if self.threshold else 0
            block = int(round(bar_length * progress))
            bar = "#" * block + "-" * (bar_length - block)
            sys.stdout.write(f"\r[{bar}] {converted:.2f} {self.default_unit} elapsed...")
            sys.stdout.flush()
            time.sleep(self.interval)  # Safe now because interval is verified to be non-None
        print("")
