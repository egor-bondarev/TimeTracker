""" Helper class with generators. """
import random
import string
import os
import re
from datetime import datetime, timedelta, date
import TaskTracker.local.helpers.constants as const

class Generators():
    """ Classs for generation test data. """

    @staticmethod
    def generate_string(length: int, str_type: str) -> str:
        """ Generate a random string. """
        valid = { 'russian', 'punctuation', 'random'}
        if str_type not in valid:
            raise ValueError(f"Wrong generation type: {type}")
        chars = string.ascii_uppercase + string.digits

        match str_type:
            case 'russian':
                chars = 'абвгдеёжзиклмнопрстуфхцчшщъыьэюя'
            case 'punctuation':
                chars = string.punctuation
            case 'random':
                chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def generate_number(min_value: int, max_value: int) -> int:
        """ Generate a random int. """
        if max_value == 0:
            return 1
        return random.randint(min_value, max_value)

    @staticmethod
    def generate_number_two_ranks(min_value: int, max_value: int) -> str:
        """ Generate number of two ranks and add 0 before it if was generated one rank number. """
        num = random.randint(min_value, max_value)
        if num < 10:
            num = f'0{num}'

        return str(num)

    @staticmethod
    def generate_json_filename() -> str:
        """ Generate random date for json filename. """

        return f'{Generators.generate_date()}.json'

    @staticmethod
    def generate_timestamp_pair() -> tuple[str, str, str]:
        """ Generate random timestamp. """

        hh1 = Generators.generate_number_two_ranks(0, 12)
        hh2 = Generators.generate_number_two_ranks(13, 23)

        mm1 = Generators.generate_number_two_ranks(0, 59)
        mm2 = Generators.generate_number_two_ranks(0, 59)

        ss1 = Generators.generate_number_two_ranks(0, 59)
        ss2 = Generators.generate_number_two_ranks(0, 59)

        start_timestamp = f'{hh1}:{mm1}:{ss1}'
        finish_timestamp = f'{hh2}:{mm2}:{ss2}'

        duration = (datetime.strptime(finish_timestamp, const.TIME_MASK) -
                    datetime.strptime(start_timestamp, const.TIME_MASK))

        return (start_timestamp, finish_timestamp, str(duration))

    @staticmethod
    def generate_date() -> str:
        """ Generate new date in the format YYYY-MM-DD. """

        dates = [files for files in os.listdir('./') if re.search(
                r'\d{4}-\d\d-\d\d.json$',
                files)]

        if len(dates) != 0:
            dates.sort()
            # 5 - is minimum days between dates
            delta_dd = timedelta(days = float(Generators.generate_number_two_ranks(7, 30)))

            result_date = datetime.strptime(str(dates[-1][:-5]), const.DATE_MASK) + delta_dd

            return datetime.strftime(result_date, const.DATE_MASK)

        return f'{date.today().year}-{Generators.generate_number_two_ranks(1, 12)}-{Generators.generate_number_two_ranks(1, 28)}'

    @staticmethod
    def generate_date_in_interval(start_date, finish_date) -> str:
        """ Generate new date in interval. """
        left_border = datetime.strptime(str(start_date), const.DATE_MASK)
        right_border = datetime.strptime(str(finish_date), const.DATE_MASK)

        delta = timedelta(days = (right_border - left_border).days // 2)

        return datetime.strftime(left_border + delta, const.DATE_MASK)
