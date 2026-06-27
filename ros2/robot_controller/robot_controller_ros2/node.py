from __future__ import annotations

from typing import Any

import rclpy
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import Imu
from std_msgs.msg import Int32MultiArray

from robot_controller import RobotController


class RobotControllerNode(Node):
    def __init__(self) -> None:
        super().__init__("robot_controller_node")

        self.declare_parameter("port", "/dev/ttyUSB0")
        self.declare_parameter("baudrate", 115200)
        self.declare_parameter("mock", True)
        self.declare_parameter("publish_rate_hz", 20.0)
        self.declare_parameter("command_timeout_ms", 500)
        self.declare_parameter("frame_id", "imu_link")

        self.frame_id = self.get_parameter("frame_id").value
        self.board = self._create_board()
        self.version = self.board.get_version()

        self.imu_pub = self.create_publisher(Imu, "/imu/data", 10)
        self.encoder_pub = self.create_publisher(Int32MultiArray, "/encoder", 10)
        self.diag_pub = self.create_publisher(DiagnosticArray, "/diagnostics", 10)
        self.cmd_sub = self.create_subscription(Twist, "/wheel_cmd", self._on_wheel_cmd, 10)

        publish_rate = float(self.get_parameter("publish_rate_hz").value)
        period_s = 1.0 / publish_rate if publish_rate > 0.0 else 0.05
        self.timer = self.create_timer(period_s, self._publish_samples)

        self.get_logger().info(
            f"robot controller connected: firmware={self.version.firmware} "
            f"protocol={self.version.protocol} board={self.version.board}"
        )

    def destroy_node(self) -> bool:
        try:
            self.board.stop()
            self.board.close()
        finally:
            return super().destroy_node()

    def _create_board(self) -> RobotController:
        mock = _as_bool(self.get_parameter("mock").value)
        if mock:
            return RobotController.mock()

        port = str(self.get_parameter("port").value)
        baudrate = int(self.get_parameter("baudrate").value)
        return RobotController(port, baudrate=baudrate)

    def _on_wheel_cmd(self, msg: Twist) -> None:
        left = float(msg.linear.x - msg.angular.z)
        right = float(msg.linear.x + msg.angular.z)
        left = max(min(left, 1.0), -1.0)
        right = max(min(right, 1.0), -1.0)
        self.board.set_motor_speed(left, right)

    def _publish_samples(self) -> None:
        imu_sample = self.board.read_imu()
        encoder_sample = self.board.read_encoder()
        status = self.board.get_status()

        imu_msg = Imu()
        imu_msg.header.stamp = self.get_clock().now().to_msg()
        imu_msg.header.frame_id = str(self.frame_id)
        imu_msg.linear_acceleration.x = imu_sample.ax
        imu_msg.linear_acceleration.y = imu_sample.ay
        imu_msg.linear_acceleration.z = imu_sample.az
        imu_msg.angular_velocity.x = imu_sample.gx
        imu_msg.angular_velocity.y = imu_sample.gy
        imu_msg.angular_velocity.z = imu_sample.gz
        self.imu_pub.publish(imu_msg)

        encoder_msg = Int32MultiArray()
        encoder_msg.data = [encoder_sample.left, encoder_sample.right]
        self.encoder_pub.publish(encoder_msg)

        diag = DiagnosticArray()
        diag.header.stamp = self.get_clock().now().to_msg()
        diag.status.append(_status_to_diagnostic(status))
        self.diag_pub.publish(diag)


def _status_to_diagnostic(status: Any) -> DiagnosticStatus:
    msg = DiagnosticStatus()
    msg.name = "robot_controller"
    msg.hardware_id = "stm32_robot_controller"
    msg.level = DiagnosticStatus.ERROR if status.error != "ERR_OK" else DiagnosticStatus.OK
    msg.message = status.error
    msg.values = [
        KeyValue(key="state", value=str(status.state)),
        KeyValue(key="uptime_ms", value=str(status.uptime_ms)),
        KeyValue(key="motor_fault", value=str(status.motor_fault)),
        KeyValue(key="imu_ready", value=str(status.imu_ready)),
        KeyValue(key="encoder_ready", value=str(status.encoder_ready)),
    ]
    return msg


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in {"1", "true", "yes", "on"}
    return bool(value)


def main() -> None:
    rclpy.init()
    node = RobotControllerNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
