import logging
import sys
import traceback
from os import path, getcwd
import threading
import time
import requests
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import qdarkstyle
import qtpy
from Application.Utils.configReader import *
from Theme.dt2 import  dt1


class addW(QWidget):
    def __init__(self):
        super(addW, self).__init__()
        self.setObjectName('addParameter')

        #####################################################################

        loc1 = getcwd().split('Application')

        print(loc1)
        ui_login = os.path.join(loc1[0] ,'Application','Stretegies','TSpecial','UI','inputParameter.ui')
        uic.loadUi(ui_login, self)

        dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
        self.setStyleSheet(dt1)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = addW()
    form.show()
    sys.exit(app.exec_())