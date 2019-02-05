from sqlobject import *
import src.connection
# from src.myString import myString


class RecurrentExpense(SQLObject):
    name = StringCol()
    businessId = IntCol()
    amount = CurrencyCol()
    type = StringCol()
    count = IntCol()
    startDate = DateCol()
    lastDate = DateCol()
    avgAmount = CurrencyCol()
    maxAmount = CurrencyCol()
    minAmount = CurrencyCol()


