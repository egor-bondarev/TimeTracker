import tkinter as tk
import os
import json
import time

from datetime import date, datetime
from tkinter import ttk

# Class with constants.
class Helpers:
    TIME_MASK = '%H:%M:%S'

    JSON_ROOT = 'Tasks'
    JSON_TASK = 'Action'
    JSON_TIME_STAMP_START = 'StartTimestamp'
    JSON_TIME_STAMP_END = 'EndTimestamp'
    JSON_TIME_DURATION = 'Duration'

    FILENAME = '{}.json'.format(date.today())

# Class with actions for json file.
class FileActions:

    # Check existing log file and create it if not.
    def create_json():
        if not os.path.exists(Helpers.FILENAME):
            with open(Helpers.FILENAME, "w") as outFile:
                outFile.write(json.dumps({Helpers.JSON_ROOT:[]}))

    def write_json_root():
        with open(Helpers.FILENAME, "w") as file:
            try:
                json.loads(file)
            except (TypeError):
                file.write(json.dumps({Helpers.JSON_ROOT:[]}))

    # Writing data to existing json log.
    def write_to_json(task_desc, task_finished = False):

        FileActions.create_json()

        def convert_time(file_data, element_number, timestamp_name):
            return datetime.strptime(file_data[Helpers.JSON_ROOT][element_number - 1][timestamp_name], Helpers.TIME_MASK)
        
        # Add new record to file.
        def add_new_record(task_finished, task_desc, start_timestamp, end_timestamp = None, duration = None):
            newRecord = file_data[Helpers.JSON_ROOT]
            if task_finished:
                newRecord.append({Helpers.JSON_TASK:task_desc, 
                                  Helpers.JSON_TIME_STAMP_START:start_timestamp, 
                                  Helpers.JSON_TIME_STAMP_END:end_timestamp,
                                  Helpers.JSON_TIME_DURATION:str(duration)})
            else:
                newRecord.append({Helpers.JSON_TASK:task_desc, 
                                  Helpers.JSON_TIME_STAMP_START:start_timestamp})           
        
        with open(Helpers.FILENAME,'r+') as file:
            file_data = json.load(file)
            number_of_tasks = len(file_data[Helpers.JSON_ROOT])
            current_timestamp = time.strftime(Helpers.TIME_MASK, time.localtime())

            # if pressed FINISH
            if task_finished:
                # if this record is first OR last record has field "duration"
                if number_of_tasks == 0:
                    add_new_record(True, task_desc, current_timestamp, current_timestamp, "Ending Timestamp for previous action NOT FOUND")
                elif (Helpers.JSON_TIME_DURATION in file_data[Helpers.JSON_ROOT][number_of_tasks - 1]):
                    last_task = file_data[Helpers.JSON_ROOT][number_of_tasks - 1]
                    start_timestamp = last_task[Helpers.JSON_TIME_STAMP_END]
                    duration = (datetime.strptime(current_timestamp, Helpers.TIME_MASK) - 
                                convert_time(file_data, number_of_tasks, Helpers.JSON_TIME_STAMP_END))
                    add_new_record(True, task_desc, start_timestamp, current_timestamp, duration)
                else:
                    last_task = file_data[Helpers.JSON_ROOT][number_of_tasks - 1]
                    last_task[Helpers.JSON_TIME_STAMP_END] = current_timestamp
                    start_datetime = convert_time(file_data, number_of_tasks, Helpers.JSON_TIME_STAMP_START)
                    end_datetime = convert_time(file_data, number_of_tasks, Helpers.JSON_TIME_STAMP_END)
                    last_task[Helpers.JSON_TIME_DURATION] = '{}'.format(end_datetime - start_datetime)
            # If pressed START
            else:
                add_new_record(False, task_desc, current_timestamp)  

            file.seek(0)
            json.dump(file_data, file, indent = 4, ensure_ascii = False)

# Changing control state after user actions.
def change_widgets_states(task_finished):
    entry['state'] = task_finished
    btn_start['state'] = task_finished

    if task_finished != 'disabled':
        entry.focus()
        entry_task_desc.set('')

# Action for Start button.
def start_task(entry_task_desc):
    FileActions.write_to_json(entry_task_desc.get())
    change_widgets_states('disabled')

# Action for Finish button.
def finish_task(entry_task_desc):
    FileActions.write_to_json(entry_task_desc.get(), True)
    change_widgets_states('enabled')

# creating window
main_window = tk.Tk()
main_window.title('TimeTracker')
main_window.geometry('170x90')

# input frame
input_frame = ttk.Frame(master = main_window)

# entry field
entry_task_desc = tk.StringVar()
entry = ttk.Entry(
    master = main_window, 
    width = 130, 
    font = ("default", 10), 
    textvariable = entry_task_desc)
entry.bind('<Shift-KeyPress-Return>', lambda event: start_task(entry_task_desc))
entry.focus()
entry.pack(padx = 20, pady = 10)

# start button
btn_start = ttk.Button(master = input_frame, text = "Start", command = lambda: start_task(entry_task_desc))
btn_start.pack(side = 'left', padx = 5)

# finish button
btn_finish = ttk.Button(master = input_frame, text = "Finish", command = lambda: finish_task(entry_task_desc))
btn_finish.pack(side = 'left')

input_frame.pack()

#run window
main_window.mainloop()
