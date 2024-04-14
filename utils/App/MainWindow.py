from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton,
    QWidget, QLabel,
    QLineEdit, QTextEdit, QVBoxLayout,
    QHBoxLayout, QComboBox)
import sys
from .StdoutRedirector import OutputRedirector

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("DDoS Detection")

        self.runButton = QPushButton("Run Detection")
        self.runButton.clicked.connect(self.runButton_was_clicked)
        
        self.stopButton = QPushButton("Stop")
        self.runButton.setCheckable(True)
        self.stopButton.clicked.connect(self.stopButton_was_clicked)

        self.modelComboBox = QComboBox()

        self.interfaceComboBox = QComboBox()

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        #Redirect standart output to the App
        sys.stdout = OutputRedirector(self.output_text)

        self.mainLayout = QVBoxLayout()

        self.headerLayout = QHBoxLayout()
        self.headerLayout.addWidget(self.runButton)
        self.headerLayout.addWidget(self.modelComboBox)
        self.headerLayout.addWidget(self.interfaceComboBox)
        self.headerLayout.addWidget(self.stopButton)

        self.loggerLayout = QHBoxLayout()
        self.loggerLayout.addWidget(self.output_text)


        self.mainLayout.addLayout(self.headerLayout)
        self.mainLayout.addLayout(self.loggerLayout)

        self.container = QWidget()
        self.container.setLayout(self.mainLayout)

        self.setCentralWidget(self.container)

    def runButton_was_clicked(self):
        print("Run Button Clicked!")
        self.runButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.modelComboBox.setEnabled(False)
        self.interfaceComboBox.setEnabled(False)

    def stopButton_was_clicked(self):
        print("Stop Button Clicked")
        self.stopButton.setEnabled(False)
        self.runButton.setEnabled(True)
        self.modelComboBox.setEnabled(True)
        self.interfaceComboBox.setEnabled(True)

    def write(self, text):
        self.output_text.insertPlainText(text)