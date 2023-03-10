import sys

import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import nibabel as nib
import math

# 水平面
class HorizontalWidget(QWidget):
    # 创建一个信号，该信号没有参数
    horizontal_signal = pyqtSignal(int)
    # 水平面-矢状面的鼠标点击的y值
    horizontal_click_signal_sagittal = pyqtSignal(int)
    # 水平面-冠状面的鼠标点击的x值
    horizontal_click_signal_coronal = pyqtSignal(int)
    # 更新自己slice index 的展示
    horizontal_signal_horizontalLabel = pyqtSignal(int)

    def __init__(self, parent=None, img=None, index=None):
        super().__init__()
        # 获取图像数据和头文件信息
        self.axis_order = None
        self.data = None
        self.max_index = None
        self.index = index
        self.img = img
        self.hCenter = self.width() / 2
        self.vCenter = self.width() / 2
        self.flag = 0
        self.setMouseTracking(True)
        self.setFixedSize(300, 300)
        self.setParent(parent)

    def paintEvent(self, event):
        if self.flag == 0:
            self.hCenter = self.width() / 2
            self.vCenter = self.height() / 2
            self.flag = 1
       # print("paintEvent called")
        painter = QPainter(self)
        self.data = self.img.get_fdata()
        # print(self.data.shape)
        self.max_index = self.data.shape[2] - 1

        # 获取坐标轴编码
        self.axis_order = nib.aff2axcodes(self.img.affine)
        if self.axis_order != ('R', 'A', 'S'):
            horizontal_data = np.rot90(self.data[:, :, self.index])
        else:
            horizontal_data = self.data[:, :, self.index]
        # 将数据转换为8位无符号整数类型，并将像素值缩放到0-255范围内
        horizontal_data = np.uint8(255 * (horizontal_data - horizontal_data.min()) / (horizontal_data.max() - horizontal_data.min()))

        # 将数据转换为QImage格式
        height, width = horizontal_data.shape
        bytesPerLine = width
        horizontal_image = QImage(horizontal_data.data.tobytes(), width, height, bytesPerLine, QImage.Format_Grayscale8)
        painter.drawImage(self.rect(), horizontal_image)

        # DashLine虚线   SolidLine实线
        pen = QPen(Qt.blue, 1, Qt.DashLine)
        painter.setPen(pen)
        # 接受四个整型参数，分别代表直线的起点和终点的 x、y 坐标
        # 绘制垂直线
        painter.drawLine(self.hCenter, 0, self.hCenter, self.height())
        # 绘制水平线
        painter.drawLine(0, self.vCenter, self.width(), self.vCenter)

    def wheelEvent(self, event: QWheelEvent) -> None:
        # print("wheelEvent called")
        angle = event.angleDelta().y()
        if angle > 0:
            print("向上滚动")
            if self.index > 0:
                self.index = self.index - 1
        elif angle < 0:
            print("向下滚动")
            if self.index < self.max_index:
                self.index = self.index + 1
        self.update()
        # print(event.pos().x())
        # print(event.pos().y())
        self.horizontal_signal.emit(angle)


        self.horizontal_signal_horizontalLabel.emit(self.index)

    def mousePressEvent(self, event):

        self.hCenter = event.pos().x()
        self.vCenter = event.pos().y()


        view_size = self.size().width()
        image_size_height = self.data.shape[1]
        img_size_width = self.data.shape[0]
        slice_pos_x = int((self.hCenter / view_size) * image_size_height)
        print("slice_pos_x",slice_pos_x)

        slice_pos_y = int(((self.vCenter) / view_size) * img_size_width)
        slice_pos_y = img_size_width - slice_pos_y
        print("slice_pos_y", slice_pos_y)




        self.update()
        self.horizontal_click_signal_sagittal.emit(slice_pos_x)
        self.horizontal_click_signal_coronal.emit(slice_pos_y)

    def resizeEvent(self, event):
        self.update()


