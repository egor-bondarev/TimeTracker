""" Class with customs asserts. """
import re
from dataclasses import dataclass
from typing import Optional
from tkinter import ttk
from TaskTracker.tests.local_tests.test_helpers.structures import ControlStateEnum
from TaskTracker.tests.local_tests.test_helpers.json_helper import JsonHelper
from TaskTracker.local.helpers.control_states import InputFrameAllControls
from TaskTracker.tests.local_tests.test_helpers.structures import AnalyticFrameWidgets, \
    AnalyticWidgetsWithValue, AnalyticFrameColumnCheckboxesNames

@dataclass
class ExpectedValues:
    """ Class of widgets value. """
    action_value: Optional[str] = None
    category_value: Optional[str] = None
    start_time_value: Optional[str] = None
    finish_time_value: Optional[str] = None
    duration_value: Optional[str] = None

class Asserts():
    """ Custom asserts. """

# Asserts for widgets states and values.
    @staticmethod
    def __get_widget_name(widget):
        if type(widget).__name__ in ['StringVar', 'BooleanVar']:
            return str(widget)

        return widget.winfo_name()

    @staticmethod
    def assert_widget_is_enabled(widget):
        """ Assert that widget state is enabled or normal. """

        widget_name = Asserts.__get_widget_name(widget)

        assert str(widget['state']) in \
            [ControlStateEnum.NORMAL, ControlStateEnum.ENABLED], \
            f"Control \'{widget_name}\' has state \'{widget['state']}\' but expected " \
                f"\'{ControlStateEnum.NORMAL}\' or \'{ControlStateEnum.ENABLED}\'"

    @staticmethod
    def assert_widget_is_disabled(widget):
        """ Assert that widget state is disabled. """

        widget_name = Asserts.__get_widget_name(widget)

        assert str(widget['state']) == ControlStateEnum.DISABLED, \
            f"Control \'{widget_name}\' has state \'{widget['state']}\' but expected " \
                f"\'{ControlStateEnum.DISABLED}\'"

    @staticmethod
    def assert_widget_value_is_empty(widget):
        """ Assert that tk.StringVar value is empty. """

        widget_name = Asserts.__get_widget_name(widget)

        assert widget.get() == '', \
            f"Widget \'{widget_name}\' has value \'{widget.get()}\' but expected empty"

    @staticmethod
    def assert_widget_value_is_equal(widget, expected_value):
        """ Assert that tk.StringVar value has expected value. """

        widget_name = Asserts.__get_widget_name(widget)

        assert str(widget.get()) == str(expected_value), \
            f"Widget \'{widget_name}\' has value \'{widget.get()}\' but expected \'{expected_value}\'"        

    @staticmethod
    def assert_controls_state_started_task(widgets: InputFrameAllControls):
        """ Assert for started widgets state. """

        disabled_widgets_list = [
            widgets.btn_start,
            widgets.category_combobox,
            widgets.entry]

        Asserts.assert_widget_is_enabled(widgets.btn_finish)

        for widget in disabled_widgets_list:
            Asserts.assert_widget_is_disabled(widget)

    @staticmethod
    def assert_controls_state_finished_task(widgets: InputFrameAllControls):
        """ Assert for finished widgets state. """

        disabled_widgets_list = [
            widgets.btn_start,
            widgets.btn_finish]

        enabled_widgets_list = [
            widgets.category_combobox,
            widgets.entry]

        Asserts.assert_widget_value_is_empty(widgets.category_value)
        Asserts.assert_widget_value_is_empty(widgets.entry_value)

        for widget in disabled_widgets_list:
            Asserts.assert_widget_is_disabled(widget)

        for widget in enabled_widgets_list:
            Asserts.assert_widget_is_enabled(widget)

    @staticmethod
    def assert_start_frame_default_state(widgets: InputFrameAllControls):
        """ Assert for default widget state. """

        Asserts.assert_widget_is_enabled(widgets.entry)
        Asserts.assert_widget_value_is_empty(widgets.entry_value)

        Asserts.assert_widget_is_enabled(widgets.category_combobox)
        Asserts.assert_widget_value_is_empty(widgets.category_value)

        Asserts.assert_widget_is_disabled(widgets.btn_start)
        Asserts.assert_widget_is_disabled(widgets.btn_finish)

    @staticmethod
    def assert_start_frame_state_with_desc(widgets: InputFrameAllControls):
        """ Assert widget state when description has symbols inside. """

        widget_list = [
            widgets.btn_start,
            widgets.btn_finish,
            widgets.category_combobox,
            widgets.entry]

        for widget in widget_list:
            Asserts.assert_widget_is_enabled(widget)

    @staticmethod
    def assert_analytic_frame_default_state(widgets: AnalyticFrameWidgets):
        """ Assert analytic frame widgets state by default. """

        enabled_widget_list = [
            widgets.start_date_entry,
            widgets.start_date_btn,
            widgets.end_date_entry,
            widgets.end_date_btn,
            widgets.date_filter_checkbox,
            widgets.desc_filter_checkbox,
            widgets.startdate_filter_checkbox,
            widgets.enddate_filter_checkbox,
            widgets.category_filter_checkbox,
            widgets.duration_filter_checkbox,
            widgets.category_merge_checkbox,
            widgets.report_btn
        ]
        for widget in enabled_widget_list:
            Asserts.assert_widget_is_enabled(widget)

        Asserts.assert_widget_is_disabled(widgets.clear_btn)

    @staticmethod
    def assert_analytic_frame_default_values(
        widgets: AnalyticWidgetsWithValue,
        start_date: str,
        end_date: str):
        """ Assert analytic frame widgets values by default. """

        true_checkboxes_list = [
            widgets.date_filter_checkbox,
            widgets.desc_filter_checkbox,
            widgets.startdate_filter_checkbox,
            widgets.enddate_filter_checkbox,
            widgets.category_filter_checkbox,
            widgets.duration_filter_checkbox
        ]
        for widget in true_checkboxes_list:
            print(widget)
            Asserts.assert_widget_value_is_equal(widget, True)

        Asserts.assert_widget_value_is_equal(widgets.category_merge_checkbox, False)
        Asserts.assert_widget_value_is_equal(widgets.start_date_entry, start_date)
        Asserts.assert_widget_value_is_equal(widgets.end_date_entry, end_date)
        assert widgets.tree_result['columns'] == '', 'Results are not empty.'

    @staticmethod
    def assert_analytic_frame_report_state(widgets: AnalyticFrameWidgets):
        """ Assert analytic frame widgets state after pressed report button. """

        enabled_widget_list = [
            widgets.start_date_entry,
            widgets.start_date_btn,
            widgets.end_date_entry,
            widgets.end_date_btn,
            widgets.date_filter_checkbox,
            widgets.desc_filter_checkbox,
            widgets.startdate_filter_checkbox,
            widgets.enddate_filter_checkbox,
            widgets.category_filter_checkbox,
            widgets.duration_filter_checkbox,
            widgets.category_merge_checkbox,
            widgets.clear_btn
        ]
        for widget in enabled_widget_list:
            Asserts.assert_widget_is_enabled(widget)

        Asserts.assert_widget_is_disabled(widgets.report_btn)

    @staticmethod
    def assert_analytic_frame_report_values(
        widgets: AnalyticWidgetsWithValue,
        start_date: str,
        end_date: str):
        """ Assert analytic frame widgets values after pressed report button. """

        true_checkboxes_list = [
            widgets.date_filter_checkbox,
            widgets.desc_filter_checkbox,
            widgets.startdate_filter_checkbox,
            widgets.enddate_filter_checkbox,
            widgets.category_filter_checkbox,
            widgets.duration_filter_checkbox
        ]
        for widget in true_checkboxes_list:
            Asserts.assert_widget_value_is_equal(widget, True)

        Asserts.assert_widget_value_is_equal(widgets.category_merge_checkbox, False)
        Asserts.assert_widget_value_is_equal(widgets.start_date_entry, start_date)
        Asserts.assert_widget_value_is_equal(widgets.end_date_entry, end_date)
        assert widgets.tree_result['columns'] != '', 'Results are empty.'

    @staticmethod
    def assert_analytic_frame_merge_checkboxes_state(widgets: AnalyticFrameWidgets):
        """ Assert analytic frame filter checkboxes states when merge is on. """

        Asserts.assert_widget_is_enabled(widgets.category_merge_checkbox)

        disabled_widget_list = [
            widgets.date_filter_checkbox,
            widgets.desc_filter_checkbox,
            widgets.startdate_filter_checkbox,
            widgets.enddate_filter_checkbox,
            widgets.category_filter_checkbox,
            widgets.duration_filter_checkbox
        ]

        for widget in disabled_widget_list:
            Asserts.assert_widget_is_disabled(widget)

    @staticmethod
    def assert_analytic_frame_merge_default_states(widgets: AnalyticFrameWidgets):
        """ Assert analytic frame widgets state when merge is on. """

        Asserts.assert_analytic_frame_merge_checkboxes_state(widgets)

        enabled_widget_list = [
            widgets.start_date_entry,
            widgets.start_date_btn,
            widgets.end_date_entry,
            widgets.end_date_btn,
            widgets.report_btn
        ]

        for widget in enabled_widget_list:
            Asserts.assert_widget_is_enabled(widget)

        Asserts.assert_widget_is_disabled(widgets.clear_btn)

    @staticmethod
    def assert_analytic_frame_merge_report_states(widgets: AnalyticFrameWidgets):
        """ Assert analytic frame widgets state after pressed report button and merge is on. """

        Asserts.assert_analytic_frame_merge_checkboxes_state(widgets)

        enabled_widget_list = [
            widgets.start_date_entry,
            widgets.start_date_btn,
            widgets.end_date_entry,
            widgets.end_date_btn,
            widgets.clear_btn
        ]
        for widget in enabled_widget_list:
            Asserts.assert_widget_is_enabled(widget)

        Asserts.assert_widget_is_disabled(widgets.report_btn)

    @staticmethod
    def assert_analytic_frame_results_is_empty(table_results: dict):
        """ Assert that result tree is empty. """

        assert len(table_results) == 0, 'Results are not empty.'

