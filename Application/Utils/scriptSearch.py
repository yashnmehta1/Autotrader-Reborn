import numpy as np
import logging
import sys
import traceback
import  numpy as np
import datatable as dt
import threading
from Application.Services.Xts.Api.servicesMD import  subscribeToken,unSubscription_feed



def addscript(self):
    try:


        print('dockMW',self.CFrame.dockMW.visibleRegion().isEmpty())
        print('dockMW_basic',self.CFrame.dockMW_basic.visibleRegion().isEmpty())


        exchange = self.cbEx.currentText()
        token = int(self.LeToken.text())
        fltr = np.asarray([token])
        filteredArray = self.marketW.table[np.in1d(self.marketW.table[:, 0], fltr)]
        isRecordExist = False
        if (filteredArray.size != 0):
            fltr = np.asarray([exchange])
            filteredArray1 = filteredArray[np.in1d(filteredArray[:, 1], fltr)]
            if (filteredArray1.size != 0):
                fltr = np.asarray([self.DefaultClient])
                filteredArray2 = filteredArray[np.in1d(filteredArray[:, 26], fltr)]
                if (filteredArray2.size != 0):
                    isRecordExist = True

        if (isRecordExist == False):
            if (exchange == 'NSEFO'):
                ins_detail = self.fo_contract[token - 35000]
            elif (exchange == 'NSECD'):
                ins_detail = self.cd_contract[token]
            elif (exchange == 'NSECM'):
                ins_detail = self.eq_contract[token]
            assetToken = ins_detail[9]
            print(token,token-3500+1,ins_detail)
            anm = dt.Frame(
                [
                    [token],
                    [exchange], [ins_detail[5]], [ins_detail[3]], [ins_detail[6]], [ins_detail[7]],
                    [ins_detail[8]], [0.0], [0.00], [0.00], ['+0.00'],
                    ['+0.00'], [0], [0], [0], [0.0],
                    [0.0], [0.0],
                    [0.0], [0.0], [0.0],
                    [0.0], [0.0], [0.0], [0], [0],
                    [0], [assetToken], [self.DClient], [self.userID], [self.marketW.lastSerialNo],
                    [0.00], [ins_detail[4]]
                ]).to_numpy()

            self.marketW.table[self.marketW.lastSerialNo, :] = anm
            self.marketW.lastSerialNo += 1
            self.marketW.model.lastSerialNo += 1
            self.marketW.model.rowCount()
            self.marketW.model.insertRows()
            self.marketW.model.dta1.append([0, 0, 0])

            self.marketW.model.color.append(['transparent', 'transparent', 'transparent'])
            # self.marketW.smodel.sort(self.marketW.sortColumn, self.marketW.sortOrder)

            ind = self.marketW.model.index(0, 0)
            ind1 = self.marketW.model.index(0, 27)
            self.marketW.model.dataChanged.emit(ind, ind1)

            th1 = threading.Thread(target=subscribeToken,
                                   args=(self,int(self.LeToken.text()), self.cbEx.currentText(), 1501))
            th1.start()

    except:
        print(traceback.print_exc(), sys.exc_info())





def ExchChange(self, aa):
    try:
        a= self.cbEx.currentText()
        print(a)
        if(a=='NSEFO'):
            lsSegment1 = np.unique(self.fo_contract1[:,1])
            self.t11 = self.fo_contract1

        elif(a=='NSECM'):
            lsSegment1 = np.unique(self.eq_contract1[:,1])
            self.t11 = self.eq_contract1
        elif(a=='NSECD'):
            lsSegment1 = np.unique(self.cd_contract1[:,1])
            self.t11 = self.cd_contract1

        self.cbSg.clear()
        self.cbSg.addItems(lsSegment1)

    except:
        print(traceback.print_exc(),'ex chab')
        logging.error(sys.exc_info()[1])

def SegmentChange(self, aa):
    try:
        a= self.cbSg.currentText()
        fltr = np.asarray([a])
        self.t12 = self.t11[np.in1d(self.t11[:, 1], fltr)]
        lsIns = np.unique(self.t12[:,5])
        self.cbIns.clear()
        self.cbIns.addItems(lsIns)
    except:
        print(traceback.print_exc())
        print(sys.exc_info())
        logging.error(sys.exc_info()[1])

