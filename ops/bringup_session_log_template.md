# Bring-Up Session Log Template

Copy this file into a private session folder before each physical session.

Suggested private path:

```text
ops/factory_test_log/LOCAL-BRINGUP-001/session_log.md
```

Do not commit private photos, raw customer data, tracking numbers, or personal machine paths to the public repository.

## Session Metadata

```text
Session ID:
Date:
Operator:
Repository commit:
Branch:
Host computer:
Operating system:
STM32 board:
Debugger / programmer:
Serial port:
Power supply:
Current limit:
```

## Session Goal

```text
Example: Identify STM32 serial/debug path and confirm mock tests pass before real firmware validation.
```

## Parts Used

| Item | Exact Part | Source | Notes |
| --- | --- | --- | --- |
| STM32 board |  |  |  |
| Debugger |  |  |  |
| USB cable |  |  |  |
| Motor driver |  |  |  |
| Motor |  |  |  |
| Sensor |  |  |  |
| Power supply |  |  |  |

## Pre-Power Checklist

- [ ] Desk is clear.
- [ ] Wiring photo captured.
- [ ] Voltage checked.
- [ ] Polarity checked.
- [ ] Current limit set.
- [ ] Motors unloaded or disconnected.
- [ ] USB cable confirmed as data cable.
- [ ] Emergency disconnect path clear.

## Commands Run

```bash

```

## Observed Output

```text

```

## Measurements

| Measurement | Value | Notes |
| --- | --- | --- |
| Logic voltage |  |  |
| Motor supply voltage |  |  |
| Current limit |  |  |
| Idle current |  |  |
| Active current |  |  |

## Photos Captured

- [ ] Bench before wiring
- [ ] Wiring before power
- [ ] Board top
- [ ] Board bottom
- [ ] Terminal output or screenshot

## Result

```text
PASS / FAIL / BLOCKED
```

## Blockers

- 

## Next Physical Action

- 

## Documentation Updates Needed

- [ ] Quick Start
- [ ] Troubleshooting
- [ ] Hardware overview
- [ ] Firmware overview
- [ ] BOM
- [ ] Factory test script

