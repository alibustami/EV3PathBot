"""This module is for testing the pixels to degrees converter."""
import unittest
from typing import List
from unittest.mock import patch

import numpy as np

from src.pixels_to_degrees_ratio import convert_pixels_to_degrees


class TestConvertPixelsToDegrees(unittest.TestCase):
    """This class defines a unit test for the convert_pixels_to_degrees function."""

    @patch(
        "src.pixels_to_degrees_ratio.get_config",
        side_effect=lambda key: 10
        if key == "robot_dimensions.wheel_diameter"
        else 263
        if key == "mat_dimensions.length_x"
        else None,
    )
    @patch(
        "src.pixels_to_degrees_ratio.image_validation", return_value=np.zeros(shape=(100, 100, 3))
    )
    def test_convert_pixels_to_degrees(self, *_):
        """Test the converter."""
        distance_list: np.array = np.array([100.0, 200.0, 300.0])

        expected_degrees_list: List[int] = [3015, 6031, 9046]
        result_degrees_list: List[int] = convert_pixels_to_degrees(distance_list)
        self.assertEqual(result_degrees_list, expected_degrees_list)
