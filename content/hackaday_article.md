# Hackaday / Hackster Project Article Draft

Working title:

```text
Building a ROS2-Compatible STM32 Robot Controller Kit from the Ground Up
```

> Status: draft. Publish only after adding real demo evidence: hardware photo, wiring photo, terminal output, GIF, or short video.

## Problem

ROS2 is powerful, but the path from a ROS2 tutorial to a moving robot is still messy for many beginners.

The high-level software may run on a laptop, Raspberry Pi, Jetson, or mini PC, but the low-level hardware layer still needs:

- reliable motor commands
- IMU and encoder readings
- firmware flashing
- serial communication
- predictable safety behavior
- clear documentation
- repeatable factory testing

Many student or maker robots start as one-off demos. The goal of this project is to turn that kind of demo into a reproducible small-batch developer kit.

## Project Goal

Build a compact STM32-based robot controller kit with:

- firmware
- Python SDK
- ROS2 package
- Quick Start guide
- troubleshooting guide
- API reference
- datasheet draft
- factory test script
- store and fulfillment planning documents

This is not positioned as an industrial controller. It is a developer kit for mobile robot prototyping and education.

## Hardware Architecture

The target hardware architecture includes:

- STM32 MCU
- power input and logic regulation
- SWD programming header
- USB or UART host communication
- motor driver interface
- IMU interface over I2C or SPI
- encoder inputs
- status LEDs
- test points
- expansion headers

The first hardware overview is documented here:

```text
docs/hardware_overview.md
```

Open hardware decisions:

- final STM32 family and package
- onboard motor driver vs external driver interface
- IMU module vs onboard IMU
- connector type and pinout
- motor voltage and current assumptions
- input protection and ESD strategy

## Firmware Architecture

The firmware is split into:

```text
firmware/
  App/
  Config/
  Drivers/
```

Current skeleton includes:

- `version.h`
- `error_code.h`
- `protocol.h`
- `protocol.c`
- `motor_driver.h`

The protocol currently defines:

```text
PING
GET_VERSION
GET_STATUS
SET_MOTOR
STOP
READ_IMU
READ_ENCODER
```

The important rule is that firmware must not start motors by default. It should expose version and status first, then accept explicit motion commands, and stop on timeout or fault.

## Python SDK

The Python SDK has a mock transport so host-side API design can be tested before the real board is ready.

Example:

```python
from robot_controller import RobotController

board = RobotController.mock()
print(board.get_version())
board.set_motor_speed(0.1, 0.1)
print(board.read_imu())
print(board.read_encoder())
board.stop()
```

This allows the API shape, examples, tests, and factory-test workflow to be developed before hardware is finalized.

## ROS2 Integration

The ROS2 package skeleton includes:

- package metadata
- launch file
- default YAML config
- Python node skeleton

Planned topics:

| Topic | Type | Purpose |
| --- | --- | --- |
| `/wheel_cmd` | `geometry_msgs/msg/Twist` | receive velocity command |
| `/imu/data` | `sensor_msgs/msg/Imu` | publish IMU sample |
| `/encoder` | `std_msgs/msg/Int32MultiArray` | publish encoder counts |
| `/diagnostics` | `diagnostic_msgs/msg/DiagnosticArray` | publish board health |

The next validation step is running this in a real ROS2 Humble workspace.

## Factory Test And Fulfillment

A small-batch hardware product needs a repeatable test flow before shipping.

Current factory-test skeleton:

```bash
python tools/factory_test.py --mock --order TEST-0001
```

Planned real hardware flow:

```bash
python tools/factory_test.py --port /dev/ttyUSB0 --order ORDER-0001 --enable-motion
```

The fulfillment SOP requires:

- firmware flashing log
- factory test log
- board photos
- packed kit photo
- tracking upload
- support record

This is intentionally boring, because boring fulfillment is how small hardware projects avoid avoidable support pain.

## Current Repository Assets

The repository currently includes:

- README
- roadmap
- Quick Start
- hardware overview
- firmware overview
- API reference
- troubleshooting guide
- datasheet draft
- FAQ
- pricing model
- shipping matrix
- fulfillment SOP
- factory test script
- Python SDK skeleton
- ROS2 package skeleton
- GitHub issue templates
- GitHub Actions smoke checks

## What Is Not Done Yet

- real schematic
- real BOM with MPNs
- PCB layout
- firmware on hardware
- real serial protocol validation
- real ROS2 workspace validation
- first moving robot demo
- shipping quotes
- final pricing
- Tindie listing

## Lessons So Far

1. The repository structure matters early.
2. Version and error codes should exist before the SDK grows.
3. A mock SDK is useful before hardware exists.
4. A factory-test habit should start before the first sale.
5. Documentation is not separate from engineering; it is part of the product.

## Project Link

```text
https://github.com/KITTIYOJIANG/ros2-stm32-robot-controller-kit
```

## Publishing Checklist

- [ ] Add real hardware photo.
- [ ] Add wiring photo.
- [ ] Add terminal output screenshot.
- [ ] Add short demo GIF or video.
- [ ] Confirm README status is accurate.
- [ ] Do not claim certification.
- [ ] Do not claim production readiness.
- [ ] Do not claim inventory before units are tested.

