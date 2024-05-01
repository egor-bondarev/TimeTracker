""" Helper class with generators. """
import random
import string

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