# TODO: remove this assert
    @staticmethod
    def assert_analytic_frame_results_is_not_empty(
        table_results: dict,
        widget_values: AnalyticWidgetsWithValue,
        file_list: list[str]):
        """ Assert that result tree is not empty. """

        Asserts.assert_widget_value_is_equal(widget_values.category_merge_checkbox, False)

        expected_result = JsonHelper.get_results_from_json_files(file_list, widget_values)
        true_counter = 0
        assert len(table_results) == len(expected_result), 'Rows count is not equal expected value'

        for expected_value in expected_result.values():
            for real_value in table_results.values():
                if expected_value == real_value:
                    true_counter += 1
                    break

        assert true_counter == len(expected_result), \
            'Results are not matching with expected values.'

    @staticmethod
    def assert_analytic_frame_results_are_equal(
        table_results: dict,
        expected_results: dict,
        widget_values: AnalyticWidgetsWithValue):
        """ Compare two dictionaries results from table and from json_file. """

        Asserts.assert_widget_value_is_equal(widget_values.category_merge_checkbox, False)

        true_counter = 0
        assert len(table_results) == len(expected_results), 'Rows count is not equal expected value'

        for expected_value in expected_results.values():
            for real_value in table_results.values():
                if expected_value == real_value:
                    true_counter += 1
                    break

        assert true_counter == len(expected_results), \
            'Results are not matching with expected values.'

        assert table_results == expected_results, 'Dictionaries are not equal.'

    @staticmethod
    def assert_analytic_frame_result_correct_columns(
        result_tree: ttk.Treeview,
        exclude_columns: list[AnalyticFrameColumnCheckboxesNames] = None):
        """ Assert that all turned on columns are exist. """

        if exclude_columns is None:
            exclude_columns = []

        for checkbox in AnalyticFrameColumnCheckboxesNames:
            column_displayed = checkbox.value in result_tree['columns']
            column_ignored = checkbox in exclude_columns

            assert column_displayed != column_ignored, \
                f"Column displayed must be {column_displayed}, but now is {not column_ignored}"

