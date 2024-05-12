import PyQt6.QtCore
from utils import App
from pytestqt import qtbot
import PyQt6
import pickle
import os

def test_load_model(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    pickle.dump(b"TEST_MODEL, TEST_MODEL", open("model/test.sav", "wb"))
    widget.modelComboBox.setCurrentText("test")
    widget_name = widget.modelComboBox.itemText(widget.modelComboBox.currentIndex())
    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    assert widget.worker.model_name == widget_name

    os.remove("model/test.sav")

def test_load_interface(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    pickle.dump(b"TEST_MODEL, TEST_MODEL", open("model/test.sav", "wb"))

    widget.modelComboBox.setCurrentText("test")
    interface_name = widget.interfaceComboBox.itemText(widget.interfaceComboBox.currentIndex())
    model_name = widget.modelComboBox.itemText(widget.modelComboBox.currentIndex())

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    assert widget.worker.model_name == model_name

    os.remove("model/test.sav")

    assert widget.worker.interface == interface_name

def test_incorrect_interface(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)
    exp = None
    widget.interfaceComboBox.setCurrentText("test")


    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    
    assert widget.selectedInterface != "test"