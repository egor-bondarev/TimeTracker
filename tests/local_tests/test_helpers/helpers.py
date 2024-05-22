""" Main helpers. """
from TaskTracker.tests.local_tests.wrappers.analytic_frame_wrapper import AnalyticFrameWrapper
from TaskTracker.tests.local_tests.test_helpers.structures import AnalyticFrameColumnCheckboxesNames

class Helpers:
    """ Main helper class. """

    @staticmethod
    def set_all_column_checkboxes_true(
        analytic_frame: AnalyticFrameWrapper,
        exclude_list: list = None):
        """ Set all column chackboxes to TRUE. """

        if exclude_list is None:
            exclude_list = []

        checkboxes_list = (
            AnalyticFrameColumnCheckboxesNames.DATE,
            AnalyticFrameColumnCheckboxesNames.DESCRIPTION,
            AnalyticFrameColumnCheckboxesNames.CATEGORY,
            AnalyticFrameColumnCheckboxesNames.START_TIME,
            AnalyticFrameColumnCheckboxesNames.FINISH_TIME,
            AnalyticFrameColumnCheckboxesNames.DURATION)

        for checkbox in checkboxes_list:
            if checkbox in exclude_list:
                analytic_frame.set_checkbox_value(checkbox.value, False)
            else:
                analytic_frame.set_checkbox_value(checkbox, True)
