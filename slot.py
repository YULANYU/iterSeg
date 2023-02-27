import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget


class Example(QWidget):
    # 鍒涘缓涓�涓俊鍙凤紝璇ヤ俊鍙锋病鏈夊弬鏁�
    my_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 鍒涘缓涓�涓寜閽�
        btn = QPushButton('Click me', self)
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        # 灏嗘寜閽殑 clicked 淇″彿杩炴帴鍒拌嚜瀹氫箟妲藉嚱鏁�
        btn.clicked.connect(self.on_click)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Signal and Slot')
        self.show()

    def on_click(self):
        # 鍙戦�佽嚜瀹氫箟淇″彿
        self.my_signal.emit()


class Communicate(QObject):

    # 鍒涘缓涓�涓Ы锛岃妲芥帴鏀� my_signal 鍙戦�佺殑淇″彿
    def my_slot(self):
        print('Signal received')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()

    # 鍒涘缓涓�涓�氫俊瀹炰緥
    comm = Communicate()

    # 灏� Example 瀹炰緥鐨� my_signal 淇″彿杩炴帴鍒� Communicate 瀹炰緥鐨� my_slot 妲藉嚱鏁�
    ex.my_signal.connect(comm.my_slot)

    sys.exit(app.exec_())
