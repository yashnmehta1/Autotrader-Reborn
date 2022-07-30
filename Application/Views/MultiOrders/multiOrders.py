from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from os import path, getcwd
import numpy as np
from Application.Services.Xts.Api.servicesIA import modifyOrder
import qdarkstyle
from Theme.dt2 import dt1
import traceback
# from Resourses.icons import icons_rc
import platform
import datatable as dt

class Ui_MultiOrders(QWidget):

    sgFin=pyqtSignal()
    ################################# Intialization Here ##################################################
    def __init__(self):
        super(Ui_MultiOrders, self).__init__()

        loc1 = getcwd().split('Application')
        # logDir = loc1[0] + '\\Logs\\%s'%today

        ui_login = path.join(loc1[0], 'Resourses','UI','multiOrder.ui')
        uic.loadUi(ui_login, self)
        osType = platform.system()
        if (osType == 'Darwin'):
            flags = Qt.WindowFlags(Qt.FramelessWindowHint )
        else:
            flags = Qt.WindowFlags(Qt.SubWindow | Qt.FramelessWindowHint)

        self.setWindowFlags(flags)
        dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
        self.setStyleSheet(dt1)
        QSizeGrip(self.sGripFrame)
        self.createShortcuts()

    def createShortcuts(self):
        self.quitSc = QShortcut(QKeySequence('Esc'), self)
        self.quitSc.activated.connect(self.hide)


    def hideWindow(self):
        self.hide()



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Ui_MultiOrders()
    form.show()
    sys.exit(app.exec_())
