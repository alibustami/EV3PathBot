"""This module constains the intro screen GUI."""
import os
import tkinter as tk
from tkinter import filedialog

import cv2

from src.GUIs.main_window_gui import MainWindow


class IntroScreen(tk.Frame):
    """This class contains the GUI for the intro screen."""

    def __init__(self, master=None):
        """Initialize the intro screen GUI.

        Arguments
        ---------
        master : tk.Tk
            The master window.
        """
        super().__init__(master)
        self.master = master
        self.master.title("EV3PathBOT")
        self.master.geometry("800x400")
        self.bg_color = "#23272D"
        self.master.configure(background=self.bg_color)
        self.master.resizable(False, False)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the intro screen."""

        def open_file_dialog():
            path_file = filedialog.askopenfilename(
                initialdir="/",
                title="Select a File",
                filetypes=(("png files", "*.png"), ("all files", "*.*")),
            )
            try:
                img = cv2.imread(path_file)
                if img is not None:
                    self.select_image_text.configure(
                        text="Image selected successfully",
                        fg="green",
                    )
                    self.select_image_text.place(x=160, y=100)
                    self.continue_button = tk.Button(
                        intro_screen,
                        text="Continue",
                        width=10,
                        height=2,
                        background="white",
                        font=("Calibri", 20),
                        fg="black",
                        bd=0,
                        activebackground="green",
                        activeforeground="white",
                        command=closew_window_and_open_main_window,
                    )
                    self.continue_button.place(x=315, y=300)

                else:
                    self.select_image_text.configure(
                        text="Unable to open image",
                        fg="red",
                    )
            except Exception as e:
                print(e)
                self.select_image_text.configure(
                    text="Unable to open image",
                    fg="red",
                )

        def _create_title_image(self):
            self.image = tk.PhotoImage(
                file=os.path.join("src", "GUIs", "assets", "ev3pathbot_logo.png")
            )
            self.image_label = tk.Label(image=self.image, bd=0)
            self.image_label.pack()

        def _add_welcoming_text(self):
            self.select_image_text = tk.Label(
                intro_screen,
                text="Select an image to start",
                font=("Calibri", 40),
                fg="white",
                bg=self.bg_color,
            )
            self.select_image_text.place(x=200, y=100)

        def _open_file_image(self):
            self.open_folder_image = tk.PhotoImage(
                file=os.path.join("src", "GUIs", "assets", "open_folder.png")
            )
            # resize the image
            self.open_folder_image = self.open_folder_image.subsample(5)
            self.open_folder_button = tk.Button(
                intro_screen,
                image=self.open_folder_image,
                command=open_file_dialog,
                bd=0,
                bg=self.bg_color,
            )
            self.open_folder_button.place(x=340, y=180)

        def closew_window_and_open_main_window():
            self.master.destroy()
            main_window = tk.Tk()
            app = MainWindow(master=main_window)
            app.mainloop()

        _create_title_image(self)
        _add_welcoming_text(self)
        _open_file_image(self)


if __name__ == "__main__":
    intro_screen = tk.Tk()
    app = IntroScreen(master=intro_screen)
    app.mainloop()
