import time, datetime, csv
from pathlib import Path

BUSINESS_NAME = 0
FILE_DATE = 1
LAYOFF_WINDOW = 2
LAYOFF_COUNT = 3
SECTOR = 4
FILING_LINK = 5


def timeFormat(format):
    return datetime.datetime.now().strftime(format)

def createDataFile(file_date):
    file_name = file_date + "_data.csv"
    base_path = Path(__file__).parent
    target_path = (base_path / "./data" / file_name).resolve()
    with open(target_path, 'a+', newline='') as data_file:
        employee_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(['Date','Time','Records','Count'])
    data_file.close()

def writeDataToFile(data_line, file_date):
    file_name = file_date + "_data.csv"
    base_path = Path(__file__).parent
    target_path = (base_path / "./data" / file_name).resolve()
    with open(target_path, 'a+', newline='') as data_file:
        employee_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow(data_line)
    data_file.close()

def getDomain():
    return "http://reactwarn.floridajobs.org"

def getRootPageYear(searchYear):
    return "http://reactwarn.floridajobs.org/WarnList/Records?year=" + str(searchYear) + "&sort=CompanyName&sortdir=ASC"

def getPageUrl(root,i):
    return root + "&page=" + str(i)

def is_duplicate(current_row, previous_row):
    if len(previous_row) == 0:
        return False
    for i in range(0,4):
        if current_row[i] != previous_row[i]:
            return False
    return True

def getTotalLayoffs(list):
    c=0
    for r in list:
        c += int(r[LAYOFF_COUNT])
    return c

def displayRowDetails(row):
    for element in row:
        print(element)
    print("\n")

def buildRow(td):
    row = [i.text for i in td]
    link = td[5].find('a')
    row[5] = getDomain() + link['href']
    return row