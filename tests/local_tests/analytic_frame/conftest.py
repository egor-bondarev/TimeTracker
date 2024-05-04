""" conftest file for analytic frame tests """
import sys
from pathlib import Path
import pytest
from tests.local_tests.test_helpers.json_helper import JsonHelper

sys.path.append(str(Path(__file__).parent.parent))

@pytest.fixture
def create_filled_json(request):
    """ Create filled json file. First param - count of files, second - records count. """
    files_count = request.param[0]
    record_count = request.param[1]

    test_json_files = []
    for _ in range(files_count):
        test_json_files.append(JsonHelper.create_json_file_filled(record_count))
    test_json_files.sort()

    return test_json_files
