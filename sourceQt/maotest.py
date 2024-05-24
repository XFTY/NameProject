import sys
import threading
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.exit()

    def exit(self):
        t = threading.Thread(target=self.throwOut, args=())
        t.start()

    def throwOut(self):
        a = 1.0
        while a > 0.1:  # 设置一个较小的不透明度阈值，比如0.1
            QMainWindow.setWindowOpacity(self, a)
            a -= 0.07
            time.sleep(0.04)

        # 当不透明度降低到一定程度，退出应用程序
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())