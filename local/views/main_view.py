""" Main application view. """
import tkinter as tk
from tkinter import ttk, BOTH

from local.views.frames.input_frame import InputFrame
from local.views.frames.analyticFrame.analytic_frame import AnalyticFrame

class MainView():
    """Main window."""
    def __init__(self):
        # Set window.
        self.main_window = tk.Tk()
        self.main_window.title('TimeTracker')
        self.main_window.geometry('180x110')

        # Set frames.
        notebook = ttk.Notebook(self.main_window)
        notebook.pack(expand=True, fill=BOTH)

        input_frame = InputFrame(notebook, self.main_window)
        analytic_frame = AnalyticFrame(notebook)

        notebook.add(input_frame.view(), text="Time")
        notebook.add(analytic_frame.view(), text="Analytics")
        notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

        # Run window.
        self.main_window.wm_attributes("-topmost" , -1)
        self.main_window.focus_force()
        self.main_window.mainloop()

    def on_tab_change(self, event):
        """ For each tab sets personal window size. """

        tab = event.widget.tab('current')['text']
        if tab == 'Time':
            self.main_window.geometry('180x110')
        elif tab == 'Analytics':
            self.main_window.geometry('420x450')
