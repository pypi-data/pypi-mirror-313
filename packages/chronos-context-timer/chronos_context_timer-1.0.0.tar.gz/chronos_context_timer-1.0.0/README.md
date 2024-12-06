# Chronos

Chronos is a Python library for advanced task timing, performance monitoring, and debugging tools. It is designed for developers who need precise control over timing tasks, distributed systems, batch processing, and more, with features like real-time visualization and debugging-friendly timers.

## Features

-   **Base Timer**: Core functionality for timing tasks with unit conversion, logging, and threshold warnings.
-   **ChronosTimer**: A basic timer with all core features.
-   **DistributedChronosTimer**: Aggregate timing data across distributed systems.
-   **BatchChronosTimer**: Time multiple tasks and compute aggregate statistics.
-   **DebuggingChronosTimer**: Pause and resume timers during debugging sessions.
-   **ChronosTimerWithVisualization**: Real-time ASCII progress bars for task timing.

---

## Installation

Install Chronos using pip:

```bash
pip install chronos-context-timer
```

---

## Usage Examples

### Basic Timer

```python
from chronos import ChronosTimer

with ChronosTimer("Basic Task") as timer:
    # Simulate some work
    import time
    time.sleep(1)

print(f"Task completed in {timer.get_elapsed('seconds')} seconds")
```

### Distributed Timer

```python
from chronos import DistributedChronosTimer

with DistributedChronosTimer("Distributed Task") as timer:
    import time
    time.sleep(1)

# Add external timings
timer.add_timing(0.5)
timer.add_timing(1.5)

print(f"Total elapsed time: {timer.get_total_time('seconds')} seconds")
```

### Batch Timer

```python
from chronos import BatchChronosTimer

def example_task():
    import time
    time.sleep(0.5)

batch_timer = BatchChronosTimer("Batch Example")
for _ in range(3):
    batch_timer.time_task(example_task)

stats = batch_timer.get_statistics("seconds")
print(f"Average time: {stats['average_time']} seconds")
print(f"Total time: {stats['total_time']} seconds")
```

### Debugging Timer

```python
from chronos import DebuggingChronosTimer

with DebuggingChronosTimer("Debug Task") as timer:
    input("Press Ctrl+Z to pause, and again to resume. Press Enter to finish.")
```

### Timer with Visualization

```python
from chronos import ChronosTimerWithVisualization

with ChronosTimerWithVisualization("Visualized Task", interval=0.2, threshold=5):
    import time
    time.sleep(5)
```

---

## Development

### Running Tests

Run all tests using pytest:

```bash
pytest tests/
```

### Type Checking

Chronos is fully type-checked using `mypy`. To run type checks:

```bash
mypy chronos/
```

---

## License

Chronos is licensed under the MIT License. See [LICENSE](/LICENSE) for details.

---

## Documentation

Complete documentation is available [here](https://github.com/adambirds/chronos).
