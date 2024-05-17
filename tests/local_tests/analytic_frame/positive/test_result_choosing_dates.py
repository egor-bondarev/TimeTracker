""" Tests for result table with selected dates. """
from datetime import timedelta, datetime
import pytest
import allure

from TaskTracker.tests.local_tests.wrappers.analytic_frame_wrapper import AnalyticFrameWrapper
from TaskTracker.tests.local_tests.asserts.asserts import Asserts
from TaskTracker.tests.local_tests.test_helpers.generators import Generators
from TaskTracker.tests.local_tests.test_helpers.json_helper import JsonHelper
import TaskTracker.local.helpers.constants as const

@allure.epic("Analytic Frame")
@allure.feature("Results and selected dates")
@allure.title("Selected dates don't include two files")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(1)
def test_choosed_dates_inside_jsonfiles_interval(create_filled_json):
    """ Selected dates don't include two files. """

    test_json_files = create_filled_json
    new_left_filename = Generators.generate_date_in_interval(test_json_files[0], test_json_files[1])
    new_right_filename = Generators.generate_date_in_interval(new_left_filename, test_json_files[1])

    analytic_frame = AnalyticFrameWrapper()
    analytic_frame.press_select_date_in_calendar(new_left_filename, 'start')
    analytic_frame.press_select_date_in_calendar(new_right_filename, 'end')

    widget_values = analytic_frame.get_widgets_value()
    Asserts.assert_widget_value_is_equal(widget_values.start_date_entry, new_left_filename)
    Asserts.assert_widget_value_is_equal(widget_values.end_date_entry, new_right_filename)

    analytic_frame.press_button_report()

    table_results = analytic_frame.get_results_from_table()
    Asserts.assert_analytic_frame_results_is_empty(table_results)
    Asserts.assert_analytic_frame_report_state(analytic_frame.get_widgets())

    analytic_frame.calendar_frame.calendar_window.destroy()
    analytic_frame.main_window.destroy()

@allure.epic("Analytic Frame")
@allure.feature("Results and selected dates")
@allure.title("Selected dates include only middle file")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(2)
def test_choosed_dates_include_middle_jsonfile(create_filled_json):
    """ Selected dates include only middle file. """

    test_json_files = create_filled_json
    middle_filename = Generators.generate_date_in_interval(test_json_files[0], test_json_files[1])
    JsonHelper.create_json_file_filled(2, False, f'{middle_filename}.json')

    new_left_filename = Generators.generate_date_in_interval(test_json_files[0], middle_filename)
    new_right_filename = Generators.generate_date_in_interval(middle_filename, test_json_files[1])

    analytic_frame = AnalyticFrameWrapper()
    analytic_frame.press_select_date_in_calendar(new_left_filename, 'start')
    analytic_frame.press_select_date_in_calendar(new_right_filename, 'end')

    widget_values = analytic_frame.get_widgets_value()
    Asserts.assert_widget_value_is_equal(widget_values.start_date_entry, new_left_filename)
    Asserts.assert_widget_value_is_equal(widget_values.end_date_entry, new_right_filename)

    analytic_frame.press_button_report()
    table_results = analytic_frame.get_results_from_table()

    Asserts.assert_analytic_frame_results_is_not_empty(
        table_results,
        widget_values,
        [middle_filename])

    analytic_frame.calendar_frame.calendar_window.destroy()
    analytic_frame.main_window.destroy()

@allure.epic("Analytic Frame")
@allure.feature("Results and selected dates")
@allure.title("Typed dates don't include two files")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(3)
def test_typed_dates_inside_jsonfiles_interval(create_filled_json):
    """ Typed dates don't include two files. """

    test_json_files = create_filled_json
    new_left_filename = Generators.generate_date_in_interval(test_json_files[0], test_json_files[1])
    new_right_filename = Generators.generate_date_in_interval(new_left_filename, test_json_files[1])

    analytic_frame = AnalyticFrameWrapper()
    analytic_frame.set_start_date(new_left_filename)
    analytic_frame.set_end_date(new_right_filename)

    widget_values = analytic_frame.get_widgets_value()
    Asserts.assert_widget_value_is_equal(widget_values.start_date_entry, new_left_filename)
    Asserts.assert_widget_value_is_equal(widget_values.end_date_entry, new_right_filename)

    analytic_frame.press_button_report()
    table_results = analytic_frame.get_results_from_table()

    Asserts.assert_analytic_frame_results_is_empty(table_results)
    Asserts.assert_analytic_frame_report_state(analytic_frame.get_widgets())

    analytic_frame.calendar_frame.calendar_window.destroy()
    analytic_frame.main_window.destroy()

