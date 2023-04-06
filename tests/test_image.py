"""This module contains tests for image_reader.py module."""
import os
import unittest

import cv2 as cv
import numpy as np
import numpy.tests as npt

from src import image_reader


class TestImage(unittest.TestCase):
    """This class contains tests for image reading."""

    def test_image_reader(self):
        """This function contains tests for image reading."""
        path = os.path.join("tests", "fixtures", "cargo1.jpg")
        img: np.ndarray = cv.imread(path)
        npt.assert_errey_equal(img, image_reader.image_validation(path))
