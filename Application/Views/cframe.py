import traceback
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from Resourses.icons import icons_rc
from os import path, getcwd
import qdarkstyle
from Theme.dt2 import dt1


class Ui_CFrame(QMainWindow):

    sgFin=pyqtSignal()
    ################################# Intialization Here ##################################################
    def __init__(self):
        super(Ui_CFrame, self).__init__()

        loc1 = getcwd().split('Application')
        # logDir = loc1[0] + '\\Logs\\%s'%today

        ui_login =path.join( loc1[0] , 'Resourses','UI','cframe.ui')
        uic.loadUi(ui_login, self)
        flags = Qt.WindowFlags(Qt.FramelessWindowHint)

        # self.tabifyDockWidget(self.dockPB, self.dockOP)
        self.tabifyDockWidget(self.dockOP, self.dockMGR)
        # print( dir(self.dockPB))
        # self.tabifyDockWidget(self.dockWidget, self.dockWidget_5)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Ui_CFrame()
    form.show()
    sys.exit(app.exec_())