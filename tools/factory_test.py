#!/usr/bin/env python3
"""Factory test runner for the ROS2-Compatible STM32 Robot Controller Kit.

This script is intentionally useful before real hardware exists:
- Use --mock to validate the factory-test workflow without a board.
- Use --port when real firmware and serial protocol are available.

The protocol is based on docs/api_reference.md and should be updated together
with firmware, Python SDK, and ROS2 package changes.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Protocol


PASS = "PASS"
FAIL = "FAIL"
SKIP = "SKIP"


class Transport(Protocol):
    def query(self, command: str, timeout_s: float = 1.0) -> str:
        ...

    def close(self) -> None:
        ...


class MockTransport:
    """Mock board responses for workflow validation."""

    def __init__(self) -> None:
        self.state = "IDLE"

    def query(self, command: str, timeout_s: float = 1.0) -> str:
        command = command.strip()
        if command == "PING":
            return "ACK PING"
        if command == "GET_VERSION":
            return "VERSION firmware=0.1.0 protocol=0.1 board=stm32_robot_controller"
        if command == "GET_STATUS":
            return (
                f"STATUS state={self.state} error=ERR_OK uptime_ms=12345 "
                "motor_fault=0 imu_ready=1 encoder_ready=1"
            )
        if command.startswith("SET_MOTOR"):
            self.state = "RUNNING"
            return "ACK SET_MOTOR"
        if command == "STOP":
            self.state = "IDLE"
            return "ACK STOP"
        if command == "READ_IMU":
            return "IMU ax=0.00 ay=0.00 az=9.80 gx=0.00 gy=0.00 gz=0.00"
        if command == "READ_ENCODER":
            return "ENCODER left=1234 right=1230"
        return 'ERROR code=0x0001 name=ERR_BAD_COMMAND message="unknown command"'

    def close(self) -> None:
        return None


class SerialLineTransport:
    """Line-oriented serial transport.

    Requires pyserial:
        python -m pip install pyserial
    """

    def __init__(self, port: str, baudrate: int, timeout_s: float) -> None:
        try:
            import serial  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "pyserial is required for real hardware mode. "
                "Install it with: python -m pip install pyserial"
            ) from exc

        self._serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout_s)
        time.sleep(0.2)

    def query(self, command: str, timeout_s: float = 1.0) -> str:
        self._serial.timeout = timeout_s
        payload = (command.strip() + "\n").encode("utf-8")
        self._serial.write(payload)
        self._serial.flush()
        response = self._serial.readline().decode("utf-8", errors="replace").strip()
        if not response:
            raise TimeoutError(f"no response for command: {command}")
        return response

    def close(self) -> None:
        self._serial.close()


@dataclass
class TestResult:
    name: str
    status: str
    command: str
    response: str
    notes: str = ""


@dataclass
class FactoryTestReport:
    order_id: str
    board_id: str
    operator: str
    mode: str
    port: str
    baudrate: int
    started_at: str
    finished_at: str
    overall_status: str
    results: list[TestResult]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def safe_order_id() -> str:
    return datetime.now().strftime("ORDER-%Y%m%d-%H%M%S")


def run_query_test(
    transport: Transport,
    name: str,
    command: str,
    expected_prefixes: Iterable[str],
    required_text: Iterable[str] = (),
) -> TestResult:
    try:
        response = transport.query(command)
    except Exception as exc:  # noqa: BLE001 - factory logs should record exact failure text.
        return TestResult(name=name, status=FAIL, command=command, response="", notes=str(exc))

    prefix_ok = any(response.startswith(prefix) for prefix in expected_prefixes)
    text_ok = all(text in response for text in required_text)
    status = PASS if prefix_ok and text_ok else FAIL
    notes = "" if status == PASS else "unexpected response"
    return TestResult(name=name, status=status, command=command, response=response, notes=notes)


def run_motion_test(
    transport: Transport,
    left: float,
    right: float,
    duration_s: float,
    enabled: bool,
) -> list[TestResult]:
    if not enabled:
        return [
            TestResult(
                name="low_speed_motor",
                status=SKIP,
                command="SET_MOTOR",
                response="",
                notes="motion disabled; rerun with --enable-motion on a safe test stand",
            )
        ]

    results: list[TestResult] = []
    command = f"SET_MOTOR left={left:.2f} right={right:.2f}"
    results.append(run_query_test(transport, "low_speed_motor", command, ["ACK SET_MOTOR"]))
    time.sleep(max(duration_s, 0.0))
    results.append(run_query_test(transport, "stop_after_motor_test", "STOP", ["ACK STOP"]))
    return results


def run_factory_test(args: argparse.Namespace) -> FactoryTestReport:
    started_at = utc_now()
    mode = "mock" if args.mock else "serial"
    port = "MOCK" if args.mock else args.port

    if args.mock:
        transport: Transport = MockTransport()
    else:
        if not args.port:
            raise ValueError("real hardware mode requires --port, or use --mock")
        transport = SerialLineTransport(args.port, args.baudrate, args.timeout)

    results: list[TestResult] = []
    try:
        results.append(run_query_test(transport, "connection_ping", "PING", ["ACK PING"]))
        results.append(run_query_test(transport, "firmware_version", "GET_VERSION", ["VERSION"]))
        results.append(
            run_query_test(
                transport,
                "initial_status",
                "GET_STATUS",
                ["STATUS"],
                required_text=["ERR_OK"],
            )
        )
        results.append(run_query_test(transport, "safe_stop", "STOP", ["ACK STOP"]))
        results.extend(
            run_motion_test(
                transport,
                left=args.motor_speed,
                right=args.motor_speed,
                duration_s=args.motor_duration,
                enabled=args.enable_motion,
            )
        )
        results.append(run_query_test(transport, "imu_read", "READ_IMU", ["IMU"], ["ax=", "gx="]))
        results.append(
            run_query_test(
                transport,
                "encoder_read",
                "READ_ENCODER",
                ["ENCODER"],
                ["left=", "right="],
            )
        )
        results.append(
            run_query_test(
                transport,
                "final_status",
                "GET_STATUS",
                ["STATUS"],
                required_text=["ERR_OK"],
            )
        )
    finally:
        transport.close()

    overall_status = PASS
    if any(result.status == FAIL for result in results):
        overall_status = FAIL

    return FactoryTestReport(
        order_id=args.order,
        board_id=args.board_id,
        operator=args.operator,
        mode=mode,
        port=port,
        baudrate=args.baudrate,
        started_at=started_at,
        finished_at=utc_now(),
        overall_status=overall_status,
        results=results,
    )


def write_report(report: FactoryTestReport, output_dir: Path) -> Path:
    order_dir = output_dir / report.order_id
    order_dir.mkdir(parents=True, exist_ok=True)

    json_path = order_dir / "factory_test.json"
    md_path = order_dir / "factory_test.md"

    data = asdict(report)
    json_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Factory Test Report",
        "",
        f"Order ID: {report.order_id}",
        f"Board ID: {report.board_id}",
        f"Operator: {report.operator}",
        f"Mode: {report.mode}",
        f"Port: {report.port}",
        f"Baudrate: {report.baudrate}",
        f"Started At: {report.started_at}",
        f"Finished At: {report.finished_at}",
        f"Overall Status: {report.overall_status}",
        "",
        "| Test | Status | Command | Response | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for result in report.results:
        lines.append(
            "| "
            + " | ".join(
                [
                    result.name,
                    result.status,
                    result.command.replace("|", "/"),
                    result.response.replace("|", "/"),
                    result.notes.replace("|", "/"),
                ]
            )
            + " |"
        )
    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run factory tests for a robot controller kit.")
    parser.add_argument("--mock", action="store_true", help="Run against mock board responses.")
    parser.add_argument("--port", default="", help="Serial port, for example /dev/ttyUSB0 or COM3.")
    parser.add_argument("--baudrate", type=int, default=115200, help="Serial baud rate.")
    parser.add_argument("--timeout", type=float, default=1.0, help="Serial read timeout in seconds.")
    parser.add_argument("--order", default=safe_order_id(), help="Order ID for report folder.")
    parser.add_argument("--board-id", default="UNKNOWN", help="Board serial or inventory ID.")
    parser.add_argument("--operator", default="UNKNOWN", help="Test operator name.")
    parser.add_argument(
        "--output-dir",
        default="ops/factory_test_log",
        help="Directory for generated private test reports.",
    )
    parser.add_argument(
        "--enable-motion",
        action="store_true",
        help="Enable low-speed motor motion test. Use only on a safe test stand.",
    )
    parser.add_argument("--motor-speed", type=float, default=0.10, help="Low-speed test command.")
    parser.add_argument("--motor-duration", type=float, default=1.0, help="Motor test duration.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        report = run_factory_test(args)
        report_path = write_report(report, Path(args.output_dir))
    except Exception as exc:  # noqa: BLE001 - command line tool should print user-facing error.
        print(f"factory test failed before report generation: {exc}", file=sys.stderr)
        return 2

    print(f"Factory test report: {report_path}")
    print(f"Overall status: {report.overall_status}")
    for result in report.results:
        print(f"{result.status:4} {result.name}: {result.response or result.notes}")

    return 0 if report.overall_status == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
