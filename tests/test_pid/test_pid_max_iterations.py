"""This module contains the unit tests for the pid_max_iterations."""
import unittest

from src.pid.pid_max_iterations import pid_max_iterations


class TestPIDMaxIterations(unittest.TestCase):
    """This class contains the unit tests for the PID max iterations."""

    def test_pid_max_iterations_with_zero_error(self):
        """Test the PID max iteration with zero error."""
        process_variable: int = 0
        set_point: int = 0
        constants: tuple = (1, 1, 1)
        appecpted_error: int = 0
        last_error: int = 0
        sum_of_errors: int = 0
        num_iterations: int = 0
        check_iterations: int = 0
        result = pid_max_iterations(
            process_variable,
            set_point,
            constants,
            appecpted_error,
            last_error,
            sum_of_errors,
            num_iterations,
            check_iterations,
        )

        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], 0)
        self.assertEqual(result[2], 0)
        self.assertEqual(result[3], num_iterations)

    def test_pid_max_iterations(self):
        """Test the PID max iteration."""
        process_variable: int = 20
        set_point: int = 0
        constants: tuple = (1, 1, 1)
        appecpted_error: int = 0
        last_error: int = 0
        sum_of_errors: int = 0
        num_iterations: int = 5
        check_iterations: int = 0
        pid, sum_of_errors, last_error, check_iterations = pid_max_iterations(
            process_variable,
            set_point,
            constants,
            appecpted_error,
            last_error,
            sum_of_errors,
            num_iterations,
            check_iterations,
        )

        self.assertEqual(pid, -40)
        self.assertEqual(sum_of_errors, -20)
        self.assertEqual(last_error, -20)
        self.assertEqual(num_iterations, check_iterations)


if __name__ == "__main__":
    unittest.main()
