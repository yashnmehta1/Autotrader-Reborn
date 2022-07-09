from PyQt5.QtCore import Qt

def res_max(self):
    if (self.isMaximized() == False):
        self.showMaximized()
        self.CFrame.resizeDocks([self.CFrame.dockOP, self.CFrame.dockMW], [700, 500], Qt.Vertical)
    else:
        self.showNormal()
        self.CFrame.resizeDocks([self.CFrame.dockOP, self.CFrame.dockMW], [500, 500], Qt.Vertical)