@allure.epic("Analytic Frame")
@allure.feature("Results and selected dates")
@allure.title("Typed dates include only middle file")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(4)
def test_typed_dates_include_middle_jsonfile(create_filled_json):
    """ Typed dates include only middle file. """

    test_json_files = create_filled_json
    middle_filename = Generators.generate_date_in_interval(test_json_files[0], test_json_files[1])
    JsonHelper.create_json_file_filled(2, False, f'{middle_filename}.json')

    new_left_filename = Generators.generate_date_in_interval(test_json_files[0], middle_filename)
    new_right_filename = Generators.generate_date_in_interval(middle_filename, test_json_files[1])

    analytic_frame = AnalyticFrameWrapper()
    analytic_frame.set_start_date(new_left_filename)
    analytic_frame.set_end_date(new_right_filename)

    widget_values = analytic_frame.get_widgets_value()
    Asserts.assert_widget_value_is_equal(widget_values.start_date_entry, new_left_filename)
    Asserts.assert_widget_value_is_equal(widget_values.end_date_entry, new_right_filename)

    analytic_frame.press_button_report()
    table_results = analytic_frame.get_results_from_table()

    Asserts.assert_analytic_frame_results_is_not_empty(
        table_results,
        widget_values,
        [middle_filename])

    analytic_frame.calendar_frame.calendar_window.destroy()
    analytic_frame.main_window.destroy()

@allure.epic("Analytic Frame")
@allure.feature("Results and selected dates")
@allure.title("Type newer date to start date field")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(5)
def test_typed_startdate_newer_then_before(create_filled_json):
    """ Type newer date to start date field. """

    test_json_files = create_filled_json

    delta = timedelta(days = Generators.generate_number(1, 20))
    old_start_date = datetime.strptime(test_json_files[0], const.DATE_MASK)
    new_start_date = datetime.strftime(old_start_date - delta, const.DATE_MASK)

    analytic_frame = AnalyticFrameWrapper()
    analytic_frame.set_start_date(new_start_date)

    widget_values = analytic_frame.get_widgets_value()
    Asserts.assert_widget_value_is_equal(widget_values.start_date_entry, new_start_date)
    Asserts.assert_widget_value_is_equal(widget_values.end_date_entry, test_json_files[1])

    analytic_frame.press_button_report()
    table_results = analytic_frame.get_results_from_table()

    Asserts.assert_analytic_frame_results_is_not_empty(
        table_results,
        widget_values,
        [test_json_files[0], test_json_files[1]])

    analytic_frame.calendar_frame.calendar_window.destroy()
    analytic_frame.main_window.destroy()

@allure.epic("Analytic Frame")
@allure.feature("Results and selected dates")
@allure.title("Type older date to start date field")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(6)
def test_typed_startdate_older_then_before(create_filled_json):
    """ Type older date to start date field. """

    test_json_files = create_filled_json
    new_start_date = Generators.generate_date_in_interval(test_json_files[0], test_json_files[1])

    analytic_frame = AnalyticFrameWrapper()
    analytic_frame.set_start_date(new_start_date)

    widget_values = analytic_frame.get_widgets_value()
    Asserts.assert_widget_value_is_equal(widget_values.start_date_entry, new_start_date)
    Asserts.assert_widget_value_is_equal(widget_values.end_date_entry, test_json_files[1])

    analytic_frame.press_button_report()
    table_results = analytic_frame.get_results_from_table()

    Asserts.assert_analytic_frame_results_is_not_empty(
        table_results,
        widget_values,
        [test_json_files[1]])

    analytic_frame.calendar_frame.calendar_window.destroy()
    analytic_frame.main_window.destroy()

