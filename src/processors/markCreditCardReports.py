from src.entities.bankEntry import BankEntry
from src.entities.fileEntry import FileEntry
from datetime import datetime, timedelta
from sqlobject.sqlbuilder import AND
from src.sessions.globals import session

class BankEntriesPostProcessor:
    #lookup by month and amount
    @staticmethod
    def hideCreditCardReport(inputDate, inputTotal):
        reportDate = datetime.strptime(inputDate, '%Y-%m-%d').date()
        start = datetime(reportDate.year,reportDate.month,1).date()
        end = datetime(reportDate.year,reportDate.month,28).date()
        # delta = timedelta(days=3)
        # start = reportDate - delta
        # end = reportDate + delta
        bList = BankEntry.select(AND(BankEntry.q.userId == session.getUserId(), BankEntry.q.date >= start, BankEntry.q.date <= end, BankEntry.q.debit == inputTotal))
        found = False
        for b in bList:
            b.hide = 1
            found = True
        return found

    #lookup entries that match credit reports
    @staticmethod
    def hideCreditCardReports():
        fList = FileEntry.select(AND( FileEntry.q.userId == session.getUserId(), FileEntry.total is not None, FileEntry.q.flagged == False))
        #Bank entries are flagged on creation so they will not appear here
        for f in fList:
            if BankEntriesPostProcessor.hideCreditCardReport(f.reportDate, f.total):
                f.flagged = True
