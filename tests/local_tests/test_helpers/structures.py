""" Helping structures for tests. """
from dataclasses import dataclass
from tkinter import ttk
import tkinter as tk


class ControlStateEnum():
    """ Class with widget available states. """
    ENABLED: str = 'enabled'
    DISABLED: str = 'disabled'
    NORMAL: str = 'normal'

@dataclass
class AnalyticFrameWidgets:
    """ Analytic frame widgets collection. """
    start_date_entry: ttk.Entry
    start_date_btn: ttk.Button
    end_date_entry: ttk.Entry
    end_date_btn: ttk.Button
    date_filter_checkbox: ttk.Checkbutton
    desc_filter_checkbox: ttk.Checkbutton
    startdate_filter_checkbox: ttk.Checkbutton
    enddate_filter_checkbox: ttk.Checkbutton
    category_filter_checkbox: ttk.Checkbutton
    duration_filter_checkbox: ttk.Checkbutton
    category_merge_checkbox: ttk.Checkbutton
    clear_btn: ttk.Button
    report_btn: ttk.Button
    tree_result: ttk.Treeview

@dataclass
class AnalyticWidgetsState:
    """ Analytic frame widgets states collection. """
    start_date_entry: ControlStateEnum
    start_date_btn: ControlStateEnum
    end_date_entry: ControlStateEnum
    end_date_btn: ControlStateEnum
    date_filter_checkbox: ControlStateEnum
    desc_filter_checkbox: ControlStateEnum
    startdate_filter_checkbox: ControlStateEnum
    enddate_filter_checkbox: ControlStateEnum
    category_filter_checkbox: ControlStateEnum
    duration_filter_checkbox: ControlStateEnum
    category_merge_checkbox: ControlStateEnum
    clear_btn: ControlStateEnum
    report_btn: ControlStateEnum

@dataclass
class AnalyticWidgetsWithValue:
    """ Analytic frame widgets values collection. """
    start_date_entry: tk.StringVar
    end_date_entry: tk.StringVar
    date_filter_checkbox: tk.BooleanVar
    desc_filter_checkbox: tk.BooleanVar
    startdate_filter_checkbox: tk.BooleanVar
    enddate_filter_checkbox: tk.BooleanVar
    category_filter_checkbox: tk.BooleanVar
    duration_filter_checkbox: tk.BooleanVar
    category_merge_checkbox: tk.BooleanVar
    tree_result: list
