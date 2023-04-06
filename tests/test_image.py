"""This module contains tests for image_reader.py module."""
import unittest

import cv2 as cv
import numpy as np

from src import image_reader


class TestImage(unittest.TestCase):
    """This class contains tests for image reading."""

    def test_image_reader(self):
        """This function contains tests for image reading."""
        path = r"C:\Users\walee\Desktop\final\cargo1.jpg"
        img: np.ndarray = cv.imread(path)
        self.assertTrue(np.array_equal(img, image_reader.image_validation(path)))
