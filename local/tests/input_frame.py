from wrappers.input_frame_mock import InputFrameMock
from test_helpers.json_helper import JsonHelper
import os
import helpers.constants as const

class InputFrameTests():
    def __init__(self):
        self.input_frame = InputFrameMock()
        self.json_helper = JsonHelper()
        
    def before_test(self):
        if os.path.exists(const.FILENAME):
            os.remove(const.FILENAME)
    
    def test(self):
        self.input_frame.input_task_description('first test')
        self.input_frame.press_button_start()
        lt = self.json_helper.get_last_record()
        
    def remove_json_after_test(self):
        pass
    
if __name__ == '__main__':
    input_frame_tests = InputFrameTests()
    input_frame_tests.test()
