# ROS2 Package

Goal: provide the first ROS2 integration skeleton for the ROS2-Compatible STM32 Robot Controller Kit.

> Status: mock skeleton. The package defines node structure, launch file, and config. It is not yet validated inside a ROS2 workspace with real hardware.

## Package Name

```text
robot_controller
```

Python module name:

```text
robot_controller_ros2
```

The module name intentionally differs from the Python SDK package name to avoid import conflicts.

## Planned Topics

| Topic | Type | Direction | Purpose |
| --- | --- | --- | --- |
| `/wheel_cmd` | `geometry_msgs/msg/Twist` | Subscribe | Receive velocity command |
| `/imu/data` | `sensor_msgs/msg/Imu` | Publish | Publish IMU sample |
| `/encoder` | `std_msgs/msg/Int32MultiArray` | Publish | Publish left/right encoder count |
| `/diagnostics` | `diagnostic_msgs/msg/DiagnosticArray` | Publish | Publish board health |

## Planned Parameters

| Parameter | Default | Purpose |
| --- | --- | --- |
| `port` | `/dev/ttyUSB0` | Serial port |
| `baudrate` | `115200` | Serial baud rate |
| `mock` | `true` | Use SDK mock transport |
| `publish_rate_hz` | `20.0` | Sensor publish rate |
| `command_timeout_ms` | `500` | Motor command timeout |
| `frame_id` | `imu_link` | IMU frame id |

## Draft Launch

```bash
ros2 launch robot_controller demo.launch.py mock:=true
ros2 launch robot_controller demo.launch.py port:=/dev/ttyUSB0 mock:=false
```

## Next Tasks

- [ ] Validate in a ROS2 Humble workspace.
- [ ] Add message type for encoder data if `Int32MultiArray` is insufficient.
- [ ] Add diagnostics updater integration.
- [ ] Add real hardware smoke test.
- [ ] Add README screenshots and topic output.
