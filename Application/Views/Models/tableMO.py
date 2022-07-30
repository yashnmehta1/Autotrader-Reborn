import sys
import traceback
from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QModelIndex
import time
from  numba import *
from PyQt5 import QtGui
from PyQt5.QtGui import QBrush

class ModelMO(QtCore.QAbstractTableModel):

    def __init__(self, data,heads,isReset=True):
        super(ModelMO, self).__init__()
        self._data = data
        # self._data1 = data
        self.heads=heads

    def data(self, index, role):
        try:
            value = self._data[index.row(), index.column()]
            if role == Qt.DisplayRole:
                return str(value)
            if role == Qt.TextAlignmentRole:
                value = self._data[index.row(), index.column()]
                if isinstance(value, int) or isinstance(value, float):
                    # Align right, vertical middle.
                    return Qt.AlignVCenter + Qt.AlignRight

        except:
            print(traceback.print_exc())
    def rowCount(self, index=''):
        return self._data.shape[0]



    def columnCount(self, index):
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
            print(sys.exc_info())

    def DelRows(self, position=0, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), 0, 0)
        self.endRemoveRows()
        return  True