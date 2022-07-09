from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QModelIndex
from PyQt5 import QtGui
from PyQt5.QtGui import QBrush,QColor
import sys
import decimal

class ModelTB(QtCore.QAbstractTableModel):

    def __init__(self, data,heads):
        super(ModelTB, self).__init__()
        # self.rwc = 5
        self._data = data
        self.heads=heads
        self.lastSerialNo =0

    def data(self, index, role):
        value = self._data[index.row(), index.column()]
        if role == Qt.DisplayRole:
            if isinstance(value, int):
                value = int(value)
            elif isinstance(value, float):
                value = '%.2f'%value
            return str(value)



    def rowCount(self, index=''):
        # print('in rowCount',self.rwc)
        return self.lastSerialNo

    def columnCount(self, index):
        return len(self.heads)

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:

                return str(self.heads[section])

    def insertRows(self, position=0, rows=1, index=QModelIndex()):
        # print("\n\t\t ...insertRows() Starting position: '%s'" % position, 'with the total rows to be inserted: ', rows)

        try:
            self.beginInsertRows(QModelIndex(), position, position + rows - 1)
            self.endInsertRows()
            return True
        except:
            print(sys.exc_info())


