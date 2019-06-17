from src.utils.myString import myString
from bs4 import BeautifulSoup
from datetime import datetime
from decimal import Decimal
from src.processors.processBankReport import BankReport
from src.processors.processHTMLFile import HTMLFile


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

