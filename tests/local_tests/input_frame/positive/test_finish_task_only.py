""" Positive tests for finishing task without start. """

import pytest
import allure

from TaskTracker.tests.local_tests.wrappers.input_frame_wrapper import InputFrameWrapper
from TaskTracker.tests.local_tests.test_helpers.json_helper import JsonHelper
from TaskTracker.tests.local_tests.asserts.asserts import Asserts, ExpectedValues
from TaskTracker.tests.local_tests.test_helpers.generators import Generators

@allure.epic("Input Frame")
@allure.feature("Finish without start")
@allure.title("Description max length")
@pytest.mark.order(1)
def test_description_max_length(add_one_task_to_json):
    """ Finish task without start where description has max length. """

    input_frame = InputFrameWrapper()
    desc_value = Generators.generate_string(100, 'random')

    input_frame.set_task_description(desc_value)
    input_frame.press_button_finish()

    expected_values = ExpectedValues(
        action_value = desc_value,
        start_time_value = JsonHelper.get_record_by_number(0)['EndTimestamp'],
        category_value = ''
    )

    Asserts.assert_record_finished_task(JsonHelper.get_last_record(), expected_values)
    Asserts.assert_controls_state_finished_task(input_frame.controls_state)

@allure.epic("Input Frame")
@allure.feature("Finish without start")
@allure.title("Description content type")
@pytest.mark.order(2)
@pytest.mark.parametrize("content_type", [('russian'), ('punctuation')])
def test_description_content_type(add_one_task_to_json, content_type):
    """ Description content type. """

    input_frame = InputFrameWrapper()
    desc_value = Generators.generate_string(Generators.generate_number(1, 100), content_type)

    input_frame.set_task_description(desc_value)
    input_frame.press_button_finish()

    expected_values = ExpectedValues(
        action_value = desc_value,
        start_time_value = JsonHelper.get_record_by_number(0)['EndTimestamp'],
        category_value = ''
    )

    Asserts.assert_record_finished_task(JsonHelper.get_last_record(), expected_values)
    Asserts.assert_controls_state_finished_task(input_frame.controls_state)

@allure.epic("Input Frame")
@allure.feature("Finish without start")
@allure.title("Category content type")
@pytest.mark.order(3)
@pytest.mark.parametrize("content_type", [('russian'), ('punctuation')])
def test_category_content_type(add_one_task_to_json, content_type):
    """ Category content type. """

    input_frame = InputFrameWrapper()
    desc_value = Generators.generate_string(Generators.generate_number(1, 100), 'random')
    category_value = Generators.generate_string(Generators.generate_number(1, 20), content_type)

    input_frame.set_task_description(desc_value)
    input_frame.set_category(category_value)
    input_frame.press_button_finish()

    expected_values = ExpectedValues(
        action_value = desc_value,
        start_time_value = JsonHelper.get_record_by_number(0)['EndTimestamp'],
        category_value = category_value
    )

    Asserts.assert_record_finished_task(JsonHelper.get_last_record(), expected_values)
    Asserts.assert_controls_state_finished_task(input_frame.controls_state)
    Asserts.assert_settings_category_added(category_value)

@allure.epic("Input Frame")
@allure.feature("Finish without start")
@allure.title("Record with existed category")
@pytest.mark.order(4)
@pytest.mark.parametrize(
    ('add_categories_to_settings'), [(1, Generators.generate_number(1, 19))], indirect=True)
def test_category_existed_value(add_one_task_to_json, add_categories_to_settings):
    """ Finish task without start task with existed category. """

    input_frame = InputFrameWrapper()
    desc_value = Generators.generate_string(Generators.generate_number(1, 100), 'random')

    category_value = add_categories_to_settings[0]
    Asserts.assert_settings_category_added(category_value.lower())

    input_frame.set_task_description(desc_value)
    input_frame.set_category(category_value)
    input_frame.press_button_finish()

    expected_values = ExpectedValues(
        action_value = desc_value,
        start_time_value = JsonHelper.get_record_by_number(0)['EndTimestamp'],
        category_value = category_value
    )

    Asserts.assert_record_finished_task(JsonHelper.get_last_record(), expected_values)
    Asserts.assert_controls_state_finished_task(input_frame.controls_state)
    Asserts.assert_settings_category_not_added(category_value)

@allure.epic("Input Frame")
@allure.feature("Finish without start")
@allure.title("Category max length")
@pytest.mark.order(5)
def test_category_max_length(add_one_task_to_json):
    """ Finish task without start where category has max length. """

    input_frame = InputFrameWrapper()
    desc_value = Generators.generate_string(Generators.generate_number(1, 100), 'random')
    category_value = Generators.generate_string(20, 'random')

    input_frame.set_task_description(desc_value)
    input_frame.set_category(category_value)
    input_frame.press_button_finish()

    expected_values = ExpectedValues(
        action_value = desc_value,
        start_time_value = JsonHelper.get_record_by_number(0)['EndTimestamp'],
        category_value = category_value
    )

    Asserts.assert_record_finished_task(JsonHelper.get_last_record(), expected_values)
    Asserts.assert_controls_state_finished_task(input_frame.controls_state)
    Asserts.assert_settings_category_added(category_value)

@allure.epic("Input Frame")
@allure.feature("Finish without start")
@allure.title("Using description from previous record")
@pytest.mark.order(6)
def test_description_previous_value(add_one_task_to_json):
    """ Finish task without start where description has value from previous record. """

    input_frame = InputFrameWrapper()
    previous_record = JsonHelper.get_last_record()
    previous_desc = previous_record['Action']
    previous_finish_time = previous_record['EndTimestamp']

    input_frame.set_task_description(previous_desc)
    input_frame.press_button_finish()

    expected_values = ExpectedValues(
        action_value = previous_desc,
        start_time_value = previous_finish_time,
        category_value = ''
    )

    Asserts.assert_record_finished_task(JsonHelper.get_last_record(), expected_values)
    Asserts.assert_controls_state_finished_task(input_frame.controls_state)

@allure.epic("Input Frame")
@allure.feature("Finish without start")
@allure.title("Using description and category from previous record")
@pytest.mark.order(7)
def test_description_and_category_previous_values(add_one_task_to_json):
    """ Finish task without start with description and category have values from previous record. """

    input_frame = InputFrameWrapper()

    previous_record = JsonHelper.get_record_by_number(0)
    previous_desc = previous_record['Action']
    previous_category = previous_record['Category']
    previous_finish_time = previous_record['EndTimestamp']

    input_frame.set_task_description(previous_desc)
    input_frame.set_category(previous_category)
    input_frame.press_button_finish()

    expected_values = ExpectedValues(
        action_value = previous_desc,
        start_time_value = previous_finish_time,
        category_value = previous_category
    )

    Asserts.assert_record_finished_task(JsonHelper.get_last_record(), expected_values)
    Asserts.assert_controls_state_finished_task(input_frame.controls_state)
    Asserts.assert_settings_category_not_added(expected_values.category_value)
