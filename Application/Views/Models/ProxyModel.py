from PyQt5.QtCore import *




class ProxyModel (QSortFilterProxyModel): #Custom Proxy Model
    def __init__(self):
        super(ProxyModel,self).__init__()
        self.onlyPoss =False

    def filterAcceptsRow(self, row, parent):
        if(self.onlyPoss==False):
            return True
        else:
            if(self.sourceModel().index(row, 10, parent).data() != 0 or self.sourceModel().index(row, 11, parent).data()!= 0 or self.sourceModel().index(row, 6, parent).data() == ' '):
                return True
            else:
                return False
