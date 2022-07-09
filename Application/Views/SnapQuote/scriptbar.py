import numpy as np



def ExchChange(self, aa):
    try:
        a = self.cbEx.currentText()
        if (a == 'NSEFO'):
            lsSegment1 = np.unique(self.fo_contract1[:, 1])
            self.t11 = self.fo_contract1

        elif (a == 'NSECM'):
            lsSegment1 = np.unique(self.eq_contract1[:, 1])
            self.t11 = self.eq_contract1
        elif (a == 'NSECD'):
            lsSegment1 = np.unique(self.cd_contract1[:, 1])
            self.t11 = self.cd_contract1

        self.cbSg.clear()
        self.cbSg.addItems(lsSegment1)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])


def SegmentChange(self, aa):
    try:
        a = self.cbSg.currentText()
        fltr = np.asarray([a])
        self.t12 = self.t11[np.in1d(self.t11[:, 1], fltr)]
        self.t12_tp = self.t12.transpose()
        lsIns = np.unique(self.t12_tp[5])
        self.cbIns.clear()
        self.cbIns.addItems(lsIns)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])


def inschange(self, aa):
    try:
        a = self.cbIns.currentText()
        fltr = np.asarray([a])
        self.t1 = self.t12[np.in1d(self.t12[:, 5], fltr)]
        # self.t1_tp = self.t1.transpose()
        lsSymbol = np.unique(self.t1[:, 3])
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
        print(sys.exc_info()[1], 'seg ch')


def symchange(self, aa):
    try:
        a = self.cbSym.currentText()
        fltr = np.asarray([a])
        self.t2 = self.t1[np.in1d(self.t1[:, 3], fltr)]
        self.t2_tp = self.t2.transpose()
        lsExp = np.unique(self.t2_tp[6])
        self.cbExp.clear()
        self.cbExp.addItems(lsExp)
    except:
        print(traceback.print_exc())
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
        else:
            lsstrk = np.unique(self.t3_tp[7])
            self.cbStrk.clear()
            self.cbStrk.addItems(lsstrk)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])


def changestrike(self, aa):
    try:
        a = self.cbStrk.currentText()
        if ('FUT' in self.cbIns.currentText()):
            self.cbOtype.clear()
            self.cbOtype.addItem(' ')

        elif ('OPT' in self.cbIns.currentText()):
            if (self.cbOtype.currentText() not in ['CE', 'PE']):
                self.cbOtype.clear()
                self.cbOtype.addItems(['CE', 'PE'])
            else:
                self.changeOtype()

    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])


def changeOtype(self):
    try:
        a = self.cbOtype.currentText()
        if (self.cbSym.currentText() != '' and self.cbExp.currentText() != ''):
            if (a != ''):
                fltr = np.asarray([a])
                self.t4 = self.t3[np.in1d(self.t3[:, 8], fltr)]
                if ('FUT' in self.cbIns.currentText()):
                    self.t5 = self.t4
                elif (self.cbIns.currentText() == 'Equity'):
                    self.t5 = self.t4
                else:
                    fltr1 = np.asarray([self.cbStrk.currentText()])
                    self.t5 = self.t4[np.in1d(self.t4[:, 7], fltr1)]
                self.LeToken.setText(str(self.t5[0][2]))
                self.unSubscription_feed(self.token)
                self.token = self.t5[0][2]
                print('change token in snapQuote ', self.token)
                self.subscription_feed(self.token)
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])
