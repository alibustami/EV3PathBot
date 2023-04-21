"""This module contains the code writer."""
import numpy as np

from src.GUIs.main_screen import run
from src.path_creation import create_path

(
    robot_positions,
    robot_angles,
    additional_motor_1,
    additional_motor_2,
    additional_motors_mode,
) = run()
create_path(
    robot_positions,
    robot_angles,
    additional_motor_1,
    additional_motor_2,
    additional_motors_mode,
)
x = create_path(
    robot_positions, robot_angles, additional_motor_1, additional_motor_2, additional_motors_mode
)
print(x)


def generate_function(name: str, args: any) -> None:
    """Generate code.

    Parameters
    ----------
    name : str
        _description_
    args : any
        _description_
    """
    # Create the function code as a string

    # Write the function code to a file
    with open(f"{name}.py", "w") as file:
        # Write the imports
        file.write("#!/usr/bin/env python3\n\n")
        file.write(
            """
from time import sleep
import ev3dev2
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B,OUTPUT_C, OUTPUT_D, SpeedDPS, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_4, INPUT_3,INPUT_2
from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.button import Button
from ev3dev2.sound import Sound\n\n
"""
        )
        # write the variables
        file.write(
            """# brain
ev3 = ev3dev2
button = Button()
sound = Sound()
# mediums
motorA = MediumMotor(OUTPUT_A)
motorD = MediumMotor(OUTPUT_D)
# larges
motorB = LargeMotor(OUTPUT_B)
motorC = LargeMotor(OUTPUT_C)
# sensors
gyro = GyroSensor(INPUT_2)
color_med = ColorSensor(INPUT_3)
color_right = ColorSensor(INPUT_4)
color_left = ColorSensor(INPUT_1)
"""
        )
        # Write the on_for_degrees_with_correction function
        file.write(
            """
def on_for_degrees_with_correction (speed: int, degrees: int, brake: bool, correction_factor: float, kp=12):
    motorB.reset()
    motorC.reset()
    motorB.on_for_degrees(speed=SpeedDPS(speed), degrees= degrees, brake=brake, block=False)
    motorC.on_for_degrees(speed=SpeedDPS(speed), degrees= degrees, brake=brake, block=True)
    errorB =  100
    errorC =  100

    while abs(errorB) > correction_factor or abs(errorC) > correction_factor:
        if degrees > 0:
            errorB =  -motorB.position + degrees
            errorC =  -motorC.position + degrees
            if abs(errorB) > correction_factor:
                motorB.on(SpeedDPS(errorB * kp))
            else:
                motorB.stop()

            if abs(errorC) > correction_factor:
                motorC.on(SpeedDPS(errorC * kp))
            else:
                motorC.stop()

        else:
            errorB =  motorB.position - degrees
            errorC =  motorC.position - degrees
            if abs(errorB) > correction_factor:
                motorB.on(SpeedDPS(-errorB * kp))
            else:
                motorB.stop()

            if abs(errorC) > correction_factor:
                motorC.on(SpeedDPS(-errorC * kp))
            else:
                motorC.stop()
    print('B = ' + str(motorB.position))
    print('C = ' + str(motorC.position))\n
"""
        )
        file.write(
            """sound.beep()
button.wait_for_pressed(['enter'])
gyro.reset()
print(gyro.angle)\n
"""
        )
        # Write the code for the first point
        if x["A"][1] == 0 and x["D"][1] == 0:
            file.write(
                f"""on_for_degrees_with_correction (speed= 150, degrees= {x["distance_degrees"][0]}, brake=False, correction_factor=0)\n"""
            )

        elif x["A"][1] != 0 and x["D"][1] != 0:
            file.write(
                f"""motorA.on_for_degrees(SpeedDPS(500), degrees={x["A"][1]})
motorD.on_for_degrees(SpeedDPS(500), degrees={x["D"][1]})
on_for_degrees_with_correction (speed= 150, degrees= {x["distance_degrees"][0]}, brake=False, correction_factor=0)\n
"""
            )
        for i in range(len(x["distance_degrees"])):
            print(i)


# class CodeWriter:
#     def __init__(self):
#         self.write_imports()

#     def write_imports(self):
#         print("import foo, motorb, gyro")

#     def write_move(self, degrees, a, d, mode):
#         print(f"move for {degrees}, {a}, {d}, {mode}")

#     def write_turn(self, angle, a, d, mode):
#         print(f"{angle}, {a}, {d}, {mode}")

# code_write = CodeWriter()

# code_write.write_move(100, 100, 0, 's')
# code_write.write_turn(90, 0, 9, 'p')
generate_function("my_function", ["arg1", "arg2"])
