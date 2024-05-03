""" Helper class with generators. """
import random
import string
import time
from datetime import datetime
from datetime import date
import local.helpers.constants as const

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
        return random.randint(min_value, max_value)
    
    @staticmethod
    def generate_number_two_ranks(min_value: int, max_value: int) -> str:
        num = random.randint(min_value, max_value)
        if num < 10:
            num = f'0{num}'
        
        return str(num)

    @staticmethod
    def generate_json_filename() -> str:
        """ Generate random date for json filename. """
        mm = Generators.generate_number_two_ranks(1, 12)
        dd = Generators.generate_number_two_ranks(1, 28)

        yy = date.today().year

        return f'{yy}-{mm}-{dd}.json'
    
    @staticmethod
    def generate_timestamp_pair() -> tuple[str, str, str]:
        """ Generate random timestamp."""
        print(time.localtime())
        print(time.localtime().tm_hour)
        print(time.localtime().tm_min)
        print(time.localtime().tm_sec)
        
        hh1 = Generators.generate_number_two_ranks(0, 23)
        hh2_greater_hh1 = True
        while hh2_greater_hh1:
            hh2 = Generators.generate_number_two_ranks(0, 23)
            if hh2 > hh1:
                hh2_greater_hh1 = False
        mm1 = Generators.generate_number_two_ranks(0, 59)
        mm2 = Generators.generate_number_two_ranks(0, 59)
        ss1 = Generators.generate_number_two_ranks(0, 59)
        ss2 = Generators.generate_number_two_ranks(0, 59)
        
        start_timestamp = f'{hh1}:{mm1}:{ss1}'
        finish_timestamp = f'{hh2}:{mm2}:{ss2}'
                
        print(f'time1 {start_timestamp} ___hh2: {finish_timestamp} ')
        # tt1 = datetime.strptime(start_timestamp, const.TIME_MASK)
        # tt2 = datetime.strptime(finish_timestamp, const.TIME_MASK)
        # print(tt2.time())
        
        duration = (datetime.strptime(finish_timestamp, const.TIME_MASK) - datetime.strptime(start_timestamp, const.TIME_MASK))
        
        print(duration)
        return (start_timestamp, finish_timestamp, str(duration))
        