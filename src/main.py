"""This module contains the main code for EV3PathBot."""
import logging

from src.GUIs.main_screen import run
from src.path_creation import create_path
from src.Writer.code_writer import CodeEditor

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: on file %(filename)s, on line %(lineno)d: %(message)s",
    filename="logs.log",
    filemode="w",
)

(
    robot_positions,
    robot_angles,
    additional_motor_1,
    additional_motor_2,
    additional_motors_mode,
    speed,
) = run()
point = create_path(
    robot_positions,
    robot_angles,
    additional_motor_1,
    additional_motor_2,
    additional_motors_mode,
    speed,
)

editor = CodeEditor()
editor(point)
