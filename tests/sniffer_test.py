import PyQt6.QtCore
from utils import App
from pytestqt import qtbot
import PyQt6
import os
from unittest import TestCase


def test_runAfterStop(qtbot):
        widget = App.MainWindow.MainWindow()
        qtbot.addWidget(widget)

        qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
        qtbot.wait(ms=1000)
        qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

        qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
        qtbot.wait(ms=1000)
        qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
        assert widget.worker != None