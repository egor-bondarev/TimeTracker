""" Tests for result table with merging categories. """
import pytest
import allure

from TaskTracker.tests.local_tests.wrappers.analytic_frame_wrapper import AnalyticFrameWrapper
from TaskTracker.tests.local_tests.asserts.asserts import Asserts
from TaskTracker.tests.local_tests.test_helpers.helpers import Helpers
from TaskTracker.tests.local_tests.test_helpers.structures import AnalyticFrameColumnCheckboxesNames
from TaskTracker.tests.local_tests.test_helpers.json_helper import JsonHelper
from TaskTracker.tests.local_tests.test_helpers.generators import Generators

import TaskTracker.local.helpers.constants as const

@allure.epic("Analytic Frame")
@allure.feature("Results and merging categories")
@allure.title("Merge by categories widget states")
@pytest.mark.parametrize(('create_filled_json'), [(1, 0)], indirect=True)
@pytest.mark.order(1)
def test_merge_widget_states(create_filled_json):
    """ Merge by categories widget states. """

    analytic_frame = AnalyticFrameWrapper()
    analytic_frame.set_checkbox_value('Merge category', True)

    Asserts.assert_analytic_frame_merge_default_states(analytic_frame.get_widgets())
    Asserts.assert_analytic_frame_results_is_empty(analytic_frame.get_results_from_table())

@allure.epic("Analytic Frame")
@allure.feature("Results and merging categories")
@allure.title("Merge by categories and report widget states")
@pytest.mark.parametrize(('create_filled_json'), [(1, 2)], indirect=True)
@pytest.mark.order(2)
def test_merge_and_report_widget_states(create_filled_json):
    """ Merge by categories and report widget states. """

    analytic_frame = AnalyticFrameWrapper()

    Helpers.add_record_to_json_file(
        2,
        f'{create_filled_json[0]}.json',
        Generators.generate_string(Generators.generate_number(1, 20), 'random'))

    analytic_frame.set_checkbox_value('Merge category', True)
    analytic_frame.press_button_report()

    widget_values = analytic_frame.get_widgets_value()

    Asserts.assert_analytic_frame_merge_report_states(analytic_frame.get_widgets())
    Asserts.assert_analytic_frame_merged_results_are_equal(
        analytic_frame.get_results_from_table(),
        JsonHelper.get_merged_results_from_json_files(widget_values, create_filled_json),
        widget_values)

@allure.epic("Analytic Frame")
@allure.feature("Results and merging categories")
@allure.title("Only one category for all records in one json file")
@pytest.mark.parametrize(('create_filled_json'), [(1, 1)], indirect=True)
@pytest.mark.order(3)
def test_one_category_in_all_records_one_file(create_filled_json):
    """ Only one gategory for all records in one json file. """

    analytic_frame = AnalyticFrameWrapper()

    filename = f'{create_filled_json[0]}.json'

    Helpers.add_record_to_json_file(
        2,
        filename,
        JsonHelper.get_last_record(filename)[const.JSON_CATEGORY])

    analytic_frame.set_checkbox_value('Merge category', True)
    analytic_frame.press_button_report()

    widget_values = analytic_frame.get_widgets_value()

    Asserts.assert_analytic_frame_merge_report_states(analytic_frame.get_widgets())
    Asserts.assert_analytic_frame_merged_results_are_equal(
        analytic_frame.get_results_from_table(),
        JsonHelper.get_merged_results_from_json_files(widget_values, create_filled_json),
        widget_values)

