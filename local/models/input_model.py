"""Class for working with .json files."""
import json
import time
import os
import logging
from datetime import datetime
import local.helpers.constants as const

from local.helpers.record_info import RecordInfo

logger = logging.getLogger(__name__)

class InputModel():
    """ Class for working with .json files."""

    def create_json(self):
        """Create .json file if it is not exist."""

        if not os.path.exists(const.FILENAME):
            with open(const.FILENAME, "w", encoding="utf-8") as file:
                file.write(json.dumps({const.JSON_ROOT:[]}))
                logger.info('JSON file created.')

    def validate_json(self):
        """ Check .json file."""

        try:
            with open(file = const.FILENAME, mode = 'r+', encoding = "utf-8") as file:
                json.load(file)
        except json.decoder.JSONDecodeError as exception:
            logger.exception(exception)
            file.write(json.dumps({const.JSON_ROOT:[]}))

    def write_to_json(self, task_desc: str, task_category: str, task_finished: bool = False):
        """Add information to .json file."""

        self.create_json()
        self.validate_json()

        with open(file = const.FILENAME, mode = 'r+', encoding="utf-8") as file:
            file_data = json.load(file)
            number_of_tasks = len(file_data[const.JSON_ROOT])
            current_timestamp = time.strftime(const.TIME_MASK, time.localtime())

            # if pressed FINISH
            if task_finished:

                # if this record is first OR last record has field "duration"
                if number_of_tasks == 0:
                    record = RecordInfo(
                        desc = task_desc,
                        start_timestamp = current_timestamp,
                        end_timestamp = current_timestamp,
                        task_duration = "Ending Timestamp for previous action NOT FOUND",
                        category = task_category)
                    self.add_new_record(file_data, True, record)

                # If last record has field duration (Pushed finish without start button)
                elif const.JSON_TIME_DURATION in file_data[const.JSON_ROOT][number_of_tasks - 1]:
                    last_task = file_data[const.JSON_ROOT][number_of_tasks - 1]
                    duration = (datetime.strptime(current_timestamp, const.TIME_MASK) -
                                self.convert_time(
                                    file_data,
                                    number_of_tasks,
                                    const.JSON_TIME_STAMP_END
                                    )
                                )

                    record = RecordInfo(
                        desc = task_desc,
                        category = task_category,
                        start_timestamp = last_task[const.JSON_TIME_STAMP_END],
                        end_timestamp = current_timestamp,
                        task_duration = str(duration))
                    self.add_new_record(file_data, True, record)

                # If start was pushed before
                else:
                    last_task_node = file_data[const.JSON_ROOT][number_of_tasks - 1]
                    duration = (datetime.strptime(current_timestamp, const.TIME_MASK) -
                                self.convert_time(
                                    file_data,
                                    number_of_tasks,
                                    const.JSON_TIME_STAMP_START
                                    )
                                )

                    record = RecordInfo(
                        end_timestamp = current_timestamp,
                        task_duration = str(duration))
                    self.add_to_record(last_task_node, record)
            # If pressed START
            else:
                record = RecordInfo(
                        desc = task_desc,
                        category = task_category,
                        start_timestamp = current_timestamp)
                self.add_new_record(file_data, False, record)

            file.seek(0)
            json.dump(file_data, file, indent = 4, ensure_ascii = False)

    def convert_time(self, file_data, element_number: int, timestamp_name: str) -> datetime:
        """ Convert time from str to datetime. """

        return datetime.strptime(
            file_data[const.JSON_ROOT][element_number - 1][timestamp_name], const.TIME_MASK)

    def add_new_record(self, file_data, task_finished: bool, task_record: RecordInfo):
        """ Add new record to .json file. """

        new_record = file_data[const.JSON_ROOT]
        if task_finished:
            new_record.append({
                const.JSON_TASK: task_record.desc,
                const.JSON_CATEGORY: task_record.category,
                const.JSON_TIME_STAMP_START: task_record.start_timestamp,
                const.JSON_TIME_STAMP_END: task_record.end_timestamp,
                const.JSON_TIME_DURATION: task_record.task_duration})

            logger.info(" <Description>: %s <Category>: %s <Start time>: %s <Finish time>: %s" \
                " <Duration>: %s", task_record.desc, task_record.category,
                task_record.start_timestamp, task_record.end_timestamp, task_record.task_duration)
        else:
            new_record.append({
                const.JSON_TASK: task_record.desc,
                const.JSON_CATEGORY: task_record.category,
                const.JSON_TIME_STAMP_START: task_record.start_timestamp})

            logger.info(" <Description>: %s <Category>: %s <Start time>: %s", 
                        task_record.desc, task_record.category, task_record.start_timestamp)

    def add_to_record(self, node, task_record: RecordInfo):
        """ Add information to existed record. """

        node[const.JSON_TIME_STAMP_END] = task_record.end_timestamp
        node[const.JSON_TIME_DURATION] = task_record.task_duration

        logger.info(" <Finish time>: %s <Duration>: %s", 
                    task_record.end_timestamp, task_record.task_duration)

    def get_categories(self):
        """ Get predefined categories from settings file. """
        with open(file = const.USER_SETTINGS_FILE, mode = 'r+', encoding="utf-8") as file:
            file_data = json.load(file)
            return file_data['Categories']

    def add_new_category(self, category: str):
        """ Add new category to settings file. """

        with open(file = const.USER_SETTINGS_FILE, mode = 'r+', encoding="utf-8") as file:
            file_data = json.load(file)
            record = file_data['Categories']
            record.append(category.lower())

            file.seek(0)
            json.dump(file_data, file, indent = 4, ensure_ascii = False)
