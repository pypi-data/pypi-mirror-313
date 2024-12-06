import time

from src.chronos.batch_timer import BatchChronosTimer


def test_batch_timer() -> None:
    def task() -> None:
        time.sleep(0.5)

    batch_timer = BatchChronosTimer("Batch Test")
    for _ in range(3):
        batch_timer.time_task(task)
    stats = batch_timer.get_statistics("seconds")
    assert stats["timing_count"] == 3
    assert stats["total_time"] >= 1.5
