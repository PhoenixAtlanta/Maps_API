import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from Samplas.geocode import get_photo
from Samplas import working_image


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_name = "map_image.png"
        uic.loadUi("map_window.ui", self)

        response = get_photo("37.530633,55.702877")  # МГУ имени Ломоносова, Москва
        working_image.open_image(response, image_name=self.file_name)

        self.pixmap = QPixmap(self.file_name)
        self.image_map_label.setPixmap(self.pixmap)

        working_image.close_image(image_name=self.file_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MapWindow()
    mw.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
