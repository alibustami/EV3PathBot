"""This module contains the utility functions for the project."""
import logging
from collections import namedtuple
from typing import Optional, Tuple, Union

from src.configs import get_config

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: on file %(filename)s, on line %(lineno)d: %(message)s",
    filename="logs.log",
    filemode="w",
)
pid_constant = namedtuple("constant", ["value"])


def gyro_pid_control(
    target_angle: Union[int, float],
    current_angle: Union[int, float],
    constants: Optional[Tuple[float]] = None,
    accepted_error: Optional[float] = None,
    termination_condition: Optional[str] = None,
):
    """PID control using the gyro sensor.

    Parameters
    ----------
    target_angle : Union[int, float]
        Target angle to reach
    current_angle : Union[int, float]
        Current angle of the robot
    constants : Optional[Tuple[float]], optional
        constants of the PID controller (kp, ki, kd), by default None
    accepted_error : Optional[float], optional
        accepted error, by default None
    termination_condition : Optional[str], optional
        termination condition, by default None

    Raises
    ------
    ValueError

        * if no constants are set in the config file
        * if no termination condition is set in the config file
        * if the termination condition is invalid (not one of the following: max_time, max_iterations, max_convergence_loop)
    """
    # get constants with validation
    if accepted_error:
        logging.warning("it's better to set the accepted error in the config file")
        logging.info(f"accepted error: {accepted_error}")
    else:
        accepted_error: float = float(get_config("pid_constants.accepted_error"))
    accepted_error: namedtuple = pid_constant(accepted_error)

    if constants:
        (kp, ki, kd) = constants
        logging.warning("it's better to set the constants in the config file")
        logging.info(f"kp: {kp}, ki: {ki}, kd: {kd}")
    else:
        (kp, ki, kd) = (
            float(get_config("pid_constants.kp")),
            float(get_config("pid_constants.ki")),
            float(get_config("pid_constants.kd")),
        )
        if any(value is None for value in [kp, ki, kd]):
            logging.error("No constants are set")
            raise ValueError("No constants are set")
        logging.info(f"kp: {kp}, ki: {ki}, kd: {kd}")
    kp: namedtuple = pid_constant(kp)
    ki: namedtuple = pid_constant(ki)
    kd: namedtuple = pid_constant(kd)

    # get termination condition with validation
    terminiation_condition_list: list = ["max_time", "max_iterations", "max_convergence_loop"]

    if termination_condition:
        logging.warning("it's better to set the termination condition in the config file")
        if termination_condition in terminiation_condition_list:
            termination: str = termination_condition
        else:
            logging.error(
                f"Invalid termination condition expected one of {terminiation_condition_list} got '{termination_condition}'"
            )
            raise ValueError(
                f"Invalid termination condition expected one of {terminiation_condition_list} got '{termination_condition}'"
            )
    else:
        termination_condition_dict: dict = get_config("pid_termination_conditions")
        termination: str = [
            key for key, value in termination_condition_dict.items() if value is not None
        ]
        if len(termination) == 1:
            termination, *_ = termination
            logging.info(f"termination condition is set to '{termination}'")
        elif len(termination) > 1:
            logging.warning(
                f"more than one termination condition is set, the first one will be used which is {termination[0]}"
            )
            termination: str = termination[0]
        elif not termination:
            logging.error("No termination condition is set")
            raise ValueError("No termination condition is set")
