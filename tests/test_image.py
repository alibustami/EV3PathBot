"""This module contains tests for configs.py module."""
import unittest
from unittest.mock import patch

from src import image_reader


class TestImage(unittest.TestCase):
    """This class contains tests for image reading"""

    def test_a(self):
        path = r"C:\Users\walee\Desktop\final\cargo1.jpg"
        self.assertEqual(2, image_reader.img_reading(path))
