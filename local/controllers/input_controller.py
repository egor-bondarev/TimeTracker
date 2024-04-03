""" Actions on input frame. """
import tkinter

from models.input_model import InputModel
from helpers.control_states import InputFrameAllControls

class InputController():
    """ Actions class. """

    inputModel = InputModel()

    def start_task(self, controls_state: InputFrameAllControls):
        """ Start button actions. """

        self.check_exist_category(controls_state.category_value)
        self.inputModel.write_to_json(
            controls_state.entry_value.get(),
            controls_state.category_value.get(),
            False)
        self.change_widgets_states(controls_state, False)

    def finish_task(self, controls_state: InputFrameAllControls):
        """ Finish button actions. """

        self.check_exist_category(controls_state.category_value)
        self.inputModel.write_to_json(
            controls_state.entry_value.get(),
            controls_state.category_value.get(),
            True)

        self.change_widgets_states(controls_state, True)

    def change_widgets_states(self,
                              controls_state: InputFrameAllControls,
                              task_finished: bool):
        """ Changing widgets state. """

        if task_finished:
            status = 'enabled'
            controls_state.entry.focus()
            controls_state.entry_value.set('')
        else:
            status = 'disabled'

        controls_state.entry['state'] = status
        controls_state.btn_start['state'] = status
        controls_state.category_combobox['state'] = status

    def check_exist_category(self, category_combobox: tkinter.StringVar):
        """ Add category to setting file if it is not exist. """

        categories_from_setting = self.inputModel.get_categories()
        for category in categories_from_setting:
            if category_combobox.get().lower() == str(category).lower():
                return

        self.inputModel.add_new_category(category_combobox.get())

    def show_categories(self):
        """ Get categories from settings file. """
        return self.inputModel.get_categories()
