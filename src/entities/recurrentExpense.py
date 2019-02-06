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

    def update(self, businessId, name, type, amount,
               count, startDate, lastDate,
               avgAmount, minAmount, maxAmount):
        self.businessId=businessId
        self.name=name
        self.type=type
        self.amount=amount
        self.count=count
        self.startDate=startDate
        self.lastDate=lastDate
        self.avgAmount=avgAmount
        self.minAmount=minAmount
        self.maxAmount=maxAmount


