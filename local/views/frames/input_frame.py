""" File with view description. """
import tkinter as tk

from tkinter import ttk
from controllers.input_controller import InputController
from helpers.control_states import InputFrameAllControls

class InputFrame():
    """Class for implementing input frame."""
    def __init__(self, notebook: ttk.Notebook):
        self.notebook = notebook
        self.input_frame = ttk.Frame(notebook)
        # entry field
        self.entry = ttk.Entry()

        # start button
        self.btn_start = ttk.Button()

        # finish button
        self.btn_finish = ttk.Button()
        self.category_combobox = ttk.Combobox()

        self.actions = InputController()

    def view(self) -> tk.Frame:
        """View for elements inside frame."""

        entry_task_desc = tk.StringVar()
        category_value = tk.StringVar(value='')

        def get_controls_state(self):
            return InputFrameAllControls(
                btn_start = self.btn_start,
                btn_finish = self.btn_finish,
                category_combobox = self.category_combobox,
                entry = self.entry,
                category_value = category_value,
                entry_value = entry_task_desc
                )

        entry_frame = ttk.Frame(self.input_frame)
        # entry field
        self.entry = ttk.Entry(
            master = entry_frame,
            width = 100,
            font = ("default", 10),
            textvariable = entry_task_desc)

        self.entry.bind('<Shift-KeyPress-Return>',
                        lambda event: self.actions.start_task(get_controls_state(self)))
        self.entry.focus()
        entry_frame.pack()
        self.entry.pack()

        category_frame = ttk.Frame(self.input_frame)
        category_frame.pack()
        label_category= ttk.Label(master = category_frame, text = "Category: ")
        label_category.pack(side = 'left')

        def update_combobox_values():
            self.category_combobox['values'] = self.actions.show_categories()

        self.category_combobox = ttk.Combobox(
            textvariable = category_value,
            master = category_frame,
            values = self.actions.show_categories(),
            postcommand = update_combobox_values
            )
        self.category_combobox.pack(side = 'left')

        #start button
        buttons_frame = ttk.Frame(self.input_frame)
        buttons_frame.pack()
        self.btn_start = ttk.Button(
            master = buttons_frame,
            text = "Start",
            command = lambda: self.actions.start_task(get_controls_state(self)))
        self.btn_start.pack(side = 'left')

        #finish button
        self.btn_finish = ttk.Button(
            master = buttons_frame,
            text = "Finish",
            command = lambda: self.actions.finish_task(get_controls_state(self)))
        self.btn_finish.pack(side = 'left')

        return self.input_frame
