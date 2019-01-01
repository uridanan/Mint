from src.myString import myString
from datetime import datetime
from src.processors.processXlsFile import XLSFile
from src.processors.processCreditReport import CreditReport

#This report includes multiple cards for only for a single month
#TODO: the card numbers and report date are there
#TODO: extract the card number from the report?

# First card starts at row 4 (counting from 1)
# Card number is in row 4 cell 1
# Report date is in row 4 cell 3
# rows start at cardnumber + 3
# purchase date in cell 1
# business in cell 2
# amount in cell 5
# currency in cell 6
# Total and end of report in the first row with cell 1 empty
# Next card number starts on total + 2 or next non-empty cell 1

# Convert XLS to XLSX so it can be parsed
# https://stackoverflow.com/questions/9918646/how-to-convert-xls-to-xlsx

class IsraCardReport(CreditReport):
    data = None
    reportDate = None

    def __init__(self,filename):
        self.data = XLSFile(filename).getData()
        #self.parseReportDate()


    def processReportHeader(self,row,data):
        cardNumber = str(row[0].internal_value)
        reportDate = str(row[2].internal_value)
        end = len(cardNumber)
        start = end-4
        data["cardNumber"] = cardNumber[start:end]
        data["reportDate"] = reportDate

    def processAll(self):
        firstRow = self.getFirstRow()
        data = {"cardNumber": "", "reportDate": None}
        self.processReportHeader(firstRow,data)
        print("stop")

    def getFirstRow(self):
        rows = self.getRows()
        for row in rows:
            return row


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