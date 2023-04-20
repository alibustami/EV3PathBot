"""This module contains the main code for EV3PathBot."""
from src.GUIs.main_screen import run
from src.path_creation import create_path

(
    robot_positions,
    robot_angles,
    additional_motor_1,
    additional_motor_2,
    additional_motors_mode,
) = run()
values = create_path(
    robot_positions, robot_angles, additional_motor_1, additional_motor_2, additional_motors_mode
)
print(values)
# print(values["x"],values["y"])
