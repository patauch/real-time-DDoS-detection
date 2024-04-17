from PyQt6.QtCore import QRunnable, QObject, pyqtSlot, pyqtSignal

import time
import traceback, sys
import os

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    prints = pyqtSignal(str)


class Worker(QRunnable):
    
    def __init__(self) -> None:
        super(Worker, self).__init__()
        self.is_stopped = False
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            #print("Thread start")
            for i in range(1000):
                if self.is_stopped:
                    break                              
                string = f"Time slept {i+1}"
                self.signals.prints.emit(string)
            time.sleep(2)  
                
        except:
            traceback.print_exc()
            print(sys.exc_info()[:2])

            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()

    def stop(self):
        self.is_stopped = True