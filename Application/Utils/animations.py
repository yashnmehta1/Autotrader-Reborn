from PyQt5.QtCore import *
import sys
import traceback

def showIndexBar(self):
    if (self.isIndexBarOpen == False):

        self.anim31.setDuration(50)
        self.anim31.setStartValue(0)
        self.anim31.setEndValue(25)
        self.anim31.start()
        self.isIndexBarOpen = True
    else:
        self.anim32.setDuration(50)
        self.anim32.setStartValue(25)
        self.anim32.setEndValue(0)
        self.anim32.start()
        self.isIndexBarOpen = False

    print('a')


def openSideBar(self):
    try:
        if(self.isSidebarOpen==False):
            self.anim = QPropertyAnimation(self.sideBarFrame, b"minimumWidth")
            self.anim.setDuration(200)
            self.anim.setStartValue(0)
            self.anim.setEndValue(250)
            self.anim.start()
            print('a')
            self.isSidebarOpen = True
        else:
            self.anim1 = QPropertyAnimation(self.sideBarFrame, b"minimumWidth")
            self.anim1.setDuration(200)
            self.anim1.setStartValue(250)
            self.anim1.setEndValue(0)
            self.anim1.start()
            self.isSidebarOpen=False

    except:
        print(traceback.print_exc())

def showSplashScreen(self):
    self.Splash.show()
    try:
        self.animSplace = QPropertyAnimation(self.Splash, b"windowOpacity")
        self.animSplace.setDuration(700)
        self.animSplace.setStartValue(0.0)
        self.animSplace.setEndValue(1.0)
        self.animSplace.start()
        self.timeSplash.start()
    except:
        print(sys.exc_info())



def showSTBar(self):
    if (self.isSTBarOpen == False):

        self.anim51.setDuration(50)
        self.anim51.setStartValue(30)
        self.anim51.setEndValue(100)
        self.anim51.start()
        # a=QWidget()
        # a.setMaximumHeight()
        self.widget_2.setMaximumHeight(20)
        self.isSTBarOpen = True
    else:
        self.anim52.setDuration(50)
        self.anim52.setStartValue(100)
        self.anim52.setEndValue(30)
        self.anim52.start()
        self.widget_2.setMaximumHeight(0)

        self.isSTBarOpen = False


def showMargins(self):
    try:
        if (self.isMrgWOpen == False):
            self.anim91.setDuration(50)
            self.anim91.setStartValue(0)
            self.anim91.setEndValue(600)
            self.anim91.start()
            self.isMrgWOpen = True
        else:
            self.anim92.setDuration(50)
            self.anim92.setStartValue(600)
            self.anim92.setEndValue(0)
            self.anim92.start()
            self.isMrgWOpen = False
    except:
        print(traceback.print_exc())


def showM2mW(self):
    try:
        print('showM2mW')
        if (self.isMMWOpen == False):
            self.anim93.setDuration(50)
            self.anim93.setStartValue(0)
            self.anim93.setEndValue(120)
            self.anim93.start()
            self.isMMWOpen = True
        else:
            self.anim94.setDuration(50)
            self.anim94.setStartValue(120)
            self.anim94.setEndValue(0)
            self.anim94.start()
            self.isMMWOpen = False
    except:
        print(traceback.print_exc())


def showSettingMenu(self):
    try:
        if (self.isMenuOpen == False):
            self.anim71.setDuration(50)
            self.anim71.setStartValue(0)
            self.anim71.setEndValue(200)
            self.anim71.start()
            self.isMenuOpen = True
        else:
            self.anim72.setDuration(50)
            self.anim72.setStartValue(200)
            self.anim72.setEndValue(0)
            self.anim72.start()
            self.isMenuOpen = False

    except:
        print(traceback.print_exc())


def showScriptBar(self):
    if (self.isScriptBarOpen == False):

        self.anim41.setDuration(50)
        self.anim41.setStartValue(0)
        self.anim41.setEndValue(30)
        self.anim41.start()
        self.isScriptBarOpen = True
    else:
        self.anim42.setDuration(50)
        self.anim42.setStartValue(25)
        self.anim42.setEndValue(0)
        self.anim42.start()
        self.isScriptBarOpen = False

