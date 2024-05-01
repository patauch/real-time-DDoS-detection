from PyQt6.QtCore import Qt, QThreadPool
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton,
    QWidget, QTextEdit,
    QVBoxLayout, QHBoxLayout, QStackedLayout,
    QComboBox, QCheckBox,
    QFileDialog)
import sys, traceback
import os
from .StdoutRedirector import OutputRedirector
from .ThreadWorker import Worker
from datetime import datetime
import psutil
from copy import copy

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.last_startTime = None
        self.availableModels = None
        self.availableInterfaces = None
        self.selectedModel = None
        self.selectedInterface = None
        self.selectedPCAP = None
        self.selectedWorkMode = None

        self.setWindowTitle("DDoS Detection")

        self.runButton = QPushButton("Run Detection")
        self.runButton.clicked.connect(self.runButton_was_clicked)
        
        self.stopButton = QPushButton("Stop")
        self.stopButton.setEnabled(False)
        self.stopButton.clicked.connect(self.stopButton_was_clicked)

        self.modelComboBox = QComboBox()
        self.modelComboBox.addItems(self.getModelNames())
        self.modelComboBox.activated.connect(self.activatedModel)
        
        self.workMode = QCheckBox('Use offline analysis')
        self.workMode.setCheckState(Qt.CheckState.Unchecked)
        self.workMode.stateChanged.connect(self.activateCheckBox)

        self.interfaceComboBox = QComboBox()
        self.interfaceComboBox.addItems(self.getInterfaceNames())
        self.interfaceComboBox.activated.connect(self.activatedInterface)

        self.browseButton = QPushButton("Select file")
        self.browseButton.clicked.connect(self.openFileDialog)

        self.fileName_text = QTextEdit()
        self.fileName_text.setReadOnly(True)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        
        #Redirect standart output to the App
        self.old_stderr = sys.stderr
        self.old_stdout = sys.stdout
        sys.stderr = OutputRedirector(self.output_text, sys.stderr)
        sys.stdout = OutputRedirector(self.output_text, sys.stdout)

        self.saveLogsButton = QPushButton("Save Logs")
        self.saveLogsButton.setEnabled(False)
        self.saveLogsButton.clicked.connect(self.saveLogsButton_was_clicked)

        self.threadpool = QThreadPool()

        self.mainLayout = QVBoxLayout()

        self.headerLayout = QHBoxLayout()
        self.headerLayout.addWidget(self.runButton)
        self.headerLayout.addWidget(self.modelComboBox)
        self.headerLayout.addWidget(self.stopButton)

        self.workModeLayout = QStackedLayout()
        self.workModeLayout.addWidget(self.interfaceComboBox)
        self.workModeLayout.addWidget(self.browseButton)

        self.sourceLayout = QHBoxLayout()
        self.sourceLayout.addWidget(self.workMode)
        self.sourceLayout.addLayout(self.workModeLayout)

        self.loggerLayout = QHBoxLayout()
        self.loggerLayout.addWidget(self.output_text)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.addWidget(self.saveLogsButton)


        self.mainLayout.addLayout(self.headerLayout)
        self.mainLayout.addLayout(self.sourceLayout)
        self.mainLayout.addLayout(self.loggerLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        self.container = QWidget()
        self.container.setLayout(self.mainLayout)

        self.setCentralWidget(self.container)

    def runButton_was_clicked(self):
        try:
            self.worker = Worker()
            self.last_startTime = datetime.now().strftime("[%y.%m.%d;%H-%M-%S]")

            if self.selectedModel is None:
                self.selectedModel = self.modelComboBox.itemText(self.modelComboBox.currentIndex())
                self.worker.set_params(model_name=self.selectedModel)
                self.worker.set_params(model_path=self.availableModels[self.selectedModel])
                self.worker.set_model()
                print(f"Selected model: {self.selectedModel}")

            if self.selectedInterface is None and self.selectedWorkMode!="Offline":
                self.selectedInterface = self.interfaceComboBox.itemText(self.interfaceComboBox.currentIndex())
                self.worker.set_params(interface=self.selectedInterface)
                print(f"Selected interface: {self.selectedInterface}")
            
            if not self.selectedPCAP and self.selectedWorkMode=="Offline":
                print("Haven't selected PCAP")
                pass
            else:
                self.worker.set_params(pcap_path=self.selectedPCAP)

                self.worker.set_params(mode=self.selectedWorkMode)

                print("Run Button Clicked!")
                
                self.runButton.setEnabled(False)
                self.stopButton.setEnabled(True)

                self.modelComboBox.setEnabled(False)
                print("Model Selection is disabled")

                self.interfaceComboBox.setEnabled(False)
                print("Interface Selection is disabled")

                self.workMode.setEnabled(False)
                self.browseButton.setEnabled(False)
                try:
                    print("Nothing here")
                    """self.snifferModel = SnifferModel(self.selectedModel,
                                                self.availableModels[self.selectedModel], self.selectedWorkMode,
                                                self.selectedInterface, self.selectedPCAP)"""
                except:
                    print("Model isn't implemented yet")
                    traceback.print_exc()

                self.run_thread()
        except:
            sys.stderr = self.old_stderr
            sys.stdout = self.old_stdout
            traceback.print_exc()

    def stopButton_was_clicked(self):
        print("Stop Button Clicked")
        self.worker.stop()

    def run_thread(self): 
        self.worker.signals.finished.connect(self.thread_complete)

        self.worker.signals.error.connect(self.error_recieved)

        self.worker.signals.prints.connect(self.print_message)
        
        self.threadpool.start(self.worker)

    def thread_complete(self):
        print("Run finished!")

        self.selectedModel = None

        self.selectedInterface = None

        self.saveLogsButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.runButton.setEnabled(True)
        self.modelComboBox.setEnabled(True)
        self.workMode.setEnabled(True)
        self.browseButton.setEnabled(True)
        self.interfaceComboBox.setEnabled(True)
        #self.worker.stop()

    def saveLogsButton_was_clicked(self):
        text = self.output_text.toPlainText()
        with open(f"output/log_{self.last_startTime}.txt", "w") as f:
            f.write(text)
        self.output_text.clear()
        self.saveLogsButton.setEnabled(False)

    def activatedModel(self, index):
        self.selectedModel = self.modelComboBox.itemText(index)
        print(f"Selected Model: {self.selectedModel}")

    def activatedInterface(self, index):
        self.selectedInterface = self.interfaceComboBox.itemText(index)
        print(f"Selected Interface: {self.selectedInterface}")

    def activateCheckBox(self, s):
        if s == 0:
            self.workModeLayout.setCurrentIndex(0)
            self.selectedWorkMode = "Live"
        if s == 2:
            self.workModeLayout.setCurrentIndex(1)
            self.selectedWorkMode = "Offline"


    def openFileDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '.\pcap', 'PCAP files (*.pcap)')
        self.selectedPCAP = fname[0]


    def error_recieved(self, *args):
        try:
            for arg in args:
                print(arg)
        except:
            traceback.print_exc()
    
    def get_last_startTime(self):
        return self.last_startTime
    
    def print_message(self, text):
        print(text)

    def getModelNames(self):
        path = "model/"
        model_paths = os.listdir(path)
        filtered_model_names = {}
        for path in model_paths:
            p = path.split('.')
            if p[-1] != "txt":
                filtered_model_names[p[0]]=path
        self.availableModels = copy(filtered_model_names)
        return filtered_model_names.keys()
    
    def getInterfaceNames(self):
        return list(psutil.net_if_addrs().keys())