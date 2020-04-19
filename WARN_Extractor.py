from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler # https://apscheduler.readthedocs.io/en/stable/userguide.html
import sched, time
import requests
import functools
import locale, os
import re
import Warn_Utilities as w
import tabulate as tab   # https://pypi.org/project/tabulate/

def captureCurrent():
    global POLL_ID
    global PAGES_INDEXED
    global MAX_PAGES
    master_row_list = []
    previous_row = []
    POLL_ID += 1
    try:
        for i in range(1,MAX_PAGES):
            req = requests.get(w.getPageUrl(w.getRootPageYear(SEARCH_YEAR),i), headers)
            req.raise_for_status()
            soup = BeautifulSoup(req.content, 'lxml')

            table = soup.find('tbody')
            table_rows = table.find_all('tr')
            if w.is_duplicate(table_rows, previous_row):
                if DEBUG: print("....End of Pages....\n")
                raise requests.HTTPError

            for tr in table_rows:
                td = tr.find_all('td')
                row = w.buildRow(td)
                master_row_list.append(row)
                # displayRowDetails(row)

            previous_row = list(table_rows)
            PAGES_INDEXED = i
            if DEBUG: print(w.getPageUrl(w.getRootPageYear(SEARCH_YEAR), i))
    except requests.exceptions.HTTPError:
        count = w.getTotalLayoffs(master_row_list)
        records = str(len(master_row_list))
        nowDate = w.timeFormat("%Y-%m-%d")
        nowTime = w.timeFormat("%H:%M:%S")
        print("\nCollection Cycle %s Completed @ %s__%s" % (POLL_ID, nowDate, nowTime))
        print(tab.tabulate([['Pages', PAGES_INDEXED], ['Records', records], ['Layoffs', f'{count:n}']], headers=['Metric', 'Value'], tablefmt='orgtbl'))

        w.writeDataToFile([POLL_ID, PAGES_INDEXED, nowDate, nowTime, records, count], FILE_DATE)
        PAGES_INDEXED = 0

DEBUG = False
SEARCH_YEAR = '2020'
SCAN_INTERVAL_MINUTES = 20
POLL_ID = 0
PAGES_INDEXED = 0
MAX_PAGES = 50
FILE_DATE = w.timeFormat("%Y%m%d_%H-%M-%S")

locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'
headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})

w.createDataFile(FILE_DATE)
print("Scan Starting. Polling every %s minutes...\n" % (SCAN_INTERVAL_MINUTES))

scheduler = BlockingScheduler()
scheduler.add_job(captureCurrent, 'interval', minutes=SCAN_INTERVAL_MINUTES, max_instances=1)
scheduler.start()



