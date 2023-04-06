"""This module contains the pixel to degrees ratio calculator."""
from typing import List, Tuple

import numpy as np


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
    _, img_length, _ = img_dims

    # this equation for calculating the length of the table in cm
    img_scale: float = img_length / 236.2

    # this equation is for calculating how many cm does 1 wheel rotation make
    wheel_scale: float = (wheel_diameter * 3.14) / 360
    degrees_list: list = []
    for distance in distance_list:
        degrees_list.append(round((distance / img_scale) / wheel_scale))
    return degrees_list
