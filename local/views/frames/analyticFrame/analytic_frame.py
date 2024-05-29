""" File for description analytic frame."""
import tkinter as tk
from tkinter import ttk, BOTH
from datetime import datetime

from local.views.frames.analyticFrame.calendar import CalendarFrame
from local.controllers.analytic_controller import AnalyticController
from local.helpers.control_states import FilterCheckboxes, FilterCheckboxValues
from local.helpers.helpers import DateInterval, ReportButtons
import local.helpers.constants as const

class AnalyticFrame():
    """ Description of analytic frame."""

    def __init__(self, notebook: ttk.Notebook):
        """ Initialise frame. """
        self.controller = AnalyticController()
        self.notebook = notebook
        self.analytic_frame = ttk.Frame(notebook)

        self.period_date_frame = ttk.Frame(self.analytic_frame)
        self.start_date_frame = ttk.Frame(self.period_date_frame)
        self.end_date_frame = ttk.Frame(self.period_date_frame)
        self.settings_frame = ttk.Labelframe(self.analytic_frame)
        self.checkboxes_frame = ttk.Frame(self.settings_frame)
        self.checkboxes_frame_2 = ttk.Frame(self.settings_frame)
        self.checkboxes_frame_3 = ttk.Frame(self.settings_frame)

        self.checkbox_date_value = tk.BooleanVar(value = True, name = 'checkbox date value')
        self.checkbox_desc_value = tk.BooleanVar(value = True, name = 'checkbox desc value')
        self.checkbox_st_value = tk.BooleanVar(value = True, name = 'checkbox start time value')
        self.checkbox_ft_value = tk.BooleanVar(value = True, name = 'checkbox finish time value')
        self.checkbox_categories_value = tk.BooleanVar(
            value = True,
            name = 'checkbox categories value')
        self.checkbox_duration_value = tk.BooleanVar(value = True, name = 'checkbox duration value')

        self.checkbox_merge_by_category = tk.BooleanVar(
            value = False,
            name = 'checkbox merge by category')
        self.merge_frame = ttk.Labelframe(self.analytic_frame, text = 'Merge by')

        self.manage_results_frame = ttk.Frame(self.analytic_frame)
        self.results_frame = ttk.Labelframe(self.analytic_frame, text = 'Result')

        self.checkboxes_value = FilterCheckboxValues(
            date_value = self.checkbox_date_value.get(),
            desc_value = self.checkbox_desc_value.get(),
            start_date_value = self.checkbox_st_value.get(),
            finish_date_value = self.checkbox_ft_value.get(),
            categories_value = self.checkbox_categories_value.get(),
            duration_value = self.checkbox_duration_value.get(),
            merge_categories_value = self.checkbox_merge_by_category.get()
            )

        self.entry_start_date_value = tk.StringVar(name = 'value start date')
        self.entry_start_date = ttk.Entry(name = 'entry start date')
        self.btn_change_start_date = ttk.Button(name = 'button start date')

        self.entry_end_date_value = tk.StringVar(name = 'value end date')
        self.entry_end_date = ttk.Entry(name = 'entry end date')
        self.btn_change_end_date = ttk.Button(name = 'button end date')

        self.checkbox_date = ttk.Checkbutton(name = 'checkbox column date')
        self.checkbox_desc = ttk.Checkbutton(name = 'checkbox column description')
        self.checkbox_st = ttk.Checkbutton(name = 'checkbox column start time')
        self.checkbox_ft = ttk.Checkbutton(name = 'checkbox column finish time')
        self.checkbox_categories = ttk.Checkbutton(name = 'checkbox column category')
        self.checkbox_duration = ttk.Checkbutton(name = 'checkbox column duration')
        self.merge_cat_checkbox = ttk.Checkbutton(name = 'checkbox merge categories')

        self.btn_clear = ttk.Button(name = 'button clear result')
        self.btn_report = ttk.Button(name = 'button report')
        self.tree = ttk.Treeview(master = self.results_frame, name = 'tree result')

    def view(self) -> tk.Frame:
        """ Analytic frame view. """

        label_start_date = ttk.Label(master = self.start_date_frame, text = "Start date: ", width = 10)

        start_date = self.controller.get_date(True)
        self.entry_start_date = ttk.Entry(
            master = self.start_date_frame,
            textvariable = self.entry_start_date_value)
        self.entry_start_date_value.set(start_date)

        self.btn_change_start_date = ttk.Button(
            master = self.start_date_frame,
            text = "Change",
            command = lambda: CalendarFrame().view(start_date, self.entry_start_date_value)
        )

        self.period_date_frame.pack()
        self.start_date_frame.pack()
        label_start_date.pack(padx=3, side = 'left')
        self.entry_start_date.pack(fill = 'x', side = 'left')
        self.btn_change_start_date.pack(padx=3, side = 'left')

        label_end_date = ttk.Label(master = self.end_date_frame, text = "End date: ", width = 10)

        end_date = self.controller.get_date()

        self.entry_end_date = ttk.Entry(
            master = self.end_date_frame,
            textvariable = self.entry_end_date_value)
        self.entry_end_date_value.set(end_date)

        self.btn_change_end_date = ttk.Button(
            master = self.end_date_frame,
            text = "Change",
            command = lambda: CalendarFrame().view(end_date, self.entry_end_date_value)
        )
        self.end_date_frame.pack()

        label_end_date.pack(padx=3, side = 'left')
        self.entry_end_date.pack(fill = 'x', side = 'left')
        self.btn_change_end_date.pack(padx=3, side = 'left')

        # Choice columns.
        self.settings_frame.pack(fill = 'x')
        self.checkboxes_frame.pack(side = 'left', anchor = 'nw')
        self.checkboxes_frame_2.pack(side = 'left', anchor = 'nw')
        self.checkboxes_frame_3.pack(side = 'left', anchor = 'nw')
        self.checkbox_date = ttk.Checkbutton(
            master = self.checkboxes_frame,
            text = 'Date',
            variable = self.checkbox_date_value)
        self.checkbox_desc = ttk.Checkbutton(
            master = self.checkboxes_frame,
            text = 'Description',
            variable = self.checkbox_desc_value)
        self.checkbox_st = ttk.Checkbutton(
            master = self.checkboxes_frame,
            text = 'Start time',
            variable = self.checkbox_st_value)

        self.checkbox_ft = ttk.Checkbutton(
            master = self.checkboxes_frame_2,
            text = 'Finish time',
            variable = self.checkbox_ft_value)
        self.checkbox_categories = ttk.Checkbutton(
            master = self.checkboxes_frame_2,
            text = 'Categories',
            variable = self.checkbox_categories_value)

        self.checkbox_duration = ttk.Checkbutton(
            master = self.checkboxes_frame_3,
            text = 'Duration',
            variable = self.checkbox_duration_value)

        self.checkbox_date.pack(side = 'top', anchor = 'nw')
        self.checkbox_desc.pack(side = 'top', anchor = 'nw')
        self.checkbox_st.pack(side = 'top', anchor = 'nw')

        self.checkbox_categories.pack(side = 'top', anchor = 'nw')
        self.checkbox_ft.pack(side = 'top', anchor = 'nw')
        self.checkbox_duration.pack(side = 'top', anchor = 'nw')

        self.merge_cat_checkbox = ttk.Checkbutton(
            master = self.merge_frame,
            text = 'categories',
            variable = self.checkbox_merge_by_category,
            command = lambda: self.controller.change_checkboxes_state(
                checkboxes_states,
                self.checkbox_merge_by_category.get()))

        self.merge_cat_checkbox.pack(side = 'left')
        self.merge_frame.pack(fill=BOTH)


        self.btn_clear = ttk.Button(
            master = self.manage_results_frame,
            text = 'Clear',
            command = lambda: self.controller.clear_report(get_report_buttons())
        )

        checkboxes_states = FilterCheckboxes(
            date = self.checkbox_date,
            desc = self.checkbox_desc,
            categories = self.checkbox_categories,
            start_date = self.checkbox_st,
            finish_date = self.checkbox_ft,
            duration = self.checkbox_duration,
            merge_categories = self.merge_cat_checkbox
        )

        def get_checkboxes_values(self):
            return FilterCheckboxValues(
                date_value = self.checkbox_date_value.get(),
                desc_value = self.checkbox_desc_value.get(),
                start_date_value = self.checkbox_st_value.get(),
                finish_date_value = self.checkbox_ft_value.get(),
                categories_value = self.checkbox_categories_value.get(),
                duration_value = self.checkbox_duration_value.get(),
                merge_categories_value = self.checkbox_merge_by_category.get())

        def get_date_interval():
            return DateInterval(
                date_start = datetime.strptime(self.entry_start_date_value.get(), const.DATE_MASK),
                date_finish = datetime.strptime(self.entry_end_date_value.get(), const.DATE_MASK))

        def get_report_buttons():
            return ReportButtons(
                button_report = self.btn_report,
                button_clear = self.btn_clear
            )

        # Button for getting report.
        self.btn_report = ttk.Button(
            master = self.manage_results_frame,
            text = 'Report',
            command = lambda: self.controller.show_report(
                get_date_interval(),
                get_checkboxes_values(self),
                get_report_buttons(),
                self.results_frame
                )
        )

        self.btn_clear['state'] = 'disabled'

        self.manage_results_frame.pack(fill = 'x')
        self.btn_report.pack(padx=3, side = 'right')
        self.btn_clear.pack(padx=3, side = 'right')
        self.results_frame.pack( expand = True, fill = BOTH)

        self.analytic_frame.pack(fill=BOTH, expand=True)
        return self.analytic_frame
