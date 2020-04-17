from bs4 import BeautifulSoup
import requests
import functools
import locale
import re
import Warn_Utilities as w
import tabulate as tab   # https://pypi.org/project/tabulate/

locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'

master_row_list = []
previous_row = []
searchYear = '2020'
headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})

try:
    for i in range(1,50):
        req = requests.get(w.getPageUrl(w.getRootPageYear(2020),i), headers)
        req.raise_for_status()
        soup = BeautifulSoup(req.content, 'lxml')

        str(soup).replace("</br>", " ")
        str(soup).replace("<br>", " ")

        table = soup.find('tbody')
        table_rows = table.find_all('tr')
        if w.is_duplicate(table_rows, previous_row):
            print("....End of Pages....\n")
            raise requests.HTTPError

        for tr in table_rows:
            td = tr.find_all('td')
            row = w.buildRow(td)
            master_row_list.append(row)
            # displayRowDetails(row)

        previous_row = list(table_rows)
        print(w.getPageUrl(w.getRootPageYear(2020),i))
except requests.exceptions.HTTPError:
    count = w.getTotalLayoffs(master_row_list)
    print(tab.tabulate([['Records', len(master_row_list)], ['Layoffs', f'{count:n}']], headers=['Metric', 'Value'], tablefmt='orgtbl'))

exit(0)

