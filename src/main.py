
import sys
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт
from dotenv import load_dotenv
import os


import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QInputDialog
from PyQt6.QtGui import QPixmap, QImage
import requests
from PIL import Image



load_dotenv(override=True)
# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])
print(sys.argv[1:3])
toponym_lattitude, toponym_longitude = sys.argv[1:3]
if ',' in toponym_longitude:
    toponym_longitude = toponym_longitude.replace(',', '')
if ',' in toponym_lattitude:
    toponym_lattitude = toponym_lattitude.replace(',', '')
print(toponym_longitude, toponym_lattitude)

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
# toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
# print(toponym_longitude, toponym_lattitude)

delta = "0.001"
apikey = os.getenv('apikey')

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta, delta]),
    "apikey": apikey,

}

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)


def load_image_from_bytesio(data):
    image = QImage()
    image.loadFromData(data.getvalue())
    return QPixmap.fromImage(image)


class MainWindow(QWidget):
    def __init__(self, width, height, im):
        super().__init__()
        pixmap = load_image_from_bytesio(im)
        label = QLabel(self)
        label.setPixmap(pixmap)
        self.resize(width, height)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(900, 900, im)
    sys.exit(app.exec())
