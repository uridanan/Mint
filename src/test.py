from src.processors.processLeumiReport import LeumiReport




def testImportVISACALReport():
    CreditEntry.createTable(ifNotExists=True)
    BusinessEntry.createTable(ifNotExists=True)
    fileName = "inbox/7872_8547_0205218_Transactions_30_05_2018.xlsx"
    sheet = loadFile(fileName)
    #TODO: the date can be extracted from the bank entry when we mark it with hide = 1
    date = datetime(2018,5,2)
    cardNum = "7872"
    bankId = "8547" #replace with the actual value
    process(sheet, date)


def testImportLeumiReport():
    htmlFile ='inbox/bankleumi30052018.html'
    leumi = LeumiReport(htmlFile)
    leumi.process()


def main():
    testImportLeumiReport()


main()