from src.processors.processLeumiReport import LeumiReport
from src.processors.processVisaCalReport import VisaCalReport
from src.processors.processLeumiCardReport import LeumiCardReport
from src.processors.processIsraCardReport import IsraCardReport
from datetime import datetime

# TODO: change to XLS instead of XLSX
def testImportVISACALReport():
    fileName = "inbox/7872_8547_0205218_Transactions_30_05_2018.xlsx"
    visaCal = VisaCalReport(fileName)
    visaCal.process()

def testImportLeumiCardReport():
    fileName = "inbox/4014_Deals.xlsx"
    cardNum = "4014"
    visaCal = LeumiCardReport(fileName,cardNum)
    visaCal.process()

def testImportLeumiReport():
    htmlFile ='inbox/bankleumi30052018.html'
    leumi = LeumiReport(htmlFile)
    leumi.process()

def testImportIsraCardReport():
    fileName ='inbox/AMEX_Export_03_2018.xls'
    amex = IsraCardReport(fileName)
    amex.process()

def main():
    testImportLeumiReport()
    testImportIsraCardReport()
    testImportVISACALReport()
    testImportLeumiCardReport()

main()