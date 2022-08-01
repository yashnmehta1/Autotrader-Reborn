import numpy as np

def getClientId(self,filterValue):
    return 0
def getSerialNumber(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 22], fltr),2]
    return value[0]

def getToken(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 22], fltr),0]
    return value[0]

def getInstrumentType(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 22], fltr),2]
    return value[0]

def getLTP(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 22], fltr),9]
    return value[0]

def getSymbol(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 22], fltr),3]
    return value[0]

def getExchange(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 22], fltr),1]
    print('getExchange',value)
    return value[0]

def getStrikePrice(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 22], fltr),5]
    return value[0]


def getExpiry(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 22], fltr),4]
    return value[0]

def getOptionType(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 22], fltr),6]
    return value[0]


