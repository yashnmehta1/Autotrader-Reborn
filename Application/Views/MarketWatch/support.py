import numpy as np

def getClientId(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),28]
    print('getClientId',value)
    return value[0]

def getToken(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),0]
    print('getClientId',value)
    return value[0]

def getSerialNumber(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),30]
    print('getClientId',value)
    return value[0]


def getInstrumentType(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),2]
    print('InstrumentType',value)
    return value[0]


def getSymbol(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),3]
    print('symbol',value)
    return value[0]

def getExchange(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),1]
    print('getExchange',value)
    return value[0]

def getStrikePrice(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),5]
    print('getStrikePrice',value)
    return value[0]


def getExpiry(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),4]
    print('getExpiry',value)
    return value[0]

def getOptionType(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),6]
    print('getOptionType',value)
    return value[0]

def getInstrumentType(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),2]
    print('InstrumentType',value)
    return value[0]

def getOrderType(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),9]
    print('getOrderType',value)
    return value[0]

def getValidity(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),24]
    print('getValidity',value)
    return value[0]

def getProductType(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),23]
    print('getProductType',value)
    return value[0]

def getTriggerPrice(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),14]
    print('getTriggerPrice',value)
    return '%.2f'%value[0]

def getQty(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),12]
    print('getQty',value)
    return value[0]

def getOUID(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),15]
    print('getQty',value)
    return value[0]

def getLimitPrice(self,filterValue):
    fltr = np.asarray([filterValue])
    value = self.table[np.in1d(self.table[:, 30], fltr),13]
    print('getLimitPrice',value)
    return value[0]
