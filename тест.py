import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.w, self.h = 230, 65
        self.delta_x, self.delta_y = 0, 20

        self.resize(QSize(self.w, self.h))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.label = QtWidgets.QLabel(
            'Родительское окно',
            self,
            alignment=QtCore.Qt.AlignCenter
        )
        self.label.setStyleSheet("background-color: rgb(165, 65, 65);")
        layout = QtWidgets.QVBoxLayout(self.centralWidget)
        layout.addWidget(self.label, 1)

        self.main_widget = QWidget()  # <---- !!!
        self.main_widget.resize(220, 180)
        self.stack = QtWidgets.QStackedLayout()  # <---- !!!
        self.btn = QPushButton("Change window")
        self.btn.clicked.connect(self.change_window)
        layout = QVBoxLayout(self.main_widget)
        layout.addLayout(self.stack)
        layout.addWidget(self.btn)

        QtCore.QTimer.singleShot(10, self.pos_main)
        self.num = 1

    def pos_main(self):
        self.main_widget.move(
            self.pos() + QPoint(self.delta_x, self.h + self.delta_y)
        )

    def change_window(self):
        currentIndex = self.stack.currentIndex()
        stackCount = self.stack.count()
        if currentIndex == stackCount - 1:
            currentIndex = 0
        else:
            currentIndex += 1
        self.stack.setCurrentIndex(currentIndex)

    # +++ vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        if event.buttons() == Qt.RightButton:
            stack1 = QtWidgets.QWidget()
            widget = self.window1UI(stack1)
            self.stack.addWidget(widget)
            self.stack.setCurrentIndex(self.stack.count() - 1)
            self.main_widget.show()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
            self.main_widget.move(self.main_widget.pos() + delta)

    # +++ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def window1UI(self, stack1):
        stack1.move(self.pos() + QPoint(self.delta_x, self.h + self.delta_y))
        label = QLabel(
            f"In Window <span style='color: red;'>{self.num}</span>",
            stack1
        )
        self.num += 1
        return stack1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
    ex = Main()
    ex.show()
    sys.exit(app.exec_())