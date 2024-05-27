""" Class for connecting to  analytic controller. """
import re
import os
import tkinter as tk
from tkinter import ttk

from datetime import datetime
import TaskTracker.local.helpers.constants as const
from TaskTracker.local.helpers.control_states import FilterCheckboxValues, FilterCheckboxes
from TaskTracker.local.helpers.helpers import DateInterval, ReportButtons
from TaskTracker.local.controllers.analytic_controller import AnalyticController
from TaskTracker.local.views.frames.analyticFrame.analytic_frame import AnalyticFrame
from TaskTracker.local.views.frames.analyticFrame.calendar import CalendarFrame
from TaskTracker.tests.local_tests.test_helpers.structures import AnalyticFrameWidgets, \
    AnalyticWidgetsWithValue, TreeResults, ControlStateEnum, AnalyticFrameColumnCheckboxesNames

class AnalyticFrameWrapper():
    """ Test class for Analytic frame and connection with view and controller. """
    def __init__(self):
        self.analytic_controller = AnalyticController()

        self.main_window = tk.Tk()
        notebook = ttk.Notebook(self.main_window)
        self.analytic_view = AnalyticFrame(notebook)
        self.__set_default_settings()

        self.calendar_frame = CalendarFrame()

    def __set_default_dates(self):
        """ Set start date and end date for initialization. """

        file_list = [files for files in os.listdir('./')
                    if (re.search(r'\d{4}-\d\d-\d\d.json$', files)
        )]
        file_list.sort()

        if len(file_list) == 0:
            self.analytic_view.entry_start_date_value.set(str(datetime.date(datetime.now())))
            self.analytic_view.entry_end_date_value.set(str(datetime.date(datetime.now())))
        else:
            self.analytic_view.entry_start_date_value.set(file_list[0][:-5])
            self.analytic_view.entry_end_date_value.set(file_list[-1][:-5])

    def __set_default_settings(self):
        self.__set_default_dates()
        self.__set_default_widget_states()

    def __set_default_widget_states(self):
        self.analytic_view.btn_clear['state'] = ControlStateEnum.DISABLED

    def get_widgets(self) -> AnalyticFrameWidgets:
        """ Return control widgets. """

        return AnalyticFrameWidgets(
            start_date_entry = self.analytic_view.entry_start_date,
            start_date_btn = self.analytic_view.btn_change_start_date,
            end_date_entry = self.analytic_view.entry_end_date,
            end_date_btn = self.analytic_view.btn_change_end_date,
            date_filter_checkbox = self.analytic_view.checkbox_date,
            desc_filter_checkbox = self.analytic_view.checkbox_desc,
            startdate_filter_checkbox = self.analytic_view.checkbox_st,
            enddate_filter_checkbox = self.analytic_view.checkbox_ft,
            category_filter_checkbox = self.analytic_view.checkbox_categories,
            duration_filter_checkbox = self.analytic_view.checkbox_duration,
            category_merge_checkbox = self.analytic_view.merge_cat_checkbox,
            clear_btn = self.analytic_view.btn_clear,
            report_btn = self.analytic_view.btn_report,
            tree_result = self.analytic_controller.tree
        )

    def get_widgets_value(self) -> AnalyticWidgetsWithValue:
        """ Return widgets containing values. """

        return AnalyticWidgetsWithValue(
            start_date_entry = self.analytic_view.entry_start_date_value,
            end_date_entry = self.analytic_view.entry_end_date_value,
            date_filter_checkbox = self.analytic_view.checkbox_date_value,
            desc_filter_checkbox = self.analytic_view.checkbox_desc_value,
            startdate_filter_checkbox = self.analytic_view.checkbox_st_value,
            enddate_filter_checkbox = self.analytic_view.checkbox_ft_value,
            category_filter_checkbox = self.analytic_view.checkbox_categories_value,
            duration_filter_checkbox = self.analytic_view.checkbox_duration_value,
            category_merge_checkbox = self.analytic_view.checkbox_merge_by_category,
            tree_result = self.analytic_controller.tree
        )

    def press_button_report(self):
        """ Press report button.  """

        widgets_with_value = self.get_widgets_value()
        widgets = self.get_widgets()

        date_interval = DateInterval(
                date_start = datetime.strptime(
                    widgets_with_value.start_date_entry.get(),
                    const.DATE_MASK),
                date_finish = datetime.strptime(
                    widgets_with_value.end_date_entry.get(),
                    const.DATE_MASK))

        checkbox_values = FilterCheckboxValues(
            date_value = widgets_with_value.date_filter_checkbox.get(),
            desc_value = widgets_with_value.desc_filter_checkbox.get(),
            start_date_value = widgets_with_value.startdate_filter_checkbox.get(),
            finish_date_value = widgets_with_value.enddate_filter_checkbox.get(),
            categories_value = widgets_with_value.category_filter_checkbox.get(),
            duration_value = widgets_with_value.duration_filter_checkbox.get(),
            merge_categories_value = widgets_with_value.category_merge_checkbox.get()
        )

        report_buttons = ReportButtons(
                button_report = widgets.report_btn,
                button_clear = widgets.clear_btn
            )

        self.analytic_controller.show_report(
            date_interval,
            checkbox_values,
            report_buttons,
            self.analytic_view.results_frame)
        widgets_with_value.tree_result = self.analytic_view.tree

    def press_button_clear(self):
        """ Press clear button. """

        widgets_with_value = self.get_widgets_value()
        widgets = self.get_widgets()

        report_buttons = ReportButtons(
                button_report = widgets.report_btn,
                button_clear = widgets.clear_btn
            )
        self.analytic_controller.clear_report(report_buttons)
        widgets_with_value.tree_result = self.analytic_controller.tree

    def set_checkbox_value(self, checkbox_name: str, value: bool):
        """ Press checkbox. """

        widgets_with_value = self.get_widgets_value()
        match checkbox_name:
            case AnalyticFrameColumnCheckboxesNames.DATE.value:
                checkbox = widgets_with_value.date_filter_checkbox
            case AnalyticFrameColumnCheckboxesNames.DESCRIPTION.value:
                checkbox = widgets_with_value.desc_filter_checkbox
            case AnalyticFrameColumnCheckboxesNames.CATEGORY.value:
                checkbox = widgets_with_value.category_filter_checkbox
            case AnalyticFrameColumnCheckboxesNames.START_TIME.value:
                checkbox = widgets_with_value.startdate_filter_checkbox
            case AnalyticFrameColumnCheckboxesNames.FINISH_TIME.value:
                checkbox = widgets_with_value.enddate_filter_checkbox
            case AnalyticFrameColumnCheckboxesNames.DURATION.value:
                checkbox = widgets_with_value.duration_filter_checkbox
            case 'Merge category':
                widgets_with_value.duration_filter_checkbox.set(True)
                widgets_with_value.category_filter_checkbox.set(True)
                checkboxes_states = FilterCheckboxes(
                    date = self.analytic_view.checkbox_date,
                    desc = self.analytic_view.checkbox_desc,
                    categories = self.analytic_view.checkbox_categories,
                    start_date = self.analytic_view.checkbox_st,
                    finish_date = self.analytic_view.checkbox_ft,
                    duration = self.analytic_view.checkbox_duration,
                    merge_categories = self.analytic_view.merge_cat_checkbox
                )

                checkbox = widgets_with_value.category_merge_checkbox
                self.analytic_controller.change_checkboxes_state(checkboxes_states, value)

        checkbox.set(value)

    def get_date_from_calendar(self):
        """ Return current date from calendar frame. """

        return self.calendar_frame.calendar_frame.selection_get().isoformat()

    def press_select_date_in_calendar(self, date: str, date_widget_type: str):
        """ Press select button on the calendar frame. """

        date_object = datetime.strptime(date, const.DATE_MASK)
        widgets_with_value = self.get_widgets_value()
        start_flag = False
        if date_widget_type == 'end':
            date_widget = widgets_with_value.end_date_entry
        elif date_widget_type == 'start':
            date_widget = widgets_with_value.start_date_entry
            start_flag = True
        else:
            assert False, \
                f'date_type parameter has value {date_widget_type}, but expected start or end. '

        date_widget.set(date)
        self.calendar_frame.view(
            self.analytic_controller.get_date(start_flag),
            date_widget.get())

        self.calendar_frame.calendar_frame.selection_set(date_object)

    def get_results_from_table(self) -> dict:
        """ Return results from tree in dictionary. """

        widgets = self.get_widgets()
        results = {}
        line_num = 1

        for line in widgets.tree_result.get_children():
            line_content = widgets.tree_result.item(line)['values']
            one_line_result = TreeResults()
            column_num = 0

            for column in widgets.tree_result['columns']:
                match column:
                    case AnalyticFrameColumnCheckboxesNames.DATE:
                        one_line_result.date=str(line_content[column_num])
                    case AnalyticFrameColumnCheckboxesNames.DESCRIPTION:
                        one_line_result.description=str(line_content[column_num])
                    case AnalyticFrameColumnCheckboxesNames.CATEGORY:
                        one_line_result.category=str(line_content[column_num])
                    case AnalyticFrameColumnCheckboxesNames.START_TIME:
                        one_line_result.start_time=str(line_content[column_num])
                    case AnalyticFrameColumnCheckboxesNames.FINISH_TIME:
                        one_line_result.finish_time=str(line_content[column_num])
                    case AnalyticFrameColumnCheckboxesNames.DURATION:
                        one_line_result.duration=str(line_content[column_num])

                column_num += 1

            results[line_num] = one_line_result
            line_num += 1

        return results

    def set_start_date(self, new_value):
        """ Set start date value to the entry field. """

        widgets = self.get_widgets_value()
        widgets.start_date_entry.set(new_value)

    def set_end_date(self, new_value):
        """ Set end date value to the entry field. """

        widgets = self.get_widgets_value()
        widgets.end_date_entry.set(new_value)

    def sort_by_column(self, column_name: str = '', descending: bool = False):
        """ Sorting by column. """

        columns = self.get_widgets().tree_result['columns']

        assert column_name in columns, f'Column \'{column_name}\' is not visiable in results.'

        self.analytic_controller.sort(columns.index(column_name), descending)
