import sys, traceback
import os
# Get the current directory of the script
current_dir = os.path.dirname(os.path.realpath(__file__))

# Add the parent directory to the Python path
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.insert(0, parent_dir)


from utils import App, Flow, Sniffer

from PyQt6.QtWidgets import QApplication

def main():
    print("hello world")

    app = QApplication(sys.argv)

    window = App.MainWindow.MainWindow()
    window.show()

    app.exec()

    


if __name__=="__main__":
    main()