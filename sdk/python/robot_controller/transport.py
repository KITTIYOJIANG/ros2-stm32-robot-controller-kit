"""Transport implementations for board communication."""

from __future__ import annotations

import time
from typing import Protocol as TypingProtocol

from .exceptions import TransportError


class Transport(TypingProtocol):
    def query(self, command: str) -> str:
        ...

    def close(self) -> None:
        ...


class MockTransport:
    """Mock transport matching the draft firmware protocol."""

    def __init__(self) -> None:
        self.state = "IDLE"

    def query(self, command: str) -> str:
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
            return "IMU ax=0.000 ay=0.000 az=9.800 gx=0.000 gy=0.000 gz=0.000"
        if command == "READ_ENCODER":
            return "ENCODER left=1234 right=1230"
        return 'ERROR code=0x0001 name=ERR_BAD_COMMAND message="unknown command"'

    def close(self) -> None:
        return None


class SerialTransport:
    """Line-oriented serial transport for real firmware."""

    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 1.0) -> None:
        try:
            import serial  # type: ignore
        except ImportError as exc:
            raise TransportError(
                "pyserial is required for real hardware mode. "
                "Install with: python -m pip install -e .[serial]"
            ) from exc

        try:
            self._serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        except Exception as exc:  # noqa: BLE001 - pyserial raises platform-specific errors.
            raise TransportError(f"failed to open serial port {port!r}: {exc}") from exc

        self._timeout = timeout
        time.sleep(0.2)

    def query(self, command: str) -> str:
        payload = (command.strip() + "\n").encode("utf-8")
        try:
            self._serial.write(payload)
            self._serial.flush()
            response = self._serial.readline().decode("utf-8", errors="replace").strip()
        except Exception as exc:  # noqa: BLE001 - pyserial raises platform-specific errors.
            raise TransportError(f"serial query failed for {command!r}: {exc}") from exc

        if not response:
            raise TransportError(f"serial timeout after {self._timeout}s for {command!r}")
        return response

    def close(self) -> None:
        self._serial.close()
