""" Tests for calendar. """
import pytest
import allure

from TaskTracker.tests.local_tests.wrappers.analytic_frame_wrapper import AnalyticFrameWrapper
from TaskTracker.tests.local_tests.asserts.asserts import Asserts
from TaskTracker.tests.local_tests.test_helpers.generators import Generators

@allure.epic("Analytic Frame")
@allure.feature("Calendar")
@allure.title("One date for both date fields")
@pytest.mark.parametrize(('create_filled_json'), [(1, 1)], indirect=True)
@pytest.mark.order(1)
def test_one_json_file(create_filled_json):
    """ One date for both date fields. """

    analytic_frame = AnalyticFrameWrapper()

    Asserts.assert_analytic_frame_default_values(
        analytic_frame.get_widgets_value(),
        create_filled_json[0],
        create_filled_json[0])

@allure.epic("Analytic Frame")
@allure.feature("Calendar")
@allure.title("Correct dates in fields for three json files")
@pytest.mark.parametrize(('create_filled_json'), [(3, 1)], indirect=True)
@pytest.mark.order(2)
@pytest.mark.timeout(2)
def test_three_json_files(create_filled_json):
    """ Correct dates in fields for three json files. """

    analytic_frame = AnalyticFrameWrapper()

    Asserts.assert_analytic_frame_default_values(
        analytic_frame.get_widgets_value(),
        create_filled_json[0],
        create_filled_json[2])

@allure.epic("Analytic Frame")
@allure.feature("Calendar")
@allure.title("End date calendar frame with newer date")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(3)
def test_end_date_frame_has_newer_date(create_filled_json):
    """ End date calendar frame with newer date. """

    analytic_frame = AnalyticFrameWrapper()

    Asserts.assert_analytic_frame_default_values(
        analytic_frame.get_widgets_value(),
        create_filled_json[0],
        create_filled_json[1])

    new_end_date = Generators.generate_date()
    analytic_frame.set_end_date(new_end_date)

    Asserts.assert_widget_value_is_equal(
        analytic_frame.get_widgets_value().end_date_entry,
        new_end_date)

@allure.epic("Analytic Frame")
@allure.feature("Calendar")
@allure.title("Start date calendar frame with older date")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(4)
def test_start_date_frame_has_older_date(create_filled_json):
    """ Start date calendar frame with older date. """

    analytic_frame = AnalyticFrameWrapper()

    Asserts.assert_analytic_frame_default_values(
        analytic_frame.get_widgets_value(),
        create_filled_json[0],
        create_filled_json[1])

    new_start_date = Generators.generate_date()
    analytic_frame.set_start_date(new_start_date)

    Asserts.assert_widget_value_is_equal(
        analytic_frame.get_widgets_value().start_date_entry,
        new_start_date)

@allure.epic("Analytic Frame")
@allure.feature("Calendar")
@allure.title("Set new start date in the calendar frame")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(5)
def test_set_start_date_in_calendar(create_filled_json):
    """ Set new start date in the calendar frame. """

    analytic_frame = AnalyticFrameWrapper()

    Asserts.assert_analytic_frame_default_values(
        analytic_frame.get_widgets_value(),
        create_filled_json[0],
        create_filled_json[1])

    new_date = Generators.generate_date()
    analytic_frame.press_select_date_in_calendar(new_date, 'start')

    assert analytic_frame.get_widgets_value().start_date_entry.get() == new_date
    assert analytic_frame.get_date_from_calendar() == new_date

@allure.epic("Analytic Frame")
@allure.feature("Calendar")
@allure.title("Set new end date in the calendar frame")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(6)
def test_set_end_date_in_calendar(create_filled_json):
    """ Set new end date in the calendar frame. """

    analytic_frame = AnalyticFrameWrapper()

    Asserts.assert_analytic_frame_default_values(
        analytic_frame.get_widgets_value(),
        create_filled_json[0],
        create_filled_json[1])

    new_date = Generators.generate_date()
    analytic_frame.press_select_date_in_calendar(new_date, 'end')
    
    assert analytic_frame.get_date_from_calendar() == new_date
    assert analytic_frame.get_widgets_value().end_date_entry.get() == new_date

@allure.epic("Analytic Frame")
@allure.feature("Calendar")
@allure.title("Set both dates in the calendar frame")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(7)
def test_set_both_dates_in_calendar(create_filled_json):
    """ Set both dates in the calendar frame. """

    analytic_frame = AnalyticFrameWrapper()

    Asserts.assert_analytic_frame_default_values(
        analytic_frame.get_widgets_value(),
        create_filled_json[0],
        create_filled_json[1])

    new_start_date = Generators.generate_date()
    new_end_date = Generators.generate_date()
    analytic_frame.press_select_date_in_calendar(new_end_date, 'end')
    analytic_frame.press_select_date_in_calendar(new_start_date, 'start')

    assert analytic_frame.get_widgets_value().start_date_entry.get() == new_start_date
    assert analytic_frame.get_widgets_value().end_date_entry.get() == new_end_date

    Asserts.assert_analytic_frame_default_state(analytic_frame.get_widgets())
