""" Actions on input frame. """
import tkinter

from TaskTracker.local.models.input_model import InputModel
from TaskTracker.local.helpers.control_states import InputFrameAllControls

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
        controls_state.category_value.set('')

    def change_widgets_states(
        self,
        controls_state: InputFrameAllControls,
        task_finished: bool):
        """ Changing widgets state. """

        if task_finished:
            status = 'enabled'
            controls_state.entry.focus()
            controls_state.entry_value.set('')
        else:
            status = 'disabled'
            self.limit_desc_length_with_block(100, controls_state)
            controls_state.btn_start['state'] = status

        controls_state.entry['state'] = status
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

    def limit_desc_length_with_block(self, limit:int, controls_state: InputFrameAllControls):
        """ Limit entry count letters and block Start and Finish buttons. """
        if len(controls_state.entry_value.get()) > 0:
            controls_state.entry_value.set(controls_state.entry_value.get()[:limit])
            controls_state.btn_start['state'] = 'enabled'
            controls_state.btn_finish['state'] = 'enabled'
        else:
            controls_state.btn_start['state'] = 'disabled'
            controls_state.btn_finish['state'] = 'disabled'

    def limit_category_name(self, limit: int, controls_state: InputFrameAllControls):
        """ Limit new category name. """
        if len(controls_state.category_value.get()) > limit:
            controls_state.category_value.set(controls_state.category_value.get()[:limit])
