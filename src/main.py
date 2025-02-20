import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QInputDialog
from PyQt6.QtGui import QPixmap, QImage


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