@allure.epic("Analytic Frame")
@allure.feature("Results and selected dates")
@allure.title("Type older date to end date field")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(7)
def test_typed_enddate_older_then_before(create_filled_json):
    """ Type older date to end date field. """

    test_json_files = create_filled_json
    new_end_date = Generators.generate_date_in_interval(test_json_files[0], test_json_files[1])

    analytic_frame = AnalyticFrameWrapper()
    analytic_frame.set_end_date(new_end_date)
    widget_values = analytic_frame.get_widgets_value()

    Asserts.assert_widget_value_is_equal(widget_values.start_date_entry, test_json_files[0])
    Asserts.assert_widget_value_is_equal(widget_values.end_date_entry, new_end_date)

    analytic_frame.press_button_report()
    table_results = analytic_frame.get_results_from_table()

    Asserts.assert_analytic_frame_results_is_not_empty(
        table_results,
        widget_values,
        [test_json_files[0]])

    analytic_frame.calendar_frame.calendar_window.destroy()
    analytic_frame.main_window.destroy()

@allure.epic("Analytic Frame")
@allure.feature("Results and selected dates")
@allure.title("Type newer date to end date field")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(8)
def test_typed_enddate_newer_then_before(create_filled_json):
    """ Type newer date to end date field. """

    test_json_files = create_filled_json
    delta = timedelta(days = Generators.generate_number(1, 20))
    old_end_date = datetime.strptime(test_json_files[1], const.DATE_MASK)
    new_end_date = datetime.strftime(old_end_date + delta, const.DATE_MASK)

    analytic_frame = AnalyticFrameWrapper()
    analytic_frame.set_end_date(new_end_date)
    widget_values = analytic_frame.get_widgets_value()

    Asserts.assert_widget_value_is_equal(widget_values.start_date_entry, test_json_files[0])
    Asserts.assert_widget_value_is_equal(widget_values.end_date_entry, new_end_date)

    analytic_frame.press_button_report()
    table_results = analytic_frame.get_results_from_table()

    Asserts.assert_analytic_frame_results_is_not_empty(
        table_results,
        widget_values,
        [test_json_files[0], test_json_files[1]])

    analytic_frame.calendar_frame.calendar_window.destroy()
    analytic_frame.main_window.destroy()

@allure.epic("Analytic Frame")
@allure.feature("Results and selected dates")
@allure.title("Start and end dates are equal middle filename")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(9)
def test_choosed_dates_equal_and_same_middle_jsonfile(create_filled_json):
    """ Start and end dates are equal middle filename. """

    test_json_files = create_filled_json
    middle_filename = Generators.generate_date_in_interval(test_json_files[0], test_json_files[1])
    JsonHelper.create_json_file_filled(2, False, f'{middle_filename}.json')

    analytic_frame = AnalyticFrameWrapper()
    analytic_frame.press_select_date_in_calendar(middle_filename, 'start')
    analytic_frame.press_select_date_in_calendar(middle_filename, 'end')

    widget_values = analytic_frame.get_widgets_value()
    Asserts.assert_widget_value_is_equal(widget_values.start_date_entry, middle_filename)
    Asserts.assert_widget_value_is_equal(widget_values.end_date_entry, middle_filename)

    analytic_frame.press_button_report()
    table_results = analytic_frame.get_results_from_table()

    Asserts.assert_analytic_frame_report_state(analytic_frame.get_widgets())
    Asserts.assert_analytic_frame_results_is_not_empty(
        table_results,
        widget_values,
        [middle_filename])

    analytic_frame.calendar_frame.calendar_window.destroy()
    analytic_frame.main_window.destroy()

@allure.epic("Analytic Frame")
@allure.feature("Results and selected dates")
@allure.title("Start date equals end dates with no files")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(10)
def test_choosed_dates_equal_and_no_jsonfile(create_filled_json):
    """ Start date equals end dates with no files. """

    test_json_files = create_filled_json
    middle_date = Generators.generate_date_in_interval(test_json_files[0], test_json_files[1])

    analytic_frame = AnalyticFrameWrapper()

    analytic_frame.press_select_date_in_calendar(middle_date, 'start')
    analytic_frame.press_select_date_in_calendar(middle_date, 'end')

    widget_values = analytic_frame.get_widgets_value()
    Asserts.assert_widget_value_is_equal(widget_values.start_date_entry, middle_date)
    Asserts.assert_widget_value_is_equal(widget_values.end_date_entry, middle_date)

    analytic_frame.press_button_report()
    table_results = analytic_frame.get_results_from_table()

    Asserts.assert_analytic_frame_report_state(analytic_frame.get_widgets())
    Asserts.assert_analytic_frame_results_is_empty(table_results)

    analytic_frame.calendar_frame.calendar_window.destroy()
    analytic_frame.main_window.destroy()
