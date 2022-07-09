from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from os import path, getcwd
import qdarkstyle
from Theme.dt2 import dt1
import traceback
# from Resourses.icons import icons_rc
import platform

class Ui_Splash(QWidget):

    sgFin=pyqtSignal()
    ################################# Intialization Here ##################################################
    def __init__(self):
        super(Ui_Splash, self).__init__()

        loc1 = getcwd().split('Application')
        # logDir = loc1[0] + '\\Logs\\%s'%today

        ui_login = path.join(loc1[0], 'Resourses','UI','splash.ui')
        uic.loadUi(ui_login, self)
        osType = platform.system()
        if (osType == 'Darwin'):
            flags = Qt.WindowFlags(Qt.FramelessWindowHint )
        else:
            flags = Qt.WindowFlags(Qt.SubWindow | Qt.FramelessWindowHint)

        self.setWindowFlags(flags)


        bgImg = path.join(loc1[0], 'Resourses','icons','icons','123.png')

        #  Resourses\icons\icons
        # self.pixmap = QPixmap('../Resourses/IMG/Untitled2.png')
        self.pixmap = QPixmap(bgImg)
        self.label.setPixmap(self.pixmap)





if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Ui_Splash()
    form.show()
    # form.show()
    sys.exit(app.exec_())