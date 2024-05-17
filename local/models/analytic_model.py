"""Analytic model"""
import os
import re
import json
from datetime import datetime, timedelta
import dataclasses
import logging

import local.helpers.constants as const
from local.helpers.record_info import RecordForView
from local.helpers.helpers import DateInterval, CheckboxRecordFile

logger = logging.getLogger(__name__)

class AnalyticModel():
    """ Parsing json. """

    def get_files(self, date_interval: DateInterval) -> list:
        """ Get files in setted period. """

        file_lst = [files for files in os.listdir('./')
                    if (re.search(r'\d{4}-\d\d-\d\d.json$', files) and
                        datetime.strptime(files[:-5], const.DATE_MASK) >= date_interval.date_start
                        and
                        datetime.strptime(files[:-5], const.DATE_MASK) <= date_interval.date_finish
                        )
                    ]

        return file_lst

    def add_info_from_one_record(self, record, checkbox_states: dict) -> RecordForView:
        """ Add information from one file record to each column. """

        new_record = RecordForView()
        struct: list[CheckboxRecordFile] = [
            CheckboxRecordFile('Description', 'desc', const.JSON_TASK),
            CheckboxRecordFile('Category', 'category', const.JSON_CATEGORY),
            CheckboxRecordFile('Start time', 'start_timestamp', const.JSON_TIME_STAMP_START),
            CheckboxRecordFile('Finish time', 'end_timestamp', const.JSON_TIME_STAMP_END),
            CheckboxRecordFile('Duration', 'task_duration', const.JSON_TIME_DURATION)]

        for item in struct:
            if checkbox_states[item.checkbox_name]:
                try:
                    setattr(new_record, item.record_field, record[item.json_field])
                except KeyError as exception:
                    logger.exception(exception)
                    setattr(new_record, item.record_field, '')

        return new_record

    def get_info_from_files(self,
                            date_interval: DateInterval,
                            checkbox_states: dict) -> list[RecordForView]:
        """ Get all statistic. """

        full_stat: list[RecordForView] = []
        files = self.get_files(date_interval)

        for file in files:
            with open(file,'r+', encoding="utf-8") as json_file:
                try:
                    file_data = json.load(json_file)
                except json.decoder.JSONDecodeError as exception:
                    logger.exception(exception)
                    continue

                for record in file_data[const.JSON_ROOT]:
                    try:
                        new_record: RecordForView = self.add_info_from_one_record(
                            record,
                            checkbox_states)

                        if checkbox_states['Date']:
                            new_record.date = file[:-5]

                    except KeyError as exception:
                        logger.exception(exception)
                        continue
                    except TypeError as exception:
                        logger.exception(exception)
                        continue
                    else:
                        full_stat.append(new_record)
        return full_stat

    def get_date_period(self) -> tuple:
        """ Create tuple with first and last allowed dates. """

        date_period = (str(datetime.date(datetime.now())), str(datetime.date(datetime.now())))

        try:
            dates = [files for files in os.listdir('./') if re.search(
                r'\d{4}-\d\d-\d\d.json$',
                files)]
            dates.sort()

            date_period = (dates[0].removesuffix(".json"), dates[-1].removesuffix(".json"))
        except IndexError as exception:
            logger.exception(exception)
            logger.fatal('There are no json files.')

        return date_period

    def get_statistic(
        self,
        date_interval: DateInterval,
        checkbox_states: dict,
        merge: bool) -> list[list[str]]:
        """ Preparing statistic for table view. """

        get_data = self.get_info_from_files(date_interval, checkbox_states)
        result_list = []

        # Create list of neccessary fields.
        fields = []
        for field in dataclasses.fields(RecordForView):
            if merge:
                if field.name in ('category', 'task_duration'):
                    fields.append(field.name)
            else:
                fields.append(field.name)

        def merge_record(lst: list[list[str]], category: str, duration: str):
            if category == '':
                return
            for record in lst:
                if record[0].lower() == category.lower():
                    record[1] = self.parse_to_timedelta(record[1])
                    record[1] += self.parse_to_timedelta(duration)
                    record[1] = self.parse_from_timedelta(record[1])

                    if record[1][:2] == '00':
                        record[1] = record[1][1:]
                    return

            lst.append([category, duration])

        for record in get_data:
            sub_list = []
            try:
                if merge:
                    merge_record(result_list, record.category, record.task_duration)
                else:
                    for field in fields:
                        if getattr(record, field) is not None:
                            sub_list.append(getattr(record, field))

                    result_list.append(sub_list)

            except AttributeError as exception:
                logger.exception(exception)
                continue

        return result_list

    def parse_to_timedelta(self, time: str) -> timedelta:
        """ Parse time from str to datetime.timedelta. """

        try:
            h, m, s = time.split(':')
            if h == '00':
                h = '0'
        except ValueError:
            h, m, s = 0, 0, 0

        return timedelta(hours = int(h), minutes = int(m), seconds = int(s))

    def parse_from_timedelta(self, duration: timedelta) -> str:
        """ Parse time from timedelta to str. """

        return str(datetime.strptime(str(duration), const.TIME_MASK).time())
