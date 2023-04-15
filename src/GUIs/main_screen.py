"""This module contains the main window GUI."""
import os

import cv2
import numpy as np

from src.configs import get_config
from src.converters import stud_to_pixel
from src.motors_extraction import motors_extraction

robot_length: int = int(get_config("robot_dimensions.length_x"))
robot_width: int = int(get_config("robot_dimensions.width_y"))

if not robot_length or not robot_width:
    raise ValueError("Robot length or width is not defined in the config file.")

mat_length: int = int(get_config("mat_dimensions.length_x"))
mat_width: int = int(get_config("mat_dimensions.width_y"))

if not mat_length or not mat_width:
    raise ValueError("Mat length or width is not defined in the config file.")

detla_theta: int = int(get_config("steps.delta_theta"))
delta_pixels: int = int(get_config("steps.delta_pixels"))
additional_motors_steps: int = int(get_config("steps.additional_motors_steps"))

if not detla_theta or not delta_pixels or not additional_motors_steps:
    raise ValueError("Steps are not defined in the config file.")

large_motors_positive_direction: str = get_config(
    "robot_movement_configurations.large_motor_positive_direction"
)
gyro_positive_direction: str = get_config("robot_movement_configurations.gyro_positive_direction")

if large_motors_positive_direction is None or gyro_positive_direction is None:
    raise ValueError("Robot movement configurations are not defined in the config file.")


