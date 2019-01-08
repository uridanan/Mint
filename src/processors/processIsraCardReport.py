from src.myString import myString
from datetime import datetime
from src.processors.processXlsFile import XLSFile
from src.processors.processCreditReport import CreditReport

#This report includes multiple cards for only for a single month

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

    def __init__(self,filename):
        self.data = XLSFile(filename).getData()
        #self.parseReportDate()

    # ------------------------------------------------------------------------------------------------------------------
    # Process the data
    # ------------------------------------------------------------------------------------------------------------------

    def processHeader(self,row):
        cardString = str(row[0].internal_value)
        reportDate = str(row[2].internal_value)
        end = len(cardString)
        start = end-4
        cardNumber = cardString[start:end]
        cardData = CardData(cardNumber, reportDate)
        #self.cards.append(cardData)
        return cardData

    # TODO: rename to processRows
    def processAll(self):
        start = 4
        while start > 0:
            start = self.processCard(start)
        print("stop")

    def getRowsFromX(self,start):
        rows = self.data.iter_rows(min_row=start, min_col=1, max_col=8)
        return rows

    def processCard(self, start):
        stop = False
        skip = 1
        nrow = start
        rows = self.getRowsFromX(start)
        card = None

        for row in rows:
            if nrow == start:
                self.currentCard = self.processHeader(row)
            elif nrow < start + 3:
                stop = False
            else:
                stop = self.processRow(row)
            nrow = nrow + 1
            if stop:
                return nrow + skip  # add one to skip the empty row
        return 0  # reached the end of the sheet, no more rows

    def getReportDate(self):
        return self.currentCard.reportDate

    def getCardNumber(self):
        return self.currentCard.cardNumber

    def processRow(self,row):
        purchaseDate = self.extractPurchaseDate(row)
        businessName = self.extractBusinessName(row)
        amount = self.extractAmount(row)
        currency = self.extractCurrency(row)

        reportDate = self.getReportDate()
        cardNumber = self.getCardNumber()


        # TODO: refactor to match the other cards
        # ComputeTotals returns true if an entry should be created
        if self.computeTotals(businessName,reportDate,amount,purchaseDate):
            self.addCreditEntry(reportDate, purchaseDate, businessName,
                                cardNumber, self.bankReportRefId, amount)
            return False

        # This was a total row, purchaseDate is None
        return True

    # ------------------------------------------------------------------------------------------------------------------
    # Serve the data to the superclass
    # ------------------------------------------------------------------------------------------------------------------

    ####################################################################################################################
    # Methods to override
    ####################################################################################################################

    def getRows(self):
        rows = self.data.iter_rows(min_row=4, min_col=1, max_col=8)
        return rows

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
        return self.reportDate

    def parseReportDate(self):
        return self.reportDate


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

    def computeTotals(self,business,reportDate,amount,purchaseDate):
        if purchaseDate is None:
            self.addTotal(reportDate, amount)
            self.currentCard.total = amount
            self.cards.append(self.currentCard)
            return False
        return True


#TODO: prepare data to return in getRows (actually I probably won't need to), setup the cards with totals and report dates, then process everything in CreditReport
#TODO: option 2 - make sure cards is generic, then override processRows