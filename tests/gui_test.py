import PyQt6.QtCore
from utils import App
from pytestqt import qtbot
import PyQt6
import time


def test_toggle_runButton(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    assert (widget.runButton.isEnabled() == False) and (widget.stopButton.isEnabled() == True)


def test_toggle_stopButton_after_run(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    with qtbot.waitSignal(widget.worker.signals.finished, timeout=5000):
        qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)


    assert (widget.runButton.isEnabled()) == True and (widget.stopButton.isEnabled() == False)

def test_toggle_modelSelect_after_run(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    assert (widget.modelComboBox.isEnabled() == False)

def test_toggle_interfaceSelect_after_run(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    
    assert (widget.interfaceComboBox.isEnabled() == False)

def test_toggle_interfaceSelect_after_stop(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    with qtbot.waitSignal(widget.worker.signals.finished, timeout=5000):
        qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    
    assert (widget.interfaceComboBox.isEnabled() == True)

    
def test_toggle_modelSelect_after_stop(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    with qtbot.waitSignal(widget.worker.signals.finished, timeout=5000):
        qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    
    assert (widget.modelComboBox.isEnabled() == True)

