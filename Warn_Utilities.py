

BUSINESS_NAME = 0
FILE_DATE = 1
LAYOFF_WINDOW = 2
LAYOFF_COUNT = 3
SECTOR = 4
FILING_LINK = 5

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