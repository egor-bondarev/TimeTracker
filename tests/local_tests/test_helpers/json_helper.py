""" Helper for working with json files. """
import os
import json
import TaskTracker.local.helpers.constants as const
from TaskTracker.tests.local_tests.test_helpers.generators import Generators

class JsonHelper():
    """ Class with method for working with jsons. """

    @staticmethod
    def get_record_by_number(number: int):
        """ Get record from json result file by number. """
        file_data = JsonHelper.__get_file_data(const.FILENAME)
        return file_data[const.JSON_ROOT][number]

    @staticmethod
    def get_last_record():
        """ Get last record from json result file. """
        file_data = JsonHelper.__get_file_data(const.FILENAME)
        task_count = len(file_data[const.JSON_ROOT])
        return file_data[const.JSON_ROOT][task_count - 1]

    @staticmethod
    def get_categories() -> list:
        """ Get list of categories from user_settings.json. """
        file_data = JsonHelper.__get_file_data(const.USER_SETTINGS_FILE)
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
