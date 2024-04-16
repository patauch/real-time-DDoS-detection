from PyQt6.QtCore import QRunnable, pyqtSlot
import time

class Worker(QRunnable):

    @pyqtSlot()
    def run(self):

        print("Thread start")
        for i in range(100):
            time.sleep(5)
            print(f"Time slept {i+1}")

        print("Thread complete")
