from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class tBar(QFrame):
    sgPoss=pyqtSignal(int,int)
    sgDClick =pyqtSignal()
    def __init__(self, name):
        super(tBar,self).__init__()
        self.pressing = False

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName("titleFrame")

        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.lbName = QLabel(name)
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lbName.setFont(font)
        self.lbName.setAlignment(Qt.AlignCenter)
        self.lbName.setObjectName("label")

        # self.titleFrame.layout.addWidget(self.lbName)
        self.horizontalLayout.addWidget(self.lbName)
    def mouseDoubleClickEvent(self,event):
        try:
            self.sgDClick.emit()
        except:
            print(sys.exc_info())

    def mousePressEvent(self, event):
        self.stratX = event.globalPos().x()
        self.stratY = event.globalPos().y()

        self.pressing = True

    # #
    def mouseMoveEvent(self, event):
        try:
            if self.pressing:
                if ((event.buttons() == Qt.LeftButton)):
                    self.end = event.globalPos()

                    self.deltaX =(self.end.x()-self.stratX)
                    self.deltaY =(self.end.y()-self.stratY)


                    self.sgPoss.emit(self.deltaX,self.deltaY)

                    self.stratX =self.end.x()
                    self.stratY =self.end.y()
        except:
            print(sys.exc_info())

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = tBar()
    form.show()
    sys.exit(app.exec_())