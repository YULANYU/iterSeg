import sys
from PyQt5.QtGui import QImage, QPainter, QPen, QWheelEvent
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QEvent


class ImageWidget(QWidget):
    def __init__(self, parent=None, image=None):
        super(ImageWidget, self).__init__(parent)
        self.image = image
        self.scaleFactor = 1.0
        self.hCenter = self.width() / 2
        self.vCenter = self.width() / 2
        self.flag = 0
        self.setMouseTracking(True)
        self.setFixedSize(300, 300)
        self.setParent(parent)

    def paintEvent(self, event):
        if self.flag == 0 :

            self.hCenter = self.width() / 2
            self.vCenter = self.height() / 2
            self.flag = 1
        print("paintEvent called")
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image)
        pen = QPen(Qt.red, 1, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(self.hCenter, 0, self.hCenter, self.height())
        painter.drawLine(0, self.vCenter, self.width(), self.vCenter)

    def wheelEvent(self, event: QWheelEvent) -> None:
        print("wheelEvent called")
        if event.angleDelta().y() > 0:
            self.scaleFactor *= 1.1
        else:
            self.scaleFactor /= 1.1
        self.hCenter = self.width() / 2
        self.vCenter = self.height() / 2
        self.update()

    def mousePressEvent(self, event):
        print("mouseMoveEvent called")
        self.hCenter = event.pos().x()
        self.vCenter = event.pos().y()
        self.update()

    def resizeEvent(self, event):
        print("resizeEvent called")
        self.update()


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        layout = QVBoxLayout(self)

        image = QImage("image.png")
        imageWidget = ImageWidget(self, image)

        layout.addWidget(imageWidget)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
