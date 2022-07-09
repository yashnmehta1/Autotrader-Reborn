import traceback
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Resourses.icons import icons_rc
from os import path, getcwd
import qdarkstyle
from Theme.dt2 import dt1
from Application.Views.titlebar import tBar



class Ui_Preferences(QMainWindow):

    sgFin=pyqtSignal()
    ################################# Intialization Here ##################################################
    def __init__(self,parent=None):
        super(Ui_Preferences, self).__init__(parent=None)
        try:
            loc1 = getcwd().split('Application')


            ui_login = path.join(loc1[0] , 'Resourses','UI','Preferences.ui')
            uic.loadUi(ui_login, self)

            flags = Qt.WindowFlags(Qt.SubWindow | Qt.FramelessWindowHint )

            self.title = tBar('OrderBook')
            self.headerFrame.layout().addWidget(self.title, 0, 0)

            self.headerFrame.setStyleSheet('  border-radius: 4px;background-color: rgb(80, 80, 80);')
            self.title.sgPoss.connect(self.movWin)
            dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
            self.setStyleSheet(dt1)



            self.setWindowFlags(flags)
            self.setStyleSheet(dt1)
            self.createShortcuts()
            self.connectAllSlots()
            QSizeGrip(self.frameGrip)
        except:
            print(traceback.print_exc())


    def connectAllSlots(self):
        self.bt_close.clicked.connect(self.hide)
        self.bt_min.clicked.connect(self.hide)
    def createShortcuts(self):
        self.quitSc = QShortcut(QKeySequence('Esc'), self)
        self.quitSc.activated.connect(self.hide)


    def movWin(self, x, y):
        self.move(self.pos().x() + x, self.pos().y() + y)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Ui_Preferences()
    form.show()
    # form.show()
    sys.exit(app.exec_())