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


class CardData:
    cardNumber = ""
    reportDate = None
    total = 0

    def __init__(self, cardNumber, reportDate):
        self.cardNumber = cardNumber
        self.reportDate = reportDate

    def setTotal(self,total):
        self.total = total


# Convert XLS to XLSX so it can be parsed
# https://stackoverflow.com/questions/9918646/how-to-convert-xls-to-xlsx

class IsraCardReport(CreditReport):
    data = None
    cards = []

    def __init__(self,filename):
        self.data = XLSFile(filename).getData()
        #self.parseReportDate()

    def processHeader(self,row):
        cardString = str(row[0].internal_value)
        reportDate = str(row[2].internal_value)
        end = len(cardString)
        start = end-4
        cardNumber = cardString[start:end]
        cardData = CardData(cardNumber, reportDate)
        self.cards.append(cardData)
        return cardData

    def processAll(self):
        start = 4
        while start > 0:
            start = self.processCard(start)
        print("stop")

    def getRows(self,start):
        rows = self.data.iter_rows(min_row=start, min_col=1, max_col=5)
        return rows

    def processCard(self, start):
        stop = False
        skip = 1
        nrow = start
        rows = self.getRows(start)
        card = None

        # TODO: handle total row
        for row in rows:
            if nrow == start:
                card = self.processHeader(row)
            else:
                stop = self.processRow(row,card)
            nrow = nrow + 1
            if stop:
                return nrow + skip # add one to skip the empty row
        return 0 # reached the end of the sheet, no more rows

    def processRow(self,row,card):
        purchaseDate = self.extractPurchaseDate(row)
        businessName = self.extractBusinessName(row)
        amount = self.extractAmount(row)
        currency = self.extractCurrency(row)

        reportDate = card.reportDate
        cardNumber = card.cardNumber

        # TODO: use total row or compute it?
        #ComputeTotals returns true if an entry should be created
        if self.computeTotals(businessName,reportDate,amount):
            self.addCreditEntry(reportDate, purchaseDate, businessName,
                                self.getCardNumber(), self.bankReportRefId, amount)


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