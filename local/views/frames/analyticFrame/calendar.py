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

    def view(self, date, entry: tk.StringVar):
        """Calendar window."""
        calendar_window = tk.Tk()

        calendar_window.title('Calendar')
        calendar_window.geometry('300x300')

        date_object = datetime.strptime(date, const.DATE_MASK)

        calendar_frame = Calendar(
            calendar_window,
            selectmode = 'day',
            year = date_object.year,
            month = date_object.month,
            day = date_object.day)

        btn_enter = ttk.Button(
            master = calendar_window,
            text = "Enter",
            command = lambda: self.actions.calendar_set_date(calendar_frame, calendar_window, entry)
            )
        btn_enter.pack(anchor = S)

        calendar_frame.pack(pady = 20)
        calendar_frame.focus_force()
        self.actions.set_window_focus(True, calendar_window)
