import time

from src.chronos.timer import ChronosTimer


def test_basic_timer() -> None:
    with ChronosTimer("Basic Test") as timer:
        time.sleep(1)
    assert timer.get_elapsed("seconds") >= 1
