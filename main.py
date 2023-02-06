import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget
from PyQt5 import uic


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("map_window.ui", self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MapWindow()
    mw.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())


