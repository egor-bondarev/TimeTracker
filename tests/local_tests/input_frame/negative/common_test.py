""" Negative tests for input frame. """

import os
import pytest
import allure
import local.helpers.constants as const

from tests.local_tests.wrappers.input_frame_mock import InputFrameMock
from tests.local_tests.test_helpers.json_helper import JsonHelper
from tests.local_tests.asserts.asserts import Asserts, ExpectedValues
from tests.local_tests.test_helpers.generators import Generators

@allure.epic("Input Frame")
@allure.feature("Common")
@allure.title("Description has length more than max")
@pytest.mark.order(1)
def test_description_more_than_max_length():
    """ Finish task without start where description has max length """

    input_frame = InputFrameMock()
    desc_value = Generators.generate_string(101, 'random')
    json_helper = JsonHelper()

    input_frame.set_task_description(desc_value)
    assert desc_value[:100] == input_frame.controls_state.entry_value.get(), \
        f"Description entry has value {input_frame.controls_state.entry_value.get()}" \
            f" but expected {desc_value[:100]}"

    input_frame.press_button_start()

    expected_values = ExpectedValues(
        action_value = desc_value[:100],
        category_value = ''
    )

    last_record = json_helper.get_last_record()

    Asserts.assert_record_started_task(last_record, expected_values)
    Asserts.assert_controls_state_started_task(input_frame.controls_state)

@allure.epic("Input Frame")
@allure.feature("Common")
@allure.title("Category has length more than max")
@pytest.mark.order(2)
def test_category_more_than_max_length():
    """ Finish task without start where category has max length """

    input_frame = InputFrameMock()

    desc_value = Generators.generate_string(Generators.generate_number(1, 100), 'random')
    category_value = Generators.generate_string(21, 'random')
    json_helper = JsonHelper()

    input_frame.set_task_description(desc_value)
    input_frame.set_category(category_value)
    assert category_value[:20] == input_frame.controls_state.category_value.get(), \
        f"Category entry has value {input_frame.controls_state.category_value.get()}" \
            f" but expected {category_value[:20]}"

    input_frame.press_button_start()

    expected_values = ExpectedValues(
        action_value = desc_value,
        category_value = category_value[:20]
    )

    last_record = json_helper.get_last_record()

    Asserts.assert_record_started_task(last_record, expected_values)
    Asserts.assert_controls_state_started_task(input_frame.controls_state)

@allure.epic("Input Frame")
@allure.feature("Common")
@allure.title("First record finished without starting")
@pytest.mark.order(3)
def test_finish_without_start_first_record():
    """ Finish task without start where json not existed before """

    assert not os.path.exists(const.FILENAME)

    input_frame = InputFrameMock()
    desc_value = Generators.generate_string(Generators.generate_number(1, 100), 'random')
    category_value = Generators.generate_string(Generators.generate_number(1, 20), 'random')
    input_frame.set_task_description(desc_value)
    input_frame.set_category(category_value)
    input_frame.press_button_finish()

    json_helper = JsonHelper()
    last_record = json_helper.get_last_record()
    expected_values = ExpectedValues(
        action_value = desc_value,
        duration_value = 'Ending Timestamp for previous action NOT FOUND',
        category_value = category_value
    )
    Asserts.assert_record_finished_task(last_record, expected_values, duration_error=True)
    Asserts.assert_controls_state_finished_task(input_frame.controls_state)
    Asserts.assert_settings_category_added(category_value)

@allure.epic("Input Frame")
@allure.feature("Common")
@allure.title("Empty categories list")
@pytest.mark.order(4)
def test_no_categories(clean_return_user_categories):
    """ No categories in combobox """    
    input_frame = InputFrameMock()
    assert input_frame.show_available_categories() == []