@allure.epic("Analytic Frame")
@allure.feature("Results and merging categories")
@allure.title("Only one category for all records in several json file")
@pytest.mark.parametrize(('create_filled_json'), [(1, 1)], indirect=True)
@pytest.mark.order(4)
def test_one_category_in_all_records_several_file(create_filled_json):
    """ Only one gategory for all records in several json file. """

    analytic_frame = AnalyticFrameWrapper()

    filename_1 = f'{create_filled_json[0]}.json'
    filename_2 = f'{JsonHelper.create_json_file_filled(0)}.json'
    category = JsonHelper.get_last_record(filename_1)[const.JSON_CATEGORY]

    Helpers.add_record_to_json_file(
        2,
        filename_1,
        category)

    Helpers.add_record_to_json_file(
        2,
        filename_2,
        category)

    analytic_frame.set_checkbox_value('Merge category', True)
    analytic_frame.press_button_report()

    widget_values = analytic_frame.get_widgets_value()

    Asserts.assert_analytic_frame_merge_report_states(analytic_frame.get_widgets())
    Asserts.assert_analytic_frame_merged_results_are_equal(
        analytic_frame.get_results_from_table(),
        JsonHelper.get_merged_results_from_json_files(widget_values, create_filled_json),
        widget_values)

@allure.epic("Analytic Frame")
@allure.feature("Results and merging categories")
@allure.title("Merge and result for empty json")
@pytest.mark.parametrize(('create_filled_json'), [(1, 0)], indirect=True)
@pytest.mark.order(5)
def test_merge_and_result_empty_json(create_filled_json):
    """ Merge and result for empty json. """

    analytic_frame = AnalyticFrameWrapper()

    analytic_frame.set_checkbox_value('Merge category', True)
    analytic_frame.press_button_report()

    Asserts.assert_analytic_frame_merge_report_states(analytic_frame.get_widgets())
    Asserts.assert_analytic_frame_results_is_empty(analytic_frame.get_results_from_table())

@allure.epic("Analytic Frame")
@allure.feature("Results and merging categories")
@allure.title("Empty categories in json file")
@pytest.mark.parametrize(('create_filled_json'), [(1, 0)], indirect=True)
@pytest.mark.order(6)
def test_empty_categories_empty_results(create_filled_json):
    """ Empty categories in json file. """

    analytic_frame = AnalyticFrameWrapper()

    Helpers.add_record_to_json_file(
        2,
        f'{create_filled_json[0]}.json',
        '')

    analytic_frame.set_checkbox_value('Merge category', True)
    analytic_frame.press_button_report()

    widget_values = analytic_frame.get_widgets_value()

    Asserts.assert_analytic_frame_merge_report_states(analytic_frame.get_widgets())
    Asserts.assert_analytic_frame_merged_results_are_equal(
        analytic_frame.get_results_from_table(),
        JsonHelper.get_merged_results_from_json_files(widget_values, create_filled_json),
        widget_values)

@allure.epic("Analytic Frame")
@allure.feature("Results and merging categories")
@allure.title("Showed only not empty categories")
@pytest.mark.parametrize(('create_filled_json'), [(1, 0)], indirect=True)
@pytest.mark.order(7)
def test_different_categories_empty_cotegories_not_visible(create_filled_json):
    """ Showed only not empty categories. """

    analytic_frame = AnalyticFrameWrapper()

    filename = f'{create_filled_json[0]}.json'

    Helpers.add_record_to_json_file(
        2,
        filename,
        '')

    Helpers.add_record_to_json_file(
        2,
        filename,
        Generators.generate_string(Generators.generate_number(1, 20), 'random'))

    analytic_frame.set_checkbox_value('Merge category', True)
    analytic_frame.press_button_report()

    widget_values = analytic_frame.get_widgets_value()

    Asserts.assert_analytic_frame_merge_report_states(analytic_frame.get_widgets())
    Asserts.assert_analytic_frame_merged_results_are_equal(
        analytic_frame.get_results_from_table(),
        JsonHelper.get_merged_results_from_json_files(widget_values, create_filled_json),
        widget_values)

