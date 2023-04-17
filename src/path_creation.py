"""This module contains the path creation code."""
from typing import List

import numpy as np

from src.motors_extraction import motors_extraction


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
    posisitions: dict = {
        "x": [],
        "y": [],
        "angle": [],
        motor_1: [],
        motor_2: [],
        "additional_motors_mode": [],
    }
    for i in range(len(robot_positions)):
        posisitions["x"].append(int(robot_positions[i][0][0]))
        posisitions["y"].append(int(robot_positions[i][0][1]))
        posisitions["angle"].append(angles[i])
        posisitions[motor_1].append(additional_motor_1[i])
        posisitions[motor_2].append(additional_motor_2[i])
        posisitions["additional_motors_mode"].append(additional_motors_mode[i])

    return posisitions
