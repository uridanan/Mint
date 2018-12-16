import lxml
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup
import requests
from src.myString import myString
from src.bankEntry import BankEntry
from src.businessEntry import BusinessEntry
import timestring
from datetime import datetime
from dateutil.parser import parse
from decimal import Decimal
from abc import ABC, abstractmethod


class HTMLFile(object):
    data = None

    def __init__(self,htmlFile):
        data = self.cleanInputFile(self,htmlFile)

    def cleanInputFile(self, htmlFile):
        cleaner = Cleaner()
        cleaner.javascript = True  # This is True because we want to activate the javascript filter
        cleaner.style = True  # This is True because we want to activate the styles & stylesheet filter
        # "WITH JAVASCRIPT & STYLES"
        htmlString = lxml.html.tostring(lxml.html.parse(htmlFile))
        # "WITHOUT JAVASCRIPT & STYLES"
        htmlClean = lxml.html.tostring(cleaner.clean_html(lxml.html.parse(htmlFile)))
        return htmlClean

    def getData(self):
        return self.data


# https://www.python-course.eu/python3_abstract_classes.php
class BankReport(ABC):
    def process(self):
        BankEntry.createTable(ifNotExists=True)
        BusinessEntry.createTable(ifNotExists=True)

        for row in self.getRows():
            self.processRow(row)

    def processRow(self,row):
        date = self.extractDate(row)
        action = self.extractBusiness(row)
        refId = self.extractRefId(row)
        credit = self.extractCredit(row)
        debit = self.extractDebit(row)
        balance = self.extractBalance(row)
        if(myString.isEmpty(date)):
            return None

        business = BusinessEntry.selectBy(businessName=action).getOne(None)
        if (business == None):
            business = BusinessEntry(businessName=action, marketingName=action, category="")
        entry = BankEntry(date=date, business=business.id, hide=0, refId=refId, credit=credit, debit=debit, balance=balance)
        entry.toCSV() # for debugging, find a better way to log only when in debug mode
        return entry

    @abstractmethod
    def getRows(self):
        pass

    @abstractmethod
    def extractDate(self,row):
        pass

    @abstractmethod
    def extractBusiness(self, row):
        pass

    @abstractmethod
    def extractRefId(self, row):
        pass

    @abstractmethod
    def extractCredit(self, row):
        pass

    @abstractmethod
    def extractDebit(self, row):
        pass

    @abstractmethod
    def extractBalance(self, row):
        pass


# Process Leumi HTML input file
class LeumiReport(BankReport):
    data = None

    def __init__(self,filename):
        html = HTMLFile(filename).getData()
        assert isinstance(html, object)
        self.data = BeautifulSoup(html, "lxml")

    def getDataTable(self,soup):
        # In the leumi files, the data is in a table with id=ctlActivityTable
        table = soup.find("table", {"id": "ctlActivityTable"})
        return table

    ####################################################################################################################
    # Methods to override
    ####################################################################################################################
    def getRows(self):
        table = self.getDataTable(self.data)
        rows = table.find_all('tr')
        return rows

    def extractDate(self,row):
        # In the leumi files, the date is in a td with class=ExtendedActivityColumnDate
        dateString = myString.strip(row.find("td", {"class": "ExtendedActivityColumnDate"}))
        if(myString.isEmpty(dateString)):
            return None
        date = datetime.strptime(dateString, '%d/%m/%y').date().strftime("%Y-%m-%d")
        return date

    def extractBusiness(self,row):
        # In the leumi files, the action is in a td with either class=ActivityTableColumn1 or class=ActivityTableColumn1LTR
        action1 = myString.strip(row.find("td", {"class": "ActivityTableColumn1"}))
        action2 = myString.strip(row.find("td", {"class": "ActivityTableColumn1LTR"}))
        return action1 + action2

    def extractRefId(self,row):
        # In the leumi files, the refId is in a td with class=ReferenceNumberUniqeClass
        refString = myString.strip(row.find("td", {"class": "ReferenceNumberUniqeClass"}))
        return refString

    def extractCredit(self,row):
        # In the leumi files, the credit is in a td with class=AmountCreditUniqeClass
        data = myString.strip(row.find("td", {"class": "AmountCreditUniqeClass"})).replace(',','')
        if (myString.isEmpty(data)):
            return None
        return Decimal(data)

    def extractDebit(self,row):
        # In the leumi files, the debit is in a td with class=AmountDebitUniqeClass
        data = myString.strip(row.find("td", {"class": "AmountDebitUniqeClass"})).replace(',','')
        if (myString.isEmpty(data)):
            return None
        return Decimal(data)

    def extractBalance(self,row):
        # In the leumi files, the balance is in a td with class=number_column
        # There are 3 such td in each row: debit, credit, balance. Balance is always the 3rd.
        totals = row.find_all("td", {"class": "number_column"})
        total = ""
        if (len(totals) > 1):
            total = myString.strip(totals[2]).replace(',','')
        if(myString.isEmpty(total)):
            return None
        return Decimal(total)


def importFile(htmlFile):
    leumi = LeumiReport(htmlFile)
    leumi.process()

def main():
    htmlFile ='inbox/bankleumi30052018.html'
    importFile(htmlFile)

# TODO: put the main debug routine in its own file
# TODO: extract each class to its own file
# TODO: create bank report factory
# TODO: implement actual logging and debug mode
# TODO: reorganize the project into folders for queries, entities, UI, processors
main()