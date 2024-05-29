""" File with view description. """
import tkinter as tk

from tkinter import ttk
from local.controllers.input_controller import InputController
from local.helpers.control_states import InputFrameAllControls

class InputFrame():
    """Class for implementing input frame."""
    def __init__(self, notebook: ttk.Notebook, main_window):
        self.notebook = notebook
        self.main_window = main_window
        self.input_frame = ttk.Frame(notebook)
        # entry field
        self.entry = ttk.Entry(name = 'description entry')

        # start button
        self.btn_start = ttk.Button(name = 'start button')

        # finish button
        self.btn_finish = ttk.Button(name = 'finish button')
        self.category_combobox = ttk.Combobox(name = 'category combobox')

        self.entry_task_desc = tk.StringVar(name = 'description value')
        self.category_value = tk.StringVar(value = '', name = 'category value')

        self.actions = InputController()

    def view(self) -> tk.Frame:
        """View for elements inside frame."""

        def get_controls_state(self):
            return InputFrameAllControls(
                btn_start = self.btn_start,
                btn_finish = self.btn_finish,
                category_combobox = self.category_combobox,
                entry = self.entry,
                category_value = self.category_value,
                entry_value = self.entry_task_desc
                )

        entry_frame = ttk.Frame(self.input_frame)
        # entry field
        self.entry = ttk.Entry(
            master = entry_frame,
            width = 20,
            font = ("default", 10),
            textvariable = self.entry_task_desc)

        self.entry_task_desc.trace_add(
            "write",
            lambda *args: self.actions.limit_desc_length_with_block(
                100,
                get_controls_state(self)))

        self.entry.bind('<Shift-KeyPress-Return>',
                        lambda event: self.actions.start_task(get_controls_state(self)))
        self.entry.focus()
        entry_frame.pack()
        self.entry.pack(padx=3, pady=3)

        category_frame = ttk.Frame(self.input_frame)
        category_frame.pack()
        label_category= ttk.Label(master = category_frame, text = "Category: ")
        label_category.pack(side = 'left', padx=3, pady=3)

        def update_combobox_values():
            self.category_combobox['values'] = self.actions.show_categories()

        self.category_combobox = ttk.Combobox(
            textvariable = self.category_value,
            master = category_frame,
            values = self.actions.show_categories(),
            postcommand = update_combobox_values,
            width = 10
            )
        self.category_value.trace_add(
            "write",
            lambda *args: self.actions.limit_category_name(
                20,
                get_controls_state(self)))
        self.category_combobox.pack(side = 'left')

        #start button
        buttons_frame = ttk.Frame(self.input_frame)
        buttons_frame.pack(padx=3, pady=3)
        self.btn_start = ttk.Button(
            master = buttons_frame,
            text = "Start",
            command = lambda: self.actions.start_task(get_controls_state(self)),
            state = 'disabled')
        self.btn_start.pack(side = 'left')

        #finish button
        self.btn_finish = ttk.Button(
            master = buttons_frame,
            text = "Finish",
            command = lambda: self.actions.finish_task(get_controls_state(self)),
            state = 'disabled')
        self.btn_finish.pack(side = 'left')

        return self.input_frame
