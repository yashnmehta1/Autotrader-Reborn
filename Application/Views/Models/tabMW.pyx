import ctypes
import cython
import sys
import traceback
from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QModelIndex
import time
from  numba import *
from PyQt5 import QtGui
from PyQt5.QtGui import QBrush

class ModelPosition(QtCore.QAbstractTableModel):

    def __init__(self,  data,heads):
        super(ModelPosition, self).__init__()

        self._data = data
        self.dta1 = []
        self.color = []
        self.heads=heads
        self.iop = 0

    def data(self, object index,int role):
        cdef int row,col
        cdef double op
        try:
            if role == 0:
                row = index.row()
                col=index.column()
                value = self._data[row, col]

                if(isinstance(value, float)):
                    if(value>999999):
                        return int(value)
                    else:
                        return value
                else:
                    return value

            if role == 7:
                row = index.row()
                col=index.column()
                value = self._data[row, col]
                if isinstance(value, int) or isinstance(value, float):
                    return Qt.AlignVCenter + Qt.AlignRight

            if role == 8:
                row = index.row()
                col=index.column()
                value = self._data[row, col]
                op= self.dta1[index.row()]

                if(col == 7):
                    if(len(self.dta1) != 0):
                        if(value > op):
                            self.color[row] = '#4FB7E0'
                            return QtGui.QColor('#4FB7E0')

                        elif (value < op):
                            self.color[row] = '#c2364b'
                            return QtGui.QColor('#c2364b')
                        else:
                            return QtGui.QColor(self.color[index.row()])

                if(col in [12,14]):
                    return QtGui.QColor(48, 57, 63)
        except:
            print(traceback.print_exc())
            print(sys.exc_info())


    def rowCount(self, index=''):
        # print('id model',id(self._data))
        return self._data.shape[0]

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
            # print('data',self._data,'dta',self.dta1)
            # print(id(self.dta1),id(self._data))

        except:
            print(sys.exc_info())

    def setDta(self,a):
        self._data = a

    def setData(self, index, value, role=Qt.EditRole):

        if role == Qt.DisplayRole:
            if (isinstance(value, float)):
                if (value > 999999):
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
            if (index.column() == 7):
                if (self.dta1.size != 0):
                    print(value, type(value), self.dta1[index.row()], type(self.dta1[index.row()]))

                    if (value > self.dta1[index.row()]):
                        return QtGui.QColor(194, 54, 75)
                    # else:
                    #     return QtGui.QColor('transparent')

            if (index.column() in [12, 14]):
                return QtGui.QColor(48, 57, 63)
