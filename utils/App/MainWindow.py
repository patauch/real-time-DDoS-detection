from PyQt6.QtCore import Qt, QThreadPool
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton,
    QWidget, QLabel,
    QLineEdit, QTextEdit, QVBoxLayout,
    QHBoxLayout, QComboBox)
import sys
from .StdoutRedirector import OutputRedirector
from .ThreadWorker import Worker
import os
from datetime import datetime

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

        self.interfaceComboBox = QComboBox()

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        #Redirect standart output to the App
        sys.stdout = OutputRedirector(self.output_text)

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
        self.last_startTime = datetime.now().strftime("[%y.%m.%d;%H-%M-%S]")
        print("Run Button Clicked!")
        self.runButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.modelComboBox.setEnabled(False)
        print("Model Selection is disabled")
        self.interfaceComboBox.setEnabled(False)
        print("Interface Selection is disabled")
        self.run_thread()

    def stopButton_was_clicked(self):
        print("Stop Button Clicked")
        self.saveLogsButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.runButton.setEnabled(True)
        self.modelComboBox.setEnabled(True)
        self.interfaceComboBox.setEnabled(True)
        self.worker.stop()

    def run_thread(self):
        self.worker = Worker()
        self.threadpool.start(self.worker)

    def write(self, text):
        self.output_text.insertPlainText(text)

    def saveLogsButton_was_clicked(self):
        text = self.output_text.toPlainText()
        with open(f"output/log_{self.last_startTime}.txt", "w") as f:
            f.write(text)
        self.output_text.clear()
        self.saveLogsButton.setEnabled(False)
    
    def get_last_startTime(self):
        return self.last_startTime
