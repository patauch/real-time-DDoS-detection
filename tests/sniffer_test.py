import PyQt6.QtCore
from utils import App
from pytestqt import qtbot
import PyQt6
import os
from unittest import TestCase


def test_runAfterStop(qtbot):
        widget = App.MainWindow.MainWindow()
        qtbot.addWidget(widget)
        exp = None
        try:
                qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
                qtbot.wait(ms=1000)
                qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

                qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
                qtbot.wait(ms=1000)
                qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
        except Exception as e:
           exp = e     
        assert exp == None # rewrite

def test_NoneWorkerAfterRun(qtbot):
        widget = App.MainWindow.MainWindow()
        qtbot.addWidget(widget)
        
        qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
        qtbot.wait(ms=1000)
        qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

        assert widget.worker == None

def test_secondRunDifferetParams(qtbot):
        widget = App.MainWindow.MainWindow()
        qtbot.addWidget(widget)
        exp = None
        try:
                qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
                qtbot.wait(ms=1000)
                qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

                widget.modelComboBox.setCurrentText("test")

                qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
        except Exception as e:
               exp = e
        assert exp == None
