import traceback


def updatePbBGColor_filter(self,pb):
    try:
        self.lastSelectedFilter.setStyleSheet('background-color: #000a14;color: #F0F0F0;')
        if(pb=='All'):
            self.pbFAll.setStyleSheet('background: #148CD2;color: #19232d;')
            self.lastSelectedFilter =self.pbFAll
        elif(pb=='Active'):
            self.pbFActive.setStyleSheet('background: #148CD2;color: #19232d;')
            self.lastSelectedFilter =self.pbFActive
        elif(pb=='Stop'):
            self.pbFStop.setStyleSheet('background: #148CD2;color: #19232d;')
            self.lastSelectedFilter =self.pbFStop

    except:
        print(traceback.print_tb())


def updatePbBGColor_stretegies(self,pb):
    try:
        self.lastSelectedStretegy.setStyleSheet('background-color: #000a14;color: #F0F0F0;')
        if(pb=='Stradle'):
            self.pbStradle.setStyleSheet('background: #148CD2;color: #19232d;')
            self.lastSelectedStretegy =self.pbStradle
        elif(pb=='Box'):
            self.pbBox.setStyleSheet('background: #148CD2;color: #19232d;')
            self.lastSelectedStretegy =self.pbBox
        elif(pb=='PairSell'):
            self.pbPairSell.setStyleSheet('background: #148CD2;color: #19232d;')
            self.lastSelectedStretegy =self.pbPairSell
        elif(pb=='PairSellAdv'):
            self.pbPairSellAdv.setStyleSheet('background: #148CD2;color: #19232d;')
            self.lastSelectedStretegy =self.pbPairSellAdv
        elif(pb=='TSpecial'):
            self.pbTSpecial.setStyleSheet('background: #148CD2;color: #19232d;')
            self.lastSelectedStretegy =self.pbTSpecial
        elif(pb=='JodiATM'):
            self.pbJodiATM.setStyleSheet('background: #148CD2;color: #19232d;')
            self.lastSelectedStretegy =self.pbJodiATM
    except:
        print(traceback.print_tb())

