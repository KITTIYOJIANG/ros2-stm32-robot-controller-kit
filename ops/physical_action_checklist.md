# Physical Action Checklist

Goal: convert the project from repository planning into safe physical preparation.

> Status: first bench-prep draft. Do not order final production parts yet. This checklist is for the first bring-up bench and prototype validation path.

## What You Can Do Now

These actions are safe to start before PCB design:

1. Prepare a clean electronics bench.
2. Confirm basic test tools.
3. Buy or locate a known STM32 development board.
4. Buy or locate a programmer/debugger.
5. Buy low-power motor test parts.
6. Prepare a small sensor and wiring kit.
7. Create a physical evidence habit: photos, logs, labels, and test folders.

## What Not To Do Yet

Do not do these yet:

- Do not order a custom PCB.
- Do not publish a product listing.
- Do not claim CE or FCC certification.
- Do not promise shipping timelines.
- Do not buy a large batch of components.
- Do not test motors on a robot with wheels touching the table.
- Do not connect motor power without checking polarity and current limit.

## Step 1: Bench Setup

Minimum bench:

- [ ] Clear desk area.
- [ ] Non-conductive work surface.
- [ ] Good lighting.
- [ ] Small storage boxes or bags for parts.
- [ ] Labels or tape for board ID and cable labels.
- [ ] Notebook or markdown log for each test.
- [ ] Phone or camera for evidence photos.

Recommended tools:

- [ ] Digital multimeter.
- [ ] Current-limited bench power supply.
- [ ] USB data cables, not charge-only cables.
- [ ] ST-Link compatible programmer.
- [ ] Jumper wires.
- [ ] Breadboard or terminal blocks.
- [ ] Small screwdriver set.
- [ ] Tweezers.
- [ ] Anti-static bag or mat.
- [ ] Logic analyzer, optional but useful.

## Step 2: First Hardware Path

Use a development board before designing a custom PCB.

Recommended path:

```text
STM32 Nucleo board
  -> serial protocol
  -> Python SDK real serial test
  -> motor driver module
  -> IMU module
  -> encoder signal
  -> ROS2 mock-to-real validation
  -> schematic decisions
```

Reason:

- The Nucleo board reduces early hardware risk.
- The built-in debugger on many Nucleo boards reduces wiring complexity.
- Firmware and host protocol can be validated before custom PCB cost.

## Step 3: First Physical Demo Target

The first physical demo should prove only this:

```text
Host computer sends command
  -> STM32 receives command
  -> motor driver responds at low speed
  -> IMU or encoder data returns
  -> Python SDK prints status
  -> factory test log is saved
```

Do not try to build a complete robot first.

## Step 4: First Shopping List

Use [../hardware/bom/bringup_bom_v0.1.csv](../hardware/bom/bringup_bom_v0.1.csv).

Buy or locate only enough parts for bench validation:

- 1 STM32 development board
- 1 programmer/debugger if not already onboard
- 1 low-power motor driver module
- 2 small DC gear motors
- 1 IMU breakout
- 1 USB cable set
- 1 jumper wire set
- 1 safe power supply setup

## Step 5: Evidence To Capture

For each physical session, capture:

- [ ] Desk photo before test.
- [ ] Wiring photo before power.
- [ ] Power supply voltage and current limit.
- [ ] Firmware commit hash.
- [ ] SDK commit hash.
- [ ] Serial port name.
- [ ] Terminal output.
- [ ] Factory test report.
- [ ] Failure notes.

Suggested private folder:

```text
ops/factory_test_log/LOCAL-BRINGUP-001/
```

Do not commit private photos or customer data to the public repository unless intentionally anonymized.

## Step 6: First Day Physical Action

Today, do this:

1. Check what tools and parts you already own.
2. Fill `Owned / Need To Buy` in the BOM.
3. Choose one STM32 development board path.
4. Choose one motor driver module path.
5. Choose one IMU module path.
6. Set a small first-purchase budget.
7. Do not buy production quantities.

## Definition Of Ready For Physical Testing

You are ready to power hardware when:

- [ ] Board power path is understood.
- [ ] USB cable is confirmed as data cable.
- [ ] Firmware flash path is understood.
- [ ] Motor power is current-limited.
- [ ] Wheels or motor shafts are safe.
- [ ] `tools/factory_test.py --mock` passes.
- [ ] You know where logs will be saved.

