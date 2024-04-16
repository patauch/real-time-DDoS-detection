from PyQt6.QtCore import QRunnable, pyqtSlot
import time

class Worker(QRunnable):
    
    def __init__(self) -> None:
        super().__init__()
        self.is_stopped = False

    @pyqtSlot()
    def run(self):

        print("Thread start")
        for i in range(100):
            if self.is_stopped:
                break                
            time.sleep(5)
            print(f"Time slept {i+1}")

        print("Thread complete")

    def stop(self):
        self.is_stopped = True