# 矢状面
class SagittalWidget(QWidget):
    sagittal_signal_sagittalLabel = pyqtSignal(int)

    def __init__(self, parent=None, img=None, index=None):
        super().__init__()
        # 获取图像数据和头文件信息
        self.scale = None
        self.axis_order = None
        self.data = None
        self.max_index = None
        self.index = index
        self.img = img
        self.hCenter = self.width() / 2
        self.vCenter = self.width() / 2
        self.flag = 0

        # scaleFactor属性用于存储当前图像的缩放比例，默认值为 1.0 表示不缩放
        self.scaleFactor = 1.0
        self.setMouseTracking(True)
        self.setFixedSize(300, 300)
        self.setParent(parent)

    def paintEvent(self, event):
        if self.flag == 0:
            self.hCenter = self.width() / 2
            self.vCenter = self.height() / 2
            self.flag = 1
        # print("paintEvent called")
        painter = QPainter(self)
        self.data = self.img.get_fdata()
        # print(self.data.shape)
        self.max_index = self.data.shape[0] - 1
        x = self.data.shape[0]
        # 鼠标点击的位置/scale = 计算切片位置
        self.scale = 300 / x
        # 获取坐标轴编码
        self.axis_order = nib.aff2axcodes(self.img.affine)
        # 获取矢状面图像数据 要显示矢状面，需要将图像在X轴方向上的位置取中间的一层
        if self.axis_order != ('R', 'A', 'S'):
            sagittal_data = np.fliplr(np.rot90(self.data[self.index, :, :]))
        else:
            sagittal_data = self.data[self.index, :, :]

        # 将数据转换为8位无符号整数类型，并将像素值缩放到0-255范围内
        sagittal_data = np.uint8(
            255 * (sagittal_data - sagittal_data.min()) / (sagittal_data.max() - sagittal_data.min()))

        # 将数据转换为QImage格式
        height, width = sagittal_data.shape
        bytesPerLine = width
        sagittal_image = QImage(sagittal_data.data.tobytes(), width, height, bytesPerLine, QImage.Format_Grayscale8)
        painter.drawImage(self.rect(), sagittal_image)

        # DashLine虚线   SolidLine实线
        pen = QPen(Qt.blue, 1, Qt.DashLine)
        painter.setPen(pen)
        # 接受四个整型参数，分别代表直线的起点和终点的 x、y 坐标
        # 绘制垂直线
        painter.drawLine(self.hCenter, 0, self.hCenter, self.height())
        # 绘制水平线
        painter.drawLine(0, self.vCenter, self.width(), self.vCenter)

    def wheelEvent(self, event: QWheelEvent) -> None:

        angle = event.angleDelta().y()
        if angle > 0:
            print("向上滚动")
            if self.index > 0:
                self.index = self.index - 1
        elif angle < 0:
            print("向下滚动")
            if self.index < self.max_index:
                self.index = self.index + 1
        self.update()
        self.sagittal_signal_sagittalLabel.emit(self.index)

    def mousePressEvent(self, event):
        #print("mouseMoveEvent called")
        self.hCenter = event.pos().x()
        self.vCenter = event.pos().y()

        print(self.vCenter)
        print(self.hCenter)
        self.update()

    def resizeEvent(self, event):

        self.update()

    @pyqtSlot(int)
    def sagittal_slot(self, angle):
        if angle > 0:
            print("向上滚动")
            if self.vCenter <= self.height() - 1:
                self.vCenter = self.vCenter + 1
        elif angle < 0:
            print("向下滚动")
            if self.vCenter > 0:
                self.vCenter = self.vCenter - 1

        print(self.vCenter)
        self.update()

    @pyqtSlot(int)
    def sagittal_click_slot(self, slice_pos_x):

        print(slice_pos_x)
        self.index = slice_pos_x
        print(self.index)
        self.update()


