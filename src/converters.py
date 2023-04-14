"""This module contains the units converters."""
import os
from typing import Tuple

import cv2

from src.configs import get_config


def extract_image_dims() -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Extract image dimensions.

    Returns
    -------
    Tuple[Tuple[int, int], Tuple[int, int]]
        The image dimensions and the mat dimensions.

    Raises
    ------
    ValueError
        If the mat image path is not defined in the config file.
    FileNotFoundError
        If the mat image is not found.
    """
    mat_image_path = get_config("mat_image_path")
    if not mat_image_path:
        raise ValueError("Mat image path is not defined in the config file.")
    if not os.path.isfile(mat_image_path):
        raise FileNotFoundError("Mat image not found.")

    try:
        mat_image_array = cv2.imread(mat_image_path)
        image_height_y, image_width_x, _ = mat_image_array.shape
        mat_length_y = int(get_config("mat_dimensions.width_y"))
        mat_width_x = int(get_config("mat_dimensions.length_x"))
        return (image_height_y, image_width_x), (mat_width_x, mat_length_y)
    except Exception as e:
        raise e


def stud_to_mm(stud: int) -> float:
    """Convert stud to mm.

    Parameters
    ----------
    stud : int
        the input stud
    Returns
    -------
    float
        the output mm
    """
    return stud * 8


def mm_to_stud(mm: float) -> int:
    """Convert mm to stud.

    Parameters
    ----------
    mm : float
        the input mm
    Returns
    -------
    int
        the output stud
    """
    return int(mm / 8)


def mm_to_pixel(mm: float) -> float:
    """Convert mm to pixel.

    Parameters
    ----------
    mm : float
        the input mm
    Returns
    -------
    float
        the output pixel
    """
    image_dims, mat_dims = extract_image_dims()
    image_height_y, image_width_x = image_dims
    mat_width_x, mat_length_y = mat_dims
    x_ratio: float = image_width_x / mat_width_x
    y_ratio: float = image_height_y / mat_length_y
    averaged_ratio: float = (x_ratio + y_ratio) / 2.0
    return float(mm * averaged_ratio)


def pixel_to_mm(pixel: int) -> float:
    """Convert pixel to mm.

    Parameters
    ----------
    pixel : int
        the input pixel
    Returns
    -------
    float
        the output mm
    """
    image_dims, mat_dims = extract_image_dims()
    image_height_y, image_width_x = image_dims
    mat_width_x, mat_length_y = mat_dims
    x_ratio: float = mat_width_x / image_width_x
    y_ratio: float = mat_length_y / image_height_y
    averaged_ratio: float = (x_ratio + y_ratio) / 2.0
    return float(pixel / averaged_ratio)


def stud_to_pixel(stud: int) -> int:
    """Convert stud to pixel.

    Parameters
    ----------
    stud : int
        the input stud
    Returns
    -------
    int
        the output pixel
    """
    return int(mm_to_pixel(stud_to_mm(stud)))


def pixel_to_stud(pixel: int) -> int:
    """Convert pixel to stud.

    Parameters
    ----------
    pixel : int
        the input pixel
    Returns
    -------
    int
        the output stud
    """
    return int(mm_to_stud(pixel_to_mm(pixel)))
