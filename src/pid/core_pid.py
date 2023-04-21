"""This module contains the utitlites for the PID controller."""
from typing import Tuple, Union


def pid_control(
    process_variable: Union[int, float],
    set_point: Union[int, float],
    constants: Tuple[float],
    appecpted_error: Union[int, float],
    last_error: int,
    sum_of_errors: int,
) -> Tuple[Union[int, float]]:
    """Calculate the PID control.

    Parameters
    ----------
    process_variable : Union[int, float]
        The process variable.
    set_point : Union[int, float]
        The set point.
    constants : Tuple[float]
        The constants for the PID controller (kp, ki, kd).
    appecpted_error : Union[int, float]
        The accepted error.
    last_error : int
        The last error.
    sum_of_errors : int
        The sum of errors.

    Returns
    -------
    Tuple[Union[int, float]]
        The PID control, sum of errors and last error.
    """
    kp, ki, kd = constants

    error: Union[int, float] = set_point - process_variable
    sum_of_errors += error

    if abs(error) < appecpted_error:
        pid: int = 0
    else:
        # P-Term Calculation
        p_term: Union[int, float] = kp * error

        # I-Term Calculation
        i_term: Union[int, float] = ki * sum_of_errors

        # D-Term Calculation
        d_term: Union[int, float] = kd * last_error

        last_error = error

        pid: Union[int, float] = p_term + i_term + d_term

    return pid, sum_of_errors, last_error
