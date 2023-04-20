"""This module contains the pixel to degrees ratio calculator."""
from typing import List, Tuple

import cv2 as cv

from src.configs import get_config

wheel_diameter = get_config("robot_dimensions.wheel_diameter")
image_path = get_config("mat_image_path")
img = cv.imread(image_path)

_, width, _ = img.shape


def convert_pixels_to_degrees(
    img_dims: Tuple[int], distance_list: List[float], wheel_diameter: float
) -> List[int]:
    """Convert pixels to degrees.

    Parameters
    ----------
    img_dims : Tuple[int]
        image table shape
    distance_list : List[float]
        the input distances
    wheel_diameter : float
        wheel diameter

    Returns
    -------
    List[int]
        the degrees the robot should move
    """
    # this equation for calculating the length of the table in cm
    img_scale: float = width / 236.2

    # this equation is for calculating how many cm does 1 wheel rotation make
    wheel_scale: float = (wheel_diameter * 3.14) / 360
    degrees_list: list = []
    for distance in distance_list:
        degrees_list.append(round((distance / img_scale) / wheel_scale))
    return degrees_list
