"""This module contains the path creation code."""
import math
from collections import namedtuple
from typing import List

import numpy as np
from scipy.spatial.transform import Rotation

from src.motors_extraction import motors_extraction
from src.pixels_to_degrees_ratio import convert_pixels_to_degrees


def create_path(
    robot_positions: List[np.ndarray],
    angles: List[int],
    additional_motor_1: List[int],
    additional_motor_2: List[int],
    additional_motors_mode: List[chr],
    robot_speed_dps: List[int],
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
    robot_speed_dps : List[int]
        Robot speeds

    Returns
    -------
    dict
        dictiorany of all the path markups.
    """
    _, medium_motors = motors_extraction()
    if len(medium_motors) == 2:
        motor_1, motor_2 = medium_motors
    elif len(medium_motors) == 1:
        motor_1 = medium_motors
        motor_2 = "X"
    else:
        motor_1 = motor_2 = "X"

    directions = determine_robot_movement(robot_positions, angles)
    positions: dict = {
        "x": [],
        "y": [],
        "distance_degrees": [],
        "angle": [],
        "angles_difference": [],
        motor_1: [],
        motor_2: [],
        "additional_motors_mode": [],
        "speed": [],
        "action": directions,
    }

    for i in range(len(robot_positions)):
        positions["x"].append(int(robot_positions[i][0][0]))
        positions["y"].append(int(robot_positions[i][0][1]))
        positions["angle"].append(angles[i])
        positions[motor_1].append(additional_motor_1[i])
        positions[motor_2].append(additional_motor_2[i])
        positions["additional_motors_mode"].append(additional_motors_mode[i])
        positions["speed"].append(robot_speed_dps[i])

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


def determine_robot_movement(robot_positions: List[np.ndarray], angles: List[int]) -> List[str]:
    """Detemine the robot movement direction.

    Parameters
    ----------
    robot_positions : List[np.ndarray]
        robot position as a numpy array representing the edges
    angles : List[int]
        step angle

    Returns
    -------
    List[str]
        movement direction
    """
    robot_vector = namedtuple("robot_vector", ["top_left_corner", "forward_angle", "action"])
    vectors_list: List[robot_vector] = []
    dx = robot_positions[0][3][0] - robot_positions[0][0][0]
    dy = robot_positions[0][3][1] - robot_positions[0][0][1]
    try:
        forward_angle = math.degrees(math.atan(-dy / dx))
    except Exception:
        forward_angle = 90 if dy > 0 else -90
    mode = "None"
    vector = robot_vector(robot_positions[0][0], int(forward_angle), mode)
    vectors_list.append(vector)
    for i in range(1, len(robot_positions)):
        dx = robot_positions[i][3][0] - robot_positions[i][0][0]
        dy = robot_positions[i][3][1] - robot_positions[i][0][1]
        try:
            forward_angle = math.degrees(math.atan(-dy / dx))
        except Exception:
            forward_angle = 90 if dy > 0 else -90
        mode = "Move" if angles[i] == angles[i - 1] else "Rotate"
        vector = robot_vector(robot_positions[i][0], int(forward_angle), mode)
        vectors_list.append(vector)

    for i in range(1, len(vectors_list)):
        if abs(vectors_list[i].forward_angle - vectors_list[i - 1].forward_angle) < 2:
            rotation = Rotation.from_euler("z", vectors_list[i - 1].forward_angle, degrees=True)

            step_before = rotation.apply(vectors_list[i - 1].top_left_corner + [0])
            step_after = rotation.apply(vectors_list[i].top_left_corner + [0])

            if step_before[0] < step_after[0]:
                vectors_list[i] = vectors_list[i]._replace(action="forward")
            else:
                vectors_list[i] = vectors_list[i]._replace(action="backward")

    return [vector.action for vector in vectors_list]


if __name__ == "__main__":
    robot_positions = [
        [[30.0, 626.0], [189.0, 626.0], [189.0, 785.0], [30.0, 785.0]],
        [[30.0, 531.0], [189.0, 531.0], [189.0, 690.0], [30.0, 690.0]],
        [[109.5, 498.07002179], [221.92997821, 610.5], [109.5, 722.92997821], [-2.92997821, 610.5]],
        [[169.5, 438.07002179], [281.92997821, 550.5], [169.5, 662.92997821], [57.07002179, 550.5]],
        [[249.0, 471.0], [249.0, 630.0], [90.0, 630.0], [90.0, 471.0]],
        [[299.0, 471.0], [299.0, 630.0], [140.0, 630.0], [140.0, 471.0]],
        [[269.0, 471.0], [269.0, 630.0], [110.0, 630.0], [110.0, 471.0]],
    ]
    angles = [0, 0, 45, 45, 90, 90, 90]
    determine_robot_movement(robot_positions, angles)
    # create_path(
    #     robot_positions,
    #     angles,
    # )