def run(image: np.ndarray):
    """Run the main window GUI."""
    _, medium_motors_list = motors_extraction()
    first_additional_motor, second_additional_motor = medium_motors_list

    image_path: str = get_config("mat_image_path")
    if image_path:
        original_image: np.ndarray = cv2.imread(image_path)
    else:
        original_image = image
    robot_lengh_x_pixels: int = stud_to_pixel(robot_length)
    robot_width_y_pixels: int = stud_to_pixel(robot_width)
    image_height_y, image_width_x, _ = original_image.shape
    robot_top_left_corner = np.array([0, image_height_y - robot_width_y_pixels])
    theta: int = 0
    additional_motor_1: int = 0
    additional_motor_2: int = 0
    saved_boxes: list = []
    saved_theta: list = []
    additional_motor_1_list: list = []
    additional_motor_2_list: list = []
    while True:
        image = original_image.copy()
        if saved_boxes:
            for i in range(len(saved_boxes)):
                cv2.polylines(image, [saved_boxes[i].astype(int)], True, (0, 255, 0), 2)
                if large_motors_positive_direction:
                    cv2.circle(
                        image,
                        (
                            (int(saved_boxes[i][0][0]) + int(saved_boxes[i][1][0])) // 2,
                            (int(saved_boxes[i][0][1]) + int(saved_boxes[i][1][1])) // 2,
                        ),
                        5,
                        (0, 0, 255),
                        -1,
                    )
                else:
                    cv2.circle(
                        image,
                        (
                            (int(saved_boxes[i][2][0]) + int(saved_boxes[i][3][0])) // 2,
                            (int(saved_boxes[i][2][1]) + int(saved_boxes[i][3][1])) // 2,
                        ),
                        5,
                        (0, 0, 255),
                        -1,
                    )
                cv2.putText(
                    image,
                    str(saved_theta[i]),
                    (int(saved_boxes[i][0][0]), int(saved_boxes[i][0][1])),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    1,
                )
                cv2.putText(
                    image,
                    first_additional_motor + ": " + str(additional_motor_1_list[i]),
                    (int(saved_boxes[i][0][0] + 40), int(saved_boxes[i][0][1])),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0),
                    1,
                )
                cv2.putText(
                    image,
                    second_additional_motor + ": " + str(additional_motor_2_list[i]),
                    (int(saved_boxes[i][0][0] + 130), int(saved_boxes[i][0][1])),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0),
                    1,
                )

            if len(saved_boxes) > 1:
                for i in range(len(saved_boxes) - 1):
                    if large_motors_positive_direction:
                        cv2.line(
                            image,
                            (
                                (int(saved_boxes[i][0][0]) + int(saved_boxes[i][1][0])) // 2,
                                (int(saved_boxes[i][0][1]) + int(saved_boxes[i][1][1])) // 2,
                            ),
                            (
                                (int(saved_boxes[i + 1][0][0]) + int(saved_boxes[i + 1][1][0]))
                                // 2,
                                (int(saved_boxes[i + 1][0][1]) + int(saved_boxes[i + 1][1][1]))
                                // 2,
                            ),
                            (0, 0, 255),
                            2,
                        )
                    else:
                        cv2.line(
                            image,
                            (
                                (int(saved_boxes[i][2][0]) + int(saved_boxes[i][3][0])) // 2,
                                (int(saved_boxes[i][2][1]) + int(saved_boxes[i][3][1])) // 2,
                            ),
                            (
                                (int(saved_boxes[i + 1][2][0]) + int(saved_boxes[i + 1][3][0]))
                                // 2,
                                (int(saved_boxes[i + 1][2][1]) + int(saved_boxes[i + 1][3][1]))
                                // 2,
                            ),
                            (0, 0, 255),
                            2,
                        )

        box = np.array(
            [
                [robot_top_left_corner[0], robot_top_left_corner[1]],
                [robot_top_left_corner[0] + robot_lengh_x_pixels, robot_top_left_corner[1]],
                [
                    robot_top_left_corner[0] + robot_lengh_x_pixels,
                    robot_top_left_corner[1] + robot_width_y_pixels,
                ],
                [robot_top_left_corner[0], robot_top_left_corner[1] + robot_width_y_pixels],
            ]
        )

        center = np.mean(box, axis=0)
        translated_box = box - center
        theta_rad = np.deg2rad(theta)
        rot_matrix = np.array(
            [[np.cos(theta_rad), -np.sin(theta_rad)], [np.sin(theta_rad), np.cos(theta_rad)]]
        )
        rotated_box = np.dot(translated_box, rot_matrix)

        rotated_box = rotated_box + center

        cv2.polylines(image, [rotated_box.astype(int)], True, (0, 255, 0), 2)
        cv2.putText(
            image,
            str(theta),
            (int(rotated_box[0][0]), int(rotated_box[0][1])),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            1,
        )
        cv2.putText(
            image,
            first_additional_motor + ": " + str(additional_motor_1),
            (int(rotated_box[0][0] + 40), int(rotated_box[0][1])),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1,
        )
        cv2.putText(
            image,
            second_additional_motor + ": " + str(additional_motor_2),
            (int(rotated_box[0][0] + 130), int(rotated_box[0][1])),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1,
        )
        if large_motors_positive_direction:
            cv2.circle(
                image,
                (
                    (int(rotated_box[0][0]) + int(rotated_box[1][0])) // 2,
                    (int(rotated_box[0][1]) + int(rotated_box[1][1])) // 2,
                ),
                5,
                (0, 0, 255),
                -1,
            )
        else:
            cv2.circle(
                image,
                (
                    (int(rotated_box[2][0]) + int(rotated_box[3][0])) // 2,
                    (int(rotated_box[2][1]) + int(rotated_box[3][1])) // 2,
                ),
                5,
                (0, 0, 255),
                -1,
            )
        cv2.imshow("image", image)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        elif key == ord(","):
            theta += detla_theta
        elif key == ord("."):
            theta -= detla_theta
        elif key == ord("a"):
            robot_top_left_corner[0] -= delta_pixels
        elif key == ord("d"):
            robot_top_left_corner[0] += delta_pixels
        elif key == ord("w"):
            robot_top_left_corner[1] -= delta_pixels
        elif key == ord("s"):
            robot_top_left_corner[1] += delta_pixels
        elif key == ord("p"):
            saved_boxes.append(rotated_box)
            saved_theta.append(theta)
            additional_motor_1_list.append(additional_motor_1)
            additional_motor_2_list.append(additional_motor_2)
            additional_motor_1: int = 0
            additional_motor_2: int = 0
        elif key == ord("z"):
            additional_motor_1 += additional_motors_steps
        elif key == ord("x"):
            additional_motor_1 -= additional_motors_steps
        elif key == ord("c"):
            additional_motor_2 += additional_motors_steps
        elif key == ord("v"):
            additional_motor_2 -= additional_motors_steps

    cv2.destroyAllWindows()
