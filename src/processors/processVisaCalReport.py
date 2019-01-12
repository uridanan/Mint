from src.myString import myString
from datetime import datetime
from src.processors.processXlsxFile import XLSXFile
from src.processors.processCreditReport import CreditReport
import re

# This report includes a single card for a single month
# TODO: Convert from XLS to XLSX automatically

class VisaCalReport(CreditReport):
    data = None
    reportDate = None
    cardNumber = None

    def __init__(self,filename):
        self.data = XLSXFile(filename).getData()
        self.parseCardNumberAndReportDate()

    # In cell A2
    # פירוט עסקות הכל לכרטיס ויזה זהב עסקי, המסתיים בספרות 7872, בבנק לאומי לישראל, חשבון מס' 678-8841076, לתאריך חיוב 05/2018, לעסקות שבוצעו בארץ ובחו''ל
    def parseCardNumberAndReportDate(self):
        cell = self.data.cell(2, 1).value
        numbers = re.findall('\d+', cell)
        card = numbers[0]
        branch = numbers[1]
        account = numbers[2]
        month = numbers[3]
        year = numbers[4]
        self.setCardNumber(card)
        self.setReportDate(datetime(int(year),int(month),1).date().strftime("%Y-%m-%d"))

    def getReportDate(self):
        return self.reportDate

    def setReportDate(self, date):
        self.reportDate = date

    ####################################################################################################################
    # Methods to override
    ####################################################################################################################

    def getCardNumber(self):
        return self.cardNumber

    def setCardNumber(self, number):
        self.cardNumber = number

    def getRows(self):
        rows = self.data.iter_rows(min_row=4, min_col=1, max_col=5)
        return rows

    def extractPurchaseDate(self,row):
        dateString = str(row[0].internal_value)
        if (myString.isEmpty(dateString)):
            return None
        try:
            date = datetime.strptime(dateString, '%Y-%m-%d %H:%M:%S').date().strftime("%Y-%m-%d")
        except:
            date = None
        return date

    def extractReportDate(self,row):
        return self.getReportDate()


    def extractAmount(self,row):
        amount = row[3].internal_value
        if (myString.isEmpty(amount)):
            return None
        amount = amount.replace(',', '')
        creditStr = amount[1:len(amount)]
        credit = float(creditStr)
        return credit

    def extractBusinessName(self, row):
        name = row[1].internal_value
        return name

    def extractComment(self,row):
        comment = row[4].internal_value
        return comment

    def extractCurrency(self,row):
        amount = row[3].internal_value
        if (myString.isEmpty(amount)):
            return None
        currency = amount[0:1]
        return currency

    def isMonthlyTotal(self,row):
        businessName = self.extractBusinessName(row)
        return myString.isEmpty(businessName)

    def computeMonthlyTotal(self, row):
        reportDate = self.extractReportDate(row)
        amount = self.extractAmount(row)
        cardNumber = self.getCardNumber()
        if (self.isMonthlyTotal(row)):
            self.addMonthlyTotal(cardNumber, reportDate, amount)
            return True
        return False