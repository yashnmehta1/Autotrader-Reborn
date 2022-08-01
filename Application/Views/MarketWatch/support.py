import numpy as np

def getClientId(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),28]
    return value[0]

def getToken(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),0]
    return value[0]

def getSerialNumber(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),30]
    return value[0]


def getInstrumentType(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),2]
    return value[0]


def getSymbol(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),3]
    print("getSYmbo:", value)
    return value[0]

def getExchange(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),1]
    return value[0]

def getStrikePrice(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),5]
    return value[0]


def getExpiry(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),4]
    return value[0]

def getOptionType(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),6]
    return value[0]

def getInstrumentType(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),2]
    return value[0]

def getOrderType(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),9]
    return value[0]

def getValidity(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),24]
    return value[0]

def getProductType(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),23]
    return value[0]

def getTriggerPrice(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),14]
    return '%.2f'%value[0]

def getQty(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),12]
    return value[0]

def getOUID(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),15]
    return value[0]

def getLimitPrice(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),13]
    return value[0]
