import sys
from PyQt6.QtGui import QTextCursor

class OutputRedirector:    
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.stdout = sys.stdout

    def write(self, text):
        self.text_widget.insertPlainText(text)
        self.stdout.write(text)

    def flush(self):
        pass