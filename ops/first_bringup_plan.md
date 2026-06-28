# First Bring-Up Plan

Goal: define the first safe physical bring-up session for the ROS2-Compatible STM32 Robot Controller Kit path.

> Status: execution plan. Use this after you have the bench parts from `hardware/bom/bringup_bom_v0.1.csv`. Do not connect motor power until the safety gates below pass.

## Scope

This plan is for the first bench session with a development board, not a custom PCB.

Primary target:

```text
Host computer
  -> STM32 development board
  -> serial command path
  -> Python SDK real serial path
  -> factory test log habit
```

Out of scope for the first session:

- custom PCB
- moving robot chassis
- high-current motor test
- production packaging
- public product listing

## Before You Start

Required repository checks:

```bash
python tools/local_smoke_check.py
```

Run it from the repository root:

```powershell
cd <repo-root>
python tools/local_smoke_check.py
```

Or run it from any directory by passing the script path:

```powershell
python <repo-root>\tools\local_smoke_check.py
```

Pass criteria:

- [ ] Factory test mock passes.
- [ ] SDK tests pass.
- [ ] SDK mock example passes.

## Safety Gates

Do not move to the next stage until the current stage passes.

### Gate 1: Desk Safety

- [ ] Work surface is clear.
- [ ] No loose metal near powered boards.
- [ ] USB cable is a data cable.
- [ ] Multimeter is available.
- [ ] Camera or phone is ready for evidence photos.

### Gate 2: Board Power

- [ ] Development board is powered by USB only.
- [ ] No motor power connected.
- [ ] No external modules connected.
- [ ] Board power LED turns on.
- [ ] Host computer detects the board or debug interface.

### Gate 3: Serial Or Debug Path

- [ ] Serial port or debug probe is visible to the host.
- [ ] Port name is recorded.
- [ ] Firmware flash method is identified.
- [ ] No motor driver is connected yet.

### Gate 4: Protocol Path

- [ ] Firmware can print or respond with version.
- [ ] Host can read version.
- [ ] Python SDK can open the real serial port.
- [ ] `PING` or equivalent connection check works.

### Gate 5: Low-Power Peripheral Test

- [ ] IMU or sensor module voltage is confirmed.
- [ ] Wiring photo is captured before power.
- [ ] Sensor can be read or failure is logged.
- [ ] No motor power connected yet.

### Gate 6: Motor Test Readiness

Motor test is allowed only after:

- [ ] Motor driver wiring is understood.
- [ ] Motor power is current-limited.
- [ ] Motors are unloaded or wheels are lifted.
- [ ] Emergency disconnect path is clear.
- [ ] `STOP` command path is known.

## Session 1: Minimum Physical Goal

Do this first:

1. Photograph the bench before connecting anything.
2. Connect STM32 development board over USB.
3. Record board name and serial/debug device.
4. Run repository mock checks.
5. Identify firmware flashing path.
6. Record what blocks real serial validation.
7. Fill `ops/bringup_session_log_template.md`.

Expected result:

```text
No motors moved.
No custom PCB used.
One clear session log exists.
Next physical blocker is explicit.
```

## Session 2: Real Serial Protocol Goal

Do this after Session 1:

1. Flash minimal firmware that can respond to `PING` and `GET_VERSION`.
2. Open serial port from host.
3. Run a small manual serial check.
4. Run Python SDK against real port.
5. Save terminal output.

Target command:

```bash
python sdk/python/examples/basic_motor_control.py --port <PORT> --left 0.0 --right 0.0 --duration 0.1
```

If firmware does not implement motor commands yet, do not force the SDK flow. Record the missing command and stop.

## Session 3: Sensor Or Motor Module Goal

Choose one path only:

```text
Path A: IMU read
Path B: motor driver low-power no-load command
```

Do not attempt both on the same first hardware day unless Session 2 is already stable.

## Evidence Requirements

Each session must produce:

- [ ] One session log.
- [ ] One bench photo.
- [ ] One wiring photo before power.
- [ ] One terminal output block.
- [ ] One clear next blocker.

Suggested private output:

```text
ops/factory_test_log/LOCAL-BRINGUP-001/
```

Do not commit private photos or raw logs if they contain personal paths, serial numbers, addresses, or customer data.

## Stop Conditions

Stop immediately if:

- Board gets hot.
- Power supply current spikes unexpectedly.
- Smoke, smell, or visible damage appears.
- Motor moves unexpectedly.
- Host cannot identify the board after cable swap.
- You are unsure about voltage or polarity.

Record the stop condition in the session log.

## Definition Of Done

The bring-up phase is ready to move forward when:

- [ ] You know which STM32 board path is being used.
- [ ] You know the real serial or debug port.
- [ ] You have at least one session log.
- [ ] Mock tests still pass.
- [ ] The next missing firmware command is explicit.
- [ ] You have not connected motor power prematurely.
