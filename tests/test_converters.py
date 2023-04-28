"""Unit testing for the converters module."""
import unittest
from unittest.mock import patch

import numpy as np

from src.converters import (
    extract_image_dims,
    mm_to_pixel,
    mm_to_stud,
    pixel_to_mm,
    pixel_to_stud,
    stud_to_mm,
    stud_to_pixel,
)


class TestConverters(unittest.TestCase):
    """Test cases for converters."""

    @patch(
        "src.converters.get_config",
        side_effect=lambda key: "src/GUIs/assets/mat-grid.png"
        if key == "mat_image_path"
        else 2020.20
        if key == "mat_dimensions.width_y"
        else 1143
        if key == "mat_dimensions.length_x"
        else None,
    )
    def test_extract_image_dims(self, mock_get_config):
        """test_extract_image_dims."""
        expected_image_dims = (810, 1461)
        expected_mat_dims = (1143, 2020)
        self.assertEqual(extract_image_dims(), (expected_image_dims, expected_mat_dims))

    @patch("src.converters.get_config", return_value=None)
    def test_extract_image_dims_exception(self, *_):
        """test_extract_image_dims_exception."""
        with self.assertRaises(Exception):
            extract_image_dims()

    def test_stud_to_mm(self):
        """test_stud_to_mm."""
        self.assertEqual(stud_to_mm(1), 8)

    def test_mm_to_stud(self):
        """test_mm_to_stud."""
        self.assertEqual(mm_to_stud(8), 1)

    @patch("src.converters.extract_image_dims", return_value=((810, 1461), (1143, 2020)))
    def test_mm_to_pixel(self, mock_extract_image_dims):
        """test_mm_to_pixel."""
        self.assertEqual(np.round(mm_to_pixel(10), 4), 8.3960)

    @patch("src.converters.extract_image_dims", return_value=((810, 1461), (1143, 2020)))
    def test_pixel_to_mm(self, mock_extract_image_dims):
        """test_pixel_to_mm."""
        self.assertEqual(np.round(pixel_to_mm(8), 4), 4.8838)

    @patch("src.converters.extract_image_dims", return_value=((810, 1461), (1143, 2020)))
    def test_stud_to_pixel(self, mock_extract_image_dims):
        """test_stud_to_pixel."""
        self.assertEqual(stud_to_pixel(1), 6)

    @patch("src.converters.extract_image_dims", return_value=((810, 1461), (1143, 2020)))
    def test_pixel_to_stud(self, mock_extract_image_dims):
        """test_pixel_to_stud."""
        self.assertEqual(pixel_to_stud(30), 2)
