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
        self.notebook = notebook
        self.analytic_frame = ttk.Frame(notebook)

        self.controller = AnalyticController()

        self.entry_start_date_value = tk.StringVar()
        self.entry_end_date_value = tk.StringVar()

        self.checkbox_date_value = tk.BooleanVar(value=True)
        self.checkbox_desc_value = tk.BooleanVar(value=True)
        self.checkbox_st_value = tk.BooleanVar(value=True)
        self.checkbox_ft_value = tk.BooleanVar(value=True)
        self.checkbox_categories_value = tk.BooleanVar(value=True)
        self.checkbox_duration_value = tk.BooleanVar(value=True)

        self.checkbox_merge_by_category = tk.BooleanVar(value=False)

        self.checkboxes_value = FilterCheckboxValues(
            date_value = self.checkbox_date_value.get(),
            desc_value = self.checkbox_desc_value.get(),
            start_date_value = self.checkbox_st_value.get(),
            finish_date_value = self.checkbox_ft_value.get(),
            categories_value = self.checkbox_categories_value.get(),
            duration_value = self.checkbox_duration_value.get(),
            merge_categories_value = self.checkbox_merge_by_category.get()
            )

    def view(self) -> tk.Frame:
        """ Analytic frame view. """
        period_date_frame = ttk.Frame(self.analytic_frame)
        start_date_frame = ttk.Frame(period_date_frame)

        label_start_date = ttk.Label(master = start_date_frame, text = "Start date: ", width=7)

        start_date = self.controller.get_date(True)
        self.entry_start_date_value.set(start_date)

        entry_start_date = ttk.Entry(
            master = start_date_frame,
            textvariable = self.entry_start_date_value)

        btn_change_start_date = ttk.Button(
            master = start_date_frame,
            text = "Change",
            command = lambda: CalendarFrame().view(start_date, self.entry_start_date_value)
        )

        period_date_frame.pack()
        start_date_frame.pack()
        label_start_date.pack(padx=3, side = 'left')
        entry_start_date.pack(fill = 'x', side = 'left')
        btn_change_start_date.pack(padx=3, side = 'left')


        end_date_frame = ttk.Frame(period_date_frame)
        # Widgets for end date.
        label_end_date = ttk.Label(master = end_date_frame, text = "End date: ", width=7)

        end_date = self.controller.get_date()
        self.entry_end_date_value.set(end_date)

        entry_end_date = ttk.Entry(
            master = end_date_frame,
            textvariable = self.entry_end_date_value)

        btn_change_end_date = ttk.Button(
            master = end_date_frame,
            text = "Change",
            command = lambda: CalendarFrame().view(end_date, self.entry_end_date_value)
        )
        end_date_frame.pack()

        label_end_date.pack(padx=3, side = 'left')
        entry_end_date.pack(fill = 'x', side = 'left')
        btn_change_end_date.pack(padx=3, side = 'left')

        # Choice columns.
        settings_frame = ttk.Labelframe(self.analytic_frame)
        checkboxes_frame = ttk.Frame(settings_frame)
        checkboxes_frame_2 = ttk.Frame(settings_frame)
        checkboxes_frame_3 = ttk.Frame(settings_frame)

        checkbox_date = ttk.Checkbutton(
            master = checkboxes_frame,
            text = 'Date',
            variable = self.checkbox_date_value)
        checkbox_desc = ttk.Checkbutton(
            master = checkboxes_frame,
            text = 'Description',
            variable = self.checkbox_desc_value)
        checkbox_st = ttk.Checkbutton(
            master = checkboxes_frame,
            text = 'Start time',
            variable = self.checkbox_st_value)

        checkbox_ft = ttk.Checkbutton(
            master = checkboxes_frame_2,
            text = 'Finish time',
            variable = self.checkbox_ft_value)
        checkbox_categories = ttk.Checkbutton(
            master = checkboxes_frame_2,
            text = 'Categories',
            variable = self.checkbox_categories_value)

        checkbox_duration = ttk.Checkbutton(
            master = checkboxes_frame_3,
            text = 'Duration',
            variable = self.checkbox_duration_value)

        settings_frame.pack(fill = 'x')
        checkboxes_frame.pack(side = 'left', anchor = 'nw')
        checkboxes_frame_2.pack(side = 'left', anchor = 'nw')
        checkboxes_frame_3.pack(side = 'left', anchor = 'nw')

        checkbox_date.pack(side = 'top', anchor = 'nw')
        checkbox_desc.pack(side = 'top', anchor = 'nw')
        checkbox_st.pack(side = 'top', anchor = 'nw')

        checkbox_categories.pack(side = 'top', anchor = 'nw')
        checkbox_ft.pack(side = 'top', anchor = 'nw')
        checkbox_duration.pack(side = 'top', anchor = 'nw')


        merge_frame = ttk.Labelframe(self.analytic_frame, text = 'Merge by')
        merge_cat_checkbox = ttk.Checkbutton(
            master = merge_frame,
            text = 'categories',
            variable = self.checkbox_merge_by_category,
            command = lambda: self.controller.change_checkboxes_state(
                checkboxes_states,
                self.checkbox_merge_by_category.get()))

        merge_cat_checkbox.pack(side = 'left')
        merge_frame.pack(fill=BOTH)

        manage_results_frame = ttk.Frame(self.analytic_frame)

        btn_clear = ttk.Button(
            master = manage_results_frame,
            text = 'Clear',
            command = lambda: self.controller.clear_report(get_report_buttons())
        )

        checkboxes_states = FilterCheckboxes(
            date = checkbox_date,
            desc = checkbox_desc,
            categories = checkbox_categories,
            start_date = checkbox_st,
            finish_date = checkbox_ft,
            duration = checkbox_duration,
            merge_categories = merge_cat_checkbox
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

        def get_date_interval(self):
            return DateInterval(
                date_start = datetime.strptime(self.entry_start_date_value.get(), const.DATE_MASK),
                date_finish = datetime.strptime(self.entry_end_date_value.get(), const.DATE_MASK))

        def get_report_buttons():
            return ReportButtons(
                button_report = btn_report,
                button_clear = btn_clear
            )

        # Button for getting report.
        results_frame = ttk.Labelframe(self.analytic_frame, text = 'Result')
        btn_report = ttk.Button(
            master = manage_results_frame,
            text = 'Report',
            command = lambda: self.controller.show_report(
                get_date_interval(self),
                get_checkboxes_values(self),
                get_report_buttons(),
                results_frame
                )
        )

        btn_clear['state'] = 'disabled'

        manage_results_frame.pack(fill = 'x')
        btn_report.pack(padx=3, side = 'right')
        btn_clear.pack(padx=3, side = 'right')
        results_frame.pack( expand = True, fill = BOTH)

        self.analytic_frame.pack(fill=BOTH, expand=True)
        return self.analytic_frame
