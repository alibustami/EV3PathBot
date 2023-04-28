"""This module contains the pixel to degrees ratio calculator."""
from typing import List, Tuple

import cv2 as cv
import numpy as np

from src.configs import get_config
from src.image_reader import image_validation


def convert_pixels_to_degrees(distance_pixels_array: np.array) -> List[int]:
    """Convert pixels to degrees.

    Parameters
    ----------
    distance_list : List[float]
        the input distances

    Returns
    -------
    List[int]
        the degrees the robot should move
    """
    mat_width = get_config("mat_dimensions.length_x")
    wheel_diameter = get_config("robot_dimensions.wheel_diameter")
    image_path = get_config("mat_image_path")
    img = image_validation(image_path)

    _, width, _ = img.shape
    # this equation for calculating the length of the table in mm
    img_scale: float = width / mat_width

    # this equation is for calculating how many mm does 1 wheel rotation make
    wheel_scale: float = (wheel_diameter * 3.14) / 360
    distance_degrees_array = (distance_pixels_array / img_scale) / wheel_scale
    distance_degrees_array = np.around(distance_degrees_array)
    distance_degrees_array = distance_degrees_array.astype(int)
    return list(distance_degrees_array)
