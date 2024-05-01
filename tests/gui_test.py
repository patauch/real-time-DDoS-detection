import PyQt6.QtCore
from utils import App
from pytestqt import qtbot
import PyQt6
import os
import psutil

def test_toggle_runButton(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)

    assert (widget.runButton.isEnabled() == False) and (widget.stopButton.isEnabled() == True)


def test_toggle_stopButton_after_run(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    qtbot.wait(ms=1000)
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
    qtbot.wait(ms=1000)
    qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    
    assert (widget.interfaceComboBox.isEnabled() == True)

    
def test_toggle_modelSelect_after_stop(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    qtbot.wait(ms=1000)
    qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    
    assert (widget.modelComboBox.isEnabled() == True)

def test_loadModelNames(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    model_path = "model/"
    model_paths = os.listdir(model_path)
    filtered_paths = []
    for path in model_paths:
        if path.split('.')[-1] != "txt":
            filtered_paths.append(path)
    model_names = [path.split('.')[0] for path in filtered_paths]

    widget_names = [widget.modelComboBox.itemText(i) for i in range(widget.modelComboBox.count())]

    assert model_names == widget_names

def test_loadInterfaces(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    ifaces = list(psutil.net_if_addrs().keys())

    widget_ifaces = [widget.interfaceComboBox.itemText(i) for i in range(widget.interfaceComboBox.count())]

    assert ifaces == widget_ifaces

def test_setModel(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    widget_name = widget.modelComboBox.itemText(widget.modelComboBox.currentIndex())
    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    assert widget.selectedModel == widget_name
    qtbot.wait(ms=1000)
    qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    assert widget.selectedModel == None

def test_setInterface(qtbot):
    widget = App.MainWindow.MainWindow()
    qtbot.addWidget(widget)

    widget_name = widget.interfaceComboBox.itemText(widget.interfaceComboBox.currentIndex())
    qtbot.mouseClick(widget.runButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    assert widget.selectedInterface == widget_name
    qtbot.wait(ms=1000)
    qtbot.mouseClick(widget.stopButton, PyQt6.QtCore.Qt.MouseButton.LeftButton)
    assert widget.selectedInterface == None
