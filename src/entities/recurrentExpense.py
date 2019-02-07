from sqlobject import *
import src.connection
import src.dbAccess as db
# from src.myString import myString


class RecurrentExpense(SQLObject):
    TYPE_FIXED = 'FIXED'
    TYPE_VARIABLE = 'VARIABLE'

    F_MARKBYAMOUNT = 'src/queries/markRecurringByAmount.sql'
    Q_MARKBANKENTRYBYBUSINESS = 'UPDATE bank_entry SET tracker_id = <tracker> WHERE business = <business>'
    Q_MARKCREDITENTRYBYBUSINESS = 'UPDATE credit_entry SET tracker_id = <tracker> WHERE business = <business>'

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

    def markExpenses(self):
        if self.type == self.TYPE_VARIABLE:
            self.markByBusiness()
        else:
            self.markByAmount()

    def markByAmount(self):
        params = [
            {'name': 'tracker', 'value': [str(self.id)]},
            {'name': 'amount', 'value': [str(self.amount)]}
        ]
        #db.runUpdateFromFile(self.F_MARKBYAMOUNT, params)

    def markByBusiness(self):
        params = [
            {'name': 'tracker', 'value': [str(self.id)]},
            {'name': 'business', 'value': [str(self.businessId)]}
        ]
        #db.runUpdate(self.Q_MARKBANKENTRYBYBUSINESS, params)
        #db.runUpdate(self.Q_MARKCREDITENTRYBYBUSINESS, params)


# TODO: pandas does not support update statements, use SQLObj to select then update ( less efficient :( )

