from src.processors.processLeumiReport import LeumiReport


def testImportLeumiReport():
    htmlFile ='inbox/bankleumi30052018.html'
    leumi = LeumiReport(htmlFile)
    leumi.process()


def main():
    testImportLeumiReport()


main()