# https://stacktuts.com/tkinter-boiler-plate
# for basic boilerplate

# A simple object oriented tkinter window
import tkinter as tk
from tkinter import ttk

from .option import *
        
class OptionsScreen(tk.Tk):
    def __init__(self, options):
        super().__init__()

        # A function that adds self.destroy to the start of a function.
        def prepend_destroy(func):
            def result(*args, **kwargs):
                self.destroy()
                func(*args, **kwargs)
            return result

        # Create all the option buttons
        for option in options:
            ttk.Button(self, text=option.name, command=prepend_destroy(option.on_choose)).pack()