def inschange(self, aa):
    try:
        a= self.cbIns.currentText()
        fltr = np.asarray([a])
        self.t1 = self.t12[np.in1d(self.t12[:, 5], fltr)]
        # self.t1_tp = self.t1.transpose()
        lsSymbol = np.unique(self.t1[:,3])
        # print('lsSymbol',lsSymbol)


        self.cbSym.clear()
        self.cbSym.addItems(lsSymbol)
        self.cbOtype.clear()
        if (a == 'Equity'):
            self.cbOtype.addItem('E')
        if ('FUT' in a):
            self.cbOtype.addItem(' ')
        elif ('OPT' in a):
            self.cbOtype.clear()
            self.cbOtype.addItems(['CE', 'PE'])
    except:
        print(sys.exc_info()[1],'seg ch')

def symchange(self, aa):
    try:
        a= self.cbSym.currentText()
        # print('cbSym',a)
        fltr = np.asarray([a])
        self.t2 = self.t1[np.in1d(self.t1[:, 3], fltr)]
        self.t2_tp = self.t2.transpose()
        # print(self.t2)
        lsExp = np.unique(self.t2_tp[6]).tolist()
        # print('LSEXP',lsExp)
        self.cbExp.clear()
        self.cbExp.addItems(lsExp)
        # print(lsExp,self.t2)
    except:
        print(traceback.print_exc(),sys.exc_info(),lsExp)
        logging.error(sys.exc_info()[1])

def expchange(self, aa):
    try:
        a = self.cbExp.currentText()
        fltr = np.asarray([a])
        self.t3 = self.t2[np.in1d(self.t2[:, 6], fltr)]
        self.t3_tp = self.t3.transpose()

        if ('FUT' in self.cbIns.currentText()):
            self.cbStrk.clear()
            self.cbStrk.addItem(' ')

        elif (self.cbIns.currentText() == 'Equity'):
            self.cbStrk.clear()
            self.cbStrk.addItem(' ')

            # self.cbOtype.clear()

        else:

            lsstrk = np.unique(self.t3_tp[7])

            self.cbStrk.clear()
            self.cbStrk.addItems(lsstrk)

    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])

def changestrike(self, aa):
    try:
        if ('FUT' in self.cbIns.currentText()):
            self.cbOtype.clear()
            self.cbOtype.addItem(' ')
        elif (self.cbIns.currentText() == 'Equity'):
            self.cbOtype.clear()
            self.cbOtype.addItem(' ')
        elif ('OPT' in self.cbIns.currentText()):
            if (self.cbOtype.currentText() not in ['CE', 'PE']):
                self.cbOtype.clear()
                self.cbOtype.addItems(['CE', 'PE'])
            else:
                changeOtype(self)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])

def changeOtype(self):
    try:
        a = self.cbOtype.currentText()

        if (self.cbSym.currentText() != '' and self.cbExp.currentText() != ''):

            if (a != ''):
                # print('value of option',a)
                fltr = np.asarray([a])
                self.t4 = self.t3[np.in1d(self.t3[:, 8], fltr)]
                if ('FUT' in self.cbIns.currentText()):
                    self.t5 = self.t4
                elif (self.cbIns.currentText() == 'Equity'):
                    self.t5 = self.t4
                else:
                    fltr1 = np.asarray([self.cbStrk.currentText()])
                    self.t5 = self.t4[np.in1d(self.t4[:, 7], fltr1)]

                self.cbDName.clear()
                self.cbDName.addItem(self.t5[0][4])
                self.LeToken.setText(str(self.t5[0][2]))
    except:
        print(traceback.print_exc(), 'opo')
        print(' aaaaa   %s,%s,%s,%s,' % (
        self.cbSym.currentText(), self.cbExp.currentText(), self.cbStrk.currentText(), self.cbOtype.currentText()))
        # logging.error(sys.exc_info())

def selExchange(self):
    if (self.isScriptBarOpen):
        self.cbEx.setFocus()
    else:
        self.anim41.start()
        self.cbEx.setFocus()
        self.isScriptBarOpen = True


def scriptBarSlots(self):
    self.cbEx.currentIndexChanged.connect(lambda: ExchChange(self, self.cbEx.currentIndex()))
    self.cbSg.currentIndexChanged.connect(lambda: SegmentChange(self, self.cbSg.currentIndex()))
    self.cbIns.currentIndexChanged.connect(lambda: inschange(self, self.cbIns.currentIndex()))
    self.cbSym.currentIndexChanged.connect(lambda: symchange(self, self.cbSym.currentIndex()))
    self.cbExp.currentIndexChanged.connect(lambda: expchange(self, self.cbExp.currentIndex()))
    self.cbStrk.currentIndexChanged.connect(lambda: changestrike(self, self.cbStrk.currentIndex()))
    self.cbOtype.currentIndexChanged.connect(lambda: changeOtype(self, ))

    self.addSc.clicked.connect(lambda: addscript(self))


