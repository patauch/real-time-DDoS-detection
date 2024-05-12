import PyQt6.QtCore
from utils import App
from pytestqt import qtbot
import PyQt6
import os
import datetime
import time


def test_press_save_on_init(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.saveLogsButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    
    assert widget.saveLogsButton.isEnabled() == False

def test_press_save_after_start(qtbot):
    widget = App.MainWindow.MainWindow()

    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    assert widget.saveLogsButton.isEnabled() == False

def test_press_save_after_stop(qtbot):
    widget = App.MainWindow.MainWindow()

    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    qtbot.wait(ms=1000)
    qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    start_time = widget.get_last_startTime()
    
    qtbot.mouseClick(widget.saveLogsButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    assert os.path.exists(f"output/log_{start_time}.txt") == True and start_time != None

def test_clear_logs_after_save(qtbot):
    widget = App.MainWindow.MainWindow()

    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    qtbot.wait(ms=1000)
    qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    start_time = widget.get_last_startTime()

    qtbot.mouseClick(widget.saveLogsButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    assert widget.output_text.toPlainText() == ''

def test_saveButton_state_after_click(qtbot):
    widget = App.MainWindow.MainWindow()

    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    qtbot.wait(ms=1000)
    qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    start_time = widget.get_last_startTime()

    qtbot.mouseClick(widget.saveLogsButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    assert widget.saveLogsButton.isEnabled() == False


def test_toggle_saveButton_after_init(qtbot):
    widget = App.MainWindow.MainWindow()

    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    qtbot.wait(ms=1000)
    qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    assert widget.saveLogsButton.isEnabled() == True


