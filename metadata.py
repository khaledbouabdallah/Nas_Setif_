from PyQt5.QtCore import QPropertyAnimation,Qt,QTimer
from PyQt5.QtGui import QPainter, QPixmap,QMovie
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QHBoxLayout, QVBoxLayout
import sys
from PyQt5.uic.properties import QtCore
from PyQt5 import QtCore, QtGui, QtWidgets



class loading_screen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200,200)
        self.setWindowFlag(Qt.WindowStaysOnTopHint,Qt.CustomizeWindowHint)

        self.label_animation = QLabel(self)

        self.movie =QMovie('loading.gif')
        self.label_animation.setMovie(self.movie)
        timer = QTimer(self)
        self.start_animation()
        timer.singleShot(3000,self.stop_animation)


    def start_animation(self):
        print('hello')
        self.movie.start()

    def stop_animation(self):
        print('bey')
        self.movie.stop()
        self.close()



class starting_screen(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setFixedSize(400,400)
        self.loading_screen = loading_screen()
        layout = QVBoxLayout()
        layout.addWidget(self.loading_screen)
        self.setLayout(layout)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = starting_screen()
    widget.show()
    app.exit(app.exec_())






class starting_screen_ui(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(450, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(450, 450))
        Form.setMaximumSize(QtCore.QSize(450, 450))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.search_file_button = QtWidgets.QPushButton(self.frame)
        self.search_file_button.setGeometry(QtCore.QRect(150, 60, 141, 61))
        self.search_file_button.setStyleSheet("background-color: #2ecc71;\n"
        "border-style: outset;\n"
        "border-radius: 15px;\n"
        "border-color: black;\n"
        "padding: 4px;\n"
        "color:white;\n"
        "\n"
        "\n"
        "\n"
        "")
        self.search_file_button.setCheckable(False)
        self.search_file_button.setAutoRepeat(False)
        self.search_file_button.setFlat(False)
        self.search_file_button.setObjectName("search_file_button")
        self.loading_widget = QtWidgets.QWidget(self.frame)
        self.loading_widget.setGeometry(QtCore.QRect(120, 140, 200, 200))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loading_widget.sizePolicy().hasHeightForWidth())
        self.loading_widget.setSizePolicy(sizePolicy)
        self.loading_widget.setMinimumSize(QtCore.QSize(200, 200))
        self.loading_widget.setMaximumSize(QtCore.QSize(200, 200))
        self.loading_widget.setObjectName("loading_widget")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(170, 350, 101, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.search_file_button.setText(_translate("Form", "اختر ملف"))
        self.label.setText(_translate("Form", "جاري التحميل"))



