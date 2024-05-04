""" Class for connecting to InputFrameController. """
import tkinter as tk
from tkinter import ttk
from tests.local_tests.test_helpers.structures import ControlStateEnum
from local.helpers.control_states import InputFrameAllControls
from local.controllers.input_controller import InputController
from local.views.frames.input_frame import InputFrame

class InputFrameMock():
    """ Class for implementing user actions. """
    def __init__(self):
        self.input_controller = InputController()

        self.main_window = tk.Tk()
        notebook = ttk.Notebook(self.main_window)
        self.input_view = InputFrame(notebook, self.main_window)

        self.controls_state = InputFrameAllControls(
                btn_start = self.input_view.btn_start,
                btn_finish = self.input_view.btn_finish,
                category_combobox = self.input_view.category_combobox,
                entry = self.input_view.entry,
                category_value = self.input_view.category_value,
                entry_value = self.input_view.entry_task_desc
                )

        self.controls_state.btn_start['state'] = ControlStateEnum.DISABLED
        self.controls_state.btn_finish['state'] = ControlStateEnum.DISABLED
        self.controls_state.category_combobox['state'] = ControlStateEnum.NORMAL
        self.controls_state.category_value.set('')
        self.controls_state.entry['state'] = ControlStateEnum.NORMAL
        self.controls_state.entry_value.set('')

    def set_task_description(self, value: str):
        """ Set task description. """
        self.controls_state.entry_value.set(value)
        self.input_controller.limit_desc_length_with_block(100, self.controls_state)

    def get_task_description(self):
        """ Get task description. """
        return self.controls_state.entry_value.get()

    def set_category(self, value: str):
        """ Set category name. """
        self.controls_state.category_value.set(value = value)
        self.input_controller.limit_category_name(20, self.controls_state)

    def press_button_start(self):
        """ Push start button. """
        self.input_controller.start_task(self.controls_state)

    def press_button_finish(self):
        """ Push finish button. """
        self.input_controller.finish_task(self.controls_state)
        self.controls_state.btn_finish['state'] = ControlStateEnum.DISABLED
        self.controls_state.btn_start['state'] = ControlStateEnum.DISABLED

    def show_available_categories(self):
        """ Show available categories from combobox. """
        return self.input_controller.show_categories()

    def press_button_finish_without_start(self):
        """ Push finish button without changing widgets state. """
        self.input_controller.finish_task(self.controls_state)
