"""This module contains the PID controller using max iterations as the termination condition."""
from typing import Optional, Tuple, Union

from src.pid.core_pid import pid_control
from src.utils import extract_pid_constants


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
    pid_configs = extract_pid_constants(sensor)

    kp = constants[0] if constants else pid_configs.kp
    ki = constants[1] if constants else pid_configs.ki
    kd = constants[2] if constants else pid_configs.kd
    accepted_error = accepted_error if accepted_error else pid_configs.accepted_error

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
