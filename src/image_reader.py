"""This module contains reading the image."""
import os

import cv2 as cv
import numpy as np


def image_validation(path: str) -> np.ndarray:
    """Validate the image.

    Parameters
    ----------
    path : str
        image path

    Returns
    -------
    np.ndarray
        image extracted from path

    Raises
    ------
    FileExistsError
        when path is not for a image file
    TypeError
        when the image is not readable
    """
    if not os.path.isfile(path):
        raise FileExistsError(f"No image file found at {path}")

    try:
        img: np.ndarray = cv.imread(path)
    except Exception:
        raise TypeError("image not readable")
    return img
