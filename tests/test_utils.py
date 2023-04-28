"""This moduel contains the unit testing for utilties."""
import unittest
from unittest.mock import patch

from src.utils import PIDConfigs, extract_pid_constants


class TestUtilites(unittest.TestCase):
    """This class for testing the utilities."""

    def test_extraction_with_value(self):
        """Test extraction with values from function."""
        pid_constants = extract_pid_constants(
            "gyro",
            constants=(1, 1, 1),
            accepted_error=1,
            sensor_port="1",
        )
        expected_output = PIDConfigs(
            **{
                "kp": 1,
                "ki": 1,
                "kd": 1,
                "accepted_error": 1,
                "sensor": "gyro",
                "sensor_port": 1,
            }
        )
        self.assertEqual(pid_constants, expected_output)

    @patch(
        "src.utils.get_config",
        side_effect=lambda key: 1
        if key
        in [
            "pid_constants.accepted_error",
            "pid_constants.kp",
            "pid_constants.ki",
            "pid_constants.kd",
        ]
        else {"port_1": "GYRO"}
        if key == "robot_sensors"
        else None,
    )
    def test_extraction_with_values_from_config(self, *_):
        """Test extraction with values from config."""
        pid_constants = extract_pid_constants("gyro")
        expected_output = PIDConfigs(
            **{
                "kp": 1,
                "ki": 1,
                "kd": 1,
                "accepted_error": 1,
                "sensor": "gyro",
                "sensor_port": 1,
            }
        )
        self.assertEqual(pid_constants, expected_output)

    @patch("src.utils.get_config", return_value=None)
    def test_extraction_without_values(self, *_):
        """Test extraction without values from function."""
        with self.assertRaises(ValueError):
            extract_pid_constants("any")

    @patch(
        "src.utils.get_config",
        side_effect=lambda key: 1 if key == "pid_constants.accepted_error" else None,
    )
    def test_extraction_with_accepted_error_from_config(self, *_):
        """Test extraction with accepted error from config."""
        with self.assertRaises(ValueError):
            extract_pid_constants("any")
