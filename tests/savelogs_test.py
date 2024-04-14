import PyQt6.QtCore
from utils import App
from pytestqt import qtbot
import PyQt6
import os
import datetime


def test_press_save_on_init(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.saveLogsButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    
    assert widget.saveLogsButton.isEnabled() == False


def test_press_save(qtbot):
    widget = App.MainWindow.MainWindow()

    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    start_time = widget.get_last_startTime()

    qtbot.mouseClick(widget.saveLogsButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    assert os.path.exists(f"output/log_{start_time}.txt") == True and start_time != None

def test_toggle_saveButton_after_init(qtbot):
    widget = App.MainWindow.MainWindow()

    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    assert widget.saveLogsButton.isEnabled() == True


