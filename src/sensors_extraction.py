"""This module contains sensor extraction code."""
from src.configs import get_config


def sensors_extraction() -> dict:
    """Extract sensors from config file.

    Returns
    -------
    dict
        Dictionary of all port sensors, with `ev3dev2` foramt

    Raises
    ------
    ValueError
        If the sensor type is invalid.
    """
    sensors_dict: dict = get_config("robot_sensors")
    if not sensors_dict:
        raise ValueError(
            "sensors are not defined in the config file, expecting GYRO to be defined."
        )
    formated_sensors_dict: dict = {}

    gyro_sensors_counter: int = 0
    color_sensors_counter: int = 0
    for port, sensor in sensors_dict.items():
        if sensor:
            if sensor.lower() == "gyro":
                gyro_sensors_counter += 1
                formated_sensors_dict[
                    f"gyro_{gyro_sensors_counter}"
                ] = f"INPUT_{port.split('_')[-1]}"
            elif sensor.lower() == "color":
                color_sensors_counter += 1
                formated_sensors_dict[
                    f"color_{color_sensors_counter}"
                ] = f"INPUT_{port.split('_')[-1]}"

    return formated_sensors_dict
