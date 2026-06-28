# Firmware

Goal: turn the STM32 firmware from a lab demo into a product-oriented firmware project.

> Status: skeleton. The current files define versioning, error codes, protocol parsing/formatting, and the first motor driver interface. They are not yet connected to a real STM32Cube project.

## Current Structure

```text
firmware/
  App/
    protocol.c
    protocol.h
  Config/
    error_code.h
    version.h
  Drivers/
    motor_driver.h
  Targets/
    stm32f103c8t6_minimal/
```

## Why This Structure Exists

- `Config` owns stable product identity: firmware version, protocol version, board name, and error codes.
- `App` owns host-facing behavior: protocol commands, responses, and message formatting.
- `Drivers` owns hardware-facing behavior: motor, IMU, encoder, and future board peripherals.

This avoids a common embedded beginner trap: putting everything into one large `main.c`.

## Draft Protocol

The first line-oriented protocol follows [../docs/api_reference.md](../docs/api_reference.md).

Initial commands:

```text
PING
GET_VERSION
GET_STATUS
SET_MOTOR left=<float> right=<float>
STOP
READ_IMU
READ_ENCODER
```

## Safety Defaults

Firmware should follow these rules:

- Motors start stopped after boot.
- Motor command values are limited to `-1.0` through `1.0`.
- Firmware exposes a version before accepting motion commands.
- Faults are reported through stable error codes.
- Host timeout should stop motor output.

## Next Implementation Tasks

- [ ] Add `motor_driver.c` with HAL or mock backend.
- [ ] Add `imu_driver.h` and `imu_driver.c`.
- [ ] Add `encoder_driver.h` and `encoder_driver.c`.
- [ ] Add `app_state_machine.h` and `app_state_machine.c`.
- [ ] Add board pin mapping in `BSP/`.
- [ ] Add a real STM32 build system.
- [ ] Connect protocol parser to UART receive code.
- [ ] Add host-side protocol tests.

## Build Status

The first hardware target is available at:

```text
firmware/Targets/stm32f103c8t6_minimal
```

It is a bare-metal STM32F103C8T6 bring-up firmware that can:

1. Blink an LED.
2. Return firmware version over USART1.
3. Reply to `PING`.
4. Reply to `GET_VERSION`.
5. Stop motors by default.

It does not implement motor, IMU, encoder, ROS2, or USB CDC behavior yet. Use it only for the first board power, flash, LED, UART, and protocol check.

