import sys
sys.path.append('../local')
sys.path.append('../local/configs')
import tkinter 
from enum import Enum
from tkinter import ttk
from helpers.control_states import InputFrameAllControls
from controllers.input_controller import InputController

    
class ControlStateEnum(Enum):
    ENABLED: str = 'enabled'
    DISABLED: str = 'disabled'
    
class InputFrameMock():
    def __init__(self):
        self.input_controller = InputController()
        
        self.controls_state = InputFrameAllControls(
                btn_start = ttk.Button(),
                btn_finish = ttk.Button(),
                category_combobox = ttk.Combobox(),
                entry = ttk.Entry(),
                category_value = tkinter.StringVar(),
                entry_value = tkinter.StringVar()
                )
    
    def input_task_description(self, value: str):
        self.controls_state.entry_value.set(value)
    
    def get_task_description(self):
        return self.controls_state.entry_value.get()
    
    def set_category_combobox(self, value: str):
        self.controls_state.category_value.set(value = value)
    
    def press_button_start(self):
        self.input_controller.start_task(self.controls_state)
        self.change_controls_state(self.controls_state, True)
    
    def press_button_finish(self):
        self.input_controller.finish_task(self.controls_state)
        self.change_controls_state(self.controls_state, True)
    
    # TODO: try change to wrapper @
    def press_button_finish_without_start(self):
        
        self.input_controller.finish_task(self.controls_state)
        self.change_controls_state(self.controls_state, False)
    
    def change_controls_state(self, control_state: InputFrameAllControls, task_started: bool) -> InputFrameAllControls:
        if task_started:
            self.controls_state.btn_start['state'] = ControlStateEnum.DISABLED
            self.controls_state.btn_finish['state'] = ControlStateEnum.ENABLED
            self.controls_state.entry['state'] = ControlStateEnum.DISABLED
            self.controls_state.category_combobox['state'] = ControlStateEnum.DISABLED
        else:
            self.controls_state.btn_start['state'] = ControlStateEnum.ENABLED
            self.controls_state.btn_finish['state'] = ControlStateEnum.ENABLED
            self.controls_state.entry['state'] = ControlStateEnum.ENABLED
            self.controls_state.category_combobox['state'] = ControlStateEnum.ENABLED
        
        return control_state
        

    


