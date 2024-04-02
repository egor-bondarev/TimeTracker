""" Data models for control states. """
from dataclasses import dataclass
from tkinter import ttk
import tkinter

@dataclass
class FilterCheckboxes:
    """ Information visible control on analytic frame. """
    date: ttk.Checkbutton
    desc: ttk.Checkbutton
    start_date: ttk.Checkbutton
    finish_date: ttk.Checkbutton
    categories: ttk.Checkbutton
    duration: ttk.Checkbutton
    merge_categories: ttk.Checkbutton

@dataclass
class FilterCheckboxValues:
    """ Information about values of analytic frame checkboxes. """
    date_value: bool
    desc_value: bool
    start_date_value: bool
    finish_date_value: bool
    categories_value: bool
    duration_value: bool
    merge_categories_value: bool

@dataclass
class InputFrameAllControls:
    """ Stated of input frame controls. """
    btn_start: ttk.Button
    btn_finish: ttk.Button
    category_combobox: ttk.Combobox
    entry: ttk.Entry
    category_value: tkinter.StringVar
    entry_value: tkinter.StringVar
