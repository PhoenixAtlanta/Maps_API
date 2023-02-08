import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from Samplas.geocode import get_photo, change_spn
from Samplas import working_image
from PyQt5.QtCore import Qt


file_name = "map_image.png"  # имя файла картинки


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("map_window.ui", self)  # загрузка ui формы
        self.address = "37.530633,55.702877"  # МГУ имени Ломоносова, Москва
        self.spn = (0.05, 0.05)  # размер по умолчанию
        response = self.get_static(address=self.address)  # получить картинку

        self.image_create(response)  # показать результат

    def image_create(self, response):  # вывести картинку
        working_image.open_image(response, image_name=file_name)
        self.pixmap = QPixmap(file_name)
        self.image_map_label.setPixmap(self.pixmap)

    def keyPressEvent(self, event):  # обработка клавиатуры
        change_size = False  # если будут изменения
        if event.key() == Qt.Key_PageUp:
            change_size = True
            self.spn = change_spn(self.spn, 1)

        elif event.key() == Qt.Key_PageDown:
            change_size = True
            self.spn = change_spn(self.spn, -1)

        if change_size:  # обновить фото
            response = self.get_static(self.address, spn=",".join(map(str, self.spn)))
            self.image_create(response)

    @staticmethod
    def get_static(address, spn="0.03,0.03"):  # запрос по получению фотографии
        response = get_photo(address, spn=spn)  # МГУ имени Ломоносова, Москва
        return response

    def closeEvent(self, event):  # удалить фото при закрытии проложения
        working_image.close_image(image_name=file_name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MapWindow()
    mw.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
