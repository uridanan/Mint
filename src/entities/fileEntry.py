from sqlobject import *


# This class encapsulates methods to manipulate data entries
# Including import / export methods

class FileEntry(SQLObject):
    userId = StringCol()
    source = StringCol()
    reportDate = StringCol()
    refId = StringCol()  #card or account number
    total = FloatCol()
    flagged = BoolCol()
    # startDate = DateCol()
    # endDate = DateCol()
    # fileName = StringCol()
