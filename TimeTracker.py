import sys
import os
import json
import time
import PyQt5.QtWidgets as QtWidgets

from PyQt5.QtWidgets import QPushButton, QLineEdit, QMainWindow
from PyQt5 import QtCore
from datetime import date, datetime

class App(QMainWindow):
     
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(300, 300, 140, 140)
        self.setWindowTitle('TimeTracker')


        # Field for action description
        self.label_task_desc = QLineEdit('', self)
        self.label_task_desc.move(20, 20)
        self.label_task_desc.resize(100, 20)

        # Button for starting task
        self.btn_start = QPushButton('Start', self)
        self.btn_start.move(20, 60)
        self.btn_start.resize(100, 30)
        self.btn_start.setShortcut("Return")
        
        # Button for finishing task
        self.btn_finish = QPushButton('Finish', self)
        self.btn_finish.move(20, 90)
        self.btn_finish.resize(100, 30)
        
        filename = '{}.json'.format(date.today())

        self.btn_start.clicked.connect(lambda: self.startTask(filename))
        self.btn_finish.clicked.connect(lambda: self.finishTask(filename))

    def finishTask(self, filename):
        self.changeControlsState(True)
        FileActions.writeToJson(time.strftime(Helpers.TIME_MASK, time.localtime()), 
                                filename, True)

    def startTask(self, filename):
        FileActions.createJson(filename)
        FileActions.writeToJson({'action':self.label_task_desc.text(), 'startTimeStamp':time.strftime(Helpers.TIME_MASK, time.localtime())}, 
                                filename)

        self.changeControlsState(False)

    # Changing control state after user actions
    def changeControlsState(self, isTaskActive):
        self.btn_start.setEnabled(isTaskActive)
        self.label_task_desc.setEnabled(isTaskActive)

        self.btn_finish.setEnabled(not isTaskActive)

        if isTaskActive:
            self.label_task_desc.setFocus(QtCore.Qt.MouseFocusReason)
            self.label_task_desc.clear()

class FileActions:
    # Check existing log file and create it if needed
    def createJson(filename):
        if not os.path.exists(filename):
            with open(filename, "w") as outFile:
                outFile.write(json.dumps({"Activity":[]}))

    # Writing data to existing json log
    def writeToJson(data, filename, append = False):

        def convertTime(file_data, element_number, timestamp_name):
            return datetime.strptime(file_data["Activity"][element_number - 1][timestamp_name], Helpers.TIME_MASK)
        
        with open(filename,'r+') as file:
            file_data = json.load(file)
            if append:
                count = len(file_data['Activity'])
                file_data["Activity"][count - 1]['endTimeStamp'] = data
                start_datetime = convertTime(file_data, count, 'startTimeStamp')
                end_datetime = convertTime(file_data, count, 'endTimeStamp')
                file_data["Activity"][count - 1]['duration'] = '{}'.format(end_datetime - start_datetime)
            else:
                file_data["Activity"].append(data)
            file.seek(0)
            json.dump(file_data, file, indent = 4, ensure_ascii = False)
        
# Helper class for overall actions
class Helpers:
    TIME_MASK = '%H:%M:%S'

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    helpers = Helpers()
    actions = FileActions()
    win = App()

    win.show()
    sys.exit(app.exec_())