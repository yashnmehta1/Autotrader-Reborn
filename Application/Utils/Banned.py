import numpy as np





def load_symbol_for_Banned(self):
    fltr1 = np.asarray(['NSEFO'])
    self.Banned.SymbolLs = np.unique(self.Contract_df[np.in1d(self.Contract_df[:, 0], fltr1)][: ,3])
    self.Banned.cbSymbol.addItems(self.Banned.SymbolLs)
    self.Banned.model.modelReset.emit()

def load_instrument_for_Banned(self):
    a = self.table[: ,0]
    self.Banned.cbInstrument.clear()
    for i in a :
        fltr = np.asarray([i])
        lua1 = self.Contract_df[np.in1d(self.Contract_df[:, 2], fltr)][0][4]
        self.Banned.listInstrument[i ] =lua1
        self.Banned.cbInstrument.addItem(lua1)

def addBannedSymbol(self):
    a= self.Banned.cbSymbol.currentText()
    if(a not  in self.listBannedSymbol):
        self.listBannedSymbol.append(a)
        self.Banned.model.pixmaps = self.listBannedSymbol
        self.Banned.model.modelReset.emit()
    print(self.listBannedSymbol,'se lf.listBannedSymbol')

def addBannedInstrument(self):
    a= self.Banned.cbInstrument.currentText()
    if(a not  in self.listBannedIns):
        self.listBannedIns.append(a)
        self.Banned.model1.pixmaps = self.listBannedIns
        self.Banned.model1.modelReset.emit()
    print(self.listBannedIns,'se lf.listBannedIns')

def remBannedSymbol(self):
    a=self.Banned.listBSym.selectedIndexes()[0].data()
    if(a  in self.listBannedSymbol):
        self.listBannedSymbol.remove(a)
        self.Banned.model.pixmaps = self.listBannedSymbol
        self.Banned.model.modelReset.emit()
    print(self.listBannedSymbol,'s elf.listBannedSymbol')


def remBannedInstrument(self):
    a=self.Banned.listBIns.selectedIndexes()[0].data()
    if(a  in self.listBannedIns):
        self.listBannedIns.remove(a)
        self.Banned.model1.pixmaps = self.listBannedIns
        self.Banned.model1.modelReset.emit()
    print(self.listBannedIns,'s elf.listBannedIns')
