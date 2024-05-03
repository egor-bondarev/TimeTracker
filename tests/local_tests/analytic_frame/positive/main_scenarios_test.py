import pytest
import allure

from tests.local_tests.wrappers.input_frame_mock import InputFrameMock
from tests.local_tests.test_helpers.json_helper import JsonHelper
from tests.local_tests.asserts.asserts import Asserts, ExpectedValues
from tests.local_tests.test_helpers.generators import Generators

@allure.epic("Analytic Frame")
@allure.feature("Main scenarios")
@allure.title("test")
@pytest.mark.order(1)
def test():
    """ Test"""

    #Generators.generate_timestamp_pair()
    print(JsonHelper.create_json_file_filled(0))
    assert 1 == 2