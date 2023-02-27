import nibabel as nib
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication,QHBoxLayout
import sys
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 璇诲彇nii鏍煎紡鍥惧儚
        img = nib.load('lung_002.nii')
        data = img.get_fdata()
        header = img.header

        # 鏄剧ず鍐犵姸闈�
        coronal = QLabel(self)
        coronal_image = self.get_coronal_image(data, header)
        coronal.setPixmap(QPixmap.fromImage(coronal_image))

        # 鏄剧ず姘村钩闈�
        horizontal = QLabel(self)
        horizontal_image = self.get_horizontal_image(data, header)
        horizontal.setPixmap(QPixmap.fromImage(horizontal_image))

        # 鏄剧ず鐭㈢姸闈�
        sagittal = QLabel(self)
        sagittal_image = self.get_sagittal_image(data, header)
        sagittal.setPixmap(QPixmap.fromImage(sagittal_image))

        imageboxlayout = QHBoxLayout()
        imageboxlayout.addWidget(coronal)
        imageboxlayout.addWidget(horizontal)
        imageboxlayout.addWidget(sagittal)

        self.setLayout(imageboxlayout)
        # palette.setColor(QPalette.Window, Qt.yellow)


        self.setWindowTitle('PyQt5 GUI')
        self.resize(500, 300)

    def get_coronal_image(self, data, header):
        # 鑾峰彇鍐犵姸闈㈠浘鍍忔暟鎹�
        coronal_data = data[:, :, header.get_data_shape()[2] // 2]

        # 灏嗘暟鎹浆鎹负8浣嶆棤绗﹀彿鏁存暟绫诲瀷锛屽苟灏嗗儚绱犲�肩缉鏀惧埌0-255鑼冨洿鍐�
        coronal_data = np.uint8(255 * (coronal_data - coronal_data.min()) / (coronal_data.max() - coronal_data.min()))

        # 灏嗘暟鎹浆鎹负QImage鏍煎紡
        height, width = coronal_data.shape
        bytesPerLine = width
        coronal_image = QImage(coronal_data.data.tobytes(), width, height, bytesPerLine, QImage.Format_Grayscale8)


        return coronal_image

    def get_horizontal_image(self, data, header):
        # 鑾峰彇姘村钩闈㈠浘鍍忔暟鎹�
        horizontal_data = data[:, header.get_data_shape()[1] // 2, :]

        # 灏嗘暟鎹浆鎹负8浣嶆棤绗﹀彿鏁存暟绫诲瀷锛屽苟灏嗗儚绱犲�肩缉鏀惧埌0-255鑼冨洿鍐�
        horizontal_data = np.uint8(255 * (horizontal_data - horizontal_data.min()) / (horizontal_data.max() - horizontal_data.min()))

        # 灏嗘暟鎹浆鎹负QImage鏍煎紡
        height, width = horizontal_data.shape
        bytesPerLine = width
        horizontal_image = QImage(horizontal_data.data.tobytes(), width, height, bytesPerLine, QImage.Format_Grayscale8)


        return horizontal_image

    def get_sagittal_image(self, data, header):
        # 鑾峰彇鐭㈢姸闈㈠浘鍍忔暟鎹�
        sagittal_data = data[header.get_data_shape()[0] // 2, :, :]

        # 灏嗘暟鎹浆鎹负8浣嶆棤绗﹀彿鏁存暟绫诲瀷锛屽苟灏嗗儚绱犲�肩缉鏀惧埌0-255鑼冨洿鍐�
        sagittal_data = np.uint8(255 * (sagittal_data - sagittal_data.min()) / (sagittal_data.max() - sagittal_data.min()))

        # 灏嗘暟鎹浆鎹负QImage鏍煎紡
        height, width = sagittal_data.shape
        bytesPerLine = width
        sagittal_image = QImage(sagittal_data.data.tobytes(), width, height, bytesPerLine, QImage.Format_Grayscale8)


        return sagittal_image

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
