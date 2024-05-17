""" conftest file for pytest """
import sys
import json
import time
import os
import uuid
import re
from pathlib import Path
import pytest
import TaskTracker.local.helpers.constants as const
from TaskTracker.tests.local_tests.test_helpers.generators import Generators
from TaskTracker.tests.local_tests.wrappers.input_frame_wrapper import InputFrameWrapper

sys.path.append(str(Path(__file__).parent.parent))

@pytest.fixture(autouse=True)
def setup_function():
    """ Remove .json file before and after test. """

    file_list = [files for files in os.listdir('./')
                if (re.search(r'\d{4}-\d\d-\d\d.json$', files))
                ]
    for file in file_list:
        os.remove(file)

    user_categories = __get_user_categories()

    yield

    file_list_after_tests = [files for files in os.listdir('./')
                            if (re.search(r'\d{4}-\d\d-\d\d.json$', files))
                            ]
    for file in file_list_after_tests:
        os.remove(file)

    __clean_test_categories(user_categories)

def __get_user_categories() -> list:
    """ Get all user categories from setting file. """

    with open(file = const.USER_SETTINGS_FILE, mode = 'r+', encoding="utf-8") as file:
        file_data = json.load(file)
        return file_data['Categories']

def __clean_test_categories(user_categories: list):
    """ Remove test categories from setting file. """

    with open(file = const.USER_SETTINGS_FILE, mode = 'r', encoding="utf-8") as file:
        file_data = json.load(file)
        test_categories = []
        for new_category in file_data['Categories']:
            if new_category not in user_categories:
                test_categories.append(new_category)

    for category in test_categories:
        file_data['Categories'].remove(category)

    with open(file = const.USER_SETTINGS_FILE, mode = 'w', encoding="utf-8") as file:
        json.dump(file_data, file, indent = 4, ensure_ascii = False)

@pytest.fixture
def add_categories_to_settings(request):
    """ Add test categpries to user_settings.json. """

    count = request.param[0]
    category_list = []

    for _ in range(count):
        category_list.append(Generators.generate_string(request.param[1], 'random').lower())

    for category in category_list:
        with open(file = const.USER_SETTINGS_FILE, mode = 'r+', encoding="utf-8") as file:
            file_data = json.load(file)
            file_data['Categories'].append(category)
            file.seek(0)
            json.dump(file_data, file, indent = 4, ensure_ascii = False)

    return category_list

@pytest.fixture
def add_one_task_to_json():
    """ Add one first record to json."""

    input_frame = InputFrameWrapper()

    input_frame.set_task_description(uuid.uuid4())
    input_frame.set_category(uuid.uuid4())
    input_frame.press_button_start()
    input_frame.press_button_finish()

    time.sleep(1)

@pytest.fixture
def clean_return_user_categories():
    """ Before test all categories will removed and will return after test. """

    user_categories = __get_user_categories()
    with open(file = const.USER_SETTINGS_FILE, mode = 'r', encoding="utf-8") as file:
        file_data = json.load(file)

    for category in user_categories:
        file_data['Categories'].remove(category)

    with open(file = const.USER_SETTINGS_FILE, mode = 'w', encoding="utf-8") as file:
        json.dump(file_data, file, indent = 4, ensure_ascii = False)

    yield

    for category in user_categories:
        file_data['Categories'].append(category)

    with open(file = const.USER_SETTINGS_FILE, mode = 'w', encoding="utf-8") as file:
        json.dump(file_data, file, indent = 4, ensure_ascii = False)
