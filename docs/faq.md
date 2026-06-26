# FAQ

Goal: answer common customer and developer questions before they become repeated support work.

> Validation status: draft. Answers will be updated as hardware, firmware, SDK, ROS2 package, shipping, and return policies are validated.

## What is this kit?

It is a compact STM32-based robot controller kit for mobile robot prototyping. The target experience includes firmware, a Python SDK, ROS2 examples, and documentation for connecting motors, sensors, and host robot software.

## Who is it for?

Target users:

- ROS2 beginners
- Robotics students
- Embedded developers
- University labs
- STEM educators
- Maker and hacker communities

## Is this a finished industrial controller?

No. It is a developer kit for prototyping and education. Do not treat early prototypes as certified industrial or consumer products.

## Is it CE or FCC certified?

No certification is claimed at this stage. Do not describe the product as CE or FCC certified until certification is completed.

## How do I flash firmware?

The planned flow is:

```bash
cd firmware
make flash
```

The exact command will be verified after the firmware build and flashing workflow are implemented.

## How do I connect it to ROS2?

The planned flow is:

```bash
colcon build --packages-select robot_controller
source install/setup.bash
ros2 launch robot_controller demo.launch.py port:=/dev/ttyUSB0
```

See [api_reference.md](api_reference.md) for the draft ROS2 topics and parameters.

## Why is the board not detected?

Common causes:

- Charge-only USB cable
- Missing USB-UART driver
- Board not powered
- Wrong serial port
- Firmware or bootloader issue

See [troubleshooting.md](troubleshooting.md).

## How do I update firmware?

Planned update flow:

1. Download the matching firmware release.
2. Connect ST-Link or supported programmer.
3. Run the documented flash command.
4. Query firmware version after flashing.
5. Use matching SDK and ROS2 package versions.

## Can I use this with Raspberry Pi?

Target answer: yes, through USB serial or UART after the interface is validated. The Raspberry Pi should run the Python SDK or ROS2 node and communicate with the STM32 board over the supported serial link.

## Can I use this with Jetson?

Target answer: yes, through USB serial or UART after validation. Jetson should run the host-side software while the STM32 board handles low-level motor and sensor timing.

## What motor drivers are supported?

The first hardware architecture targets a motor driver interface with signals such as PWM, DIR, EN, and optional FAULT. Exact supported drivers will be confirmed after schematic and firmware validation.

## Does it include motors or sensors?

Draft kit contents include the controller board, cable set, documentation, firmware, SDK, and ROS2 examples. Motors, batteries, IMU modules, or encoders may not be included unless stated in the final listing.

## Does it support encoders?

Encoder support is planned. The first draft targets left and right A/B encoder inputs for wheel odometry experiments.

## Does it support IMU data?

IMU support is planned through I2C or SPI. Exact IMU part and data format will be confirmed during hardware validation.

## What operating system should I use?

Recommended development environment:

```text
Ubuntu 22.04 + ROS2 Humble + Python 3.10 or later
```

Other systems may work but will be documented after validation.

## Can I use Docker?

Docker support is planned, but USB serial access must be passed into the container. See [troubleshooting.md](troubleshooting.md) for the draft USB pass-through notes.

## What happens if the host stops sending commands?

The firmware should stop motor output after a command timeout. This behavior must be tested before selling hardware.

## What is the return policy?

Final return policy is not set yet. The draft policy will live in [shipping_and_returns.md](shipping_and_returns.md). Early prototypes should not be sold as mature consumer products.

## Where can I buy it?

Not available yet. First public sales target is a small-batch Tindie listing after hardware validation, firmware testing, documentation, pricing, and fulfillment planning.

## How can I report an issue?

Use GitHub issues after the issue template is added. Include:

- Board revision
- Firmware version
- SDK version
- ROS2 package version
- Operating system
- Serial port
- Exact command
- Exact error message
- Photos of wiring when relevant

## Draft Gaps

- [ ] Add final issue template link
- [ ] Add final supported motor driver list
- [ ] Add final return policy
- [ ] Add final kit contents
- [ ] Add final supported OS list

