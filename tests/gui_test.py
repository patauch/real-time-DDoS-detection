from utils import App
from pytestqt import qtbot
import PyQt6


def test_toggle_runButton(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    assert (widget.runButton.isEnabled() == False) and (widget.stopButton.isEnabled() == True)


def test_toggle_stopButton(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    assert (widget.runButton.isEnabled()) == True and (widget.stopButton.isEnabled() == False)

