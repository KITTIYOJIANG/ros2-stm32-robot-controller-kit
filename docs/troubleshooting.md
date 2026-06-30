# Troubleshooting

Goal: help developers diagnose common setup, flashing, serial, sensor, motor, and ROS2 issues when using the ROS2-Compatible STM32 Robot Controller Kit.

> Validation status: draft. Exact commands, device names, and error messages will be updated after the first firmware, SDK, and ROS2 package are validated on real hardware.

## How To Use This Guide

Start with the symptom that matches what you see. Work through the checks in order. Do not skip the basic checks: most bring-up issues come from cable, power, serial port, firmware version, or wiring mistakes.

Before debugging:

- Disconnect motor power if the robot can move unexpectedly.
- Lift wheels off the table during motor tests.
- Use a current-limited bench supply for early hardware bring-up when possible.
- Record the firmware version, SDK version, operating system, and serial port.

## Quick Diagnosis Table

| Symptom | Most Common Cause | First Action |
| --- | --- | --- |
| Board not detected | Bad USB cable, no power, driver issue | Try another data cable and check power LED |
| Flash failed | SWD wiring, boot mode, target voltage | Recheck SWDIO, SWCLK, GND, VTREF, and NRST |
| Serial permission denied | User lacks serial permissions | Add user to the serial group or use the correct COM port |
| No sensor data | IMU wiring, firmware mismatch, wrong bus config | Check firmware version and IMU connection |
| Motor not moving | No motor power, disabled driver, safety timeout | Check motor supply and run `STOP` then command again |
| ROS2 node not publishing | Wrong serial port or package not sourced | Check `port:=...` and source ROS2 workspace |
| Docker cannot access USB | Device not passed into container | Pass the serial device into Docker |
| Firmware version mismatch | Host tools expect another protocol | Upgrade firmware, SDK, and ROS2 package together |

## Collect Debug Information

When asking for help, collect this information first:

```text
Board revision:
Firmware version:
Python SDK version:
ROS2 package version:
Operating system:
Serial port:
Power supply voltage:
Motor driver:
IMU module:
Encoder type:
Exact command run:
Exact error message:
```

Planned version query:

```bash
python examples/get_version.py --port /dev/ttyUSB0
```

Expected output:

```text
Firmware version: 0.1.0
Protocol version: 0.1
Board state: IDLE
Last error: ERR_OK
```

## Board Not Detected

Symptoms:

- No serial port appears.
- The board does not show up in device manager.
- Python cannot open the port.
- No power LED is visible.

Checks:

1. Confirm the USB cable supports data, not charge-only.
2. Try another USB port.
3. Confirm the board power LED is on.
4. Disconnect motor power and test logic power only.
5. Check whether the board uses native USB or a USB-UART bridge.
6. Install the required USB-UART or ST-Link driver if needed.

For the STM32F103C8T6 minimal target:

- ST-LINK/V2-compatible SWD can flash the board but usually does not create a serial port.
- The firmware serial test uses USART1 on PA9 and PA10.
- Use a USB-UART adapter or a debugger that explicitly provides a virtual COM port.
- The Blue Pill USB connector will not act as USB CDC serial for this minimal firmware.

Linux checks:

```bash
lsusb
ls /dev/ttyUSB* /dev/ttyACM*
dmesg | tail -50
```

macOS checks:

```bash
ls /dev/tty.usb*
system_profiler SPUSBDataType
```

Windows check:

```powershell
[System.IO.Ports.SerialPort]::getportnames()
```

Likely fixes:

- Replace the USB cable.
- Install the USB-UART driver.
- Confirm board power.
- Try a different host USB port.
- Reflash firmware if the bootloader or USB firmware is corrupted.

## Flash Failed

Symptoms:

- `make flash` fails.
- STM32CubeProgrammer cannot connect.
- OpenOCD reports target not found.
- ST-Link LED shows an error.
- OpenOCD detects Cortex-M3 but reports `target needs reset`, `Target not halted`, or `failed erasing sectors`.

Checks:

1. Confirm SWDIO, SWCLK, GND, VTREF, and NRST wiring.
2. Confirm the board is powered.
3. Confirm the ST-Link sees target voltage.
4. Disconnect external modules during first flashing test.
5. Try a lower SWD clock speed.
6. Confirm boot pins are in the expected state.

Planned command:

```bash
cd firmware/Targets/stm32f103c8t6_minimal
make flash
```

Expected output:

```text
Connecting to target...
Erasing...
Flashing...
Verify OK
```

Likely fixes:

- Rewire SWD.
- Power the target board.
- Lower flash speed.
- Hold reset while connecting, then release.
- Try STM32CubeProgrammer if OpenOCD fails.

### OpenOCD Detects C8T6 But Cannot Halt

Known good signs:

```text
Target voltage: 3.25...
SWD DPIDR 0x1ba01477
Cortex-M3 processor detected
Examination succeed
```

Problem signs:

```text
target needs reset
TARGET: STM32F103C8Tx.cpu - Not halted
failed erasing sectors
```

If the board does not expose `RST` or `NRST`, do not use a hard-reset debug mode. In STM32CubeIDE OpenOCD debug settings:

- Do not use `connect_under_reset`.
- Do not use `reset_config srst_only ... connect_assert_srst`.
- Prefer a no-reset OpenOCD script or software reset mode.
- Lower adapter speed to 100 kHz or 240 kHz.

Fallback sequence:

1. Power off the board.
2. Set `BOOT0 = 1`.
3. Power on the board.
4. Connect with OpenOCD or STM32CubeProgrammer in SWD mode.
5. Erase or program flash.
6. Power off.
7. Set `BOOT0 = 0`.
8. Power on and test LED blink.

