from PyQt6.QtCore import Qt, QThreadPool
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton,
    QWidget, QTextEdit,
    QVBoxLayout, QHBoxLayout,
    QComboBox)
import sys, traceback
import os
from .StdoutRedirector import OutputRedirector
from .ThreadWorker import Worker
from datetime import datetime
import psutil


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.last_startTime = None

        self.setWindowTitle("DDoS Detection")

        self.runButton = QPushButton("Run Detection")
        self.runButton.clicked.connect(self.runButton_was_clicked)
        
        self.stopButton = QPushButton("Stop")
        self.stopButton.setEnabled(False)
        self.stopButton.clicked.connect(self.stopButton_was_clicked)

        self.modelComboBox = QComboBox()
        self.modelComboBox.addItems(self.getModelNames())
        self.modelComboBox.activated.connect(self.activated)
        self.modelComboBox.currentTextChanged.connect(self.text_changed)
        self.modelComboBox.currentIndexChanged.connect(self.index_changed)
        

        self.interfaceComboBox = QComboBox()
        self.interfaceComboBox.addItems(self.getInterfaceNames())

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        
        #Redirect standart output to the App
        self.old_stderr = sys.stderr
        self.old_stdout = sys.stdout
        sys.stderr = OutputRedirector(self.output_text, sys.stderr)
        sys.stdout = OutputRedirector(self.output_text, sys.stdout)

        self.saveLogsButton = QPushButton("Save Logs")
        self.saveLogsButton.setEnabled(False)
        self.saveLogsButton.clicked.connect(self.saveLogsButton_was_clicked)

        self.threadpool = QThreadPool()

        self.mainLayout = QVBoxLayout()

        self.headerLayout = QHBoxLayout()
        self.headerLayout.addWidget(self.runButton)
        self.headerLayout.addWidget(self.modelComboBox)
        self.headerLayout.addWidget(self.interfaceComboBox)
        self.headerLayout.addWidget(self.stopButton)

        self.loggerLayout = QHBoxLayout()
        self.loggerLayout.addWidget(self.output_text)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.addWidget(self.saveLogsButton)


        self.mainLayout.addLayout(self.headerLayout)
        self.mainLayout.addLayout(self.loggerLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        self.container = QWidget()
        self.container.setLayout(self.mainLayout)

        self.setCentralWidget(self.container)

    def runButton_was_clicked(self):
        try:
            self.last_startTime = datetime.now().strftime("[%y.%m.%d;%H-%M-%S]")

            print("Run Button Clicked!")
            
            self.runButton.setEnabled(False)
            self.stopButton.setEnabled(True)

            self.modelComboBox.setEnabled(False)
            print("Model Selection is disabled")

            self.interfaceComboBox.setEnabled(False)
            print("Interface Selection is disabled")

            self.run_thread()
        except:
            sys.stderr = self.old_stderr
            sys.stdout = self.old_stdout
            traceback.print_exc()

    def stopButton_was_clicked(self):
        print("Stop Button Clicked")
        self.worker.stop()


    def run_thread(self):
        self.worker = Worker()
        self.worker.signals.finished.connect(self.thread_complete)

        self.worker.signals.error.connect(self.error_recieved)

        self.worker.signals.prints.connect(self.print_message)

        self.threadpool.start(self.worker)

    def thread_complete(self):
        print("Run finished!")

        self.saveLogsButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.runButton.setEnabled(True)
        self.modelComboBox.setEnabled(True)
        self.interfaceComboBox.setEnabled(True)
        self.worker.stop()

    def saveLogsButton_was_clicked(self):
        text = self.output_text.toPlainText()
        with open(f"output/log_{self.last_startTime}.txt", "w") as f:
            f.write(text)
        self.output_text.clear()
        self.saveLogsButton.setEnabled(False)

    def activated(self, index):
        print(f"Activated index: {index}")

    def text_changed(self, s):
        print(f"Text changed: {s}")

    def index_changed(self, index):
        print(f"Index changed", index) 

    def error_recieved(self, *args):
        try:
            for arg in args:
                print(arg)
        except:
            traceback.print_exc()
    
    def get_last_startTime(self):
        return self.last_startTime
    
    def print_message(self, text):
        print(text)

    def getModelNames(self):
        path = "model/"
        model_paths = os.listdir(path)
        filtered_model_names = []
        for path in model_paths:
            p = path.split('.')
            if p[-1] != "txt":
                filtered_model_names.append(p[0])
        return filtered_model_names
    
    def getInterfaceNames(self):
        return list(psutil.net_if_addrs().keys())