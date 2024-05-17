""" Positive tests for strarting task. """

import os
import pytest
import allure
import TaskTracker.local.helpers.constants as const

from TaskTracker.tests.local_tests.wrappers.input_frame_wrapper import InputFrameWrapper
from TaskTracker.tests.local_tests.test_helpers.json_helper import JsonHelper
from TaskTracker.tests.local_tests.asserts.asserts import Asserts, ExpectedValues
from TaskTracker.tests.local_tests.test_helpers.generators import Generators

@allure.epic("Input Frame")
@allure.feature("Only start task")
@allure.title("Default widget states")
@pytest.mark.order(1)
def test_default_states():
    """ Default state. """

    input_frame = InputFrameWrapper()
    Asserts.assert_start_frame_default_state(input_frame.controls_state)

@allure.epic("Input Frame")
@allure.feature("Only start task")
@allure.title("Active widget states")
@pytest.mark.order(2)
def test_description_one_symbol():
    """ Description has 1 symbol state. """

    desc_value = Generators.generate_string(1, 'random')
    input_frame = InputFrameWrapper()
    input_frame.set_task_description(desc_value)

    Asserts.assert_start_frame_state_with_desc(input_frame.controls_state)
    Asserts.assert_widget_is_enabled(input_frame.controls_state.entry)
    Asserts.assert_widget_value_is_equal(input_frame.controls_state.entry_value, desc_value)

@allure.epic("Input Frame")
@allure.feature("Only start task")
@allure.title("Category combobox content")
@pytest.mark.parametrize(('add_categories_to_settings'), [(4, 10)], indirect=True)
@pytest.mark.order(3)
def test_category_combobox_content(clean_return_user_categories, add_categories_to_settings):
    """ Content of the category list. """

    input_frame = InputFrameWrapper()
    categories_list = input_frame.show_available_categories()
    expected_category_list = add_categories_to_settings

    categories_list.sort()
    expected_category_list.sort()
    for expected_category in expected_category_list:
        if expected_category not in categories_list:
            assert categories_list == expected_category_list, \
                "Current categories list is not equal expected categories list."

@allure.epic("Input Frame")
@allure.feature("Only start task")
@allure.title("Max symbols in the description")
@pytest.mark.order(4)
def test_description_max_symbols():
    """ Start task where description has 100 symbols. """

    input_frame = InputFrameWrapper()
    desc_value = Generators.generate_string(100, 'random')
    input_frame.set_task_description(desc_value)
    input_frame.press_button_start()

    json_helper = JsonHelper()
    last_record = json_helper.get_last_record()
    expected_values = ExpectedValues(
        action_value = desc_value,
        category_value = ''
    )

    Asserts.assert_record_started_task(last_record, expected_values)
    Asserts.assert_controls_state_started_task(input_frame.controls_state)

@allure.epic("Input Frame")
@allure.feature("Only start task")
@allure.title("Description content type")
@pytest.mark.order(5)
@pytest.mark.parametrize("content_type", [('russian'), ('punctuation')])
def test_description_content_type(content_type):
    """ Description content type. """

    input_frame = InputFrameWrapper()
    desc_value = Generators.generate_string(Generators.generate_number(1, 100), content_type)
    input_frame.set_task_description(desc_value)
    input_frame.press_button_start()

    json_helper = JsonHelper()
    last_record = json_helper.get_last_record()
    expected_values = ExpectedValues(
        action_value = desc_value,
        category_value = ''
    )

    Asserts.assert_record_started_task(last_record, expected_values)
    Asserts.assert_controls_state_started_task(input_frame.controls_state)

@allure.epic("Input Frame")
@allure.feature("Only start task")
@allure.title("Category content type")
@pytest.mark.order(6)
@pytest.mark.parametrize("content_type", [('russian'), ('punctuation')])
def test_category_content_type(content_type):
    """ Category content type. """

    input_frame = InputFrameWrapper()
    desc_value = Generators.generate_string(Generators.generate_number(1, 100), 'random')
    category_value = Generators.generate_string(Generators.generate_number(1, 20), content_type)

    input_frame.set_task_description(desc_value)
    input_frame.set_category(category_value)
    input_frame.press_button_start()

    json_helper = JsonHelper()
    last_record = json_helper.get_last_record()
    expected_values = ExpectedValues(
        action_value = desc_value,
        category_value = category_value
    )

    Asserts.assert_record_started_task(last_record, expected_values)
    Asserts.assert_controls_state_started_task(input_frame.controls_state)
    Asserts.assert_settings_category_added(category_value)

@allure.epic("Input Frame")
@allure.feature("Only start task")
@allure.title("Record with existed category")
@pytest.mark.order(7)
@pytest.mark.parametrize(
    ('add_categories_to_settings'), [(1, Generators.generate_number(1, 19))], indirect=True)
def test_category_existed_value(add_categories_to_settings):
    """ Record with existed category. """

    input_frame = InputFrameWrapper()
    desc_value = Generators.generate_string(Generators.generate_number(1, 100), 'random')
    category_value = add_categories_to_settings[0]

    input_frame.set_task_description(desc_value)
    input_frame.set_category(category_value)
    input_frame.press_button_start()

    json_helper = JsonHelper()
    last_record = json_helper.get_last_record()
    expected_values = ExpectedValues(
        action_value = desc_value,
        category_value = category_value
    )

    Asserts.assert_record_started_task(last_record, expected_values)
    Asserts.assert_controls_state_started_task(input_frame.controls_state)
    Asserts.assert_settings_category_not_added(category_value)

