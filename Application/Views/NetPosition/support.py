from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def filterData(self, a):
    self.filterStr = a
    self.smodelP.setFilterFixedString(self.filterStr)
    self.smodelPD.setFilterFixedString(self.filterStr)


def clearFilter(self):
    self.filterStr = ''
    self.smodelPD.setFilterFixedString('')



def rightClickMenu(self,position):
    try:
        a=(self.tableView.selectedIndexes()[0].data())
        menu = QMenu()
        squareAction = menu.addAction("Square")
        # cancelAction = menu.addAction("Cancel")
        action = menu.exec_(self.tableView.mapToGlobal(position))
        if action == squareAction:
            abc=self.tableView.selectedIndexes()
            noOfcolumnsinNetPoss = self.Apipos.shape[1]

            lent=int((len(abc))/noOfcolumnsinNetPoss)
            print('lent',lent)
            for i in range(lent):

                token = abc[1 + (noOfcolumnsinNetPoss*i)].data()
                qty = int(abc[7 + (noOfcolumnsinNetPoss*i)].data())
                Maxqty = int(abc[13 + (noOfcolumnsinNetPoss*i)].data())

                print(token,qty)

                if(qty>0):
                    absQty = abs(qty)

                    orderSide = 'SELL'
                    while absQty > Maxqty :

                        self.PlaceOrder(token,orderSide,Maxqty,0)
                        absQty = absQty - Maxqty
                    self.PlaceOrder(token, orderSide, absQty, 0)

                elif(qty<0):
                    absQty = abs(qty)
                    orderSide = 'BUY'
                    while absQty > Maxqty :
                        self.PlaceOrder(token,orderSide,Maxqty,0)
                        absQty = absQty - Maxqty
                    self.PlaceOrder(token, orderSide, absQty, 0)


    except:
        print(sys.exc_info()[1])


def createShortcuts(self):
    self.quitSc = QShortcut(QKeySequence('Esc'), self)
    self.quitSc.activated.connect(self.hide)


def changeDayNet(self):
    if(self.rb1.isChecked()):
        self.DayNet = 'DAY'
        self.tableView.setModel(self.smodelPD)

    elif(self.rb2.isChecked()):
        self.DayNet = 'NET'

        self.tableView.setModel(self.smodelP)
        self.rcount = self.Apipos.shape[0]

def orderRaise(self):
    token = int(self.tableView.selectedIndexes()[3].data())
    self.sgCallPOrderBook.emit(str(token))


def showTB(self):
    token = int(self.tableView.selectedIndexes()[3].data())
    self.sgCallTB.emit(token)




def filtr(self):
    try:
        self.smodelP.setFilterFixedString(self.listView.selectedIndexes()[0].data())
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])


