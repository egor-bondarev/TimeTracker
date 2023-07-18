import sys
import os
import json
import time
import PyQt5.QtWidgets as QtWidgets

from PyQt5.QtWidgets import QPushButton, QLineEdit, QMainWindow
from PyQt5 import QtCore
from datetime import date

class App(QMainWindow):
     
    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(300, 300, 140, 100)
        self.setWindowTitle('TimeTracker')

        # Field for action description
        self.label_checkpoint = QLineEdit(self)
        self.label_checkpoint.move(20, 20)
        self.label_checkpoint.resize(100, 20)

        # Button for writing to log
        btn_checkpoint = QPushButton('Checkpoint', self)
        btn_checkpoint.move(20, 60)
        btn_checkpoint.resize(100, 30)
        btn_checkpoint.setShortcut("Return")

        btn_checkpoint.clicked.connect(self.writeToLog)

    def writeToLog(self):
        filename=FileActions.createJson()
        FileActions.writeToJson({'time':time.strftime("%H:%M:%S", time.localtime()), 'action':self.label_checkpoint.text()}, filename)
        self.label_checkpoint.clear()

class FileActions:
    # Check existing log file and create it if needed
    def createJson():
        filename = '{}.json'.format(date.today())
        newObject = json.dumps({"Timestamps":[]})
        os.path.exists(filename)
        if not os.path.exists(filename):
            with open(filename, "w") as outFile:
                outFile.write(newObject)
        return filename

    # Writing data to existing json log
    def writeToJson(data, filename):
        with open(filename,'r+') as file:
            file_data = json.load(file)
            file_data["Timestamps"].append(data)
            file.seek(0)
            json.dump(file_data, file, indent = 4, ensure_ascii = False)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    actions = FileActions()
    win = App()

    win.show()
    sys.exit(app.exec_())