@allure.epic("Input Frame")
@allure.feature("Only start task")
@allure.title("Category max length")
@pytest.mark.order(8)
def test_category_max_length():
    """ Start task where category has max length. """

    input_frame = InputFrameWrapper()
    desc_value = Generators.generate_string(Generators.generate_number(1, 100), 'random')
    category_value = Generators.generate_string(20, 'random')

    input_frame.set_task_description(desc_value)
    input_frame.set_category(category_value)
    input_frame.press_button_start()

    json_helper = JsonHelper()
    last_record = json_helper.get_last_record()
    expected_values = ExpectedValues(
        action_value = desc_value,
        category_value = category_value
    )

    Asserts.assert_record_started_task(last_record, expected_values)
    Asserts.assert_controls_state_started_task(input_frame.controls_state)
    Asserts.assert_settings_category_added(category_value)

@allure.epic("Input Frame")
@allure.feature("Only start task")
@allure.title("Using description from previous record")
@pytest.mark.order(9)
def test_description_previous_value(add_one_task_to_json):
    """ Start task where description has value from previous record. """

    input_frame = InputFrameWrapper()
    json_helper = JsonHelper()
    previous_record = json_helper.get_record_by_number(0)
    previous_desc = previous_record['Action']
    input_frame.set_task_description(previous_desc)
    input_frame.press_button_start()

    expected_values = ExpectedValues(
        action_value = previous_desc,
        category_value = ''
    )

    last_record = json_helper.get_last_record()

    Asserts.assert_record_started_task(last_record, expected_values)
    Asserts.assert_controls_state_started_task(input_frame.controls_state)

@allure.epic("Input Frame")
@allure.feature("Only start task")
@allure.title("Using description and category from previous record")
@pytest.mark.order(10)
def test_description_and_category_previous_values(add_one_task_to_json):
    """ Start task where description and category have values from previous record. """

    input_frame = InputFrameWrapper()
    json_helper = JsonHelper()
    previous_record = json_helper.get_record_by_number(0)
    previous_desc = previous_record['Action']
    previous_category = previous_record['Category']

    input_frame.set_task_description(previous_desc)
    input_frame.set_category(previous_category)
    input_frame.press_button_start()

    expected_values = ExpectedValues(
        action_value = previous_desc,
        category_value = previous_category
    )

    last_record = json_helper.get_last_record()

    Asserts.assert_record_started_task(last_record, expected_values)
    Asserts.assert_controls_state_started_task(input_frame.controls_state)
    Asserts.assert_settings_category_not_added(expected_values.category_value)

@allure.epic("Input Frame")
@allure.feature("Only start task")
@allure.title("Json file created")
@pytest.mark.order(11)
def test_create_file_for_first_record():
    """ Json file created after starting the task. """

    assert not os.path.exists(const.FILENAME)

    input_frame = InputFrameWrapper()
    desc_value = Generators.generate_string(Generators.generate_number(1, 100), 'random')
    category_value = Generators.generate_string(Generators.generate_number(1, 20), 'random')

    input_frame.set_task_description(desc_value)
    input_frame.set_category(category_value)
    input_frame.press_button_start()

    assert os.path.exists(const.FILENAME)

    expected_values = ExpectedValues(
        action_value = desc_value,
        category_value = category_value
    )

    json_helper = JsonHelper()
    last_record = json_helper.get_last_record()

    Asserts.assert_record_started_task(last_record, expected_values)
    Asserts.assert_controls_state_started_task(input_frame.controls_state)
    Asserts.assert_settings_category_added(category_value)

@allure.epic("Input Frame")
@allure.feature("Only start task")
@allure.title("Record added to existed json file")
@pytest.mark.order(12)
def test_add_record_to_existed_json(add_one_task_to_json):
    """ Record added to existed json file. """

    assert os.path.exists(const.FILENAME)

    input_frame = InputFrameWrapper()
    json_helper = JsonHelper()
    predefined_record = json_helper.get_last_record()

    expected_previous_values = ExpectedValues(
        action_value = predefined_record['Action'],
        category_value = predefined_record['Category']
    )

    desc_value = Generators.generate_string(Generators.generate_number(1, 100), 'random')
    category_value = Generators.generate_string(Generators.generate_number(1, 20), 'random')

    input_frame.set_task_description(desc_value)
    input_frame.set_category(category_value)
    input_frame.press_button_start()
    previous_record = json_helper.get_record_by_number(0)
    Asserts.assert_record_started_task(previous_record, expected_previous_values)

    expected_values = ExpectedValues(
        action_value = desc_value,
        category_value = category_value
    )

    last_record = json_helper.get_last_record()

    Asserts.assert_record_started_task(last_record, expected_values)
    Asserts.assert_controls_state_started_task(input_frame.controls_state)
    Asserts.assert_settings_category_added(category_value)