# Asserts for records in json.
    @staticmethod
    def __assert_record_is_equal(record_value, expected_value):
        assert str(record_value) == str(expected_value), \
            f"Record value \'{record_value}\' is not equal expected value: \'{expected_value}\'"

    @staticmethod
    def __assert_record_is_not_empty(record_value, field_name):
        assert str(record_value) != '', f"Field \'{field_name}\' is empty."

    @staticmethod
    def assert_record_started_task(record, expected_values: ExpectedValues):
        """ Assert for started task record in json. """

        Asserts.__assert_record_is_equal(record['Action'], expected_values.action_value)
        Asserts.__assert_record_is_equal(record['Category'], expected_values.category_value)
        Asserts.__assert_record_is_not_empty(record['StartTimestamp'], 'StartTimestamp')

    @staticmethod
    def assert_record_finished_task(
        record,
        expected_values: ExpectedValues,
        duration_error = False):
        """ Assert for finished task record in json. """

        Asserts.__assert_record_is_equal(record['Action'], expected_values.action_value)
        Asserts.__assert_record_is_equal(record['Category'], expected_values.category_value)

        if expected_values.start_time_value is not None:
            Asserts.__assert_record_is_equal(
                record['StartTimestamp'],
                expected_values.start_time_value)
        else:
            Asserts.__assert_record_is_not_empty(record['StartTimestamp'], 'StartTimestamp')

        if expected_values.finish_time_value is not None:
            Asserts.__assert_record_is_equal(
                record['EndTimestamp'],
                expected_values.finish_time_value)
        else:
            Asserts.__assert_record_is_not_empty(record['EndTimestamp'], 'EndTimestamp')

        if expected_values.duration_value is not None:
            Asserts.__assert_record_is_equal(record['Duration'], expected_values.duration_value)
        else:
            Asserts.__assert_record_is_not_empty(record['Duration'], 'Duration')

        assert re.fullmatch(r'\d{2}:\d{2}:\d{2}', record['EndTimestamp']) is not None, \
            f"Value of EndTimestamp \'{record['EndTimestamp']}\' is not matching with mask"

        assert re.fullmatch(r'\d{2}:\d{2}:\d{2}', record['StartTimestamp']) is not None, \
            f"The value of StartTimestamp \'{record['StartTimestamp']}\' is not matching with mask"

        if not duration_error:
            assert re.fullmatch(r'\d{1}:\d{2}:\d{2}', record['Duration']) is not None, \
                f"The value of Duration \'{record['Duration']}\' is not matching with mask"

# Asserts for user_settings.json.
    @staticmethod
    def assert_settings_category_not_added(category: str):
        """ Assert that new added category doesn't repeat in settings file. """

        categories_list = JsonHelper.get_categories()
        count = categories_list.count(category.lower())

        assert count == 1, f"Category \'{category}\' contains in user_settings.json" \
            f" {count} times but expected 1."

    @staticmethod
    def assert_settings_category_added(category: str):
        """ Assert that new category was added in user_settings.json. """

        categories_list = JsonHelper.get_categories()
        assert category.lower() in categories_list, \
            f"New category \'{category}\' was not found in user_settings.json"
