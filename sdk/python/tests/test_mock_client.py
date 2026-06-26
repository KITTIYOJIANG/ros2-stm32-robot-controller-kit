import unittest

from robot_controller import RobotController


class MockClientTest(unittest.TestCase):
    def test_mock_smoke_flow(self) -> None:
        board = RobotController.mock()
        self.assertTrue(board.ping())
        self.assertEqual(board.get_version().protocol, "0.1")
        self.assertEqual(board.get_status().error, "ERR_OK")
        board.set_motor_speed(0.1, 0.1)
        self.assertEqual(board.get_status().state, "RUNNING")
        self.assertGreater(board.read_imu().az, 9.0)
        self.assertEqual(board.read_encoder().left, 1234)
        board.stop()
        self.assertEqual(board.get_status().state, "IDLE")
        board.close()

    def test_speed_validation(self) -> None:
        board = RobotController.mock()
        with self.assertRaises(ValueError):
            board.set_motor_speed(1.5, 0.0)


if __name__ == "__main__":
    unittest.main()
