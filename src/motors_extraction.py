"""This module contains motor extraction code."""
from typing import List, Tuple

from src.configs import get_config


def motors_extraction() -> Tuple[List[chr], List[chr]]:
    """Extract motors from config file.

    Returns
    -------
    Tuple[List[chr], List[chr]]
        The large motors list and the medium motors list.

    Raises
    ------
    ValueError
        If the motors are not defined in the config file.
    ValueError
        If the motor type is invalid.
    """
    motors_dict: dict = get_config("robot_motors")
    if not motors_dict:
        raise ValueError("Motors are not defined in the config file.")
    large_motors_list: list = []
    medium_motors_list: list = []

    for port, motor in motors_dict.items():
        if motor:
            if motor.lower() == "large":
                large_motors_list.append(port.split("_")[1])
            elif motor.lower() == "medium":
                medium_motors_list.append(port.split("_")[1])
            else:
                raise ValueError(f"Invalid motor type: {motor}")

    return large_motors_list, medium_motors_list
