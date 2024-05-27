""" Tests for result table with sorting by column. """
import pytest
import allure

from TaskTracker.tests.local_tests.wrappers.analytic_frame_wrapper import AnalyticFrameWrapper
from TaskTracker.tests.local_tests.wrappers.input_frame_wrapper import InputFrameWrapper
from TaskTracker.tests.local_tests.asserts.asserts import Asserts
from TaskTracker.tests.local_tests.test_helpers.helpers import Helpers
from TaskTracker.tests.local_tests.test_helpers.structures import AnalyticFrameColumnCheckboxesNames
from TaskTracker.tests.local_tests.test_helpers.json_helper import JsonHelper
from TaskTracker.tests.local_tests.test_helpers.generators import Generators

import TaskTracker.local.helpers.constants as const

@allure.epic("Analytic Frame")
@allure.feature("Results and sorting")
@allure.title("Ascending and descending sort by the column")
@pytest.mark.parametrize(('create_filled_json'), [(2, 2)], indirect=True)
@pytest.mark.parametrize(
    "sorted_by_column",
    [(AnalyticFrameColumnCheckboxesNames.DATE),
    (AnalyticFrameColumnCheckboxesNames.DESCRIPTION),
    (AnalyticFrameColumnCheckboxesNames.CATEGORY),
    (AnalyticFrameColumnCheckboxesNames.START_TIME),
    (AnalyticFrameColumnCheckboxesNames.FINISH_TIME),
    (AnalyticFrameColumnCheckboxesNames.DURATION)])
@pytest.mark.parametrize("sort_by_desc", [(False), (True)])
@pytest.mark.order(1)
def test_sorting_by_column(create_filled_json, sorted_by_column, sort_by_desc):
    """ Ascending and descending sort by the column. """

    helpers = Helpers()
    analytic_frame = AnalyticFrameWrapper()

    helpers.set_all_column_checkboxes_true(analytic_frame)
    analytic_frame.press_button_report()
    analytic_frame.sort_by_column(sorted_by_column.value, sort_by_desc)

    expected_results = JsonHelper.get_sorted_results_from_json_files(
        sort_by_desc,
        analytic_frame.get_widgets_value(),
        create_filled_json,
        sorted_by_column.name.lower()
    )

    Asserts.assert_analytic_frame_results_are_equal(
        analytic_frame.get_results_from_table(),
        expected_results,
        analytic_frame.get_widgets_value()
    )

@allure.epic("Analytic Frame")
@allure.feature("Results and sorting")
@allure.title("Ascending and descending sort by the only one column")
@pytest.mark.parametrize(('create_filled_json'), [(2, 2)], indirect=True)
@pytest.mark.parametrize(
    "sorted_by_column",
    [(AnalyticFrameColumnCheckboxesNames.DATE),
    (AnalyticFrameColumnCheckboxesNames.CATEGORY)])
@pytest.mark.parametrize("sort_by_desc", [(False), (True)])
@pytest.mark.order(2)
def test_sorting_by_column_which_single_visible(create_filled_json, sorted_by_column, sort_by_desc):
    """ Ascending and descending sort by the only one column. """

    helpers = Helpers()
    analytic_frame = AnalyticFrameWrapper()
    turned_off_columns = []

    for checkbox in AnalyticFrameColumnCheckboxesNames:
        if checkbox != sorted_by_column:
            turned_off_columns.append(checkbox.value)

    helpers.set_all_column_checkboxes_true(analytic_frame)
    analytic_frame.press_button_report()
    analytic_frame.sort_by_column(sorted_by_column.value, sort_by_desc)

    expected_results = JsonHelper.get_sorted_results_from_json_files(
        sort_by_desc,
        analytic_frame.get_widgets_value(),
        create_filled_json,
        sorted_by_column.name.lower()
    )

    Asserts.assert_analytic_frame_results_are_equal(
        analytic_frame.get_results_from_table(),
        expected_results,
        analytic_frame.get_widgets_value()
    )

@allure.epic("Analytic Frame")
@allure.feature("Results and sorting")
@allure.title("Ascending and descending sort by the column with same values")
@pytest.mark.parametrize("sort_by_desc", [(False), (True)])
@pytest.mark.order(3)
def test_sorting_by_column_with_same_values(sort_by_desc):
    """ Ascending and descending sort by the column with same values. """

    input_frame = InputFrameWrapper()
    json_helper = JsonHelper()
    helpers = Helpers()
    column = AnalyticFrameColumnCheckboxesNames.CATEGORY

    category = Generators.generate_string(Generators.generate_number(1, 20), 'random')
    desc_value = Generators.generate_string(Generators.generate_number(1, 100), 'random')

    input_frame.set_task_description(desc_value)
    input_frame.set_category(category)
    input_frame.press_button_start()
    input_frame.press_button_finish()

    last_record = json_helper.get_last_record(const.FILENAME)
    category = last_record[column.value]
    desc_value_2 = Generators.generate_string(Generators.generate_number(1, 100), 'random')
    input_frame.set_task_description(desc_value_2)
    input_frame.set_category(category)
    input_frame.press_button_start()
    input_frame.press_button_finish()

    analytic_frame = AnalyticFrameWrapper()
    helpers.set_all_column_checkboxes_true(analytic_frame)
    analytic_frame.press_button_report()
    analytic_frame.sort_by_column(column.value, sort_by_desc)

    expected_results = JsonHelper.get_sorted_results_from_json_files(
        sort_by_desc,
        analytic_frame.get_widgets_value(),
        [const.FILENAME[:-5]],
        column.name.lower()
    )

    Asserts.assert_analytic_frame_results_are_equal(
        analytic_frame.get_results_from_table(),
        expected_results,
        analytic_frame.get_widgets_value()
    )
