"""This module contains the unit tests for the pid_max_iterations."""
import unittest
from typing import Tuple
from unittest.mock import patch

from src.pid.pid_max_iterations import pid_max_iterations
from src.utils import PIDConfigs


class TestPIDMaxIterations(unittest.TestCase):
    """This class contains the unit tests for the PID max iterations."""

    @patch("src.pid.pid_max_iterations.extract_pid_constants")
    def test_pid_max_iterations_with_zero_error(self, mock_extract_pid_constants):
        """Test the PID max iteration with zero error."""
        process_variable: int = 0
        set_point: int = 0
        sensor: str = "test"
        iterations: int = 10
        sum_of_errors: int = 0
        last_error: int = 0
        constants: Tuple[float] = (1.0, 1.0, 1.0)
        accepted_error: float = 0.0
        mock_extract_pid_constants.return_value = PIDConfigs(
            **{
                "kp": constants[0],
                "ki": constants[1],
                "kd": constants[2],
                "accepted_error": accepted_error,
                "sensor": sensor,
                "sensor_port": 1,
            }
        )
        pid = pid_max_iterations(
            process_variable=process_variable,
            set_point=set_point,
            sensor=sensor,
            iterations=iterations,
            sum_of_errors=sum_of_errors,
            last_error=last_error,
            constants=constants,
            accepted_error=accepted_error,
        )

        self.assertEqual(pid, 0)

    @patch("src.pid.pid_max_iterations.extract_pid_constants")
    def test_pid_max_iterations(self, mock_extract_pid_constants):
        """Test the PID max iteration."""
        process_variable: int = 20
        set_point: int = 0
        sensor: str = "test"
        iterations: int = 5
        sum_of_errors: int = 0
        last_error: int = 0
        constants: Tuple[float] = (1.0, 1.0, 1.0)
        accepted_error: float = 0.0
        mock_extract_pid_constants.return_value = PIDConfigs(
            **{
                "kp": constants[0],
                "ki": constants[1],
                "kd": constants[2],
                "accepted_error": accepted_error,
                "sensor": sensor,
                "sensor_port": 1,
            }
        )
        pid = pid_max_iterations(
            process_variable=process_variable,
            set_point=set_point,
            sensor=sensor,
            iterations=iterations,
            sum_of_errors=sum_of_errors,
            last_error=last_error,
            constants=constants,
            accepted_error=accepted_error,
        )

        self.assertEqual(pid, -140)
