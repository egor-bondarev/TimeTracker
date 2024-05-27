""" Actions on analytic frame. """
import tkinter as tk
from datetime import datetime
from tkinter import ttk, BOTH, RIGHT, BOTTOM
from tkcalendar import Calendar

from TaskTracker.local.models.analytic_model import AnalyticModel
from TaskTracker.local.helpers.control_states import FilterCheckboxes, FilterCheckboxValues
from TaskTracker.local.helpers.helpers import DateInterval, ReportButtons

class AnalyticController():
    """ Actions class. """
    def __init__(self):
        self.model = AnalyticModel()
        self.tree = ttk.Treeview()
        self.tree_scroll_y = ttk.Scrollbar()
        self.tree_scroll_x = ttk.Scrollbar()

    def change_checkboxes_state(
        self,
        checkboxes: FilterCheckboxes,
        checkbox_merge_value: bool = False):
        """ Change checkbox state in filter frame. """
        if checkbox_merge_value:
            checkboxes.date['state'] = 'disabled'
            checkboxes.desc['state'] = 'disabled'
            checkboxes.categories['state'] = 'disabled'
            checkboxes.duration['state'] = 'disabled'
            checkboxes.start_date['state'] = 'disabled'
            checkboxes.finish_date['state'] = 'disabled'
        else:
            checkboxes.date['state'] = 'enabled'
            checkboxes.desc['state'] = 'enabled'
            checkboxes.categories['state'] = 'enabled'
            checkboxes.duration['state'] = 'enabled'
            checkboxes.start_date['state'] = 'enabled'
            checkboxes.finish_date['state'] = 'enabled'

    def change_widgets_states(
        self,
        report_pressed: bool,
        report_buttons: ReportButtons):
        """ Change wifgets states after showing report. """
        if report_pressed:
            report_buttons.button_report['state'] = 'disabled'
            report_buttons.button_clear['state'] = 'enabled'
        else:
            report_buttons.button_report['state'] = 'enabled'
            report_buttons.button_clear['state'] = 'disabled'

    def calendar_set_date(
        self,
        calendar: Calendar,
        calendar_window: tk.Tk,
        entry: tk.StringVar):
        """ Choose date in calendar. """
        current_date = datetime.strptime(calendar.get_date(), '%m/%d/%y')
        entry.set(current_date.date())
        calendar_window.destroy()

    def set_window_focus(self, flag: bool, window: tk.Tk):
        """ Change window focus depends on flag. """
        if flag:
            window.wm_attributes("-topmost" , -1)
            window.focus_force()
        else:
            window.focus_displayof()
            window.wm_attributes("-topmost" , 0)

    def get_date(self, is_start_date: bool = False):
        """ Get date from existed json files. """
        period = self.model.get_date_period()
        if is_start_date:
            return period[0]

        return period[1]

    def show_report(self,
                    date_interval: DateInterval,
                    checkboxes_value: FilterCheckboxValues,
                    report_buttons: ReportButtons,
                    frame: ttk.Frame):
        """ Show table with statistic data. """

        # Column state.
        if checkboxes_value.merge_categories_value:
            checkboxes_value.date_value = False
            checkboxes_value.desc_value = False
            checkboxes_value.start_date_value = False
            checkboxes_value.finish_date_value = False
            checkboxes_value.categories_value = True
            checkboxes_value.duration_value = True

        checkbox_states = {
            'Date': checkboxes_value.date_value,
            'Description': checkboxes_value.desc_value, 
            'Category': checkboxes_value.categories_value,
            'Start time': checkboxes_value.start_date_value,
            'Finish time': checkboxes_value.finish_date_value,
            'Duration': checkboxes_value.duration_value
            }

        # List with columns for view.
        display_columns = []
        for column, value in checkbox_states.items():
            if value:
                display_columns.append(column)

        self.tree = ttk.Treeview(
            master = frame,
            columns = display_columns,
            show = "headings",
            name = 'tree result')

        # Creating heading for table.
        for column in display_columns:
            self.tree.heading(
                column,
                text = column,
                command = lambda column_index = column:
                self.sort(column_index, False))

        # Get statistic for view.
        statistic_data = self.model.get_statistic(
            date_interval,
            checkbox_states,
            checkboxes_value.merge_categories_value)

        # Insert data into table.
        for record in statistic_data:
            self.tree.insert("", 0, values = record)
        self.add_scrollbars(frame)
        self.tree.pack(fill=BOTH, expand=1)
        self.change_widgets_states(True, report_buttons)

    def add_scrollbars(self, frame: ttk.Frame):
        """ Add scrollbars to result table view. """
        self.tree_scroll_y = ttk.Scrollbar(
            master=frame,
            command=self.tree.yview,
            orient ="vertical")
        self.tree.configure(yscrollcommand=self.tree_scroll_y.set)
        self.tree_scroll_y.pack(side= RIGHT, fill= BOTH)

        self.tree_scroll_x = ttk.Scrollbar(
            master=frame,
            command=self.tree.xview,
            orient='horizontal')
        self.tree.configure(xscrollcommand=self.tree_scroll_x.set)
        self.tree_scroll_x.pack(side= BOTTOM, fill= BOTH)

    def clear_report(self, report_buttons: ReportButtons):
        """ Destroy table and scroll bars."""

        self.tree.destroy()
        self.tree = ttk.Treeview(show = "headings", name = 'tree result')
        self.tree_scroll_x.destroy()
        self.tree_scroll_y.destroy()
        self.change_widgets_states(False, report_buttons)

    def sort(self, column_number: int, descending: bool):
        """ Sort data in the column. """
        column_data = [
            (self.tree.set(item, column_number), item)
            for item in self.tree.get_children("")]
        column_data.sort(reverse = descending)

        for index, (_, item) in enumerate(column_data):
            self.tree.move(item, '', index)

        self.tree.heading(
            column_number,
            command = lambda: self.sort(column_number, not descending))
