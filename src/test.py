from src.processors.processLeumiReport import LeumiReport
from src.processors.processVisaCalReport import VisaCalReport
from datetime import datetime


def testImportVISACALReport():
    fileName = "inbox/7872_8547_0205218_Transactions_30_05_2018.xlsx"
    reportDate = datetime(2018, 5, 2)
    cardNum = "7872"
    bankId = "8547"
    visaCal = VisaCalReport(fileName,reportDate,bankId,cardNum)
    #TODO: the date can be extracted from the bank entry when we mark it with hide = 1
    #TODO: handle the case when the credit report is imported before the bank report
    visaCal.process()


def testImportLeumiReport():
    htmlFile ='inbox/bankleumi30052018.html'
    leumi = LeumiReport(htmlFile)
    leumi.process()


def main():
    #testImportLeumiReport()
    testImportVISACALReport()

main()