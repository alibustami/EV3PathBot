"""This module contains the path creation code."""
import math
from typing import List

import numpy as np

from src.motors_extraction import motors_extraction
from src.pixels_to_degrees_ratio import convert_pixels_to_degrees


def create_path(
    robot_positions: List[np.ndarray],
    angles: List[int],
    additional_motor_1: List[int],
    additional_motor_2: List[int],
    additional_motors_mode: List[chr],
) -> dict:
    """Create the path file.

    Parameters
    ----------
    robot_positions : List[np.ndarray]
        The robot positions.
    angles : List[int]
        The angles.
    additional_motor_1 : List[int]
        The additional motor 1.
    additional_motor_2 : List[int]
        The additional motor 2.
    additional_motors_mode : List[chr]
        The additional motors mode weather it is Parallel (P) or Series (S).

    Returns
    -------
    dict
        dictiorany of all the path markups.
    """
    _, meduim_motors = motors_extraction()
    motor_1 = meduim_motors[0]
    motor_2 = meduim_motors[1]
    positions: dict = {
        "x": [],
        "y": [],
        "distance_degrees": [],
        "angle": [],
        "angles_difference": [],
        motor_1: [],
        motor_2: [],
        "additional_motors_mode": [],
    }
    for i in range(len(robot_positions)):
        positions["x"].append(int(robot_positions[i][0][0]))
        positions["y"].append(int(robot_positions[i][0][1]))
        positions["angle"].append(angles[i])
        positions[motor_1].append(additional_motor_1[i])
        positions[motor_2].append(additional_motor_2[i])
        positions["additional_motors_mode"].append(additional_motors_mode[i])

    for i in range(len(positions["x"]) - 1):
        p1 = (positions["x"][i], positions["y"][i])
        p2 = (positions["x"][i + 1], positions["y"][i + 1])

        distance = math.dist(p1, p2)

        positions["distance_degrees"].append((distance))

    for i in range(len(positions["angle"]) - 1):
        an1 = positions["angle"][i]
        an2 = positions["angle"][i + 1]
        angle = an2 - an1

        positions["angles_difference"].append((angle))

    positions["distance_degrees"] = convert_pixels_to_degrees(
        np.array(positions["distance_degrees"])
    )
    return positions
