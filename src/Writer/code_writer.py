"""This module contains the code writer."""

from src.configs import get_config
from src.motors_extraction import motors_extraction
from src.sensors_extraction import sensors_extraction

robot_sensors = list(sensors_extraction())


class CodeEditor:
    """Write EV3DEV code."""

    def __init__(self):
        """Class Constructor."""
        self.code = ""
        self.large_motors, self.medium_motors = motors_extraction()
        self.robot_sensors = sensors_extraction()

    def _add_medium_motors(self):
        medium_motors_import = ""
        for i in range(len(self.medium_motors)):
            medium_motors_import += (
                f"motor{self.medium_motors[i]} = MediumMotor(OUTPUT_{self.medium_motors[i]})\n"
            )
        return medium_motors_import

    def _add_large_motors(self):
        large_motors_import = ""
        for i in range(len(self.large_motors)):
            large_motors_import += (
                f"motor{self.large_motors[i]} = LargeMotor(OUTPUT_{self.large_motors[i]})\n"
            )
        return large_motors_import

    def add_imports_and_variables(self) -> None:
        """Add imports and variables to the code."""
        imports_and_variables = f"""
from time import sleep
import ev3dev2
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B,OUTPUT_C, OUTPUT_D, SpeedDPS, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_4, INPUT_3,INPUT_2
from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.button import Button
from ev3dev2.sound import Sound\n\n
# brain
ev3 = ev3dev2
button = Button()
sound = Sound()

# motors
{self._add_large_motors()}

{self._add_medium_motors()}

motorB = {self.port_b}Motor(OUTPUT_B)
motorC = {self.port_c}Motor(OUTPUT_C)
# sensors
{"TODO"}
        """
        self.code += imports_and_variables

    def add_function(self) -> None:
        """Add a function to the code."""
        function_code = f"""
def on_for_degrees_with_correction (
    speed: int,
    degrees: int,
    brake: bool,
    correction_factor: int = 0,
    kp={get_config("pid_constants.kp")}):
    motor{self.large_motors[0]}.reset()
    motor{self.large_motors[1]}.reset()
    motor{self.large_motors[0]}.on_for_degrees(speed=SpeedDPS(speed), degrees= degrees, brake=brake, block=False)
    motor{self.large_motors[1]}.on_for_degrees(speed=SpeedDPS(speed), degrees= degrees, brake=brake, block=True)
    error{self.large_motors[0]} =  100
    error{self.large_motors[1]} =  100

    while abs(error{self.large_motors[0]}) > correction_factor or abs(error{self.large_motors[1]}) > correction_factor:
        if degrees > 0:
            error{self.large_motors[0]} =  -motor{self.large_motors[0]}.position + degrees
            error{self.large_motors[1]} =  -motor{self.large_motors[1]}.position + degrees
            if abs(error{self.large_motors[0]}) > correction_factor:
                motor{self.large_motors[0]}.on(SpeedDPS(error{self.large_motors[0]} * kp))
            else:
                motor{self.large_motors[0]}.stop()

            if abs(error{self.large_motors[1]}) > correction_factor:
                motor{self.large_motors[1]}.on(SpeedDPS(error{self.large_motors[1]} * kp))
            else:
                motor{self.large_motors[1]}.stop()

        else:
            error{self.large_motors[0]} =  motor{self.large_motors[0]}.position - degrees
            error{self.large_motors[1]} =  motor{self.large_motors[1]}.position - degrees
            if abs(error{self.large_motors[0]}) > correction_factor:
                motor{self.large_motors[0]}.on(SpeedDPS(-error{self.large_motors[0]} * kp))
            else:
                motor{self.large_motors[0]}.stop()

            if abs(error{self.large_motors[1]}) > correction_factor:
                motor{self.large_motors[1]}.on(SpeedDPS(-error{self.large_motors[1]} * kp))
            else:
                motor{self.large_motors[1]}.stop()
    print('{self.large_motors[0]} = ' + str(motor{self.large_motors[0]}.position))
    print('{self.large_motors[1]} = ' + str(motor{self.large_motors[1]}.position))\n
        """
        self.code += function_code

    def write_code(self, filename: str) -> None:
        """Write the code to a file.

        Parameters
        ----------
        filename : str
            The name of the file to write the code to.

        Returns
        -------
        None
        """
        with open(filename, "w") as file:
            # Write the imports
            file.write("#!/usr/bin/env python3\n\n")

            # Write the code string
            file.write(self.code)


editor = CodeEditor()
editor.add_imports_and_variables()
editor.add_function()
editor.write_code("my_code.py")
