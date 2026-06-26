"""SDK exception hierarchy."""


class RobotControllerError(Exception):
    """Base exception for the robot controller SDK."""


class TransportError(RobotControllerError):
    """Raised when the host cannot communicate with the board."""


class ProtocolError(RobotControllerError):
    """Raised when a board response cannot be parsed or validated."""


class FirmwareError(RobotControllerError):
    """Raised when firmware returns an ERROR response."""


class VersionMismatchError(RobotControllerError):
    """Raised when firmware protocol version is not supported by this SDK."""
