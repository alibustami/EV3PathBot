"""This module is for testing the pixels to degrees converter."""
import unittest
from typing import List, Tuple

import numpy as np

from src.pixels_to_degrees_ratio import convert_pixels_to_degrees


class TestConvertPixelsToDegrees(unittest.TestCase):
    """This class defines a unit test for the convert_pixels_to_degrees function."""

    def test_convert_pixels_to_degrees(self):
        """Test the converter."""
        img_dims: Tuple[int] = (0, 236, 0)
        distance_list: List[float] = [100, 200, 300]
        wheel_diameter: float = 10
        expected_degrees_list: List[float] = [1147, 2295, 3442]
        result_degrees_list: List[float] = convert_pixels_to_degrees(
            img_dims, distance_list, wheel_diameter
        )
        self.assertEqual(result_degrees_list, expected_degrees_list)
