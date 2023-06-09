"""This module contains the utility functions for the project."""
import logging
from collections import namedtuple
from typing import Optional, Tuple, Union

from pydantic import BaseModel

from src.configs import get_config

logger = logging.getLogger(__name__)


class PIDConfigs(BaseModel):
    """PIDConfigs object."""

    kp: float
    ki: float
    kd: float
    accepted_error: float
    sensor: str
    sensor_port: int


def extract_pid_constants(
    sensor: str,
    constants: Optional[Tuple[float]] = None,
    accepted_error: Optional[float] = None,
    sensor_port: Optional[int] = None,
) -> PIDConfigs:
    """PID control using the gyro sensor.

    Parameters
    ----------
    sensor : str
        sensor name one of the following: gyro, color
    constants : Optional[Tuple[float]], optional
        constants of the PID controller (kp, ki, kd), by default None
    accepted_error : Optional[float], optional
        accepted error, by default None
    sensor_port : Optional[int], optional
        sensor port must be 1, 2, 3 or 4, by default None

    Returns
    -------
    PIDConfigs
        PIDConfigs object

    Raises
    ------
    ValueError

        * if no constants are set in the config file
        * if no termination condition is set in the config file
        * if the termination condition is invalid (not one of the following: max_time, max_iterations, max_convergence_loop)
    """
    pid_constant = namedtuple("constant", ["value"])
    # get constants with validation
    if accepted_error:
        logger.warning("it's better to set the accepted error in the config file")
        logger.info(f"accepted error: {accepted_error}")
    else:
        accepted_error = get_config("pid_constants.accepted_error")
        if not accepted_error:
            logger.error("No accepted error is set")
            raise ValueError("No accepted error is set")
        logger.info(f"accepted error: {accepted_error}")
        accepted_error: float = float(accepted_error)
    accepted_error: namedtuple = pid_constant(accepted_error)

    if constants:
        (kp, ki, kd) = constants
        logger.warning("it's better to set the constants in the config file")
        logger.info(
            f"kp: {kp}, ki: {ki}, kd: {kd}, accepted_error: {accepted_error.value} from function arguments"
        )
    else:
        (kp, ki, kd) = (
            get_config("pid_constants.kp"),
            get_config("pid_constants.ki"),
            get_config("pid_constants.kd"),
        )
        if any(value is None for value in [kp, ki, kd]):
            logger.error("No constants are set")
            raise ValueError("No constants are set")
        logger.info(
            f"kp: {kp}, ki: {ki}, kd: {kd}, accepted_error: {accepted_error.value} form config file"
        )
        kp: float = float(kp)
        ki: float = float(ki)
        kd: float = float(kd)
    kp: namedtuple = pid_constant(kp)
    ki: namedtuple = pid_constant(ki)
    kd: namedtuple = pid_constant(kd)

    # get sensor port with validation
    logger.info(f"selected sensor: {sensor}")
    if sensor_port:
        if sensor_port not in ["1", "2", "3", "4"]:
            logger.error(f"Invalid sensor port, must be 1, 2, 3 or 4 got '{sensor_port}'")
            raise ValueError("Invalid sensor port")
        logger.warning("it's better to set the sensor port in the config file")
        logger.info(f"sensor port: {sensor_port} from function arguments")
    else:
        ports_counter: int = 0
        sensors_dict: dict = get_config("robot_sensors")
        for key, value in sensors_dict.items():
            if value:
                if value.lower() == sensor.lower():
                    sensor_port = key.split("_")[1]
                    ports_counter += 1
                else:
                    logger.error(f"Invalid sensor name, expected on of [Gyro, Color] got '{value}'")
                    raise ValueError("Invalid sensor name")
        if ports_counter == 0:
            logger.error("No gyro sensor is set")
            raise ValueError("No gyro sensor is set")
        elif ports_counter > 1:
            logger.warning(
                f"more than one gyro sensor is set, the last one will be used which is {sensor_port}"
            )
    sensor_port: int = int(sensor_port)
    logger.info(f"sensor port: {sensor_port} from config file")

    pid_configs = PIDConfigs(
        **{
            "kp": kp.value,
            "ki": ki.value,
            "kd": kd.value,
            "accepted_error": accepted_error.value,
            "sensor": sensor,
            "sensor_port": sensor_port,
        }
    )
    return pid_configs
