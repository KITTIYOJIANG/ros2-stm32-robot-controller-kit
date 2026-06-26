# YouTube Demo Script Draft

Goal: create a three-minute English demo that proves the controller board is real, usable, and relevant to ROS2 mobile robot prototyping.

## Video Structure

### 0:00 - Show The Robot Moving

Show the robot responding to a simple command. Do not start with slides.

Voiceover:

```text
This is a compact STM32 robot controller kit running a basic motor and sensor demo for ROS2 mobile robot prototyping.
```

### 0:15 - Problem

Voiceover:

```text
When building small mobile robots, developers often spend too much time wiring motor drivers, reading sensors, and bridging microcontroller firmware to ROS2.
```

### 0:45 - Hardware Overview

Show the board and label the major blocks:

- STM32 MCU
- Power input
- Motor interface
- IMU and encoder interfaces
- SWD programming header
- UART, I2C, and SPI expansion

### 1:15 - Code Overview

Show the repository:

- Firmware folder
- Python SDK folder
- ROS2 package folder
- Quick Start document

### 1:45 - Wiring

Show the board connected to:

- Host computer
- Motor power
- Motors
- Sensor inputs

### 2:15 - Live Test

Show terminal commands and expected output:

```bash
python examples/basic_motor_control.py
ros2 topic echo /imu/data
```

### 2:45 - GitHub And Product Link

Voiceover:

```text
The firmware, Python examples, ROS2 package, and documentation are available on GitHub. A small-batch developer kit listing will be added after hardware validation.
```

## Footage Checklist

- [ ] Robot moving
- [ ] Close-up board shot
- [ ] Wiring shot
- [ ] Firmware flashing
- [ ] Python demo
- [ ] ROS2 topic output
- [ ] GitHub README

## Notes

Do not claim CE or FCC certification before certification is complete. Do not describe untested prototypes as production-ready hardware.
