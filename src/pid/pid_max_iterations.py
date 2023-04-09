"""This module contains the PID controller using max iterations as the termination condition."""
from typing import Tuple, Union


def pid_max_iterations(
    process_variable: Union[int, float],
    set_point: Union[int, float],
    constants: Tuple[float],
    appecpted_error: Union[int, float],
    last_error: int,
    sum_of_errors: int,
    num_iterations: int,
    check_iterations: int = 0,
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
    num_iterations : int
        The number of iterations to perform.
    check_iterations : int
    Returns
    -------
    Tuple[Union[int, float]]
        The PID control, sum of errors and last error, check iterations.
    """
    kp, ki, kd = constants
    pid = 0

    for i in range(num_iterations):
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

        check_iterations += 1

    return pid, sum_of_errors, last_error, check_iterations


process_variable: int = 20
set_point: int = 0
constants: tuple = (1, 1, 1)
appecpted_error: int = 0
last_error: int = 0
sum_of_errors: int = 0
num_iterations: int = 5
check_iterations: int = 0

pid_value, sum_of_errors, last_error, check_iterations = pid_max_iterations(
    process_variable,
    set_point,
    constants,
    appecpted_error,
    last_error,
    sum_of_errors,
    num_iterations,
    check_iterations,
)
print(pid_value)