# 冠状面
class CoronalWidget(QWidget):
    coronal_signal_coronalLabel = pyqtSignal(int)

    def __init__(self, parent=None, img=None, index=None):
        super().__init__()
        # 获取图像数据和头文件信息
        self.scale = None
        self.axis_order = None
        self.data = None
        self.max_index = None
        self.index = index
        self.img = img
        self.hCenter = self.width() / 2
        self.vCenter = self.width() / 2
        self.flag = 0

        # scaleFactor属性用于存储当前图像的缩放比例，默认值为 1.0 表示不缩放
        self.scaleFactor = 1.0
        self.setMouseTracking(True)
        self.setFixedSize(300, 300)
        self.setParent(parent)

    def paintEvent(self, event):
        if self.flag == 0:
            self.hCenter = self.width() / 2
            self.vCenter = self.height() / 2
            self.flag = 1
        # print("paintEvent called")
        painter = QPainter(self)
        self.data = self.img.get_fdata()
        # (512, 512, 304)
        print(self.data.shape)
        self.max_index = self.data.shape[1] - 1
        self.scale = self.width() / self.data.shape[2]  # 300 / 512
        # 获取坐标轴编码
        self.axis_order = nib.aff2axcodes(self.img.affine)
        if self.axis_order != ('R', 'A', 'S'):
            # np.fliplr() 左右翻转 np.rot90()图像旋转90度或将图像沿水平或垂直轴进行翻转
            coronal_data = np.fliplr(np.rot90(self.data[:, self.index, :]))

        else:

            coronal_data = self.data[:, self.index, :]

            # 将数据转换为8位无符号整数类型，并将像素值缩放到0-255范围内
        horizontal_data = np.uint8(
            255 * (coronal_data - coronal_data.min()) / (coronal_data.max() - coronal_data.min()))

        # 将数据转换为QImage格式
        height, width = horizontal_data.shape
        bytesPerLine = width
        coronal_image = QImage(horizontal_data.data.tobytes(), width, height, bytesPerLine, QImage.Format_Grayscale8)

        painter.drawImage(self.rect(), coronal_image)

        # DashLine虚线   SolidLine实线
        pen = QPen(Qt.blue, 1, Qt.DashLine)
        painter.setPen(pen)
        # 接受四个整型参数，分别代表直线的起点和终点的 x、y 坐标
        # 绘制垂直线
        painter.drawLine(self.hCenter, 0, self.hCenter, self.height())
        # 绘制水平线
        painter.drawLine(0, self.vCenter, self.width(), self.vCenter)

    def wheelEvent(self, event: QWheelEvent) -> None:
        print("wheelEvent called")
        angle = event.angleDelta().y()
        if angle > 0:
            print("向上滚动")
            if self.index > 0:
                self.index = self.index - 1
        elif angle < 0:
            print("向下滚动")
            if self.index <= self.max_index - 1:
                self.index = self.index + 1
        self.update()
        print('fmax', self.max_index)
        self.coronal_signal_coronalLabel.emit(self.index)

    def mousePressEvent(self, event):
        print("mouseMoveEvent called")
        self.hCenter = event.pos().x()
        self.vCenter = event.pos().y()
        self.update()

    def resizeEvent(self, event):

        self.update()

    @pyqtSlot(int)
    def coronal_slot(self, angle):
        print('Signal received')
        if angle > 0:
            print("向上滚动")
            if self.vCenter <= self.height() - 1:
                self.vCenter = self.vCenter + 1
        elif angle < 0:
            print("向下滚动")
            if self.vCenter > 0:
                self.vCenter = self.vCenter - 1

        print(self.vCenter)
        self.update()

    @pyqtSlot(int)
    def coronal_click_slot(self, slice_pos_y):
        print('Click Signal received')
        print(slice_pos_y)
        self.index = slice_pos_y
        print(self.index)
        self.update()


# 水平面切片label
class HorizontalLabelWidget(QLabel):
    def __init__(self, current_index=None, max_z_index=None):
        super().__init__()

        self.current_index = current_index + 1
        self.max_z_index = max_z_index
        self.text = str(self.current_index) + ' of ' + str(self.max_z_index)
        self.setText(self.text)
        # 右对齐
        self.setAlignment(Qt.AlignRight)
        font = QFont('SimHei', 10)
        self.setFont(font)

    @pyqtSlot(int)
    def update_label_slot(self, index):
        self.current_index = index + 1
        self.text = str(self.current_index) + ' of ' + str(self.max_z_index)
        self.setText(self.text)


# 矢状面切片label
class SagittalLabelWidget(QLabel):
    def __init__(self, current_index=None, max_x_index=None):
        super().__init__()

        self.current_index = current_index + 1
        self.max_x_index = max_x_index
        self.scale = 300 / self.max_x_index
        self.text = str(self.current_index) + ' of ' + str(self.max_x_index)
        self.setText(self.text)
        # 右对齐
        self.setAlignment(Qt.AlignRight)
        font = QFont('SimHei', 10)
        self.setFont(font)

    @pyqtSlot(int)
    def update_label_slot(self, index):
        self.current_index = index + 1

        self.text = str(self.current_index) + ' of ' + str(self.max_x_index)
        self.setText(self.text)


# 冠状面切片label
class CoronalLabelWidget(QLabel):
    def __init__(self, current_index=None, max_y_index=None):
        super().__init__()

        self.current_index = current_index + 1
        self.max_y_index = max_y_index
        self.scale = 300 / self.max_y_index
        self.text = str(self.current_index) + ' of ' + str(self.max_y_index)
        self.setText(self.text)
        # 右对齐
        self.setAlignment(Qt.AlignRight)
        font = QFont('SimHei', 10)
        self.setFont(font)

    @pyqtSlot(int)
    def update_label_slot(self, index):
        self.current_index = index + 1
        self.text = str(self.current_index) + ' of ' + str(self.max_y_index)
        self.setText(self.text)


