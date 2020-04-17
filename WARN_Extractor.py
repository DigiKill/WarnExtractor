from bs4 import BeautifulSoup
import sched, time
import requests
import functools
import locale, os
import re
import Warn_Utilities as w
import tabulate as tab   # https://pypi.org/project/tabulate/

def periodic(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 2, periodic,
                    (scheduler, interval, action, actionargs))
    action(*actionargs)

def captureCurrent():
    master_row_list = []
    previous_row = []
    try:
        for i in range(1,50):
            req = requests.get(w.getPageUrl(w.getRootPageYear(2020),i), headers)
            req.raise_for_status()
            soup = BeautifulSoup(req.content, 'lxml')

            table = soup.find('tbody')
            table_rows = table.find_all('tr')
            if w.is_duplicate(table_rows, previous_row):
                if debug: print("....End of Pages....\n")
                raise requests.HTTPError

            for tr in table_rows:
                td = tr.find_all('td')
                row = w.buildRow(td)
                master_row_list.append(row)
                # displayRowDetails(row)

            previous_row = list(table_rows)
            if debug: print(w.getPageUrl(w.getRootPageYear(2020),i))
    except requests.exceptions.HTTPError:
        count = w.getTotalLayoffs(master_row_list)
        records = str(len(master_row_list))
        # fnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nowDate = w.timeFormat("%Y-%m-%d")
        nowTime = w.timeFormat("%H:%M:%S")
        print("\nCollection Cycle Completed @ %s__%s" % (nowDate, nowTime))
        print(tab.tabulate([['Records', records], ['Layoffs', f'{count:n}']], headers=['Metric', 'Value'], tablefmt='orgtbl'))

        w.writeDataToFile([nowDate, nowTime, records, count], fileDate)
    periodic(scheduler, 7000, captureCurrent)

debug = False
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'
searchYear = '2020'
headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
scheduler = sched.scheduler(time.time, time.sleep)
fileDate = w.timeFormat("%Y%m%d_%H-%M-%S")
w.createDataFile(fileDate)

periodic(scheduler, 7000, captureCurrent)

