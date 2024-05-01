""" Class with customs asserts. """
import re
from dataclasses import dataclass
from typing import Optional
from tests.local_tests.wrappers.input_frame_mock import ControlStateEnum
from tests.local_tests.test_helpers.json_helper import JsonHelper
from local.helpers.control_states import InputFrameAllControls

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

# Asserts for controls state
    @staticmethod
    def assert_widget_is_enabled(widget):
        """ Assert that widget state is enabled or normal. """
        assert str(widget['state']) in \
            [ControlStateEnum.NORMAL, ControlStateEnum.ENABLED], \
            f"Control {widget.winfo_name()} has state {widget['state']} but expected " \
                f"{ControlStateEnum.NORMAL} or {ControlStateEnum.ENABLED}"

    @staticmethod
    def assert_widget_is_disabled(widget):
        """ Assert that widget state is disabled. """
        assert str(widget['state']) == ControlStateEnum.DISABLED, \
            f"Control {widget.winfo_name()} has state {widget['state']} but expected " \
                f"{ControlStateEnum.DISABLED}"

    @staticmethod
    def assert_widget_value_is_empty(widget):
        """ Assert that tk.StringVar value is empty. """
        assert widget.get() == '', \
            f"Widget {widget.winfo_name()} has value {widget.get()} but expected empty"

    @staticmethod
    def assert_widget_value_is_equal(widget, expected_value):
        """ Assert that tk.StringVar value has expected value. """   
        assert widget.get() == expected_value, \
            f"Widget {widget.winfo_name()} has value {widget.get()} but expected {expected_value}"        

    @staticmethod
    def assert_controls_state_started_task(controls: InputFrameAllControls):
        """ Assert for started widgets state. """
        disabled_widgets_list = [
            controls.btn_start,
            controls.category_combobox,
            controls.entry]

        Asserts.assert_widget_is_enabled(controls.btn_finish)

        for widget in disabled_widgets_list:
            Asserts.assert_widget_is_disabled(widget)

    @staticmethod
    def assert_controls_state_finished_task(controls: InputFrameAllControls):
        """ Assert for finished widgets state. """
        disabled_widgets_list = [
            controls.btn_start,
            controls.btn_finish]

        enabled_widgets_list = [
            controls.category_combobox,
            controls.entry]

        Asserts.assert_widget_value_is_empty(controls.category_value)
        Asserts.assert_widget_value_is_empty(controls.entry_value)

        for widget in disabled_widgets_list:
            Asserts.assert_widget_is_disabled(widget)

        for widget in enabled_widgets_list:
            Asserts.assert_widget_is_enabled(widget)

    @staticmethod
    def assert_start_frame_default_state(controls: InputFrameAllControls):
        """ Assert for default widget state. """
        Asserts.assert_widget_is_enabled(controls.entry)
        Asserts.assert_widget_value_is_empty(controls.entry_value)

        Asserts.assert_widget_is_enabled(controls.category_combobox)
        Asserts.assert_widget_value_is_empty(controls.category_value)

        Asserts.assert_widget_is_disabled(controls.btn_start)
        Asserts.assert_widget_is_disabled(controls.btn_finish)

    @staticmethod
    def assert_start_frame_state_with_desc(controls: InputFrameAllControls):
        """ Assert widget state when description has symbols inside. """
        widget_list = [
            controls.btn_start,
            controls.btn_finish,
            controls.category_combobox,
            controls.entry]

        for widget in widget_list:
            Asserts.assert_widget_is_enabled(widget)

# Asserts for records in json
    @staticmethod
    def __assert_record_is_equal(record_value, expected_value):
        assert str(record_value) == str(expected_value), \
            f"{record_value} is not equal expected value: {expected_value}"

    @staticmethod
    def __assert_record_is_not_empty(record_value, field_name):
        assert str(record_value) != '', f"{field_name} is empty"

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
            f"{record['EndTimestamp']} is not matching with mask"

        assert re.fullmatch(r'\d{2}:\d{2}:\d{2}', record['StartTimestamp']) is not None, \
            f"{record['StartTimestamp']} is not matching with mask"

        if not duration_error:
            assert re.fullmatch(r'\d{1}:\d{2}:\d{2}', record['Duration']) is not None, \
                f"{record['Duration']} is not matching with mask"

# Asserts for user_settings.json
    @staticmethod
    def assert_settings_category_not_added(category: str):
        """ Assert that new added category doesn't repeat in settings file. """
        categories_list = JsonHelper.get_categories()
        count = categories_list.count(category.lower())

        assert count == 1, f"Category {category} contains in user_settings.json" \
            f" {count} times but expected 1."

    @staticmethod
    def assert_settings_category_added(category: str):
        """ Assert that new category was added in user_settings.json. """
        categories_list = JsonHelper.get_categories()
        assert category.lower() in categories_list, \
            f"New category {category} was not found in user_settings.json"
