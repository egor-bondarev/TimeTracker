""" Tests for result table with selected checkboxes. """
from datetime import date, datetime
import pytest
import allure

from TaskTracker.tests.local_tests.wrappers.analytic_frame_wrapper import AnalyticFrameWrapper
from TaskTracker.tests.local_tests.asserts.asserts import Asserts
from TaskTracker.tests.local_tests.test_helpers.helpers import Helpers
from TaskTracker.tests.local_tests.test_helpers.structures import AnalyticFrameColumnCheckboxesNames

import TaskTracker.local.helpers.constants as const

@allure.epic("Analytic Frame")
@allure.feature("Results and selected checkboxes")
@allure.title("Selected all checkboxes and no json files")
@pytest.mark.order(1)
def test_all_checkboxes_choosed_no_json_files():
    """ Selected all checkboxes and no json files. """

    analytic_frame = AnalyticFrameWrapper()

    Helpers.set_all_column_checkboxes_true(analytic_frame)
    analytic_frame.press_button_report()

    Asserts.assert_analytic_frame_results_is_empty(analytic_frame.get_results_from_table())
    Asserts.assert_analytic_frame_result_correct_columns(analytic_frame.get_widgets().tree_result)

@allure.epic("Analytic Frame")
@allure.feature("Results and selected checkboxes")
@allure.title("Selected all checkboxes with files")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(2)
def test_all_checkboxes_choosed_with_json_files(create_filled_json):
    """ Selected all checkboxes with json files. """

    analytic_frame = AnalyticFrameWrapper()

    Helpers.set_all_column_checkboxes_true(analytic_frame)
    analytic_frame.press_button_report()

    Asserts.assert_analytic_frame_results_is_not_empty(
        analytic_frame.get_results_from_table(),
        analytic_frame.get_widgets_value(),
        create_filled_json)
    Asserts.assert_analytic_frame_result_correct_columns(analytic_frame.get_widgets().tree_result)

@allure.epic("Analytic Frame")
@allure.feature("Results and selected checkboxes")
@allure.title("Selected only one checkboxe with files")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.parametrize(
    "column_name",
    [(AnalyticFrameColumnCheckboxesNames.DATE),
    (AnalyticFrameColumnCheckboxesNames.DESCRIPTION),
    (AnalyticFrameColumnCheckboxesNames.CATEGORY),
    (AnalyticFrameColumnCheckboxesNames.START_TIME),
    (AnalyticFrameColumnCheckboxesNames.FINISH_TIME),
    (AnalyticFrameColumnCheckboxesNames.DURATION)])
@pytest.mark.order(3)
def test_one_checkboxes_choosed_with_json_files(create_filled_json, column_name):
    """ Selected only one checkboxe with json files. """

    analytic_frame = AnalyticFrameWrapper()

    excluded_columns = []
    for checkbox in AnalyticFrameColumnCheckboxesNames:
        if checkbox != column_name:
            excluded_columns.append(checkbox.value)

    Helpers.set_all_column_checkboxes_true(analytic_frame, excluded_columns)
    analytic_frame.press_button_report()

    Asserts.assert_analytic_frame_results_is_not_empty(
        analytic_frame.get_results_from_table(),
        analytic_frame.get_widgets_value(),
        create_filled_json)
    Asserts.assert_analytic_frame_result_correct_columns(
        analytic_frame.get_widgets().tree_result,
        excluded_columns)

@allure.epic("Analytic Frame")
@allure.feature("Results and selected checkboxes")
@allure.title("Single record in json isn't finished")
@pytest.mark.order(4)
def test_single_json_record_not_finished(add_one_not_finished_task_to_json):
    """ Single record in json isn't finished. """

    analytic_frame = AnalyticFrameWrapper()

    Helpers.set_all_column_checkboxes_true(analytic_frame)
    analytic_frame.press_button_report()

    Asserts.assert_analytic_frame_results_is_not_empty(
        analytic_frame.get_results_from_table(),
        analytic_frame.get_widgets_value(),
        [str(datetime.strftime(date.today(), const.DATE_MASK))])

    Asserts.assert_analytic_frame_result_correct_columns(
        analytic_frame.get_widgets().tree_result)

@allure.epic("Analytic Frame")
@allure.feature("Results and selected checkboxes")
@allure.title("Single record in json without category")
@pytest.mark.parametrize(('add_one_task_to_json'), [('')], indirect=True)
@pytest.mark.order(5)
def test_single_json_record_without_category(add_one_task_to_json):
    """ Single record in json without category. """

    analytic_frame = AnalyticFrameWrapper()

    Helpers.set_all_column_checkboxes_true(analytic_frame)
    analytic_frame.press_button_report()

    Asserts.assert_analytic_frame_results_is_not_empty(
        analytic_frame.get_results_from_table(),
        analytic_frame.get_widgets_value(),
        [str(datetime.strftime(date.today(), const.DATE_MASK))])

    Asserts.assert_analytic_frame_result_correct_columns(
        analytic_frame.get_widgets().tree_result)
