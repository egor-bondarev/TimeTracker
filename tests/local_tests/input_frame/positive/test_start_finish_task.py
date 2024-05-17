""" Positive tests for starting and then finishing task. """

import time
import pytest
import allure

from TaskTracker.tests.local_tests.wrappers.input_frame_wrapper import InputFrameWrapper
from TaskTracker.tests.local_tests.test_helpers.json_helper import JsonHelper
from TaskTracker.tests.local_tests.asserts.asserts import Asserts, ExpectedValues
from TaskTracker.tests.local_tests.test_helpers.generators import Generators

@allure.epic("Input Frame")
@allure.feature("Start then finish")
@allure.title("Record added to existed file")
@pytest.mark.order(1)
def test_record_added_to_existed_json(add_one_task_to_json):
    """ After start and finish task added to json. """

    input_frame = InputFrameWrapper()
    desc_value = Generators.generate_string(Generators.generate_number(1, 100), 'random')
    category_value = Generators.generate_string(Generators.generate_number(1, 20), 'random')

    input_frame.set_task_description(desc_value)
    input_frame.set_category(category_value)
    input_frame.press_button_start()
    time.sleep(1)
    input_frame.press_button_finish()

    json_helper = JsonHelper()
    last_record = json_helper.get_last_record()

    expected_values = ExpectedValues(
        action_value = desc_value,
        category_value = category_value,
        duration_value = '0:00:01'
    )

    Asserts.assert_record_finished_task(last_record, expected_values)
    Asserts.assert_controls_state_finished_task(input_frame.controls_state)

@allure.epic("Input Frame")
@allure.feature("Start then finish")
@allure.title("Description and category like in previous record")
@pytest.mark.order(2)
def test_description_and_category_previous_values(add_one_task_to_json):
    """ Start and finish task where description and category have values from previous record. """

    input_frame = InputFrameWrapper()
    json_helper = JsonHelper()
    previous_record = json_helper.get_last_record()
    previous_desc = previous_record['Action']
    previous_category = previous_record['Category']

    input_frame.set_task_description(previous_desc)
    input_frame.set_category(previous_category)
    input_frame.press_button_start()
    time.sleep(1)
    input_frame.press_button_finish()

    json_helper = JsonHelper()
    last_record = json_helper.get_last_record()

    expected_values = ExpectedValues(
        action_value = previous_desc,
        category_value = previous_category,
        duration_value = '0:00:01'
    )

    Asserts.assert_record_finished_task(last_record, expected_values)
    Asserts.assert_controls_state_finished_task(input_frame.controls_state)

@allure.epic("Input Frame")
@allure.feature("Start then finish")
@allure.title("Two same records")
@pytest.mark.order(1)
def test_two_same_tasks():
    """ Two same record in json result file.  """

    input_frame = InputFrameWrapper()

    desc_value = Generators.generate_string(Generators.generate_number(1, 100), 'random')
    category_value = Generators.generate_string(Generators.generate_number(1, 20), 'random')

    for _ in range(2):
        input_frame.set_task_description(desc_value)
        input_frame.set_category(category_value)
        input_frame.press_button_start()
        input_frame.press_button_finish()

    json_helper = JsonHelper()
    first_record = json_helper.get_record_by_number(0)
    second_record = json_helper.get_record_by_number(1)

    Asserts.assert_settings_category_not_added(category_value)
    assert first_record['Action'] == second_record['Action']
    assert first_record['Category'] == second_record['Category']
    assert first_record['Duration'] == second_record['Duration']
    assert first_record['StartTimestamp'] == second_record['StartTimestamp']
    assert first_record['EndTimestamp'] == second_record['EndTimestamp']
