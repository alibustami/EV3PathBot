"""This module contains the unit tests for the core_pid."""
import unittest

from src.pid.core_pid import pid_control


class TestPIDControl(unittest.TestCase):
    """This class contains the unit tests for the PID control."""

    def test_pid_control_with_zero_error(self):
        """Test the PID control with zero error."""
        process_variable: int = 0
        set_point: int = 0
        constants: tuple = (1, 1, 1)
        appecpted_error: int = 0
        last_error: int = 0
        sum_of_errors: int = 0

        pid, sum_of_errors, last_error = pid_control(
            process_variable,
            set_point,
            constants,
            appecpted_error,
            last_error,
            sum_of_errors,
        )

        self.assertEqual(pid, 0)
        self.assertEqual(sum_of_errors, 0)
        self.assertEqual(last_error, 0)

    def test_pid_control(self):
        """Test the PID control."""
        process_variable: int = 20
        set_point: int = 0
        constants: tuple = (1, 1, 1)
        appecpted_error: int = 0
        last_error: int = 0
        sum_of_errors: int = 0

        pid, sum_of_errors, last_error = pid_control(
            process_variable,
            set_point,
            constants,
            appecpted_error,
            last_error,
            sum_of_errors,
        )

        self.assertEqual(pid, -40)
        self.assertEqual(sum_of_errors, -20)
        self.assertEqual(last_error, -20)
