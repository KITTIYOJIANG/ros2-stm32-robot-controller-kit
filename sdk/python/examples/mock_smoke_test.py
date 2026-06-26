from robot_controller import RobotController


def main() -> None:
    board = RobotController.mock()
    try:
        print("ping:", board.ping())
        print("version:", board.get_version())
        print("status:", board.get_status())
        board.set_motor_speed(0.1, 0.1)
        print("imu:", board.read_imu())
        print("encoder:", board.read_encoder())
        board.stop()
        print("final_status:", board.get_status())
    finally:
        board.close()


if __name__ == "__main__":
    main()
