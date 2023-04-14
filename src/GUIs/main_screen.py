"""This module contains the main window GUI."""
import os

import cv2
import numpy as np

from src.configs import get_config
from src.converters import stud_to_pixel

robot_length: int = int(get_config("robot_dimensions.length"))
robot_width: int = int(get_config("robot_dimensions.width"))

mat_length: int = int(get_config("mat_dimensions.length_x"))
mat_width: int = int(get_config("mat_dimensions.width_y"))

if not robot_length or not robot_width:
    raise ValueError("Robot length or width is not defined in the config file.")

if not mat_length or not mat_width:
    raise ValueError("Mat length or width is not defined in the config file.")


image_path: str = get_config("mat_image_path")
original_image: np.ndarray = cv2.imread(image_path)
robot_lengh_x_pixels: int = stud_to_pixel(robot_length)
robot_width_y_pixels: int = stud_to_pixel(robot_width)
image_height_y, image_width_x, _ = original_image.shape
robot_top_left_corner = np.array([0, image_height_y - robot_width_y_pixels])

theta: int = 0
saved_boxes: list = []
saved_theta: list = []
saved_lines: list = []
while True:
    image = original_image.copy()
    if saved_boxes:
        for i in range(len(saved_boxes)):
            cv2.polylines(image, [saved_boxes[i].astype(int)], True, (0, 255, 0), 2)
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
            cv2.putText(
                image,
                str(saved_theta[i]),
                (int(saved_boxes[i][0][0]), int(saved_boxes[i][0][1])),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                1,
            )
        if len(saved_boxes) > 1:
            for i in range(len(saved_boxes) - 1):
                cv2.line(
                    image,
                    (
                        (int(saved_boxes[i][0][0]) + int(saved_boxes[i][1][0])) // 2,
                        (int(saved_boxes[i][0][1]) + int(saved_boxes[i][1][1])) // 2,
                    ),
                    (
                        (int(saved_boxes[i + 1][0][0]) + int(saved_boxes[i + 1][1][0])) // 2,
                        (int(saved_boxes[i + 1][0][1]) + int(saved_boxes[i + 1][1][1])) // 2,
                    ),
                    (255, 0, 0),
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
    cv2.imshow("image", image)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord(","):
        theta += 3
    elif key == ord("."):
        theta -= 3
    elif key == ord("a"):
        robot_top_left_corner[0] -= 5
    elif key == ord("d"):
        robot_top_left_corner[0] += 5
    elif key == ord("w"):
        robot_top_left_corner[1] -= 5
    elif key == ord("s"):
        robot_top_left_corner[1] += 5
    elif key == ord("p"):
        saved_boxes.append(rotated_box)
        saved_theta.append(theta)

cv2.destroyAllWindows()
