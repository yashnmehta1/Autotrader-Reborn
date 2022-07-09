from os import path,getcwd,remove,rename
import requests
import zipfile
import datetime
import traceback

loc1 = getcwd().split('Application')
downloadLoc = path.join(loc1[0], 'Downloads')

tod =datetime.datetime.today()
print(tod.weekday())


def get_bhavcopy():
    user_agent = 'Mozilla/5.0'
    headers = {'User-Agent': user_agent}
    try:
        diffdays = 1
        if(tod.weekday()==6):
            diffdays = 3


        yesterday = datetime.datetime.today() - datetime.timedelta(days=diffdays)


        fo_bhav1 = "https://archives.nseindia.com/content/historical/DERIVATIVES/" + yesterday.strftime(
            '%Y') + r"/" + yesterday.strftime('%b').upper() + r"/fo" + yesterday.strftime(
            "%d%b%Y").upper() + "bhav.csv.zip"

        re = requests.get(fo_bhav1, headers={'User-Agent': user_agent})

        trial = 0
        while(re.status_code != 200 or trial < 5):
            diffdays -= 1
            fo_bhav1 = "https://archives.nseindia.com/content/historical/DERIVATIVES/" + yesterday.strftime(
                '%Y') + r"/" + yesterday.strftime('%b').upper() + r"/fo" + yesterday.strftime(
                "%d%b%Y").upper() + "bhav.csv.zip"
            re = requests.get(fo_bhav1, headers={'User-Agent': user_agent})
            trial +=1


        fo_bhav1 = "https://www1.nseindia.com/content/historical/DERIVATIVES/" + yesterday.strftime(
            '%Y') + r"/" + yesterday.strftime('%b').upper() + r"/fo" + yesterday.strftime(
            "%d%b%Y").upper() + "bhav.csv.zip"
        cm_bhav = "https://www1.nseindia.com/content/historical/EQUITIES/" + yesterday.strftime(
            '%Y') + r"/" + yesterday.strftime(
            '%b').upper() + r"/cm" + yesterday.strftime("%d%b%Y").upper() + r"bhav.csv.zip"
        ind_bhav = r"https://www1.nseindia.com/content/indices/ind_close_all_" + yesterday.strftime(
            '%d%m%Y') + ".csv"

        # https://www1.nseindia.com/content/indices/ind_close_all_06092021.csv
        dat = yesterday.strftime('%d%b%Y').upper()
        dt = yesterday

        re = requests.get(fo_bhav1, headers={'User-Agent': user_agent})


        fobhavLoc = path.join(downloadLoc,"fo_bhav.zip")
        with open(fobhavLoc, 'wb+') as f:
            f.write(re.content)
        f.close()

        zf = zipfile.ZipFile(fobhavLoc, 'r')
        zf.extractall(downloadLoc)
        zf.close()

        if path.isfile(path.join(downloadLoc,"fo_bhav.csv")):
            remove(path.join(downloadLoc,"fo_bhav.csv"))
        fname = path.join(downloadLoc,'fo' + dat + 'bhav.csv')

        sf = fname

        rename(sf, path.join(downloadLoc,'fo_bhav.csv'))

        req = requests.get(cm_bhav, headers={'User-Agent': user_agent})


        cmBHavLoc = path.join(downloadLoc,"cm_bhav.zip")
        with open(cmBHavLoc, 'wb') as f:
            f.write(req.content)
        f.close()

        zf = zipfile.ZipFile(cmBHavLoc, 'r')
        zf.extractall(downloadLoc)
        zf.close()
        if path.isfile(path.join(downloadLoc,"cm_bhav.csv")):
            remove(path.join(downloadLoc,"cm_bhav.csv"))
        fname = path.join(downloadLoc,'cm' + dat + 'bhav.csv')

        sf = fname

        rename(sf, path.join(downloadLoc,'cm_bhav.csv'))
        a = dt.strftime('%d%m%Y')

        rez = requests.get(ind_bhav, headers={'User-Agent': user_agent})

        with open(path.join(downloadLoc,"idx_bhav.csv"), 'wb') as f:
            f.write(rez.content)
        f.close()
    except:
        print(traceback.print_exc())
