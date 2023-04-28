"""Test cases for motors extraction."""
import unittest
from unittest.mock import patch

from src.motors_extraction import motors_extraction


class TestMotorsExtraction(unittest.TestCase):
    """Test cases for motors extraction."""

    @patch(
        "src.motors_extraction.get_config",
        side_effect=lambda key: {
            "motor_a": "large",
            "motor_b": "medium",
            "motor_c": "large",
            "motor_d": "medium",
        }
        if key == "robot_motors"
        else None,
    )
    def test_motors_extraction(self, mock_get_config):
        """test_motors_extraction."""
        expected_large_motors_list = ["a", "c"]
        expected_medium_motors_list = ["b", "d"]
        self.assertEqual(
            motors_extraction(), (expected_large_motors_list, expected_medium_motors_list)
        )

    @patch(
        "src.motors_extraction.get_config",
        side_effect=lambda key: {} if key == "robot_motors" else None,
    )
    def test_motors_extraction_exception(self, *_):
        """test_motors_extraction_exception."""
        with self.assertRaises(Exception):
            motors_extraction()
