import json
import helpers.constants as const

class JsonHelper():
    def __init__(self):
        pass
            
    def get_record_by_number(self, number: int):
        file_data = self._get_file_date(const.FILENAME)
        return file_data[const.JSON_ROOT][number]
    
    def get_record_by_description(self, desc: str):
        pass
        
    def get_last_record(self):
        file_data = self._get_file_date(const.FILENAME)
        task_count = len(file_data[const.JSON_ROOT])
        return file_data[const.JSON_ROOT][task_count - 1]
    
    def get_categories(self) -> list:
        file_data = self._get_file_date(const.USER_SETTINGS_FILE)
        return file_data['Categories']
        
    def _get_file_date(self, filename: str):
        with open(file = filename, mode = 'r', encoding="utf-8") as file:
            return json.load(file)