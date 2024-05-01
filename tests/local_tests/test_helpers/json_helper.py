""" Helper for working with json files. """
import json
import local.helpers.constants as const

class JsonHelper():
    """ Class with method for working with jsons. """

    @staticmethod
    def get_record_by_number(number: int):
        """ Get record from json result file by number. """
        file_data = JsonHelper.__get_file_date(const.FILENAME)
        return file_data[const.JSON_ROOT][number]

    @staticmethod
    def get_last_record():
        """ Get last record from json result file. """
        file_data = JsonHelper.__get_file_date(const.FILENAME)
        task_count = len(file_data[const.JSON_ROOT])
        return file_data[const.JSON_ROOT][task_count - 1]

    @staticmethod
    def get_categories() -> list:
        """ Get list of categories from user_settings.json. """
        file_data = JsonHelper.__get_file_date(const.USER_SETTINGS_FILE)
        return file_data['Categories']

    @staticmethod
    def __get_file_date(filename: str):
        with open(file = filename, mode = 'r', encoding="utf-8") as file:
            return json.load(file)
