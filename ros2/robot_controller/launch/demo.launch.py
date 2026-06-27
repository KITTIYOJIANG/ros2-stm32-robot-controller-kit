from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    port = LaunchConfiguration("port")
    baudrate = LaunchConfiguration("baudrate")
    mock = LaunchConfiguration("mock")

    return LaunchDescription(
        [
            DeclareLaunchArgument("port", default_value="/dev/ttyUSB0"),
            DeclareLaunchArgument("baudrate", default_value="115200"),
            DeclareLaunchArgument("mock", default_value="true"),
            Node(
                package="robot_controller",
                executable="robot_controller_node",
                name="robot_controller_node",
                output="screen",
                parameters=[
                    {
                        "port": port,
                        "baudrate": baudrate,
                        "mock": mock,
                    }
                ],
            ),
        ]
    )
