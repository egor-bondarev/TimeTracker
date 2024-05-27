""" Helper for working with json files. """
import os
import json
import re
from datetime import timedelta
import TaskTracker.local.helpers.constants as const
import TaskTracker.tests.local_tests.test_helpers.constants as test_settings
from TaskTracker.tests.local_tests.test_helpers.generators import Generators
from TaskTracker.tests.local_tests.test_helpers.structures import AnalyticWidgetsWithValue, \
    TreeResults

class JsonHelper():
    """ Class with method for working with jsons. """

    @staticmethod
    def get_record_by_number(number: int, file_name: str = const.FILENAME):
        """ Get record from json result file by number. """
        file_data = JsonHelper.__get_file_data(file_name)
        return file_data[const.JSON_ROOT][number]

    @staticmethod
    def get_last_record(file_name: str = const.FILENAME):
        """ Get last record from json result file. """
        file_data = JsonHelper.__get_file_data(file_name)
        task_count = len(file_data[const.JSON_ROOT])
        return file_data[const.JSON_ROOT][task_count - 1]

    @staticmethod
    def get_categories() -> list:
        """ Get list of categories from user_settings.json. """
        file_data = JsonHelper.__get_file_data(test_settings.USER_SETTINGS_FILE)
        return file_data['Categories']

    @staticmethod
    def __get_file_data(filename: str):
        with open(file = filename, mode = 'r', encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def create_json_file_filled(
        records_count = 1,
        last_record_not_finished = False,
        filename = '') -> str:
        """ Create one json filled file. """

        file_existed = True
        while file_existed:
            if filename == '':
                filename = Generators.generate_json_filename()
            if not os.path.exists(filename):
                file_existed = False

        with open(filename, "w", encoding="utf-8") as file:
            file.write(json.dumps({const.JSON_ROOT:[]}))

        for num in range(records_count):
            time_data = Generators.generate_timestamp_pair()

            with open(file = filename, mode = 'r+', encoding="utf-8") as file:
                file_data = json.load(file)
                new_record = file_data[const.JSON_ROOT]

                if num == records_count - 1 and last_record_not_finished:
                    new_record.append({
                        const.JSON_TASK: Generators.generate_string(
                            Generators.generate_number(1, 100), 'random'),
                        const.JSON_CATEGORY: Generators.generate_string(
                            Generators.generate_number(1, 20), 'random'),
                        const.JSON_TIME_STAMP_START: time_data[0]})
                else:
                    new_record.append({
                        const.JSON_TASK: Generators.generate_string(
                            Generators.generate_number(1, 100), 'random'),
                        const.JSON_CATEGORY: Generators.generate_string(
                            Generators.generate_number(1, 20), 'random'),
                        const.JSON_TIME_STAMP_START: time_data[0],
                        const.JSON_TIME_STAMP_END: time_data[1],
                        const.JSON_TIME_DURATION: time_data[2]})

                file.seek(0)
                json.dump(file_data, file, indent = 4, ensure_ascii = False)

        return filename[:-5]

    @staticmethod
    def add_field_by_conditions(checkbox_widget, value):
        """ Return value depends on chackbox value. """
        if checkbox_widget is False:
            return None

        return value

    @staticmethod
    def get_results_from_json_files(
        file_list: list[str],
        widget_values: AnalyticWidgetsWithValue,
        descending: bool = True) -> dict:
        """ Return dictionary with json files content. """

        expected_result = {}
        row_number = 1
        file_list.reverse()

        for file in file_list:
            assert os.path.exists(f'{file}.json'), 'Json file doesn\'t exist.'

            with open(f'{file}.json','r+', encoding="utf-8") as json_file:
                file_data = json.load(json_file)
                content = list(file_data[const.JSON_ROOT])
                if descending:
                    content.reverse()

                for record in content:
                    row = TreeResults()
# TODO: Redo this construction
                    row.date = JsonHelper.add_field_by_conditions(
                        widget_values.date_filter_checkbox.get(),
                        file)
                    row.description = JsonHelper.add_field_by_conditions(
                        widget_values.desc_filter_checkbox.get(),
                        record[const.JSON_TASK])
                    row.category = JsonHelper.add_field_by_conditions(
                        widget_values.category_filter_checkbox.get(),
                        record[const.JSON_CATEGORY])
                    row.start_time = JsonHelper.add_field_by_conditions(
                        widget_values.startdate_filter_checkbox.get(),
                        record[const.JSON_TIME_STAMP_START])

                    if const.JSON_TIME_STAMP_END in record:
                        value = record[const.JSON_TIME_STAMP_END]
                    else:
                        value = ''
                    row.finish_time = JsonHelper.add_field_by_conditions(
                        widget_values.enddate_filter_checkbox.get(),
                        value)

                    if const.JSON_TIME_DURATION in record:
                        value = record[const.JSON_TIME_DURATION]
                    else:
                        value = ''
                    row.duration = JsonHelper.add_field_by_conditions(
                        widget_values.duration_filter_checkbox.get(),
                        value)

                    expected_result[row_number] = row
                    row_number += 1
        return expected_result

    @staticmethod
    def get_sorted_results_from_json_files(
        descending: bool,
        widget_values: AnalyticWidgetsWithValue,
        file_list: list[str],
        sorted_column: str) -> dict:
        """ Return rsorted result by selected column. """

        result_from_json = JsonHelper.get_results_from_json_files(
            file_list,
            widget_values,
            descending)

        return JsonHelper.sort_results(result_from_json, sorted_column, descending)

    @staticmethod
    def sort_results(result_dict: dict, sorted_column: str, descending) -> dict:
        """ Return sorted results. """

        sorted_by_values_dict = {}
        for result in result_dict.items():
            tree = TreeResults.__reduce__(result[1])
            sorted_by_values_dict[result[0]] = tree[2][sorted_column]

        sorted_by_values_dict = dict(sorted(sorted_by_values_dict.items(),
                                            key=lambda item: item[1],
                                            reverse = descending))

        result_from_json_sorted = {}
        new_key = 1
        for key in sorted_by_values_dict.keys():
            result_from_json_sorted[new_key] = result_dict[key]
            new_key += 1

        return result_from_json_sorted

    @staticmethod
    def get_merged_results_from_json_files(
        widget_values: AnalyticWidgetsWithValue,
        file_list: list[str]) -> dict:
        """ Return merged by categories results from json files. """
        result_from_json = JsonHelper.get_results_from_json_files(
            file_list,
            widget_values)

        dict_for_cat_and_duration = {}

        for value in result_from_json.values():
            line = TreeResults.__reduce__(value)[2]
            category = line['category']
            duration = line['duration']
            if category == '':
                continue

            if category in dict_for_cat_and_duration:
                dict_for_cat_and_duration[category] = JsonHelper.__convert_str_to_timedelta(
                    dict_for_cat_and_duration[category])
                dict_for_cat_and_duration[category] += JsonHelper.__convert_str_to_timedelta(
                    duration)
                dict_for_cat_and_duration[category] = JsonHelper.__convert_from_timedelta(
                    dict_for_cat_and_duration[category])
            else:
                dict_for_cat_and_duration[category] = JsonHelper.__convert_str_to_timedelta(
                    duration)

            dict_for_cat_and_duration[category] = \
                str(dict_for_cat_and_duration[category])

        result_from_json_merged = {}
        new_key = 1
        for key, value in dict_for_cat_and_duration.items():
            row = TreeResults()
            row.date = None
            row.description = None
            row.category = key
            row.start_time = None
            row.finish_time = None
            row.duration = value
            result_from_json_merged[new_key] = row
            new_key += 1

        return result_from_json_merged

    @staticmethod
    def __convert_str_to_timedelta(time: str) -> timedelta:
        time = re.findall(r'\d\d*:\d\d:\d\d', time)[0]

        try:
            h, m, s = time.split(':')
            if h == '00':
                h = '0'
        except ValueError:
            h, m, s = 0, 0, 0

        return timedelta(hours = int(h), minutes = int(m), seconds = int(s))

    @staticmethod
    def __convert_from_timedelta(duration: timedelta) -> str:
        hours_delta = duration.days * 24
        time = re.findall(r'\d\d*:\d\d:\d\d', str(duration))[0]
        h, m, s = time.split(':')
        new_h = int(h) + hours_delta
        result = f'{new_h}:{m}:{s}'
        return result

    @staticmethod
    def add_record_to_json(filename: str, desc: str, category: str):
        """ Add record to existed json file. """

        time_data = Generators.generate_timestamp_pair()

        with open(file = filename, mode = 'r+', encoding="utf-8") as file:
            file_data = json.load(file)
            new_record = file_data[const.JSON_ROOT]
            new_record.append({
                const.JSON_TASK: desc,
                const.JSON_CATEGORY: category,
                const.JSON_TIME_STAMP_START: time_data[0],
                const.JSON_TIME_STAMP_END: time_data[1],
                const.JSON_TIME_DURATION: time_data[2]})

            file.seek(0)
            json.dump(file_data, file, indent = 4, ensure_ascii = False)
