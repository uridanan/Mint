from sqlobject import *


# This class encapsulates methods to manipulate data entries
# Including import / export methods

class FileEntry(SQLObject):
    userId = StringCol()
    source = StringCol()
    reportDate = StringCol()
    refId = StringCol()  #card or account number
    total = FloatCol()
    # startDate = DateCol()
    # endDate = DateCol()
    # fileName = StringCol()
