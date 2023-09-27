import sys
import os
import json
import time
import PyQt5.QtWidgets as QtWidgets

from PyQt5.QtWidgets import QPushButton, QLineEdit, QMainWindow
from PyQt5 import QtCore
from datetime import date, datetime
from PyQt5.QtGui import QKeySequence

class App(QMainWindow):
     
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(800, 400, 170, 90)
        self.setWindowTitle('TimeTracker')

        # Field for action description.
        self.label_task_desc = QLineEdit('', self)
        self.label_task_desc.move(20, 10)
        self.label_task_desc.resize(130, 25)

        # Button for starting task.
        self.btn_start = QPushButton('Start', self)
        self.btn_start.move(10, 50)
        self.btn_start.resize(80, 25)
        self.btn_start.setShortcut(QKeySequence("Shift+Return"))
        
        # Button for finishing task.
        self.btn_finish = QPushButton('Finish', self)
        self.btn_finish.move(80, 50)
        self.btn_finish.resize(80, 25)
        self.btn_finish.setEnabled(True)
        
        filename = '{}.json'.format(date.today())

        self.btn_start.clicked.connect(lambda: self.startTask(filename))
        self.btn_finish.clicked.connect(lambda: self.finishTask(filename))

    # Action for Finish button.
    def finishTask(self, filename):
        FileActions.writeToJson(self.label_task_desc.text(), filename, self.label_task_desc.isEnabled())
        self.changeControlsState(True)

    # Action for Start button.
    def startTask(self, filename):
        FileActions.writeToJson(self.label_task_desc.text(), filename)
        self.changeControlsState(False)

    # Changing control state after user actions.
    def changeControlsState(self, isTaskFinished):
        self.label_task_desc.setEnabled(isTaskFinished)
        self.btn_start.setEnabled(isTaskFinished)

        if isTaskFinished:
            self.label_task_desc.clear()
            self.label_task_desc.setFocus(QtCore.Qt.MouseFocusReason)


class FileActions:

    # Check existing log file and create it if needed.
    def createJson(filename):
        if not os.path.exists(filename):
            with open(filename, "w") as outFile:
                outFile.write(json.dumps({Helpers.JSON_TIME_ARRAY:[]}))

    # Writing data to existing json log.
    def writeToJson(action, filename, appendAll = False):

        FileActions.createJson(filename)

        def convertTime(file_data, element_number, timestamp_name):
            return datetime.strptime(file_data[Helpers.JSON_TIME_ARRAY][element_number - 1][timestamp_name], Helpers.TIME_MASK)
        
        # Add new record to file.
        def newRecord(isTaskEnded, action, startTimestamp, finishTimestamp = None, duration = None):
            newRecord = file_data[Helpers.JSON_TIME_ARRAY]
            if isTaskEnded:
                newRecord.append({'action':action, 
                                  Helpers.TIME_STAMP_START:startTimestamp, 
                                  Helpers.TIME_STAMP_END:finishTimestamp,
                                  'duration':str(duration)})
            else:
                newRecord.append({'action':action, Helpers.TIME_STAMP_START:startTimestamp})           
        
        with open(filename,'r+') as file:
            file_data = json.load(file)
            count = len(file_data[Helpers.JSON_TIME_ARRAY])
            currentTimeStamp = time.strftime(Helpers.TIME_MASK, time.localtime())

            try:
                lastRecord = file_data[Helpers.JSON_TIME_ARRAY][count - 1]
                if 'duration' in lastRecord:
                    if appendAll:
                        previousEndTime = lastRecord[Helpers.TIME_STAMP_END]
                        duration = (datetime.strptime(currentTimeStamp, Helpers.TIME_MASK) - 
                                    convertTime(file_data, count, Helpers.TIME_STAMP_END))
                    
                        newRecord(True, action, previousEndTime, currentTimeStamp, duration)
                    else:
                        newRecord(False, action, currentTimeStamp)
                else:
                    lastRecord[Helpers.TIME_STAMP_END] = currentTimeStamp
                    start_datetime = convertTime(file_data, count, Helpers.TIME_STAMP_START)
                    end_datetime = convertTime(file_data, count, Helpers.TIME_STAMP_END)
                    lastRecord['duration'] = '{}'.format(end_datetime - start_datetime)

            except IndexError:
                print("[warning]: The first record in the file can't complete the task.")
                newRecord(True, action, currentTimeStamp, currentTimeStamp, 0)

            file.seek(0)
            json.dump(file_data, file, indent = 4, ensure_ascii = False)
        
# Helper class for overall actions.
class Helpers:
    TIME_MASK = '%H:%M:%S'
    TIME_STAMP_START = 'startTimeStamp'
    TIME_STAMP_END = 'endTimeStamp'
    JSON_TIME_ARRAY = 'Activity'

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    helpers = Helpers()
    actions = FileActions()
    win = App()

    win.show()
    sys.exit(app.exec_())