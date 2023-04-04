"""This module contains the pixel to degrees ratio calculator."""
from typing import List

import numpy as np


def convert_pixels_to_degrees(
    img: np.array, distance_list: List[float], wheel_diameter: float
) -> List[int]:
    """Convert pixels to degrees.

    Parameters
    ----------
    img : np.array
        table image
    distance_list : List[float]
        the input distances
    wheel_diameter : float
        wheel diameter

    Returns
    -------
    List[int]
        the degrees the robot should move
    """
    img_scale: float = img.shape[1] / 236.2
    wheel_scale: float = (wheel_diameter * 3.14) / 360
    degrees_list: list = []
    for distance in distance_list:
        degrees_list.append(round((distance / img_scale) / wheel_scale))
    return degrees_list
