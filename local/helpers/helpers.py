""" Data models for different structures. """
from dataclasses import dataclass
from datetime import datetime
from tkinter import ttk

@dataclass
class DateInterval:
    """ Date interval from gui. """
    date_start: datetime
    date_finish: datetime

@dataclass
class ReportButtons:
    """ Description of clear and report button. """
    button_clear: ttk.Button
    button_report: ttk.Button

@dataclass
class CheckboxRecordFile:
    """ Accordance structure between checkbox name, field name in record, field name from file. """
    checkbox_name: str
    record_field: str
    json_field: str
