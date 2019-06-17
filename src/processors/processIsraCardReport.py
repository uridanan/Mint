from src.utils.myString import myString
from datetime import datetime
from src.processors.processXlsFile import XLSFile
from src.processors.processCreditReport import CreditReport


# This report includes multiple cards for only for a single month
# Because it is different from the other reports, we will override processRows

# First card starts at row 4 (counting from 1)
# Card number is in row 4 cell 0
# Report date is in row 4 cell 2
# rows start at cardnumber + 3
# purchase date in cell 0
# business in cell 1
# amount in cell 4
# currency in cell 5
# Total and end of report in the first row with cell 1 empty
# Next card number starts on total + 2 or next non-empty cell 1


class IsraCardReport(CreditReport):
    data = None
    cardNumber = None
    reportDate = None

    def __init__(self,filename):
        self.data = XLSFile(filename).getData()

    def processRows(self):
        start = 4
        while start > 0:
            start = self.processCard(start)
        print("stop")

    def processCard(self, start):
        stop = False
        skip = 1
        nrow = start
        rows = self.getRowsFromX(start)

        for row in rows:
            if nrow == start:
                self.processHeader(row)
            elif nrow < start + 3:
                stop = False
            else:
                stop = self.processRow(row)
            nrow = nrow + 1
            if stop:
                return nrow + skip  # add one to skip the empty row
        return 0  # reached the end of the sheet, no more rows

    def getRowsFromX(self,start):
        rows = self.data.iter_rows(min_row=start, min_col=1, max_col=8)
        return rows

    def processHeader(self,row):
        cardString = str(row[0].internal_value)
        dateString = str(row[2].internal_value)
        end = len(cardString)
        start = end-4
        cardNumber = cardString[start:end]
        reportDate = datetime.strptime(dateString, '%d/%m/%y').date().strftime("%Y-%m-%d")
        self.setCardNumber(cardNumber)
        self.setReportDate(reportDate)

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
        #rows = self.data.iter_rows(min_row=4, min_col=1, max_col=8)
        return None

    def extractPurchaseDate(self,row):
        dateString = str(row[0].internal_value)
        if (myString.isEmpty(dateString)):
            return None
        try:
            date = datetime.strptime(dateString, '%d/%m/%Y').date().strftime("%Y-%m-%d")
        except:
            date = None
        return date

    def extractReportDate(self,row):
        return self.getReportDate()

    def extractAmount(self,row):
        amount = row[4].internal_value
        return amount

    def extractBusinessName(self, row):
        name = row[1].internal_value
        return name

    def extractComment(self,row):
        comment = row[7].internal_value
        return comment

    def extractCurrency(self,row):
        currency = row[5].internal_value
        return currency

    def isMonthlyTotal(self,row):
        purchaseDate = self.extractPurchaseDate(row)
        return purchaseDate is None

    def computeMonthlyTotal(self, row):
        reportDate = self.extractReportDate(row)
        amount = self.extractAmount(row)
        cardNumber = self.getCardNumber()
        if (self.isMonthlyTotal(row)):
            self.addMonthlyTotal(cardNumber, reportDate, amount)
            return True
        return False
