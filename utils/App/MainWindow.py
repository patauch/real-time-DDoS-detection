from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QPushButton, QWidget

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("DDoS Detection")
        
        self.runButton = QPushButton("Run Detection")
        self.runButton.setCheckable(True)
        self.runButton.clicked.connect(self.runButton_was_clicked)

        self.setCentralWidget(self.runButton)

    def runButton_was_clicked(self):
        print("Run Button Clicked!")