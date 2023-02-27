import sys

import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import nibabel as nib


class ImageWidget(QWidget):
    def __init__(self, parent=None, image=None):
        super().__init__()
        self.image = image
        #scaleFactor灞炴�х敤浜庡瓨鍌ㄥ綋鍓嶅浘鍍忕殑缂╂斁姣斾緥锛岄粯璁ゅ�间负 1.0 琛ㄧず涓嶇缉鏀�
        self.scaleFactor = 1.0
        self.setMouseTracking(True)
        self.setFixedSize(200, 200)
        self.setParent(parent)

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.Wheel:
            print("Wheel event received by ImageWidget")
            self.parent().event(event)
            return True
        return super().event(event)

    def paintEvent(self, event):
        x = self.width() / 2  # 100
        y = self.height() / 2  # 100
        print("paintEvent called")
        painter = QPainter(self)
        # scaled_image = self.image.scaled(200, 200)
        painter.drawImage(self.rect(), self.image)
        # DashLine铏氱嚎   SolidLine瀹炵嚎
        pen = QPen(Qt.blue, 1, Qt.DashLine)
        painter.setPen(pen)
        # 鎺ュ彈鍥涗釜鏁村瀷鍙傛暟锛屽垎鍒唬琛ㄧ洿绾跨殑璧风偣鍜岀粓鐐圭殑 x銆亂 鍧愭爣
        # 缁樺埗鍨傜洿绾�
        painter.drawLine(x, 0, x, self.height())
        # 缁樺埗姘村钩绾�
        painter.drawLine(0, y, self.width(), y)

    def wheelEvent(self, event: QWheelEvent) -> None:
        print("wheelEvent called")
        if event.angleDelta().y() > 0:
            self.scaleFactor *= 1.1
        else:
            self.scaleFactor /= 1.1
        self.hCenter = self.width() / 2
        self.vCenter = self.height() / 2
        self.update()

    def mouseMoveEvent(self, event):
        print(123)
        self.hCenter = event.pos().x()
        self.vCenter = event.pos().y()
        self.update()

    def resizeEvent(self, event):
        print(456)
        self.update()


class MainWindow(QWidget):
    def __init__(self):
        # 鍒囪涓�瀹氳璋冪敤鐖剁被鐨刬nit鏂规硶锛屽洜涓哄畠閲岄潰鏈夊緢澶氬UI鎺т欢鐨勫垵濮嬪寲鎿嶄綔
        super().__init__()
        self.initUI()

    def initUI(self):
        #self.window = QMainWindow()
        #self.window.setWindowTitle('Interactive Segmentation')
        # mainWidget = QWidget()
        # 璇诲彇nii鏍煎紡鍥惧儚
        img = nib.load('lung_002.nii')
        # 鑾峰彇鍥惧儚鏁版嵁鍜屽ご鏂囦欢淇℃伅
        self.data = img.get_fdata()
        self.header = img.header
        # 鑾峰彇鍧愭爣杞寸紪鐮�
        nii_affine = img.affine
        self.axis_order = nib.aff2axcodes(nii_affine)

        # 鍐犵姸闈㈠垏鐗囨粦鍧�
        self.coronalSlider = QSlider(Qt.Horizontal, self)
        self.coronalSlider.setMinimum(0)
        z = self.header.get_data_shape()[2]
        self.coronalSlider.setMaximum(z - 1)
        self.coronalSlider.valueChanged.connect(self.get_coronal_image)
        # 鍐犵姸闈�
        self.coronalLabel = QLabel()
        coronal_image = self.get_coronal_image(z // 2)
        self.imageWidget = ImageWidget(self, coronal_image)

        # self.coronalLabel.setPixmap(imageWidget.grab())
        self.coronalLabel.setFixedSize(200, 200)  # 璁剧疆鍥哄畾澶у皬
        sliderImglayout = QVBoxLayout()
        sliderImglayout.addWidget(self.coronalSlider)
        sliderImglayout.addWidget(self.imageWidget)


        self.setLayout(sliderImglayout)
        # self.window.setCentralWidget(mainWidget)
        self.resize(500, 300)
        # self.window.show()
    #
    def get_coronal_image(self, index):
        print(index)
        # 鑾峰彇鍐犵姸闈㈠浘鍍忔暟鎹� 鏄剧ず鍐犵姸闈㈡椂锛岄渶瑕佸皢鍥惧儚鍦╖杞存柟鍚戜笂鐨勪綅缃彇涓棿鐨勪竴灞�
        z = self.header.get_data_shape()[2]
        if self.axis_order != ('R', 'A', 'S'):
            coronal_data = np.rot90(self.data[:, :, index])
        else:
            coronal_data = self.data[:, :, index]
        # 灏嗘暟鎹浆鎹负8浣嶆棤绗﹀彿鏁存暟绫诲瀷锛屽苟灏嗗儚绱犲�肩缉鏀惧埌0-255鑼冨洿鍐�
        coronal_data = np.uint8(255 * (coronal_data - coronal_data.min()) / (coronal_data.max() - coronal_data.min()))

        # 灏嗘暟鎹浆鎹负QImage鏍煎紡
        height, width = coronal_data.shape
        bytesPerLine = width
        coronal_image = QImage(coronal_data.data.tobytes(), width, height, bytesPerLine, QImage.Format_Grayscale8)


        return coronal_image


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # app.exec_() 绋嬪簭杩涜寰幆绛夊緟鐘舵��
    sys.exit(app.exec_())
