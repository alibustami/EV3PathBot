"""This module contains the PID controller using max iterations as the termination condition."""
import logging
from typing import Optional, Tuple, Union

from src.pid.core_pid import pid_control
from src.utils import extract_pid_constants

logger = logging.getLogger(__name__)


def pid_max_iterations(
    process_variable: Union[int, float],
    set_point: Union[int, float],
    sensor: str,
    iterations: int,
    sum_of_errors: Union[int, float],
    last_error: Union[int, float],
    constants: Optional[Tuple[float]] = None,
    accepted_error: Optional[Union[int, float]] = None,
) -> Union[int, float]:
    """Calculate the PID control.

    Parameters
    ----------
    process_variable : Union[int, float]
        The process variable.
    set_point : Union[int, float]
        The set point.
    sensor : str
        The sensor name.
    iterations : int
        The number of iterations.
    constants : Tuple[float]
        The constants for the PID controller (kp, ki, kd).
    accepted_error : Union[int, float]
        The accepted error.

    Returns
    -------
    Union[int, float]
        The PID control value.
    """
    if constants:
        logger.warning("It's better to set the constants in the config file")
    if accepted_error:
        logger.warning("It's better to set the accepted error in the config file")
    pid_configs = extract_pid_constants(sensor)

    kp = constants[0] if constants else pid_configs.kp
    ki = constants[1] if constants else pid_configs.ki
    kd = constants[2] if constants else pid_configs.kd
    accepted_error = accepted_error if accepted_error else pid_configs.accepted_error

    logger.info(
        f"""Starting PID control with the following parameters:
        process variable: {process_variable}
        set point: {set_point}
        sensor: {sensor}
        iterations: {iterations}
        constants: {constants}
        accepted error: {accepted_error}"""
    )
    iterations_counter: int = 0
    for _ in range(iterations):
        pid, sum_of_errors, last_error = pid_control(
            process_variable,
            set_point,
            (kp, ki, kd),
            accepted_error,
            last_error,
            sum_of_errors,
        )
        iterations_counter += 1

    return pid
