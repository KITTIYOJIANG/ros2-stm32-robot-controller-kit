"""High-level RobotController client."""

from __future__ import annotations

from dataclasses import dataclass

from .exceptions import FirmwareError, ProtocolError, VersionMismatchError
from .transport import MockTransport, SerialTransport, Transport


SUPPORTED_PROTOCOL_PREFIX = "0.1"


@dataclass(frozen=True)
class VersionInfo:
    firmware: str
    protocol: str
    board: str


@dataclass(frozen=True)
class BoardStatus:
    state: str
    error: str
    uptime_ms: int
    motor_fault: bool
    imu_ready: bool
    encoder_ready: bool


@dataclass(frozen=True)
class ImuSample:
    ax: float
    ay: float
    az: float
    gx: float
    gy: float
    gz: float


@dataclass(frozen=True)
class EncoderSample:
    left: int
    right: int


class RobotController:
    """Client for the robot controller serial protocol."""

    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        timeout: float = 1.0,
        transport: Transport | None = None,
    ) -> None:
        self._transport = transport or SerialTransport(port, baudrate=baudrate, timeout=timeout)

    @classmethod
    def mock(cls) -> "RobotController":
        return cls(port="MOCK", transport=MockTransport())

    def close(self) -> None:
        self._transport.close()

    def ping(self) -> bool:
        response = self._query("PING")
        return response == "ACK PING"

    def get_version(self, validate: bool = True) -> VersionInfo:
        response = self._query("GET_VERSION")
        self._expect_prefix(response, "VERSION")
        values = _parse_key_values(response)
        version = VersionInfo(
            firmware=values.get("firmware", ""),
            protocol=values.get("protocol", ""),
            board=values.get("board", ""),
        )
        if validate and not version.protocol.startswith(SUPPORTED_PROTOCOL_PREFIX):
            raise VersionMismatchError(
                f"unsupported protocol {version.protocol}; expected {SUPPORTED_PROTOCOL_PREFIX}.x"
            )
        return version

    def get_status(self) -> BoardStatus:
        response = self._query("GET_STATUS")
        self._expect_prefix(response, "STATUS")
        values = _parse_key_values(response)
        return BoardStatus(
            state=values.get("state", "UNKNOWN"),
            error=values.get("error", "ERR_UNKNOWN"),
            uptime_ms=_to_int(values.get("uptime_ms", "0")),
            motor_fault=_to_bool(values.get("motor_fault", "0")),
            imu_ready=_to_bool(values.get("imu_ready", "0")),
            encoder_ready=_to_bool(values.get("encoder_ready", "0")),
        )

    def set_motor_speed(self, left: float, right: float) -> None:
        _validate_speed(left, "left")
        _validate_speed(right, "right")
        response = self._query(f"SET_MOTOR left={left:.2f} right={right:.2f}")
        self._expect_ack(response, "SET_MOTOR")

    def stop(self) -> None:
        response = self._query("STOP")
        self._expect_ack(response, "STOP")

    def read_imu(self) -> ImuSample:
        response = self._query("READ_IMU")
        self._expect_prefix(response, "IMU")
        values = _parse_key_values(response)
        return ImuSample(
            ax=_to_float(values.get("ax", "0")),
            ay=_to_float(values.get("ay", "0")),
            az=_to_float(values.get("az", "0")),
            gx=_to_float(values.get("gx", "0")),
            gy=_to_float(values.get("gy", "0")),
            gz=_to_float(values.get("gz", "0")),
        )

    def read_encoder(self) -> EncoderSample:
        response = self._query("READ_ENCODER")
        self._expect_prefix(response, "ENCODER")
        values = _parse_key_values(response)
        return EncoderSample(
            left=_to_int(values.get("left", "0")),
            right=_to_int(values.get("right", "0")),
        )

    def _query(self, command: str) -> str:
        response = self._transport.query(command)
        if response.startswith("ERROR"):
            raise FirmwareError(response)
        return response

    @staticmethod
    def _expect_ack(response: str, command: str) -> None:
        expected = f"ACK {command}"
        if response != expected:
            raise ProtocolError(f"expected {expected!r}, got {response!r}")

    @staticmethod
    def _expect_prefix(response: str, prefix: str) -> None:
        if not response.startswith(prefix):
            raise ProtocolError(f"expected prefix {prefix!r}, got {response!r}")


def _parse_key_values(line: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for token in line.split()[1:]:
        if "=" not in token:
            continue
        key, value = token.split("=", 1)
        values[key] = value.strip('"')
    return values


def _to_bool(value: str) -> bool:
    return value in {"1", "true", "True", "yes", "YES"}


def _to_float(value: str) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise ProtocolError(f"invalid float value {value!r}") from exc


def _to_int(value: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise ProtocolError(f"invalid int value {value!r}") from exc


def _validate_speed(value: float, name: str) -> None:
    if value < -1.0 or value > 1.0:
        raise ValueError(f"{name} speed must be between -1.0 and 1.0")
