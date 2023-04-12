"""This module contains the main window GUI class."""
import tkinter as tk


class MainWindow(tk.Frame):
    """This class contains the GUI for the main window."""

    def __init__(self, master=None, image=None):
        """Initialize the main window GUI.

        Arguments
        ---------
        master : tk.Tk
            The master window.
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

    def create_widgets(self):
        """Create the widgets for the main window."""
