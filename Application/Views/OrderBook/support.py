from Application.Views.Models.tableOrder import ModelOB
import traceback
import logging
import sys


def updateGetApi(self, data):
    try:
        # print('updateGetApi',data)
        self.ApiOrder = data
        self.modelO = ModelOB(self.ApiOrder, self.heads)
        self.smodelO.setSourceModel(self.modelO)
        self.tableView.setModel(self.smodelO)
        self.rcount = self.ApiOrder.shape[0]
    except:
        print(traceback.print_exc())
        logging.error(sys.exc_info())
