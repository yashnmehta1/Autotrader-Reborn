import sys
import traceback
from PyQt5 import QtCore
from PyQt5.QtCore import Qt,QModelIndex
import time
from  numba import *
from PyQt5 import QtGui
from PyQt5.QtGui import QBrush

class DTableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(DTableModel, self).__init__()
        self._data = data
        self._data1 = data




    def data(self, index, role):
        try:
            value = self._data[index.row(), index.column()]

            if role == Qt.DisplayRole:
                # print('displ', role)
                # print(value)
                return str(value)

            if role == Qt.TextAlignmentRole:
                # print('textali',role)

                value = self._data[index.row(), index.column()]

                if isinstance(value, int) or isinstance(value, float):
                    # Align right, vertical middle.
                    return Qt.AlignVCenter + Qt.AlignRight


            # if role == Qt.BackgroundColorRole:
            #     # print('BACK', role)
            #     if(index.column()==5):
            #         value1=self._data1[index.row(), index.column()]
            #         if(value>value1):
            #             return QtGui.QColor(79, 183, 224)
            #
            #         if(value<value1):
            #             return QtGui.QColor(194, 54, 75)
            #         if (value == value1):
            #             return QtGui.QColor('transparent')


        except:
            print(traceback.print_exc())
            print(sys.exc_info())


    def rowCount(self, index):
        # print('in rowCount',self.rwc)
        return self._data.shape[0]

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
