""" Helpers classes. """

from datetime import date

TIME_MASK = '%H:%M:%S'
DATE_MASK = '%Y-%m-%d'

JSON_ROOT = 'Tasks'
JSON_TASK = 'Action'
JSON_TIME_STAMP_START = 'StartTimestamp'
JSON_TIME_STAMP_END = 'EndTimestamp'
JSON_TIME_DURATION = 'Duration'
JSON_CATEGORY = 'Category'

FILENAME = f'{date.today()}.json'
USER_SETTINGS_FILE = './user_settings.json'

LOG_FILENAME = 'log.txt'