If CubeIDE keeps regenerating a hard-reset configuration, use the repository OpenOCD script:

```text
firmware/Targets/stm32f103c8t6_minimal/flash_openocd.cfg
```

It avoids the hardware reset line and is safer for Blue Pill-compatible boards without an exposed NRST pin.

## Serial Permission Denied

Symptoms:

- Python raises a permission error.
- ROS2 node cannot open `/dev/ttyUSB0`.
- Serial monitor works only with `sudo`.

Linux fix:

```bash
sudo usermod -aG dialout $USER
```

Then log out and log back in.

Temporary Linux check:

```bash
ls -l /dev/ttyUSB0
groups
```

macOS checks:

- Confirm the serial device exists under `/dev/tty.usb*`.
- Close other serial monitors before running the SDK.

Windows checks:

- Use the correct COM port.
- Close Arduino Serial Monitor, STM32CubeProgrammer, or any other app using the port.

## No Sensor Data

Symptoms:

- IMU output is empty.
- Sensor values are always zero.
- ROS2 `/imu/data` does not update.
- Firmware reports `ERR_IMU_NOT_READY`.

Checks:

1. Confirm the firmware version.
2. Confirm the sensor is connected to the expected bus.
3. Check power and ground.
4. Check I2C address or SPI chip select.
5. Check pull-up resistors for I2C.
6. Check whether the sensor module is 3.3 V compatible.

Planned Python check:

```bash
python examples/read_imu.py --port /dev/ttyUSB0
```

Expected output:

```text
IMU ready: true
ax=... ay=... az=...
gx=... gy=... gz=...
```

Likely fixes:

- Reconnect sensor wiring.
- Use the correct firmware build for the selected IMU.
- Confirm I2C address or SPI chip select.
- Replace the sensor module if it is not detected.

## Motor Not Moving

Symptoms:

- Python command is accepted but wheels do not move.
- Motor driver fault LED is on.
- ROS2 `/wheel_cmd` appears but robot does not move.
- Firmware reports `ERR_MOTOR_FAULT`.

Safety first:

- Lift wheels before testing.
- Use low speed such as `0.1`.
- Keep a physical power switch nearby.

Checks:

1. Confirm motor power is connected and enabled.
2. Confirm motor power voltage matches the driver and motor.
3. Confirm motor driver enable pin state.
4. Confirm PWM and direction pins are wired correctly.
5. Confirm firmware is not in `FAULT`.
6. Confirm command timeout has not stopped the motor.
7. Send `STOP`, then send a new motor command.

Planned Python test:

```bash
python examples/basic_motor_control.py --port /dev/ttyUSB0 --left 0.1 --right 0.1 --duration 1.0
```

Expected output:

```text
Connected
State: ARMED
Motor command accepted
Motors stopped
```

Likely fixes:

- Enable motor power.
- Check motor driver wiring.
- Clear firmware fault after resolving the cause.
- Lower speed command.
- Verify driver input polarity.

## ROS2 Node Not Publishing

Symptoms:

- `ros2 topic list` does not show expected topics.
- `/imu/data` is missing.
- `/encoder` is missing.
- Node starts and exits immediately.

Checks:

1. Confirm ROS2 workspace was built.
2. Source the workspace.
3. Pass the correct serial port.
4. Confirm the Python SDK can talk to the board first.
5. Confirm firmware version is compatible.

Planned commands:

```bash
colcon build --packages-select robot_controller
source install/setup.bash
ros2 launch robot_controller demo.launch.py port:=/dev/ttyUSB0
```

Check topics:

```bash
ros2 topic list
ros2 topic echo /imu/data
```

Likely fixes:

- Run `source install/setup.bash`.
- Use the right port argument.
- Close other programs using the serial port.
- Run the Python smoke test before ROS2.

## Docker Cannot Access USB

Symptoms:

- The board works on the host but not inside Docker.
- Container cannot see `/dev/ttyUSB0`.
- Permission denied inside container.

Checks:

1. Confirm the host sees the device.
2. Pass the device into the container.
3. Add permissions or run with the correct group.

Example Docker command:

```bash
docker run --rm -it \
  --device=/dev/ttyUSB0 \
  --group-add dialout \
  robot-controller-dev:latest
```

Likely fixes:

- Pass the device with `--device`.
- Run the container after the board is plugged in.
- Avoid unplugging and replugging during the container session.

## Firmware Version Mismatch

Symptoms:

- Python SDK connects but commands fail.
- ROS2 node reports unsupported protocol.
- Firmware returns `ERR_BAD_COMMAND`.
- Diagnostics show an unexpected protocol version.

Checks:

1. Query firmware version.
2. Check SDK version.
3. Check ROS2 package version.
4. Confirm all tools came from the same release tag.

Planned version query:

```bash
python examples/get_version.py --port /dev/ttyUSB0
```

Expected version policy:

```text
Firmware 0.1.x works with SDK 0.1.x and ROS2 package 0.1.x.
Firmware 0.2.x may require SDK 0.2.x and ROS2 package 0.2.x.
```

Likely fixes:

- Flash the matching firmware release.
- Reinstall the matching Python SDK.
- Rebuild the matching ROS2 package.
- Use a GitHub release tag instead of mixing files from different branches.

## Escalation Checklist

If the issue still cannot be solved, create a GitHub issue with:

- Exact symptom
- Board revision
- Firmware version
- Host OS
- Serial port name
- Power setup
- Motor driver and sensor modules
- Full terminal output
- Photos of wiring
- What you already tried

## Known Draft Gaps

- [ ] Replace planned commands with validated commands.
- [ ] Add screenshots of successful flashing.
- [ ] Add real serial logs.
- [ ] Add real ROS2 terminal output.
- [ ] Add photos of correct wiring.
- [ ] Add GitHub issue template link.

