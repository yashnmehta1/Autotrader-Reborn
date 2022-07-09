import ctypes
import sys
import traceback
from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QModelIndex
import time
from  numba import *
from PyQt5 import QtGui
from PyQt5.QtGui import QBrush
import numpy as np
class ModelPosition(QtCore.QAbstractTableModel):

    def __init__(self, data,heads):
        super(ModelPosition, self).__init__()
        self._data = data
        # print('in Model Position',data)
        self.dta1 = []

        self.color = []
        self.heads=heads
        self.iop = 0

        self.lastSerialNo =0

    def data(self, index, role):
        try:
            if role == Qt.DisplayRole:

                value = self._data[index.row(), index.column()]

                if(isinstance(value, float)):
                    if(value>999999):
                        return int(value)
                    else:
                        return value
                else:
                    return value

            if role == Qt.TextAlignmentRole:
                value = self._data[index.row(), index.column()]

                if isinstance(value, int) or isinstance(value, float):
                    # Align right, vertical middle.
                    return Qt.AlignVCenter + Qt.AlignRight


            if role == Qt.BackgroundColorRole:
                # print(role)
                value = self._data[index.row(), index.column()]
                if(index.column() in [7,8,9]):
                    if(len(self.dta1) != 0):
                        # print(value,type(value), self.dta1[index.row()], type(self.dta1[index.row()]))


                        if(value > self.dta1[index.row()][index.column()-7]):
                            self.color[index.row()][index.column()-7] = '#4FB7E0'
                            return QtGui.QColor('#4FB7E0')

                        elif (value < self.dta1[index.row()][index.column()-7]):
                            self.color[index.row()][index.column()-7] = '#c2364b'

                            return QtGui.QColor('#c2364b')
                        else:
                            return QtGui.QColor(self.color[index.row()][index.column()-7])

                # if(index.column() in [13,15]):
                #     return QtGui.QColor(48, 57, 63)



        except:
            print(self.color,traceback.print_exc(),index.column(),index.row())
            print(sys.exc_info())
            pass



    def rowCount(self, index=''):
        return self.lastSerialNo

    def columnCount(self, index=''):
        return len(self.heads)



    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:

            if orientation == Qt.Horizontal:
                return str(self.heads[section])

    def insertRows(self, position=0, rows=1, index=QModelIndex()):
        try:
            self.beginInsertRows(QModelIndex(), position, position + rows - 1)
            self.endInsertRows()
            return True
        except:
            print(traceback.print_exc())

    def setDta1(self):
        try:
            self.dta1 = self._data[:,7].tolist()

        except:
            print(sys.exc_info())

    def setDta(self,a):
        # pass
        self._data = a

