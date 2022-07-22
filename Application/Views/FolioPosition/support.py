


def cbClientChange(self):
    self.cbUID.clear()
    clientId = self.cbClient.currentText()
    for i in self.clientFolios[clientId]:
        self.cbUID.addItem(i)



def filterData(self):
    self.filterStr = self.cbUID.currentText()
    print('self.cbUID.currentIndex()',self.cbUID.currentIndex())
    if(self.cbUID.currentIndex()==-1):
        self.filterStr = 'zzzzz'
    self.smodelFP.setFilterFixedString(self.filterStr)

def clearFilter(self):
    self.filterStr = ''
    self.smodelFP.setFilterFixedString('')

def squareAll(self):
    try:
        xyz = self.Apipos
        for i in self.Apipos:
            print(i)
            if(i[7] !=0):
                if (i[7] > 0):
                    qty=abs(i[7])
                    maxqty = int(i[13])
                    while(qty>maxqty):
                        self.PlaceOrder(i[1],'SELL',maxqty,1.1)
                        qty = qty - maxqty
                    self.PlaceOrder(i[1],'SELL',qty,1.1)
                elif (i[7] < 0):
                    maxqty = int(i[13])
                    qty=abs(i[7])
                    while(qty>maxqty):
                        self.PlaceOrder(i[1],'BUY',maxqty,1.1)
                        qty = qty - maxqty
                    self.PlaceOrder(i[1],'BUY',qty,1.1)

    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info()[1])

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



