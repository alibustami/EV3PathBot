"""This module contains the code writer."""

from src.configs import get_config
from src.GUIs.main_screen import run
from src.motors_extraction import motors_extraction
from src.path_creation import create_path

large_motors, meduim_motors = motors_extraction()
robot_motors = get_config("robot_motors")
port_a = robot_motors["port_A"].capitalize()
port_b = robot_motors["port_B"].capitalize()
port_c = robot_motors["port_C"].capitalize()
pord_d = robot_motors["port_D"].capitalize()

robot_sensors = get_config("robot sensors")
sensors = list(robot_sensors.values())


class CodeEditor:
    """Write EV3DEV code."""

    def __init__(self):
        """Class Constructor."""
        self.code = ""

    def add_imports_and_variables(self, imports_and_variables: str) -> None:
        """Add imports and variables to the code.

        Parameters
        ----------
        imports : str
            The imports.
        """
        self.code += imports_and_variables

    def add_function(self, function_code: str) -> None:
        """Add a function to the code.

        Parameters
        ----------
        function_code : str
            The code for the function to be added.

        Returns
        -------
        None
        """
        # Append the function code to the code string
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

motorA = {port_a}Motor(OUTPUT_A)
motorD = {pord_d}Motor(OUTPUT_D)

motorB = {port_b}Motor(OUTPUT_B)
motorC = {port_c}Motor(OUTPUT_C)
# sensors
gyro = GyroSensor(INPUT_2)
color_med = ColorSensor(INPUT_3)
color_right = ColorSensor(INPUT_4)
color_left = ColorSensor(INPUT_1)
"""
editor.add_imports_and_variables(imports_and_variables)

function1_code = f"""
def on_for_degrees_with_correction (speed: int, degrees: int, brake: bool, correction_factor: float, kp=12)
    motor{large_motors[0]}.reset()
    motor{large_motors[1]}.reset()
    motor{large_motors[0]}.on_for_degrees(speed=SpeedDPS(speed), degrees= degrees, brake=brake, block=False)
    motor{large_motors[1]}.on_for_degrees(speed=SpeedDPS(speed), degrees= degrees, brake=brake, block=True)
    error{large_motors[0]} =  100
    error{large_motors[1]} =  100

    while abs(error{large_motors[0]}) > correction_factor or abs(error{large_motors[1]}) > correction_factor:
        if degrees > 0:
            error{large_motors[0]} =  -motor{large_motors[0]}.position + degrees
            error{large_motors[1]} =  -motor{large_motors[1]}.position + degrees
            if abs(error{large_motors[0]}) > correction_factor:
                motor{large_motors[0]}.on(SpeedDPS(error{large_motors[0]} * kp))
            else:
                motor{large_motors[0]}.stop()

            if abs(error{large_motors[1]}) > correction_factor:
                motor{large_motors[1]}.on(SpeedDPS(error{large_motors[1]} * kp))
            else:
                motor{large_motors[1]}.stop()

        else:
            error{large_motors[0]} =  motor{large_motors[0]}.position - degrees
            error{large_motors[1]} =  motor{large_motors[1]}.position - degrees
            if abs(error{large_motors[0]}) > correction_factor:
                motor{large_motors[0]}.on(SpeedDPS(-error{large_motors[0]} * kp))
            else:
                motor{large_motors[0]}.stop()

            if abs(error{large_motors[1]}) > correction_factor:
                motor{large_motors[1]}.on(SpeedDPS(-error{large_motors[1]} * kp))
            else:
                motor{large_motors[1]}.stop()
    print('{large_motors[0]} = ' + str(motor{large_motors[0]}.position))
    print('{large_motors[1]} = ' + str(motor{large_motors[1]}.position))\n
"""
editor.add_function(function1_code)

editor.write_code("my_function.py")
