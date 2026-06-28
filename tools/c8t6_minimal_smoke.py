"""Smoke test for the STM32F103C8T6 minimal bring-up firmware.

This test intentionally checks only the first real-hardware protocol surface:

- PING -> ACK PING
- GET_VERSION -> VERSION firmware=... protocol=... board=...
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SDK_PATH = REPO_ROOT / "sdk" / "python"
if str(SDK_PATH) not in sys.path:
    sys.path.insert(0, str(SDK_PATH))

from robot_controller import RobotController  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True, help="Serial port, for example COM3 or /dev/ttyUSB0")
    parser.add_argument("--baudrate", type=int, default=115200, help="Serial baudrate")
    parser.add_argument("--timeout", type=float, default=1.0, help="Serial timeout in seconds")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    board = RobotController(port=args.port, baudrate=args.baudrate, timeout=args.timeout)
    try:
        if not board.ping():
            print("ping: FAIL")
            return 1
        print("ping: PASS")

        version = board.get_version()
        print(f"version: {version}")
        return 0
    finally:
        board.close()


if __name__ == "__main__":
    raise SystemExit(main())
