import lxml
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup
import requests


class MyClass:
    def method(self):
        return 'instance method called', self

    @classmethod
    def classmethod(cls):
        return 'class method called', cls

    @staticmethod
    def staticmethod():
        return 'static method called'


def example():
    url = 'http://www.google.com'
    r = requests.get("http://" + url)
    data = r.text
    soup = BeautifulSoup(data)
    for link in soup.find_all('a'):
        print(link.get('href'))


#-----------------------------------------------------------------------------------------------------------------------
# Helper class for string manipulations
class myString(object):

    # Remove all \n characters to flatten the string
    @staticmethod
    def stripNewLine(s):
        if (s == None):
            return ""
        return s.replace("\n", "")

    # Returns true if the string is empty
    @staticmethod
    def isEmpty(s):
        if (s == None):
            return True
        return myString.stripNewLine(s).strip() == ""

    @staticmethod
    def strip(s):
        if (s == None):
            return ""
        t = s.text.strip()
        return t

#-----------------------------------------------------------------------------------------------------------------------

#Process Leumi HTML input file
class LeumiProcessor(object):

    def importFile(self,htmlFile):
        clean = self.cleanInputFile(htmlFile)
        self.process(clean)

    def cleanInputFile(self,htmlFile):
        cleaner = Cleaner()
        cleaner.javascript = True  # This is True because we want to activate the javascript filter
        cleaner.style = True  # This is True because we want to activate the styles & stylesheet filter

        #"WITH JAVASCRIPT & STYLES"
        htmlString = lxml.html.tostring(lxml.html.parse(htmlFile))
        #"WITHOUT JAVASCRIPT & STYLES"
        htmlClean = lxml.html.tostring(cleaner.clean_html(lxml.html.parse(htmlFile)))

        return htmlClean

    def process(self, htmlInput):
        assert isinstance(htmlInput, object)
        soup = BeautifulSoup(htmlInput)
        table = self.getDataTable(soup)
        for row in table.find_all('tr'):
            e = self.processRow(row)
            e.toCSV()

    def processRow(self,row):
        date = self.extractDate(row)
        action = self.extractAction(row)
        refId = self.extractRefId(row)
        credit = self.extractCredit(row)
        debit = self.extractDebit(row)
        balance = self.extractBalance(row)
        entry = DataEntry(date,action,refId,credit,debit,balance)
        return entry

    ####################################################################################################################
    # Methods to override
    ####################################################################################################################
    def getDataTable(self,soup):
        # In the leumi files, the data is in a table with id=ctlActivityTable
        return soup.find("table", {"id": "ctlActivityTable"})

    def extractDate(self,row):
        # In the leumi files, the date is in a td with class=ExtendedActivityColumnDate
        return myString.strip(row.find("td", {"class": "ExtendedActivityColumnDate"}))

    def extractAction(self,row):
        # In the leumi files, the action is in a td with either class=ActivityTableColumn1 or class=ActivityTableColumn1LTR
        action1 = myString.strip(row.find("td", {"class": "ActivityTableColumn1"}))
        action2 = myString.strip(row.find("td", {"class": "ActivityTableColumn1LTR"}))
        return action1 + action2

    def extractRefId(self,row):
        # In the leumi files, the refId is in a td with class=ReferenceNumberUniqeClass
        return myString.strip(row.find("td", {"class": "ReferenceNumberUniqeClass"}))

    def extractCredit(self,row):
        # In the leumi files, the credit is in a td with class=AmountCreditUniqeClass
        return myString.strip(row.find("td", {"class": "AmountCreditUniqeClass"}))

    def extractDebit(self,row):
        # In the leumi files, the debit is in a td with class=AmountDebitUniqeClass
        return myString.strip(row.find("td", {"class": "AmountDebitUniqeClass"}))

    def extractBalance(self,row):
        # In the leumi files, the balance is in a td with class=number_column
        # There are 3 such td in each row: debit, credit, balance. Balance is always the 3rd.
        totals = row.find_all("td", {"class": "number_column"})
        total = ""
        if (len(totals) > 1):
            total = myString.strip(totals[2])
        return total


# This class encapsulates methods to manipulate data entries
# Including import / export methods
class DataEntry(object):
    date = ""
    action = ""
    refId = ""
    credit = ""
    debit = ""
    balance = ""
    isEmpty = False

    def __init__(self,d,a,r,c,de,b):
        self.date = d
        self.action = a
        self.refId = r
        self.credit = c
        self.debit = de
        self.balance = b
        if(myString.isEmpty(self.date)):
            self.isEmpty = True

    def toCSV(self):
        if(self.isEmpty):
            return
        set = [self.date,self.action,self.refId,self.credit,self.debit,self.balance]
        if (len(set) > 0):
            print(",".join(set))


def main():
    htmlFile = "../inbox/bankleumi11062018.html"
    processor = LeumiProcessor()
    processor.importFile(htmlFile)


main()