"""Unit testing for path creation module."""
import unittest
from unittest.mock import patch

import cv2
import numpy as np

from src.path_creation import create_path


class TestPathCreation(unittest.TestCase):
    """Unit testing for path creation module."""

    @patch("src.path_creation.motors_extraction", return_value=(None, ["A", "D"]))
    @patch("src.path_creation.convert_pixels_to_degrees", return_value=[945, 476, 779, 556, 833])
    def test_create_path(self, *_):
        """Test create path function."""
        robot_positions = np.array(
            [
                ([[10.0, 685.0], [147.0, 685.0], [147.0, 805.0], [10.0, 805.0]]),
                ([[10.0, 430.0], [147.0, 430.0], [147.0, 550.0], [10.0, 550.0]]),
                ([[138.5, 421.5], [138.5, 558.5], [18.5, 558.5], [18.5, 421.5]]),
                ([[348.5, 421.5], [348.5, 558.5], [228.5, 558.5], [228.5, 421.5]]),
                (
                    [
                        [330.94818224, 570.56303013],
                        [203.04766381, 521.46662105],
                        [246.05181776, 409.43696987],
                        [373.95233619, 458.53337895],
                    ]
                ),
                (
                    [
                        [250.94818224, 780.56303013],
                        [123.04766381, 731.46662105],
                        [166.05181776, 619.43696987],
                        [293.95233619, 668.53337895],
                    ]
                ),
            ]
        )
        angles = [0, 0, 90, 90, 201, 201]
        additional_motor_1 = [0, -100, 0, 110, 0, 0]
        additional_motor_2 = [0, 0, 0, 0, 0, 0]
        additional_motors_mode = ["P", "P", "P", "S", "S", "S"]
        robot_speed_dps = [500, 300, 300, 500, 300, 300]
        expected = {
            "x": [10, 10, 138, 348, 330, 250],
            "y": [685, 430, 421, 421, 570, 780],
            "angle": [0, 0, 90, 90, 201, 201],
            "A": [0, -100, 0, 110, 0, 0],
            "D": [0, 0, 0, 0, 0, 0],
            "action": ["None", "backward", "Rotate", "forward", "Rotate", "backward"],
            "additional_motors_mode": ["P", "P", "P", "S", "S", "S"],
            "angles_difference": [0, 90, 0, 111, 0],
            "distance_degrees": [945, 476, 779, 556, 833],
            "speed": [500, 300, 300, 500, 300, 300],
        }

        result = create_path(
            robot_positions,
            angles,
            additional_motor_1,
            additional_motor_2,
            additional_motors_mode,
            robot_speed_dps,
        )
        self.assertEqual(result, expected)
