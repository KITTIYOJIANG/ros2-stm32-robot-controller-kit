# Python SDK

Goal: provide a small host-side Python API for controlling the ROS2-Compatible STM32 Robot Controller Kit.

> Status: skeleton. The SDK can run with a mock transport today. Real serial mode requires firmware and `pyserial`.

## Install For Development

From this directory:

```bash
python -m pip install -e .
```

For real serial hardware mode:

```bash
python -m pip install -e .[serial]
```

## Mock Smoke Test

Run without hardware:

```bash
python examples/mock_smoke_test.py
```

Expected behavior:

- Connects to mock board
- Reads firmware version
- Reads status
- Sends a low-speed motor command
- Reads IMU and encoder samples
- Stops motors

## Basic Usage

```python
from robot_controller import RobotController

board = RobotController.mock()
print(board.get_version())
board.set_motor_speed(0.1, 0.1)
print(board.read_imu())
print(board.read_encoder())
board.stop()
board.close()
```

## Real Serial Usage

```python
from robot_controller import RobotController

board = RobotController("/dev/ttyUSB0")
print(board.get_version())
board.stop()
board.close()
```

## Current API

- `RobotController.mock()`
- `RobotController(port, baudrate=115200, timeout=1.0)`
- `get_version()`
- `get_status()`
- `set_motor_speed(left, right)`
- `stop()`
- `read_imu()`
- `read_encoder()`
- `close()`

## Next Tasks

- [ ] Confirm real serial protocol with firmware.
- [ ] Add package publishing metadata.
- [ ] Add CI for SDK tests.
- [ ] Add richer response parsing.
- [ ] Add typed ROS2 adapter layer.
