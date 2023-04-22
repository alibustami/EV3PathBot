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
        self.robot_motors = get_config("robot_motors")
        self.robot_sensors = sensors_extraction()
        self.robot_sensors_types = list(sensors_extraction())
        self.port_a = self.robot_motors["port_A"].capitalize()
        self.port_b = self.robot_motors["port_B"].capitalize()
        self.port_c = self.robot_motors["port_C"].capitalize()
        self.pord_d = self.robot_motors["port_D"].capitalize()

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

motorA = {self.port_a}Motor(OUTPUT_A)
motorD = {self.pord_d}Motor(OUTPUT_D)

motorB = {self.port_b}Motor(OUTPUT_B)
motorC = {self.port_c}Motor(OUTPUT_C)
# sensors
{self.robot_sensors_types[0]} = {self.robot_sensors_types[0][:-2].capitalize()}Sensor({self.robot_sensors[self.robot_sensors_types[0]]})
{self.robot_sensors_types[1]} = {self.robot_sensors_types[1][:-2].capitalize()}Sensor({self.robot_sensors[self.robot_sensors_types[1]]})
{self.robot_sensors_types[2]} = {self.robot_sensors_types[2][:-2].capitalize()}Sensor({self.robot_sensors[self.robot_sensors_types[2]]})
{self.robot_sensors_types[3]} = {self.robot_sensors_types[3][:-2].capitalize()}Sensor({self.robot_sensors[self.robot_sensors_types[3]]})
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
