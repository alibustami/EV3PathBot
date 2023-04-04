import unittest
from src.pixels_to_degrees_ratio import convert_pixels_to_degrees
import numpy as np

class TestConvertPixelsToDegrees(unittest.TestCase):
    def test_convert_pixels_to_degrees(self):
        img = np.zeros((100, 236), dtype=np.uint8)
        distance_list = [100, 200, 300]
        wheel_diameter = 10
        expected_degrees_list = [1147, 2295, 3442]
        result_degrees_list = convert_pixels_to_degrees(img, distance_list, wheel_diameter)
        self.assertEqual(result_degrees_list, expected_degrees_list)

