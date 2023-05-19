"""This module contains the code writer."""
import logging
import os
from typing import List

from src.configs import get_config
from src.motors_extraction import motors_extraction
from src.sensors_extraction import sensors_extraction

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: on file %(filename)s, on line %(lineno)d: %(message)s",
    filename="logs.log",
    filemode="a",
)


class CodeEditor:
    """Write EV3DEV code."""

    def __init__(self):
        """Class Constructor."""
        self.code = ""
        self.large_motors, self.medium_motors = motors_extraction()
        logging.info(f"large motors: {self.large_motors}")
        self.robot_sensors = sensors_extraction()
        logging.info(f"robot sensors: {self.robot_sensors}")

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

    def _add_sensors(self):
        sensors_import = ""
        for sensor, port in self.robot_sensors.items():
            if sensor.startswith("gyro"):
                sensors_import += f"{sensor} = GyroSensor({port})\n"
            if sensor.startswith("color"):
                sensors_import += f"{sensor} = ColorSensor({port})\n"
        return sensors_import

    def _write_medium_motors(self, medium_motors_list: List[float], path_dict: dict, counter: int):
        text: str = ""
        if len(medium_motors_list) == 2:
            text += f"motor{medium_motors_list[0]}.on_for_degrees(SpeedDPS(500), degrees={path_dict[medium_motors_list[0]][counter]}, block=False)\n"
            text += f"motor{medium_motors_list[1]}.on_for_degrees(SpeedDPS(500), degrees={path_dict[medium_motors_list[1]][counter]}, block=False)\n"
        elif len(medium_motors_list) == 1:
            text += f"motor{medium_motors_list[1]}.on_for_degrees(SpeedDPS(500), degrees={path_dict[medium_motors_list[0]][counter]}, block=False)\n"
        return text

    def add_imports_and_variables(self) -> None:
        """Add imports and variables to the code."""
        for sensor in self.robot_sensors:
            if "gyro" in sensor:
                self.gyro = sensor
                break
        imports_and_variables = f"""
from time import sleep

import ev3dev2
from ev3dev2.button import Button
from ev3dev2.motor import (
    OUTPUT_A,
    OUTPUT_B,
    OUTPUT_C,
    OUTPUT_D,
    LargeMotor,
    MediumMotor,
    SpeedDPS,
)
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from ev3dev2.sound import Sound\n
# brain
ev3 = ev3dev2
button = Button()
sound = Sound()

# motors
{self._add_large_motors()}
{self._add_medium_motors()}
# sensors
{self._add_sensors()}
        """
        self.code += imports_and_variables

    def add_function(self) -> None:
        """Add a function to the code."""
        function_code = f"""
def on_for_degrees_with_correction(
    speed: int, degrees: int, brake: bool, block: bool, correction_factor: int = 0, kp={get_config("pid_constants.kp")}
):
    motor{self.large_motors[0]}.reset()
    motor{self.large_motors[1]}.reset()
    motor{self.large_motors[0]}.on_for_degrees(speed=SpeedDPS(speed), degrees=degrees, brake=brake, block=False)
    motor{self.large_motors[1]}.on_for_degrees(speed=SpeedDPS(speed), degrees=degrees, brake=brake, block=block)
    error{self.large_motors[0]} = 100
    error{self.large_motors[1]} = 100

    while abs(error{self.large_motors[0]}) > correction_factor or abs(error{self.large_motors[1]}) > correction_factor:
        if degrees > 0:
            error{self.large_motors[0]} = -motor{self.large_motors[0]}.position + degrees
            error{self.large_motors[1]} = -motor{self.large_motors[1]}.position + degrees
            if abs(error{self.large_motors[0]}) > correction_factor:
                motor{self.large_motors[0]}.on(SpeedDPS(error{self.large_motors[0]} * kp))
            else:
                motor{self.large_motors[0]}.stop()

            if abs(error{self.large_motors[1]}) > correction_factor:
                motor{self.large_motors[1]}.on(SpeedDPS(error{self.large_motors[1]} * kp))
            else:
                motor{self.large_motors[1]}.stop()

        else:
            error{self.large_motors[0]} = motor{self.large_motors[0]}.position - degrees
            error{self.large_motors[1]} = motor{self.large_motors[1]}.position - degrees
            if abs(error{self.large_motors[0]}) > correction_factor:
                motor{self.large_motors[0]}.on(SpeedDPS(-error{self.large_motors[0]} * kp))
            else:
                motor{self.large_motors[0]}.stop()

            if abs(error{self.large_motors[1]}) > correction_factor:
                motor{self.large_motors[1]}.on(SpeedDPS(-error{self.large_motors[1]} * kp))
            else:
                motor{self.large_motors[1]}.stop()
    print('{self.large_motors[0]} = ' + str(motor{self.large_motors[0]}.position))
    print('{self.large_motors[1]} = ' + str(motor{self.large_motors[1]}.position))\n\n
def PID_turn(
    set_point: int,
    reset = False,
    kp ={get_config("pid_constants.kp")}):

    motor{self.large_motors[0]}.reset()
    motor{self.large_motors[1]}.reset()
    if reset:
        sleep(0.1)
        {self.gyro}.reset()
        sleep(0.1)

    while {self.gyro}.angle != set_point:
        current_value = {self.gyro}.angle
        error = set_point - current_value
        correcting_speed = error * kp
        motor{self.large_motors[0]}.on(SpeedDPS(-correcting_speed), brake=False, block=False)
        motor{self.large_motors[1]}.on(SpeedDPS(correcting_speed), brake=False, block=False)

    motor{self.large_motors[0]}.stop()
    motor{self.large_motors[1]}.stop()
    print('gyro angle: ' + str({self.gyro}.angle))
    """
        self.code += function_code

    def write_main_code(self, points: dict) -> None:
        """Write the main code from the points.

        Parameters
        ----------
        points : dict
            Point dictionary.
        """
        main_code = ""
        main_code += f"""
sound.beep()
button.wait_for_pressed(['enter'])
{self.gyro}.reset()
print({self.gyro}.angle)
"""
        for i in range(len(points["x"])):
            main_code += f"""
# move_{i+1}"""
            block: bool
            if points["additional_motors_mode"][i] == "S":
                block = True
            elif points["additional_motors_mode"][i] == "P":
                block = False

            if i <= (len(points["angles_difference"]) - 1):
                if points["action"][i] == "backward":
                    points["distance_degrees"][i] = -1 * points["distance_degrees"][i]

                if points["angles_difference"][i] == 0:
                    main_code += f"""
on_for_degrees_with_correction(speed={points['speed'][i]}, degrees={points['distance_degrees'][i]}, brake=True, block={block}, kp={get_config("pid_constants.kp")})
{self._write_medium_motors(medium_motors_list=self.medium_motors, path_dict=points, counter=i)}
"""
                elif points["angles_difference"][i] != 0:
                    main_code += f"""
PID_turn(set_point={points["angle"][i+1]})
{self._write_medium_motors(medium_motors_list=self.medium_motors, path_dict=points, counter=i)}

"""

            else:
                main_code += f"""
PID_turn(set_point={points["angle"][-1]})
{self._write_medium_motors(medium_motors_list=self.medium_motors, path_dict=points, counter=-1)}
"""

        self.code += main_code

    def write_code(self):
        """Write the code to a file."""
        if len(os.listdir("ev3dev-codes")) > 1:
            for afile in sorted(os.listdir("ev3dev-codes"), reverse=True):
                if afile.endswith(".py"):
                    afile = afile[:-3]
                    file_name_list = afile.split("_")
                    file_number: int = int(file_name_list[-1])
                    break
        else:
            file_number: int = 0

        with open(os.path.join("ev3dev-codes", f"code_{file_number+1}.py"), "w") as file:
            # Write the imports
            file.write("#!/usr/bin/env python3\n\n")

            # Write the code string
            file.write(self.code)

    def __call__(self, point: dict):
        """Call function for the class.

        Parameters
        ---------
        point: dict
            path dictionary
        """
        self.add_imports_and_variables()
        self.add_function()
        self.write_main_code(point)
        self.write_code()
