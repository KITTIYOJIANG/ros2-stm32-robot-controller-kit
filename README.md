# ROS2-Compatible STM32 Robot Controller Kit

A compact STM32-based robot controller kit with firmware, Python SDK, and ROS2 examples for fast mobile robot prototyping.

> Status: early productization draft. This repository is being shaped from a lab demo into a reproducible developer kit.

## Why This Exists

ROS2 beginners, robotics students, embedded developers, and makers often lose time wiring motors, reading sensors, and bridging microcontroller firmware to ROS2 software. This kit aims to provide a small, documented controller board that can connect common robot peripherals and expose simple firmware, Python, and ROS2 interfaces.

## Demo

Demo evidence will be added as the hardware and firmware stabilize.

- Demo GIF: `media/gifs/demo_placeholder.gif`
- Demo video: planned
- Test log: planned

## Features

- STM32-based embedded controller board
- Motor control interface for mobile robot prototypes
- IMU and encoder interface targets
- Firmware project with a product-oriented structure
- Python SDK examples for direct board control
- ROS2 package examples for robot software integration
- Quick Start documentation for first-time setup
- Troubleshooting and datasheet documents planned

## Target Users

- ROS2 beginners
- Robotics students
- Embedded developers
- University labs
- STEM educators
- Maker and hacker communities

## Repository Layout

```text
docs/       Quick Start, hardware notes, firmware notes, API reference, FAQ
hardware/   Schematic, PCB, Gerber, BOM, enclosure files
firmware/   STM32 firmware project
sdk/        Python SDK and examples
ros2/       ROS2 package and launch files
examples/   End-to-end demos
media/      Images, GIFs, and videos
store/      Tindie, Shopify, pricing, and shipping drafts
content/    YouTube, Reddit, and Hackaday content drafts
ops/        Cost table, supplier list, order tracker, factory test logs
```

## Quick Start

The first Quick Start draft lives in [docs/quick_start.md](docs/quick_start.md).

Current planned flow:

1. Connect the controller board to a host computer over USB or UART.
2. Flash the STM32 firmware.
3. Run a Python motor-control smoke test.
4. Run a ROS2 publishing demo.
5. Check expected serial and ROS2 topic output.

## Hardware Overview

Planned hardware blocks:

- STM32 MCU minimum system
- Power input and regulation
- SWD programming header
- UART, I2C, and SPI expansion
- Motor driver interface
- IMU and encoder interfaces
- Power indicator LEDs
- Factory test points

## Software Overview

Planned software blocks:

- Firmware drivers for motors, IMU, encoders, and protocol handling
- Python SDK for serial communication and simple control
- ROS2 package for publishing sensor data and receiving wheel commands
- Examples for basic motor control, IMU reading, and ROS2 integration

## Buy Link

Not available yet. First public sales target: small-batch developer kits through Tindie after hardware, firmware, tests, documentation, and fulfillment checks are complete.

## Safety And Compliance Notes

This is a developer kit for prototyping and education. It is not a certified consumer appliance. Do not claim CE or FCC certification until certification has been completed. Use it in a safe lab environment and avoid selling untested boards as ready stock.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## License

License is not selected yet. The first public release should define separate licenses for hardware files, firmware, SDK code, and documentation.
