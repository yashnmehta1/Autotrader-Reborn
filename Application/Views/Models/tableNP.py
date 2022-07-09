import sys
import traceback
from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QModelIndex
import time
from  numba import *
from PyQt5 import QtGui
from PyQt5.QtGui import QBrush

class ModelPosition(QtCore.QAbstractTableModel):

    def __init__(self, data,heads):
        super(ModelPosition, self).__init__()
        self._data = data
        # self._data1 = data
        self.heads=heads
        self.lastSerialNo = 0




    def data(self, index, role):
        try:
            rown = index.row()
            coln =index.column()
            value = self._data[rown, coln]
            if role == Qt.DisplayRole:

                if(isinstance(value, float)):
                    if(value>999999):
                        return int(value)
                    else:
                        return value
                else:
                    return value



            if role == Qt.TextAlignmentRole:
                value = self._data[index.row(), index.column()]
                if coln > 6 :
                    return Qt.AlignVCenter + Qt.AlignRight
        except:
            print(traceback.print_exc())
            print(sys.exc_info())


    def rowCount(self, index=''):
        return self.lastSerialNo

    def columnCount(self, index):
            return len(self.heads)



    def headerData(self, section, orientation, role):
        # section is the index of the column/row.

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                # print(self._data.names[section])
                return str(self.heads[section])

            # if orientation == Qt.Vertical:
            #     return str(self._data.names[section])



    def insertRows(self, position=0, rows=1, index=QModelIndex()):
        # print("\n\t\t ...insertRows() Starting position: '%s'" % position, 'with the total rows to be inserted: ', rows)

        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        self.endInsertRows()
        return True



    def setDta(self,a):
        self._data = a