from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import sys
import logging
import traceback
from os import path,getcwd

def clearStatus(self):
    self.lbStatus.setText('')
    self.timerChStatus.stop()


def updateStatusLable(self, a):
    self.lbStatus.setText(a)
    self.timerChStatus.stop()
    self.timerChStatus.setInterval(5000)
    self.timerChStatus.start()




def showBuyWindow(self):
    pass
def showSellWindow(self):
    pass
def ShowPending(self):
    token = self.tableView.selectedIndexes()[0].data()
    self.sgShowPending.emit(str(token))

def changeIAS_connIcon(self,a):
    try:
        if(a==0):
            loc = path.join(self.loc1[0] , 'Resourses','icons','icons','red_icon.png')
            pixmap = QPixmap()
        else:
            loc = path.join(self.loc1[0], 'Resourses', 'icons', 'icons', 'green_icon.png')
            pixmap = QPixmap(loc)
        pixmap = pixmap.scaledToWidth(20)
        pixmap = pixmap.scaledToHeight(20)
        icon = QIcon()
        icon.addPixmap(pixmap)
        self.Interactive_icon.setIcon(icon)
    except:
        print(traceback.print_exc())

def changeMD_connIcon(self,a):
    try:
        if (a == 0):
            pixmap = QPixmap(':/icon1/icons/green_icon.png')
        else:
            pixmap = QPixmap(':/icon1/icons/red_icon.png')
        icon = QIcon()
        icon.addPixmap(pixmap)
        self.MData_icon.setIcon(icon)
        print('f')

    except:
        print(traceback.print_exc())
