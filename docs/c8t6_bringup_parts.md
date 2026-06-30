# C8T6 Bring-Up Parts

Goal: list the minimum parts needed for the first STM32F103C8T6 flash and serial test.

> Status: first bench checklist. This is not the final robot controller BOM.

## Buy Or Locate Now

| Priority | Item | Qty | Notes |
| --- | --- | ---: | --- |
| Must | STM32F103C8T6 Blue Pill-compatible board | 1-2 | Buy 2 if low cost; one can be a spare |
| Must | ST-LINK/V2-compatible programmer | 1 | Used by STM32CubeIDE for SWD flash/debug |
| Must | USB-UART adapter with 3.3 V logic | 1 | Required for `PING` and `GET_VERSION` over USART1 |
| Must | USB data cable for ST-LINK | 1 | Charge-only cables will not work |
| Must | USB data cable for USB-UART or board power | 1 | Keep separate from the ST-LINK cable |
| Must | Female-female jumper wires | 1 kit | For SWD and UART wiring |
| Must | Digital multimeter | 1 | Check voltage before connecting modules |
| Should | Breadboard or non-conductive base | 1 | Keeps the board stable |
| Should | Labels or masking tape | 1 | Mark SWDIO, SWCLK, PA9, PA10, GND |

## Software Needed

Install these before the board arrives:

- STM32CubeIDE
- ST-LINK driver if Windows does not detect the programmer
- USB-UART driver for your adapter, such as CH340, CP210x, or FTDI
- Python 3.10 or later for the host smoke test

Keil is not required for this route.

## First Wiring

### ST-LINK To C8T6

| ST-LINK Pin | C8T6 Pin | Required |
| --- | --- | --- |
| SWDIO | PA13 / SWDIO | Yes |
| SWCLK | PA14 / SWCLK | Yes |
| GND | GND | Yes |
| 3.3 V / VTREF | 3V3 / target reference | Usually yes |
| NRST | RST / NRST | Optional but useful |

Do not connect a 5 V programmer pin to a 3.3 V logic pin.

### USB-UART To C8T6

| USB-UART Pin | C8T6 Pin | Required |
| --- | --- | --- |
| RX | PA9 / USART1 TX | Yes |
| TX | PA10 / USART1 RX | Yes |
| GND | GND | Yes |
| 3.3 V | 3V3 | Optional; avoid if the board is already powered |

Set the USB-UART adapter to 3.3 V logic if it has a voltage selector.

## Buy Later

Only buy or connect these after LED blink and serial `PING` pass:

- TB6612FNG motor driver module
- 2 small DC gear motors with encoders
- Current-limited motor power supply
- IMU breakout module
- USB logic analyzer

## First Pass Criteria

The first hardware stage passes when:

- STM32CubeIDE can connect through ST-LINK.
- Firmware flashes successfully.
- PC13 LED blinks.
- USB-UART serial port appears on the host.
- `tools/c8t6_minimal_smoke.py` returns `ping: PASS`.
