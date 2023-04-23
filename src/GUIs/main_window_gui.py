"""This module contains the main window GUI class."""
import tkinter as tk
from time import sleep

import cv2
import numpy as np
from PIL import Image, ImageTk

from src.configs import get_config
from src.GUIs.key_logger import keylogger
from src.GUIs.mouse_logger import mouselogger

robot_length = get_config("robot_dimensions.length_x")
robot_width = get_config("robot_dimensions.width_y")

mat_length = get_config("mat_dimensions.length_x")
mat_width = get_config("mat_dimensions.width_y")

if not robot_length or not robot_width:
    raise ValueError("Robot length or width is not defined in the config file.")

if not mat_length or not mat_width:
    raise ValueError("Mat length or width is not defined in the config file.")


class MainWindow(tk.Frame):
    """This class contains the GUI for the main window."""

    def __init__(self, master=None, image: np.ndarray = None):
        """Initialize the main window GUI.

        Arguments
        ---------
        master : tk.Tk
            The master window.
        image : np.ndarray
            The image to be displayed.
        """
        super().__init__(master)
        self.master = master
        self.master.title("EV3PathBOT")
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        self.master.geometry(f"{width}x{height}")
        self.bg_color = "#23272D"
        self.master.configure(background=self.bg_color)
        self.master.resizable(False, False)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image)
        self.photo = ImageTk.PhotoImage(img)
        self.off_white = "#FAF9F6"
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the main window."""

        def _create_image_frame():
            """Create the image frame."""
            self.image_frame = tk.Frame(self.master, bg=self.off_white)
            self.image_frame.place(
                x=230,
                y=0,
                width=self.photo.width(),
                height=self.photo.height(),
            )
            self.image_canvas = tk.Canvas(
                self.image_frame,
                width=self.photo.width(),
                height=self.photo.height(),
                bg=self.off_white,
            )
            self.image_canvas.place(
                x=self.master.winfo_width(),
                y=self.master.winfo_height(),
            )
            self.image_canvas.create_image(0, 0, anchor="nw", image=self.photo)

        _create_image_frame()
