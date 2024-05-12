import traceback, sys
from PyQt6.QtGui import QTextCursor

class OutputRedirector:    
    def __init__(self, text_widget, stream):
        self.text_widget = text_widget
        self.stdout = stream
        self.old_stdout = stream

    def write(self, text):
        try:
            self.stdout.write(text)
            self.text_widget.moveCursor(QTextCursor.MoveOperation.End)
            self.text_widget.insertPlainText(text)
            
        except:
            sys.stream = self.old_stdout
            traceback.print_exc()

    def flush(self):
        pass