""" Class with calendar widget."""
import tkinter as tk
from tkinter import ttk, S
from datetime import datetime
from tkcalendar import Calendar

from local.controllers.analytic_controller import AnalyticController
import local.helpers.constants as const

class CalendarFrame:
    """Calendar class"""
    def __init__(self):
        self.actions = AnalyticController()
        self.calendar_frame = Calendar()
        self.calendar_window = tk.Tk()

    def view(self, date, entry: tk.StringVar):
        """Calendar window."""
        self.calendar_window.title('Calendar')
        self.calendar_window.geometry('300x300')

        date_object = datetime.strptime(date, const.DATE_MASK)

        self.calendar_frame = Calendar(
            self.calendar_window,
            selectmode = 'day',
            year = date_object.year,
            month = date_object.month,
            day = date_object.day)

        btn_enter = ttk.Button(
            master = self.calendar_window,
            text = "Select",
            command = lambda: self.actions.calendar_set_date(
                self.calendar_frame,
                self.calendar_window,
                entry)
            )
        btn_enter.pack(anchor = S)

        self.calendar_frame.pack(pady = 20)
        self.calendar_frame.focus_force()
        self.actions.set_window_focus(True, self.calendar_window)
