from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton,
    QWidget, QLabel,
    QLineEdit, QVBoxLayout,
    QHBoxLayout, QComboBox)

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("DDoS Detection")

        self.runButton = QPushButton("Run Detection")
        self.runButton.clicked.connect(self.runButton_was_clicked)
        self.runButton_is_checked = True
        
        self.stopButton = QPushButton("Stop")
        self.stopButton.clicked.connect(self.stopButton_was_clicked)

        self.modelComboBox = QComboBox()

        self.interfaceComboBox = QComboBox()

        self.mainLayout = QVBoxLayout()

        self.headerLayout = QHBoxLayout()
        self.headerLayout.addWidget(self.runButton)
        self.headerLayout.addWidget(self.modelComboBox)
        self.headerLayout.addWidget(self.interfaceComboBox)
        self.headerLayout.addWidget(self.stopButton)

        self.loggerLayout = QHBoxLayout()

        self.mainLayout.addLayout(self.headerLayout)
        self.mainLayout.addLayout(self.loggerLayout)

        self.container = QWidget()
        self.container.setLayout(self.mainLayout)

        self.setCentralWidget(self.container)

    def runButton_was_clicked(self):
        print("Run Button Clicked!")

    def stopButton_was_clicked(self):
        print("Stop Button Clicked")