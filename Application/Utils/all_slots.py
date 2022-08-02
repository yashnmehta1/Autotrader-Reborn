
from Application.Utils.scriptSearch import scriptBarSlots
import  sys

from Application.Utils.openRequstedWindow import showPendingW,showFolioPosW,showOrderBookW,showTradeBookW
from Application.Utils.animations import *
from Application.Utils.feedHandler import FeedHandler
from Application.Utils.supMethods import *
from Application.Utils.configReader import refresh
from Application.Utils.updation import *


from Application.Utils.basicWinOps import res_max

from Application.Utils.animations import *


from Application.Stretegies import TSpecial




def createSlots_main(main):
    try:
        scriptBarSlots(main)
        main.pbFolioPos.clicked.connect(main.FolioPos.hide)
        main.pbFolioPos.clicked.connect(main.FolioPos.show)
        main.pbNetPos.clicked.connect(main.NetPos.hide)
        main.pbNetPos.clicked.connect(main.NetPos.show)
        main.pbTradeB.clicked.connect(main.TradeW.hide)
        main.pbTradeB.clicked.connect(main.TradeW.show)
        main.pbOrderB.clicked.connect(main.OrderBook.hide)
        main.pbOrderB.clicked.connect(main.OrderBook.show)

        main.pbPreferences.clicked.connect(main.PreferanceW.show)
        main.PreferanceW.pbApply.clicked.connect(lambda: main.setDefaultClient(main.PreferanceW.cbCList.currentText))

        ################################## Trade Setting Slot  ##########################################

        ################################# Login Class Slota ####################################

        main.login.pbLogin.clicked.connect(main.proceed2login)
        main.login.pbNext.clicked.connect(main.proceed2Main)
        main.login.pbCancel.clicked.connect(sys.exit)

        main.IAS.sgSocketConn.connect(main.LiveFeed.start_socket)
        main.IAS.sgSocketConn.connect(lambda: changeIAS_connIcon(main, 0))
        main.IAS.sgSocketConn.connect(lambda: main.login.label.append('Interactive socket is connected'))

        main.LiveFeed.sgSocketConn.connect(lambda: changeMD_connIcon(main, 0))
        main.LiveFeed.sgSocketConn.connect(lambda: main.login.label.append('Marketdata socket is connected'))
        main.LiveFeed.sgSocketConn.connect(main.login.pbNext.show)

        ################################################################################3
        # main.marketW.buyw.sgAppOrderID.connect(main.inPoreccessOrderIds.append)
        # main.marketW.sellw.sgAppOrderID.connect(main.inPoreccessOrderIds.append)
        #########################################################################################3
        # main.IAS.sgGetAPIpos.connect(lambda: updateGetPosition(main))
        main.IAS.sgOpenPos.connect(lambda: updateOpenPosition(main))

        main.IAS.sgAPIpos.connect(main.updateOnPosition)
        main.IAS.sgTrdSoc.connect(main.updateOnTrade)
        main.IAS.sgPendSoc.connect(main.updateOderSocket)

        ######################################################################
        # both getOrderbook process is done directly from Api call methos only
        # main.IAS.sgGetOrder.connect(main.updateGetorderBook)
        # main.IAS.sgGetPOrder.connect(main.updateGetPendinOrderBook)
        # main.IAS.sgGetTrd.connect(main.on_get_tradeBook)

        ######################################################################

        ############################################################################################
        main.LiveFeed.sgindexfd.connect(lambda: main.on_new_feed_Index)
        main.LiveFeed.sgNPFrec.connect(main.on_new_feed_1501)
        main.LiveFeed.sgNSQrec.connect(main.on_new_feed_1502)
        #########################################################################################3
        main.IAS.sgStatusUp.connect(lambda: updateStatusLable(main, 'x'))
        #########################################################################################3
        # main.PositionW.sgTMTM.connect(main.setMTM)
        main.bt_close.clicked.connect(main.close)
        main.bt_min.clicked.connect(main.showMinimized)
        main.bt_max.clicked.connect(lambda: res_max(main))
        main.title.sgPoss.connect(main.movWin)
        # main.pbMenu.clicked.connect(main.openSideBar)
        # main.pbDPosition.clicked.connect(lambda:showDetailPos(main.marketW.DetailPos))

        main.pbBanned.clicked.connect(main.Banned.show)

        # main.Splash.sgFin.connect(lambda: splashWork(main))

        main.btnIB.clicked.connect(lambda: showIndexBar(main))
        main.btnSB.clicked.connect(lambda: showScriptBar(main))
        main.btnSttn.clicked.connect(lambda: showSettingMenu(main))
        main.btnMMW.clicked.connect(lambda: showM2mW(main))
        main.title.sgDClick.connect(lambda: res_max(main))
        main.marketW.sgShowPending.connect(lambda: showPendingW(main))




        main.Banned.pbAddBSym.clicked.connect(lambda: addBannedSymbol(main))
        main.Banned.pbAddBIns.clicked.connect(lambda: addBannedInstrument(main))
        main.Banned.pbRemBSym.clicked.connect(lambda: remBannedSymbol(main))
        main.Banned.pbRemBIns.clicked.connect(lambda: remBannedInstrument(main))

        main.Manager.pbAdd.clicked.connect(main.addNewStretegy)
    except:
        print(traceback.print_exc())
