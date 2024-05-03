""" Class for connecting to  analytic controller. """
import tkinter as tk
from tkinter import ttk
from local.helpers.control_states import FilterCheckboxValues, FilterCheckboxes
from local.controllers.analytic_controller import AnalyticController
from local.views.frames.analyticFrame.analytic_frame import AnalyticFrame
import dataclasses

@dataclasses.dataclass
class AnalyticFrameControls():
    start_date_entry = ttk.Entry(),
    start_date_btn = ttk.Button()
    

class AnalyticFrameMock():
    def __init__(self):
        self.input_controller = AnalyticController()

        self.main_window = tk.Tk()
        notebook = ttk.Notebook(self.main_window)
        self.analytic_view = AnalyticFrame(notebook, self.main_window)
        
        self.analytic_view.analytic_frame
    