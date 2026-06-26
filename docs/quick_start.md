# Quick Start

Goal: help a robotics developer run the first board demo in about 10 minutes after the hardware and firmware are ready.

> Status: draft. Commands, board name, serial device, and firmware paths will be validated after the first firmware build is available.

## What You Need

- ROS2-Compatible STM32 Robot Controller Kit
- USB cable or USB-UART adapter
- Host computer running Linux, macOS, or Windows
- Python 3.10 or later
- ROS2 environment for ROS2 demos
- ST-Link or supported programmer for firmware flashing

## 1. Connect The Board

Planned connection flow:

1. Connect the board to the host computer.
2. Connect motor power only after checking polarity and voltage.
3. Connect motors, IMU, and encoder lines according to the hardware overview.
4. Confirm the power LED turns on.
5. Confirm the board appears as a serial device.

Expected serial device examples:

```text
Linux: /dev/ttyUSB0 or /dev/ttyACM0
macOS: /dev/tty.usbserial-*
Windows: COM3 or similar
```

## 2. Flash Firmware

Planned command:

```bash
make flash
```

If the board is not detected, check:

- ST-Link connection
- Boot mode
- USB cable data support
- Serial or programmer permissions
- Board power

## 3. Run Python Smoke Test

Planned example:

```python
from robot_controller import RobotController

board = RobotController("/dev/ttyUSB0")
board.set_motor_speed(0.3, 0.3)
print(board.read_imu())
```

Expected output:

```text
Connected to robot controller
Motor command accepted
IMU: ax=..., ay=..., az=..., gx=..., gy=..., gz=...
```

## 4. Run ROS2 Demo

Planned command:

```bash
ros2 launch robot_controller demo.launch.py
```

Expected topics:

```text
/wheel_cmd
/imu/data
/encoder
```

## 5. Troubleshooting Checklist

- Board not detected: check cable, power, driver, and boot mode.
- Flash failed: check programmer wiring and target voltage.
- Serial permission denied: add the user to the correct serial group or run with proper permissions.
- No sensor data: check wiring and firmware version.
- Motor not moving: check external motor power, polarity, driver enable pin, and safety stop state.
- ROS2 node not publishing: check serial port, baud rate, and launch config.

## Next Validation Tasks

- [ ] Confirm exact board serial device name
- [ ] Confirm firmware flash command
- [ ] Confirm Python package install command
- [ ] Confirm ROS2 package name
- [ ] Add wiring diagram
- [ ] Add screenshots or terminal logs
