from src.myString import myString
from datetime import datetime
from src.processors.processXslxFile import XSLXFile
from src.processors.processCreditReport import CreditReport

#This report includes multiple cards for only for a single month
#TODO: the card numbers and report date are there
#TODO: extract the card number from the report?

class IsraCardReport(CreditReport):
    data = None
    reportDate = None

    def __init__(self,filename,cardNumber):
        self.data = XSLXFile(filename).getData()
        self.setCardNumber(cardNumber)
        self.parseReportDate()


    ####################################################################################################################
    # Methods to override
    ####################################################################################################################

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
        return self.reportDate

    def parseReportDate(self):
        #TODO: The date is probably wrong, let it slide for now, correct it later
        cell = self.data.cell(1,1).value
        date = cell[25:35]
        self.reportDate = datetime.strptime(date, '%d/%m/%Y').date().strftime("%Y-%m-%d")
        return self.reportDate


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

    def computeTotals(self,business,date,amount):
        if (myString.isEmpty(business)):
            self.addTotal(date,amount)
            skip = False
        return True