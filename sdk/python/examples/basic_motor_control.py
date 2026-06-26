import argparse
import time

from robot_controller import RobotController


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a basic motor command.")
    parser.add_argument("--port", default="", help="Serial port such as /dev/ttyUSB0 or COM3.")
    parser.add_argument("--mock", action="store_true", help="Use mock transport.")
    parser.add_argument("--left", type=float, default=0.1)
    parser.add_argument("--right", type=float, default=0.1)
    parser.add_argument("--duration", type=float, default=1.0)
    args = parser.parse_args()

    if args.mock:
        board = RobotController.mock()
    else:
        if not args.port:
            raise SystemExit("--port is required unless --mock is set")
        board = RobotController(args.port)

    try:
        print(board.get_version())
        board.set_motor_speed(args.left, args.right)
        time.sleep(max(args.duration, 0.0))
        board.stop()
        print(board.get_status())
    finally:
        board.close()


if __name__ == "__main__":
    main()