class MainWindow(QWidget):
    def __init__(self):
        # 切记一定要调用父类的init方法，因为它里面有很多对UI控件的初始化操作
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
        # 加入一个分割线的方法
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

        # QHBoxLayout：水平布局
        # QVBoxLayout：垂直布局
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
        # 字体大小
        tipsFont.setPointSize(10)

        StateLine.setFixedHeight(30)
        # setWordWrap是PyQt5中QLabel组件的一个方法，用于设置文本是否自动换行
        StateLine.setWordWrap(True)
        StateLine.setFont(tipsFont)
        MethodLine.setFixedHeight(30)
        MethodLine.setWordWrap(True)
        MethodLine.setFont(tipsFont)
        SaveLine.setFixedHeight(30)
        SaveLine.setWordWrap(True)
        SaveLine.setFont(tipsFont)

        # 读取nii格式图像
        img = nib.load('lung_001.nii.gz')
        self.data = img.get_fdata()
        self.header = img.header
        nii_affine = img.affine
        self.axis_order = nib.aff2axcodes(nii_affine)
        # 1.水平面切片滑块
        self.horizontalSlider = QSlider(Qt.Horizontal, self)
        self.horizontalSlider.setMinimum(0)
        z = self.header.get_data_shape()[2]
        self.horizontalSlider.setMaximum(z - 1)
        self.horizontalSlider.valueChanged.connect(self.get_coronal_image)
        # 2.水平面
        self.horizontalWidget = HorizontalWidget(self, img, z // 2)

        # 3.水平面切片数展示
        self.horizontalLabel = HorizontalLabelWidget(z // 2, z)

        sliderImglayout = QVBoxLayout()
        sliderImglayout.addWidget(self.horizontalSlider)
        sliderImglayout.addWidget(self.horizontalWidget)
        sliderImglayout.addWidget(self.horizontalLabel)

        # 矢状面滑块
        self.sagittalSlider = QSlider(Qt.Horizontal, self)
        self.sagittalSlider.setMinimum(0)
        x = self.header.get_data_shape()[0]

        self.sagittalSlider.setMaximum(z - 1)
        self.sagittalSlider.valueChanged.connect(self.get_horizontal_image)

        # 矢状面
        self.sagittalWidget = SagittalWidget(self, img, x // 2)

        # 矢状面切片数展示
        self.sagittalLabel = SagittalLabelWidget(x // 2, x)

        sliderImglayout2 = QVBoxLayout()
        sliderImglayout2.addWidget(self.sagittalSlider)
        sliderImglayout2.addWidget(self.sagittalWidget)
        sliderImglayout2.addWidget(self.sagittalLabel)

        # 3.冠状面滑块
        self.coronalSlider = QSlider(Qt.Horizontal, self)
        self.coronalSlider.setMinimum(0)

        self.coronalSlider.setMaximum(z - 1)
        self.coronalSlider.valueChanged.connect(self.get_sagittal_image)
        y = self.header.get_data_shape()[1]
        # 3.冠状面
        self.coronalWidget = CoronalWidget(self, img, y // 2)
        # 矢状面切片数展示
        self.coronalLabel = CoronalLabelWidget(y // 2, y)
        sliderImglayout3 = QVBoxLayout()
        sliderImglayout3.addWidget(self.coronalSlider)
        sliderImglayout3.addWidget(self.coronalWidget)
        sliderImglayout3.addWidget(self.coronalLabel)

        # 水平面发信号 - 槽  水平面滚轮滑动
        self.horizontalWidget.horizontal_signal.connect(self.sagittalWidget.sagittal_slot)
        self.horizontalWidget.horizontal_signal.connect(self.coronalWidget.coronal_slot)
        # 水平面发信号 - 槽  水平面点击 其他面切换切面
        self.horizontalWidget.horizontal_click_signal_sagittal.connect(self.sagittalWidget.sagittal_click_slot)
        self.horizontalWidget.horizontal_click_signal_coronal.connect(self.coronalWidget.coronal_click_slot)

        # 水平面发信号 - 槽  水平面滚轮滑动 自己的切片展示
        self.horizontalWidget.horizontal_signal_horizontalLabel.connect(self.horizontalLabel.update_label_slot)

        # 水平面发信号 - 槽  水平面点击 其他面切换的label展示

        self.horizontalWidget.horizontal_click_signal_sagittal.connect(self.sagittalLabel.update_label_slot)
        self.horizontalWidget.horizontal_click_signal_coronal.connect(self.coronalLabel.update_label_slot)

        # 矢状面发信号 - 槽
        self.sagittalWidget.sagittal_signal_sagittalLabel.connect(self.sagittalLabel.update_label_slot)
        self.horizontalWidget.horizontal_click_signal_sagittal.connect(self.sagittalLabel.update_label_slot)
        # 冠状面发信号 - 槽
        self.coronalWidget.coronal_signal_coronalLabel.connect(self.coronalLabel.update_label_slot)

        self.vtkLabel = QLabel()
        # vtk_image = self.get_sagittal_image(data, header)
        self.vtkLabel.setPixmap(QPixmap.fromImage(QImage("logo.png")))
        self.vtkLabel.setFixedSize(300, 300)

        imagebox = QVBoxLayout()

        imageboxlayout = QHBoxLayout()

        imageboxlayout.addLayout(sliderImglayout)
        imageboxlayout.addLayout(sliderImglayout2)

        imagebox2layout = QHBoxLayout()

        imagebox2layout.addWidget(self.vtkLabel)
        imagebox2layout.addLayout(sliderImglayout3)

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

        self.resize(800, 600)

        self.window.show()

    def doSomething(self):
        print('openAction triggered')

    def mouse_down(self, event):
        print(event.x(), event.y())

    def get_coronal_image(self, index):
        print(index)
        # 获取冠状面图像数据 显示冠状面时，需要将图像在Z轴方向上的位置取中间的一层
        z = self.header.get_data_shape()[2]
        if self.axis_order != ('R', 'A', 'S'):
            coronal_data = np.rot90(self.data[:, :, index])
        else:
            coronal_data = self.data[:, :, index]
        # 将数据转换为8位无符号整数类型，并将像素值缩放到0-255范围内
        coronal_data = np.uint8(255 * (coronal_data - coronal_data.min()) / (coronal_data.max() - coronal_data.min()))

        # 将数据转换为QImage格式
        height, width = coronal_data.shape
        bytesPerLine = width
        coronal_image = QImage(coronal_data.data.tobytes(), width, height, bytesPerLine, QImage.Format_Grayscale8)
        coronal_pixmap = QPixmap.fromImage(coronal_image)
        coronal_pixmap = coronal_pixmap.scaled(200, 200)  # 缩放图像
        # self.coronalLabel.setFixedSize(200, 200)  # 设置固定大小

    # self.imageWidget = ImageWidget(self, coronal_image)

    # self.coronalLabel.setPixmap(imageWidget.grab())
    # return coronal_image

    def get_horizontal_image(self, index):
        # 获取水平面图像数据 要显示轴状面，需要将图像在Y轴方向上的位置取中间的一层

        if self.axis_order != ('R', 'A', 'S'):
            # np.fliplr() 左右翻转 np.rot90()图像旋转90度或将图像沿水平或垂直轴进行翻转
            horizontal_data = np.fliplr(np.rot90(self.data[:, index, :]))

        else:

            horizontal_data = self.data[:, index, :]

        # 将数据转换为8位无符号整数类型，并将像素值缩放到0-255范围内
        horizontal_data = np.uint8(
            255 * (horizontal_data - horizontal_data.min()) / (horizontal_data.max() - horizontal_data.min()))

        # 将数据转换为QImage格式
        height, width = horizontal_data.shape
        bytesPerLine = width
        horizontal_image = QImage(horizontal_data.data.tobytes(), width, height, bytesPerLine, QImage.Format_Grayscale8)
        horizontal_pixmap = QPixmap.fromImage(horizontal_image)
        horizontal_pixmap = horizontal_pixmap.scaled(200, 200)  # 缩放图像
        self.horizontalLabel.setPixmap(horizontal_pixmap)

    def get_sagittal_image(self, index):
        # 获取矢状面图像数据 要显示矢状面，需要将图像在X轴方向上的位置取中间的一层
        if self.axis_order != ('R', 'A', 'S'):
            sagittal_data = np.fliplr(np.rot90(self.data[index, :, :]))
        else:
            sagittal_data = self.data[index, :, :]

        # 将数据转换为8位无符号整数类型，并将像素值缩放到0-255范围内
        sagittal_data = np.uint8(
            255 * (sagittal_data - sagittal_data.min()) / (sagittal_data.max() - sagittal_data.min()))

        # 将数据转换为QImage格式
        height, width = sagittal_data.shape
        bytesPerLine = width
        sagittal_image = QImage(sagittal_data.data.tobytes(), width, height, bytesPerLine, QImage.Format_Grayscale8)
        sagittal_pixmap = QPixmap.fromImage(sagittal_image)
        sagittal_pixmap = sagittal_pixmap.scaled(200, 200)  # 缩放图像
        self.sagittalLabel.setPixmap(sagittal_pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    # app.exec_() 程序进行循环等待状态
    sys.exit(app.exec_())
