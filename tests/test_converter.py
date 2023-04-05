"""This module is for testing the pixels to degrees converter."""
import unittest
from typing import List

import numpy as np

from src.pixels_to_degrees_ratio import convert_pixels_to_degrees


class TestConvertPixelsToDegrees(unittest.TestCase):
    """This class defines a unit test for the convert_pixels_to_degrees function.

    Parameters
    ----------
    unittest : TestCase
        A subclass of unittest.TestCase that defines the individual unit tests.
    """

    def test_convert_pixels_to_degrees(self):
        """Test the converter."""
        img = np.zeros((100, 236), dtype=np.uint8)
        distance_list: List[float] = [100, 200, 300]
        wheel_diameter: float = 10
        expected_degrees_list: List[float] = [1147, 2295, 3442]
        result_degrees_list: List[float] = convert_pixels_to_degrees(
            img, distance_list, wheel_diameter
        )
        self.assertEqual(result_degrees_list, expected_degrees_list)
