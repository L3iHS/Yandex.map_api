
import sys

from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from PyQt6.QtCore import Qt

API_KEY_STATIC = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"


class MainWindow(QMainWindow):
    g_map: QLabel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("main_window.ui", self)
        self.map_zoom = 10
        self.map_ll = [37.977751, 55.757718]
        self.map_key = ""

        self.refresh_map()

    def refresh_map(self):
        map_params = {
            "ll": ",".join(map(str, self.map_ll)),
            "z": self.map_zoom,
            "apikey": API_KEY_STATIC,
        }
        session = requests.Session()
        retry = Retry(total=10, connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        response = session.get("https://static-maps.yandex.ru/v1", params=map_params)
        img = QImage.fromData(response.content)
        pixmap = QPixmap.fromImage(img)
        self.g_map.setPixmap(pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageDown:
            self.onPgDownClicked()
        elif event.key() == Qt.Key.Key_PageUp:
            self.onPgUpClicked()

        else:
            super().keyPressEvent(event)

    def onPgUpClicked(self):
        if self.map_zoom < 19:
            self.map_zoom += 1
            self.refresh_map()

    def onPgDownClicked(self):
        if self.map_zoom > 2:
            self.map_zoom -= 1
            self.refresh_map()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
