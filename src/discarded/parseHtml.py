import lxml
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup
import requests
from src.myString import myString
from src.entities.bankEntry import BankEntry
from src.entities.businessEntry import BusinessEntry
from datetime import datetime
from decimal import Decimal


def example():
    url = 'http://www.google.com'
    r = requests.get("http://" + url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    for link in soup.find_all('a'):
        print(link.get('href'))


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
        soup = BeautifulSoup(htmlInput, "lxml")
        table = self.getDataTable(soup)
        for row in table.find_all('tr'):
            e = self.processRow(row)
            if(e != None):
                e.toCSV()

    def processRow(self,row):
        date = self.extractDate(row)
        action = self.extractAction(row)
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
        return entry

    ####################################################################################################################
    # Methods to override
    ####################################################################################################################
    def getDataTable(self,soup):
        # In the leumi files, the data is in a table with id=ctlActivityTable
        return soup.find("table", {"id": "ctlActivityTable"})

    def extractDate(self,row):
        # In the leumi files, the date is in a td with class=ExtendedActivityColumnDate
        dateString = myString.strip(row.find("td", {"class": "ExtendedActivityColumnDate"}))
        if(myString.isEmpty(dateString)):
            return None

        date = datetime.strptime(dateString, '%d/%m/%y').date().strftime("%Y-%m-%d")
        return date

    def extractAction(self,row):
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


def main():
    BankEntry.createTable(ifNotExists=True)
    BusinessEntry.createTable(ifNotExists=True)
    htmlFile ='inbox/bankleumi30052018.html'
    processor = LeumiProcessor()
    processor.importFile(htmlFile)


main()