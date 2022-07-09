import traceback

from PyQt5.QtCore import QObject,pyqtSlot,pyqtSignal,QTimer


class FeedHandler(QObject):
    sgUserTrd = pyqtSignal(object)
    sgNewTrade = pyqtSignal()
    def __init__(self):
        super(FeedHandler, self).__init__()
        self.d1501 = {}
        self.d1501 = {}

    def add1501(self,token):
        try:
            if(token not in self.d1501.keys()):
                self.d1501[token]=0
            self.d1501[token]=self.d1501[token]+1
        except:
            print(traceback.print_exc())


    def less1501(self,token):
        try:
            self.d1501[token] = self.d1501[token] - 1
        except:
            print(traceback.print_exc())


    def get_count1501(self,token):
        return self.d1501[token]

    def add1502(self, token):
        try:
            if (token not in self.d1502.keys()):
                self.d1502[token] = 0
            self.d1502[token] = self.d1502[token] + 1
        except:
            print(traceback.print_exc())

    def less1502(self, token):
        try:
            self.d1502[token] = self.d1502[token] - 1
        except:
            print(traceback.print_exc())

    def get_count1502(self, token):
        return self.d1502[token]