@allure.epic("Analytic Frame")
@allure.feature("Results and merging categories")
@allure.title("Merge not depend on column checkboxes")
@pytest.mark.parametrize(('create_filled_json'), [(1, 3)], indirect=True)
@pytest.mark.order(8)
def test_merge_not_depend_on_column_checkboxes(create_filled_json):
    """ Merge not depend on column checkboxes. """

    analytic_frame = AnalyticFrameWrapper()

    filename = f'{create_filled_json[0]}.json'

    Helpers.add_record_to_json_file(
        2,
        filename,
        JsonHelper.get_last_record(filename)[const.JSON_CATEGORY])

    analytic_frame.set_checkbox_value(AnalyticFrameColumnCheckboxesNames.CATEGORY.value, False)
    analytic_frame.set_checkbox_value(AnalyticFrameColumnCheckboxesNames.DURATION.value, False)
    analytic_frame.set_checkbox_value('Merge category', True)
    analytic_frame.press_button_report()

    widget_values = analytic_frame.get_widgets_value()

    Asserts.assert_analytic_frame_merge_report_states(analytic_frame.get_widgets())
    Asserts.assert_analytic_frame_merged_results_are_equal(
        analytic_frame.get_results_from_table(),
        JsonHelper.get_merged_results_from_json_files(widget_values, create_filled_json),
        widget_values)

@allure.epic("Analytic Frame")
@allure.feature("Results and merging categories")
@allure.title("Sort merged results")
@pytest.mark.parametrize(('create_filled_json'), [(1, 3)], indirect=True)
@pytest.mark.parametrize("sort_by_desc", [(False), (True)])
@pytest.mark.parametrize(
    "sorted_by_column",
    [(AnalyticFrameColumnCheckboxesNames.DURATION),
    (AnalyticFrameColumnCheckboxesNames.CATEGORY)])
@pytest.mark.order(9)
def test_sort_merged_results(create_filled_json, sort_by_desc, sorted_by_column):
    """ Sort merged results. """

    analytic_frame = AnalyticFrameWrapper()

    filename = f'{create_filled_json[0]}.json'

    Helpers.add_record_to_json_file(
        2,
        filename,
        JsonHelper.get_last_record(filename)[const.JSON_CATEGORY])

    analytic_frame.set_checkbox_value('Merge category', True)
    analytic_frame.press_button_report()
    analytic_frame.sort_by_column(sorted_by_column.value, sort_by_desc)

    widget_values = analytic_frame.get_widgets_value()

    Asserts.assert_analytic_frame_merge_report_states(analytic_frame.get_widgets())
    Asserts.assert_analytic_frame_merged_results_are_equal(
        analytic_frame.get_results_from_table(),
        JsonHelper.sort_results(
            JsonHelper.get_merged_results_from_json_files(widget_values, create_filled_json),
            sorted_by_column.name.lower(),
            sort_by_desc),
        widget_values)

@allure.epic("Analytic Frame")
@allure.feature("Results and merging categories")
@allure.title("Merge no repeated categories")
@pytest.mark.parametrize(('create_filled_json'), [(2, 3)], indirect=True)
@pytest.mark.order(10)
def test_merge_not_repeated_categories(create_filled_json):
    """ Merge no repeated categories. """

    analytic_frame = AnalyticFrameWrapper()

    analytic_frame.set_checkbox_value('Merge category', True)
    analytic_frame.press_button_report()
    widget_values = analytic_frame.get_widgets_value()

    Asserts.assert_analytic_frame_merge_report_states(analytic_frame.get_widgets())
    Asserts.assert_analytic_frame_merged_results_are_equal(
        analytic_frame.get_results_from_table(),
        JsonHelper.get_merged_results_from_json_files(widget_values, create_filled_json),
        widget_values)

@allure.epic("Analytic Frame")
@allure.feature("Results and merging categories")
@allure.title("Clean merged results")
@pytest.mark.parametrize(('create_filled_json'), [(2, 2)], indirect=True)
@pytest.mark.order(11)
def test_clear_merged_results(create_filled_json):
    """ Clean merged results. """

    analytic_frame = AnalyticFrameWrapper()

    analytic_frame.set_checkbox_value('Merge category', True)
    analytic_frame.press_button_report()
    analytic_frame.press_button_clear()

    Asserts.assert_analytic_frame_merge_default_states(analytic_frame.get_widgets())
    Asserts.assert_widget_value_is_equal(
        analytic_frame.get_widgets_value().category_merge_checkbox,
        True)
    Asserts.assert_analytic_frame_results_is_empty(analytic_frame.get_results_from_table())
