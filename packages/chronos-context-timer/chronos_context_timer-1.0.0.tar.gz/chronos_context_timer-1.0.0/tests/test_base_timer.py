import time

from pytest import CaptureFixture

from src.chronos.base_timer import BaseChronosTimer


def test_base_timer_basic() -> None:
    with BaseChronosTimer("Base Timer Test") as timer:
        time.sleep(1)
    assert timer.get_elapsed("seconds") >= 1


def test_base_timer_conversion() -> None:
    with BaseChronosTimer("Conversion Test") as timer:
        time.sleep(1)
    assert timer.get_elapsed("milliseconds") >= 1000


def test_base_timer_threshold_warning(capfd: CaptureFixture[str]) -> None:
    with BaseChronosTimer("Threshold Test", threshold=0.5) as _:
        time.sleep(1)
    captured = capfd.readouterr()
    assert "WARNING: Threshold Test exceeded the threshold" in captured.out
