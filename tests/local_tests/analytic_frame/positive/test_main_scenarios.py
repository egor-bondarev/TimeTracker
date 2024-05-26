""" Main test for analytic frame. """
import pytest
import allure

from TaskTracker.tests.local_tests.wrappers.analytic_frame_wrapper import AnalyticFrameWrapper
from TaskTracker.tests.local_tests.asserts.asserts import Asserts

@allure.epic("Analytic Frame")
@allure.feature("Main scenarios")
@allure.title("Default widgets states and values")
@pytest.mark.parametrize(('create_filled_json'), [(2, 0)], indirect=True)
@pytest.mark.order(1)
def test_default_state(create_filled_json):
    """ Default widgets states and values"""

    test_json_files = create_filled_json
    analytic_frame = AnalyticFrameWrapper()

    Asserts.assert_analytic_frame_default_state(analytic_frame.get_widgets())
    Asserts.assert_analytic_frame_default_values(
        analytic_frame.get_widgets_value(),
        test_json_files[0],
        test_json_files[1])

@allure.epic("Analytic Frame")
@allure.feature("Main scenarios")
@allure.title("Widgets states and values after report")
@pytest.mark.parametrize(('create_filled_json'), [(2, 1)], indirect=True)
@pytest.mark.order(2)
def test_state_after_reporting(create_filled_json):
    """ Widgets states and values after report """

    test_json_files = create_filled_json
    analytic_frame = AnalyticFrameWrapper()
    analytic_frame.press_button_report()

    Asserts.assert_analytic_frame_report_state(analytic_frame.get_widgets())
    Asserts.assert_analytic_frame_report_values(
        analytic_frame.get_widgets_value(),
        test_json_files[0],
        test_json_files[1])

@allure.epic("Analytic Frame")
@allure.feature("Main scenarios")
@allure.title("Widgets states and values after cleaning report")
@pytest.mark.parametrize(('create_filled_json'), [(2, 0)], indirect=True)
@pytest.mark.order(3)
def test_state_after_cleaning_report(create_filled_json):
    """ Widgets states and values after cleaning report """
    test_json_files = create_filled_json

    analytic_frame = AnalyticFrameWrapper()
    analytic_frame.press_button_report()
    analytic_frame.press_button_clear()

    Asserts.assert_analytic_frame_default_state(analytic_frame.get_widgets())
    Asserts.assert_analytic_frame_default_values(
        analytic_frame.get_widgets_value(),
        test_json_files[0],
        test_json_files[1])

@allure.epic("Analytic Frame")
@allure.feature("Main scenarios")
@allure.title("Checkboxes states saved after cleaning report")
@pytest.mark.order(4)
def test_checkboxes_state_saved_after_cleaning_report():
    """ Checkboxes states saved after cleaning report """

    analytic_frame = AnalyticFrameWrapper()

    analytic_frame.set_checkbox_value('Date', False)
    analytic_frame.set_checkbox_value('Start time', False)
    analytic_frame.set_checkbox_value('Duration', False)
    analytic_frame.press_button_report()
    analytic_frame.press_button_clear()

    Asserts.assert_analytic_frame_default_state(analytic_frame.get_widgets())
    Asserts.assert_widget_value_is_equal(
        analytic_frame.get_widgets_value().date_filter_checkbox, False)
    Asserts.assert_widget_value_is_equal(
        analytic_frame.get_widgets_value().startdate_filter_checkbox, False)
    Asserts.assert_widget_value_is_equal(
        analytic_frame.get_widgets_value().duration_filter_checkbox, False)

@allure.epic("Analytic Frame")
@allure.feature("Main scenarios")
@allure.title("Checkboxes are disabled if merge is enabled")
@pytest.mark.order(5)
def test_checkboxes_state_disabled_when_merge_enabled():
    """ Checkboxes are disabled if merge is enabled """

    analytic_frame = AnalyticFrameWrapper()
    analytic_frame.set_checkbox_value('Merge category', True)

    Asserts.assert_analytic_frame_merge_default_states(analytic_frame.get_widgets())

@allure.epic("Analytic Frame")
@allure.feature("Main scenarios")
@allure.title("Checkboxes values saved after on and off merge")
@pytest.mark.order(6)
def test_checkboxes_values_saveded_after_merge_on_off():
    """ Checkboxes values saved after on and off merge """

    analytic_frame = AnalyticFrameWrapper()

    analytic_frame.set_checkbox_value('Date', False)
    analytic_frame.set_checkbox_value('Start time', False)
    analytic_frame.set_checkbox_value('Duration', False)

    analytic_frame.set_checkbox_value('Merge category', True)
    analytic_frame.set_checkbox_value('Merge category', False)

    Asserts.assert_analytic_frame_default_state(analytic_frame.get_widgets())
    Asserts.assert_widget_value_is_equal(
        analytic_frame.get_widgets_value().date_filter_checkbox, False)
    Asserts.assert_widget_value_is_equal(
        analytic_frame.get_widgets_value().startdate_filter_checkbox, False)
    Asserts.assert_widget_value_is_equal(
        analytic_frame.get_widgets_value().duration_filter_checkbox, True)

@allure.epic("Analytic Frame")
@allure.feature("Main scenarios")
@allure.title("Checkboxes values saved after on and off merge and reporting")
@pytest.mark.order(7)
def test_checkboxes_values_saveded_after_merge_and_report_on_off():
    """ Checkboxes values saved after on and off merge and reporting"""

    analytic_frame = AnalyticFrameWrapper()

    analytic_frame.set_checkbox_value('Date', False)
    analytic_frame.set_checkbox_value('Start time', False)
    analytic_frame.set_checkbox_value('Duration', False)

    analytic_frame.set_checkbox_value('Merge category', True)
    analytic_frame.press_button_report()
    analytic_frame.press_button_clear()
    analytic_frame.set_checkbox_value('Merge category', False)

    Asserts.assert_analytic_frame_default_state(analytic_frame.get_widgets())
    Asserts.assert_widget_value_is_equal(
        analytic_frame.get_widgets_value().date_filter_checkbox, False)
    Asserts.assert_widget_value_is_equal(
        analytic_frame.get_widgets_value().startdate_filter_checkbox, False)
    Asserts.assert_widget_value_is_equal(
        analytic_frame.get_widgets_value().duration_filter_checkbox, True)
