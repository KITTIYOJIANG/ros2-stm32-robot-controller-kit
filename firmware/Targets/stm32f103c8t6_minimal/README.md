# STM32F103C8T6 Minimal Bring-Up Firmware

Goal: provide the first real C8T6 firmware target for safe bench bring-up.

This target is intentionally small. It does not control motors, read sensors, or use an RTOS. It proves only this chain:

```text
power -> flash -> LED blink -> UART command -> version -> PING
```

## Hardware Assumptions

Target board:

```text
STM32F103C8T6 Blue Pill-compatible development board
```

Default pins:

| Function | STM32 Pin | Blue Pill Label | Notes |
| --- | --- | --- | --- |
| Status LED | PC13 | onboard LED | Usually active-low |
| UART TX | PA9 | A9 | Connect to USB-UART RX |
| UART RX | PA10 | A10 | Connect to USB-UART TX |
| SWDIO | PA13 | SWDIO | Connect to ST-LINK/V2 SWDIO |
| SWCLK | PA14 | SWCLK | Connect to ST-LINK/V2 SWCLK |
| Ground | GND | GND | Common ground required |
| Target reference | 3.3 V / VTREF | 3V3 | Do not connect 5 V to 3.3 V logic pins |

Serial settings:

```text
115200 baud, 8 data bits, no parity, 1 stop bit
```

Important: a cheap ST-LINK/V2 compatible dongle usually does not provide a serial port. For the UART test, use a USB-UART adapter on PA9/PA10, or a debugger that explicitly includes a virtual COM port.

## Protocol

Send line endings as `\n` or `\r\n`.

Supported commands:

```text
PING
GET_VERSION
STOP
```

Expected responses:

```text
ACK PING
VERSION firmware=0.1.0 protocol=0.1 board=stm32_robot_controller
ACK STOP
```

Unknown commands return:

```text
ERROR code=0x0001 name=ERR_BAD_COMMAND message="unknown command"
```

The firmware does not print an unsolicited boot banner. That keeps Python SDK request/response reads deterministic.

## Build On Windows PowerShell

Install GNU Arm Embedded Toolchain or STM32CubeCLT, then make sure these tools are in `PATH`:

```text
arm-none-eabi-gcc
arm-none-eabi-objcopy
arm-none-eabi-size
```

Build:

```powershell
cd firmware\Targets\stm32f103c8t6_minimal
.\build.ps1
```

Output:

```text
build\c8t6_minimal.elf
build\c8t6_minimal.bin
```

## Build With Make

```bash
cd firmware/Targets/stm32f103c8t6_minimal
make
```

## Flash With OpenOCD

Install OpenOCD and connect ST-LINK/V2-compatible SWD:

```bash
cd firmware/Targets/stm32f103c8t6_minimal
make flash
```

Equivalent manual command:

```bash
openocd -f flash_openocd.cfg -c "program build/c8t6_minimal.elf verify reset exit"
```

## Flash With STM32CubeProgrammer

From this target directory:

```powershell
STM32_Programmer_CLI -c port=SWD -w build\c8t6_minimal.bin 0x08000000 -v -rst
```

## Test Serial From Host

Install the Python SDK serial extra:

```powershell
cd ..\..\..\sdk\python
python -m pip install -e ".[serial]"
```

Run the minimal smoke check from the repository root:

```powershell
python tools\c8t6_minimal_smoke.py --port COM3
```

Replace `COM3` with the real USB-UART port.

Expected output:

```text
ping: PASS
version: VersionInfo(firmware='0.1.0', protocol='0.1', board='stm32_robot_controller')
```

## Stop Here Before Motor Work

Do not connect the TB6612FNG motor driver yet. The next firmware milestone after this target passes is:

```text
GPIO-safe STOP state -> motor driver enable pin mapping -> low-power no-load motor command
```
