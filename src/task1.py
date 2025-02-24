import sys
import os

from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

load_dotenv(override=True)
API_KEY_STATIC = os.getenv('API_KEY_STATIC')


class MainWindow(QMainWindow):
    g_map: QLabel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('src/main_window.ui', self)

        # self.g_map = self.findChild(QLabel, "g_map")
        self.map_zoom = 10
        self.map_ll = [37.977751, 55.757718]
        self.map_key = ''

        self.refresh_map()

    def keyPressEvent(self, event):
        pass

    def refresh_map(self, theme):
        map_params = {
            'theme': theme,   # темная тема -> 'dark'  светлая -> 'light'
            "ll": ','.join(map(str, self.map_ll)),
            'z': self.map_zoom,
            'apikey': API_KEY_STATIC,
        }
        session = requests.Session()
        retry = Retry(total=10, connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.get('https://static-maps.yandex.ru/v1',
                               params=map_params)
        img = QImage.fromData(response.content)
        pixmap = QPixmap.fromImage(img)
        self.g_map.setPixmap(pixmap)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())