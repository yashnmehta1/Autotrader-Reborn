from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QModelIndex
from PyQt5 import QtGui
from PyQt5.QtGui import QBrush,QColor
import sys
import decimal

class DTableModel1(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(DTableModel1, self).__init__()
        # self.rwc = 5
        self._data = data
        self.lastSerialNo =0


    # def addrwcount(self,a):
    #     self.rwc = a

    def data(self, index, role):
        value = self._data[index.row(), index.column()]

        if role == Qt.DisplayRole:
            if isinstance(value, int):
                value = int(value)
            elif isinstance(value, float):
                value = float(value)
                if(abs(value)>1000000):
                    value = int(value)
            return value

        if role == Qt.BackgroundRole:
            if self._data[index.row(), 7] == 'Buy':
                return QBrush(QColor(116, 130, 255))

            if self._data[index.row(), 7] == 'Sell':
                return QBrush(QColor(242, 98, 149))

            if(index.column()==5):
                if self._data[index.row(), 5] == 'New':
                    return QBrush(QColor(116,130,255))

                if self._data[index.row(), 5] == 'Rejected':
                    return QBrush(QColor(242,98,149))

            if(index.column()==7):
                if self._data[index.row(), 7] == 'Started':
                    return QBrush(QColor(116,130,255))

                if self._data[index.row(), 7] == 'Stopped':
                    return QBrush(QColor(242,98,149))



        if role == Qt.TextAlignmentRole:
            value = self._data[index.row(), index.column()]

            if isinstance(value, int) or isinstance(value, float):
                # Align right, vertical middle.
                return Qt.AlignVCenter + Qt.AlignRight


    def rowCount(self, index=''):
        return self.lastSerialNo

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.names[section])


    def insertRows(self, position=0, rows=1, index=QModelIndex()):
        # print("\n\t\t ...insertRows() Starting position: '%s'" % position, 'with the total rows to be inserted: ', rows)

        try:
            self.beginInsertRows(QModelIndex(), position, position + rows - 1)
            self.endInsertRows()
            return True
        except:
            print(sys.exc_info())


    def DelRows(self, position=0, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.endRemoveRows()
        return  True