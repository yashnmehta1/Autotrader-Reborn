from PyQt5 import QtCore,QtGui
from PyQt5.QtCore import Qt
class PiecesModel(QtCore.QAbstractListModel):
    def __init__(self,data, parent=None):
        super(PiecesModel, self).__init__(parent)
        self.pixmaps = data

    def supportedDragActions(self):
        super().supportedDragActions()
        return Qt.CopyAction | Qt.MoveAction | Qt.LinkAction

    def data(self, index, role=Qt.DisplayRole):

        if role == Qt.DisplayRole:
            return self.pixmaps[index.row()]

    def setDtt(self,a):
        self.pixmaps = a


    def addPieces(self, pixmap):
        row = len(self.pixmaps)

        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.pixmaps.append(pixmap)
        self.endInsertRows()

    def flags(self,index):
        if index.isValid():
            return (Qt.ItemIsEnabled | Qt.ItemIsSelectable |
                    Qt.ItemIsDragEnabled)

    def clear(self):
        row = len(self.pixmaps)

        del self.pixmaps[:]




    def rowCount(self, parent):
        if parent.isValid():
            return 0
        else:
            return len(self.pixmaps)

    def supportedDragActions(self):
        return Qt.CopyAction | Qt.MoveAction

