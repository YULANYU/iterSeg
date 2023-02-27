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
        print(self.image.shape)
        #scaleFactor灞炴�х敤浜庡瓨鍌ㄥ綋鍓嶅浘鍍忕殑缂╂斁姣斾緥锛岄粯璁ゅ�间负 1.0 琛ㄧず涓嶇缉鏀�
        self.scaleFactor = 1.0
        self.setMouseTracking(True)
        self.setFixedSize(200, 200)
        self.setParent(parent)

    # def event(self, event: QEvent) -> bool:
    #     if event.type() == QEvent.Wheel:
    #         print("Wheel event received by ImageWidget")
    #         self.parent().event(event)
    #         return True
    #     return super().event(event)

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
        # if event.angleDelta().y() > 0:
        #     self.scaleFactor *= 1.1
        # else:
        #     self.scaleFactor /= 1.1
        # self.hCenter = self.width() / 2
        # self.vCenter = self.height() / 2

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
        self.window = QMainWindow()
        self.window.setWindowTitle('Interactive Segmentation')
        menubar = self.window.menuBar()
        file_menu = menubar.addMenu('File')

        openAction = QAction(QIcon('open.png'), 'Open Image', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a file for segmenting.')
        openAction.triggered.connect(self.doSomething)
        file_menu.addAction(openAction)

        saveAction = QAction(QIcon('save.png'), 'Save Image', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save file to disk.')
        saveAction.triggered.connect(self.doSomething)
        file_menu.addAction(saveAction)
        # 鍔犲叆涓�涓垎鍓茬嚎鐨勬柟娉�
        file_menu.addSeparator()

        closeAction = QAction(QIcon('quit.png'), 'Exit', self)
        closeAction.setShortcut('Ctrl+Q')
        closeAction.setStatusTip('Exit application')
        closeAction.triggered.connect(self.close)
        file_menu.addAction(closeAction)

        mainWidget = QWidget()

        annotationButton = QPushButton("Load Image")
        # button.setStyleSheet("background-color: red")
        annotationButton.setStyleSheet("background-color:#03B2F2;color: white;")
        annotationButton.clicked.connect(self.doSomething)

        segmentButton = QPushButton("Segment")
        segmentButton.setStyleSheet("background-color:#03B2F2;color: white;")
        segmentButton.clicked.connect(self.doSomething)

        refinementButton = QPushButton("Refinement")
        refinementButton.setStyleSheet("background-color:#03B2F2;color: white;")
        refinementButton.clicked.connect(self.doSomething)

        CleanButton = QPushButton("Clear all seeds")
        CleanButton.setStyleSheet("background-color:#03B2F2;color: white;")
        CleanButton.clicked.connect(self.doSomething)

        NextButton = QPushButton("Save segmentation")
        NextButton.setStyleSheet("background-color:#03B2F2;color: white;")
        NextButton.clicked.connect(self.doSomething)

        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        StateLine = QLabel()
        StateLine.setText("Clicks as user input")
        palette = QPalette()
        palette.setColor(StateLine.foregroundRole(), Qt.blue)
        #  palette.setColor(QPalette.WindowText, Qt.blue)

        font = QFont('SimHei', 20)
        StateLine.setFont(font)
        StateLine.setPalette(palette)

        MethodLine = QLabel()
        MethodLine.setText("Segmentation")
        mpalette = QPalette()
        mpalette.setColor(MethodLine.foregroundRole(), Qt.blue)
        MethodLine.setPalette(mpalette)

        SaveLine = QLabel()
        SaveLine.setText("Clean or Save")
        spalette = QPalette()
        spalette.setColor(SaveLine.foregroundRole(), Qt.blue)
        SaveLine.setPalette(spalette)

        # QHBoxLayout锛氭按骞冲竷灞�
        # QVBoxLayout锛氬瀭鐩村竷灞�
        rightlayout = QVBoxLayout()

        rightlayout.addWidget(StateLine)
        rightlayout.addWidget(annotationButton)
        rightlayout.addWidget(MethodLine)
        rightlayout.addWidget(segmentButton)
        rightlayout.addWidget(refinementButton)
        rightlayout.addWidget(SaveLine)
        rightlayout.addWidget(CleanButton)
        rightlayout.addWidget(NextButton)
        rightlayout.addStretch()

        tipsFont = StateLine.font()
        # 瀛椾綋澶у皬
        tipsFont.setPointSize(10)

        StateLine.setFixedHeight(30)
        # setWordWrap鏄疨yQt5涓璔Label缁勪欢鐨勪竴涓柟娉曪紝鐢ㄤ簬璁剧疆鏂囨湰鏄惁鑷姩鎹㈣
        StateLine.setWordWrap(True)
        StateLine.setFont(tipsFont)
        MethodLine.setFixedHeight(30)
        MethodLine.setWordWrap(True)
        MethodLine.setFont(tipsFont)
        SaveLine.setFixedHeight(30)
        SaveLine.setWordWrap(True)
        SaveLine.setFont(tipsFont)

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
        self.get_coronal_image(z // 2)
        # self.coronalLabel.setFixedSize(200, 200)  # 璁剧疆鍥哄畾澶у皬
        sliderImglayout = QVBoxLayout()
        sliderImglayout.addWidget(self.coronalSlider)
        sliderImglayout.addWidget(self.imageWidget)

        # 姘村钩闈㈡粦鍧�
        self.horizontalSlider = QSlider(Qt.Horizontal, self)
        self.horizontalSlider.setMinimum(0)
        y = self.header.get_data_shape()[1]
        self.horizontalSlider.setMaximum(z - 1)
        self.horizontalSlider.valueChanged.connect(self.get_horizontal_image)

        # 姘村钩闈�
        self.horizontalLabel = QLabel()
        self.get_horizontal_image(y // 2)
        self.horizontalLabel.setFixedSize(200, 200)  # 璁剧疆鍥哄畾澶у皬
        # self.horizontalLabel.setPixmap(QPixmap.fromImage(QImage("logo.png")))

        sliderImglayout2 = QVBoxLayout()
        sliderImglayout2.addWidget(self.horizontalSlider)
        sliderImglayout2.addWidget(self.horizontalLabel)

        # 3.鐭㈢姸闈㈡粦鍧�
        self.sagittalSlider = QSlider(Qt.Horizontal, self)
        self.sagittalSlider.setMinimum(0)
        x = self.header.get_data_shape()[0]
        self.sagittalSlider.setMaximum(z - 1)
        self.sagittalSlider.valueChanged.connect(self.get_sagittal_image)

        # 3.鐭㈢姸闈�
        self.sagittalLabel = QLabel()
        self.get_sagittal_image(x // 2)
        self.sagittalLabel.setFixedSize(200, 200)  # 璁剧疆鍥哄畾澶у皬
        sliderImglayout3 = QVBoxLayout()
        sliderImglayout3.addWidget(self.sagittalSlider)
        sliderImglayout3.addWidget(self.sagittalLabel)

        self.vtkLabel = QLabel()
        # vtk_image = self.get_sagittal_image(data, header)
        self.vtkLabel.setPixmap(QPixmap.fromImage(QImage("logo.png")))
        self.vtkLabel.setFixedSize(200, 200)

        imagebox = QVBoxLayout()

        imageboxlayout = QHBoxLayout()

        imageboxlayout.addLayout(sliderImglayout)
        imageboxlayout.addLayout(sliderImglayout2)

        imagebox2layout = QHBoxLayout()

        imagebox2layout.addLayout(sliderImglayout3)
        imagebox2layout.addWidget(self.vtkLabel)

        imagebox.addLayout(imageboxlayout)
        imagebox.addLayout(imagebox2layout)

        vboxlayout = QHBoxLayout()

        vboxlayout.addLayout(imagebox)
        vboxlayout.addLayout(rightlayout)

        layout = QVBoxLayout()
        # layout.setMenuBar(menubar)
        layout.addLayout(vboxlayout)
        mainWidget.setLayout(layout)

        palette.setColor(QPalette.Window, Qt.white)

        self.window.setCentralWidget(mainWidget)
        self.window.setPalette(palette)

        self.resize(500, 300)

        self.window.show()

    def doSomething(self):
        print('openAction triggered')

    def mouse_down(self, event):
        print(event.x(), event.y())

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
        coronal_pixmap = QPixmap.fromImage(coronal_image)
        coronal_pixmap = coronal_pixmap.scaled(200, 200)  # 缂╂斁鍥惧儚
        # self.coronalLabel.setFixedSize(200, 200)  # 璁剧疆鍥哄畾澶у皬
        self.imageWidget = ImageWidget(self, coronal_image)

        # self.coronalLabel.setPixmap(imageWidget.grab())
        # return coronal_image

    def get_horizontal_image(self, index):
        # 鑾峰彇姘村钩闈㈠浘鍍忔暟鎹� 瑕佹樉绀鸿酱鐘堕潰锛岄渶瑕佸皢鍥惧儚鍦╕杞存柟鍚戜笂鐨勪綅缃彇涓棿鐨勪竴灞�

        if self.axis_order != ('R', 'A', 'S'):
            # np.fliplr() 宸﹀彸缈昏浆 np.rot90()鍥惧儚鏃嬭浆90搴︽垨灏嗗浘鍍忔部姘村钩鎴栧瀭鐩磋酱杩涜缈昏浆
            horizontal_data = np.fliplr(np.rot90(self.data[:, index, :]))

        else:

            horizontal_data = self.data[:, index, :]

        # 灏嗘暟鎹浆鎹负8浣嶆棤绗﹀彿鏁存暟绫诲瀷锛屽苟灏嗗儚绱犲�肩缉鏀惧埌0-255鑼冨洿鍐�
        horizontal_data = np.uint8(
            255 * (horizontal_data - horizontal_data.min()) / (horizontal_data.max() - horizontal_data.min()))

        # 灏嗘暟鎹浆鎹负QImage鏍煎紡
        height, width = horizontal_data.shape
        bytesPerLine = width
        horizontal_image = QImage(horizontal_data.data.tobytes(), width, height, bytesPerLine, QImage.Format_Grayscale8)
        horizontal_pixmap = QPixmap.fromImage(horizontal_image)
        horizontal_pixmap = horizontal_pixmap.scaled(200, 200)  # 缂╂斁鍥惧儚
        self.horizontalLabel.setPixmap(horizontal_pixmap)

    def get_sagittal_image(self, index):
        # 鑾峰彇鐭㈢姸闈㈠浘鍍忔暟鎹� 瑕佹樉绀虹煝鐘堕潰锛岄渶瑕佸皢鍥惧儚鍦╔杞存柟鍚戜笂鐨勪綅缃彇涓棿鐨勪竴灞�

        if self.axis_order != ('R', 'A', 'S'):
            sagittal_data = np.fliplr(np.rot90(self.data[index, :, :]))
        else:
            sagittal_data = self.data[index, :, :]

        # 灏嗘暟鎹浆鎹负8浣嶆棤绗﹀彿鏁存暟绫诲瀷锛屽苟灏嗗儚绱犲�肩缉鏀惧埌0-255鑼冨洿鍐�
        sagittal_data = np.uint8(
            255 * (sagittal_data - sagittal_data.min()) / (sagittal_data.max() - sagittal_data.min()))

        # 灏嗘暟鎹浆鎹负QImage鏍煎紡
        height, width = sagittal_data.shape
        bytesPerLine = width
        sagittal_image = QImage(sagittal_data.data.tobytes(), width, height, bytesPerLine, QImage.Format_Grayscale8)
        sagittal_pixmap = QPixmap.fromImage(sagittal_image)
        sagittal_pixmap = sagittal_pixmap.scaled(200, 200)  # 缂╂斁鍥惧儚
        self.sagittalLabel.setPixmap(sagittal_pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    # app.exec_() 绋嬪簭杩涜寰幆绛夊緟鐘舵��
    sys.exit(app.exec_())
