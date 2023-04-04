"""This module contains reading the image."""
import os

import cv2 as cv
import numpy as np


def img_reading(path: str) -> int:
    """Read the image.

    Parameters
    ----------
    path : str
        image path

    Returns
    -------
    int
        counter
    """
    img = cv.imread(path)

    counter = 0
    if os.path.exists(path):
        counter += 1

    if img is not None:
        counter += 1
    return counter


print(img_reading(r"C:\Users\walee\Desktop\project\robot1.png"))
