import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from Samplas.geocode import get_photo, change_spn, change_ll
from Samplas import working_image
from PyQt5.QtCore import Qt


file_name = "map_image.png"  # имя файла картинки


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def transform_address(ll: tuple):  # вернуть корректные координаты
    return ",".join(map(str, ll))


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("map_window.ui", self)  # загрузка ui формы
        self.address = "37.530633,55.702877"  # МГУ имени Ломоносова, Москва
        self.spn = (0.05, 0.05)
        self.ll = (37.530633, 55.702877)
        response = self.get_static(address=transform_address(self.ll))  # получить картинку

        self.image_create(response)  # показать результат

        # словарь с нажатыми кнопками и инструкциями
        self.key_move = {
            "PGUP": {"key": Qt.Key_PageUp, "callback": change_spn, "value": 1, "type": "scale"},
            "PGDN": {"key": Qt.Key_PageDown, "callback": change_spn, "value": -1, "type": "scale"},
            "UP": {"key": Qt.Key_Up, "callback": change_ll, "value": (0, 1), "type": "move"},
            "DOWN": {"key": Qt.Key_Down, "callback": change_ll, "value": (0, -1), "type": "move"},
            "LEFT": {"key": Qt.Key_Left, "callback": change_ll, "value": (-1, 0), "type": "move"},
            "RIGHT": {"key": Qt.Key_Right, "callback": change_ll, "value": (1, 0), "type": "move"}
        }

    def image_create(self, response):  # вывести картинку
        working_image.open_image(response, image_name=file_name)
        self.pixmap = QPixmap(file_name)
        self.image_map_label.setPixmap(self.pixmap)

    def keyPressEvent(self, event):  # обработка клавиатуры
        change_map = False  # если будут изменения
        key = event.key()
        for elem in self.key_move:
            if key == self.key_move[elem]["key"]:

                change_map = True

                if self.key_move[elem]["type"] == "scale":  # прожата кнопка, которая меняет spn
                    self.spn = self.key_move[elem]["callback"](self.spn, self.key_move[elem]["value"])

                elif self.key_move[elem]["type"] == "move":  # прожата кнопка, которая меняет ll
                    self.ll = self.key_move[elem]["callback"](self.ll, self.spn, self.key_move[elem]["value"])

        if change_map:  # обновить фото
            response = self.get_static(transform_address(self.ll), spn=",".join(map(str, self.spn)))
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
