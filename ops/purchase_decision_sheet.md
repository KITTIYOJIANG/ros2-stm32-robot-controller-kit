# Purchase Decision Sheet

Goal: define the minimum safe purchase set for the first STM32F103C8T6 bench bring-up.

> Status: decision checklist. Do not treat this as a final production BOM. Use it to choose the first low-cost bench parts only.

## Current Purchase Path

```text
STM32F103C8T6 Blue Pill-compatible board
  + ST-LINK/V2 compatible SWD programmer
  + TB6612FNG low-power motor driver module
  + small motors or sensor modules for later sessions
```

## Buy First

Buy or locate these first:

| Priority | Item | Qty | Decision Rule |
| --- | --- | ---: | --- |
| Must | STM32F103C8T6 Blue Pill-compatible board | 1-2 | Buy 2 if low cost; one can be a spare if bring-up wiring damages a board |
| Must | ST-LINK/V2 compatible programmer | 1 | Needed for repeatable SWD flashing and debug |
| Must | USB data cable | 1-2 | Must support data, not charge-only |
| Must | Jumper wires | 1 kit | Female-female and female-male are both useful |
| Must | Digital multimeter | 1 | Required before applying motor or external module power |
| Should | Breadboard or terminal block | 1 | Makes early wiring easier to inspect |

## Buy After Board Flash Works

Wait until the C8T6 board can be flashed before buying or wiring these:

| Priority | Item | Qty | Reason To Wait |
| --- | --- | ---: | --- |
| Must later | TB6612FNG motor driver module | 1 | Motor tests should wait until firmware flash and stop command path are known |
| Must later | Small DC gear motors with encoders | 2 | Avoid motor wiring until low-power protocol validation passes |
| Should later | IMU breakout | 1 | Sensor choice can change after the first board path is confirmed |
| Optional | USB logic analyzer | 1 | Useful if UART, I2C, or SPI debugging becomes unclear |

## STM32F103C8T6 Board Checks

Before buying, confirm the seller page or photo shows:

- `STM32F103C8T6` marking, or a clearly stated compatible clone.
- SWD pins labeled at minimum: `SWDIO`, `SWCLK`, `GND`, and `3.3V` or `VTREF`.
- `BOOT0` jumper or button is accessible.
- `RESET` button or reset pin is accessible.
- USB connector is physically solid.
- Board is advertised as 3.3 V logic.

Reject or pause the purchase if:

- The listing only says "STM32" with no exact model.
- SWD pins are not visible or not documented.
- The photo is too blurred to inspect chip marking or pin labels.
- The seller claims unrealistic features that are not shown on the board.
- The board ships without headers and you do not want to solder yet.

## ST-LINK/V2 Compatible Checks

Before connecting it to the board:

- Identify `SWDIO`.
- Identify `SWCLK`.
- Identify `GND`.
- Identify target reference voltage or `3.3V`.
- Do not connect a `5V` pin to any 3.3 V target logic pin.
- Use the programmer only after the pinout is clear from the label or seller documentation.

## First Purchase Budget Rule

Keep the first order small:

```text
Buy only enough parts to prove:
host -> flash -> serial/protocol -> logged test evidence
```

Do not buy production quantities until:

- Firmware can be flashed repeatedly.
- Real serial communication works.
- At least one factory-style log exists.
- The next hardware risk is explicit.

## Evidence To Save

Save these privately after purchase:

- Order screenshot or invoice.
- Seller product image.
- Board top photo.
- Board bottom photo.
- ST-LINK pinout photo.
- First flash terminal output.

Do not commit invoices, addresses, order IDs, or private seller account data to the public repository.

## Next Action

Choose one STM32F103C8T6 board listing and one ST-LINK/V2 compatible listing. After choosing, update:

- `hardware/bom/bringup_bom_v0.1.csv`
- `hardware/bom/bringup_bom_gallery.md`
- `ops/supplier_list.csv`
