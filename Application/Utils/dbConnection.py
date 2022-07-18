import sqlite3
#import  sqlalchemy
import os
import traceback
# import pyodbc


try:
    loc1 = os.getcwd().split('Application')
    dbLocation = os.path.join(loc1[0], 'Application','DB','app.db')

    dbconn = sqlite3.connect(dbLocation)
    cursor = dbconn.cursor()
except:

    print(traceback.print_exc())