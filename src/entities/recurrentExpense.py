from sqlobject import *
# from src.myString import myString
from src.entities.bankEntry import BankEntry
from src.entities.businessEntry import BusinessEntry
from src.entities.creditEntry import CreditEntry
from src.sessions.globals import session


class RecurrentExpense(SQLObject):
    TYPE_FIXED = 'FIXED'
    TYPE_VARIABLE = 'VARIABLE'

    # F_MARKBYAMOUNT = 'src/queries/markRecurringByAmount.sql'
    # Q_MARKBANKENTRYBYBUSINESS = 'UPDATE bank_entry SET tracker_id = <tracker> WHERE business = <business>'
    # Q_MARKCREDITENTRYBYBUSINESS = 'UPDATE credit_entry SET tracker_id = <tracker> WHERE business = <business>'

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
    userId = StringCol()

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

    # TODO: add user Id parameter to teh update queries
    # pandas does not support update statements, use SQLObj to select then update ( less efficient :( )
    # UPDATE bank_entry SET tracker_id = < tracker >
    # WHERE business IN(SELECT id FROM business_entry WHERE marketing_name ~ '.*check.*')
    # AND debit = < amount >
    def markByAmount(self):
        # params = [
        #     {'name': 'tracker', 'value': [str(self.id)]},
        #     {'name': 'amount', 'value': [str(self.amount)]}
        # ]
        #db.runUpdateFromFile(self.F_MARKBYAMOUNT, params)

        businesses = BusinessEntry.select(AND(LIKE(BusinessEntry.q.marketingName,"%check%"),BusinessEntry.q.userId == session.getUserId()))
        businessIds = []
        for b in businesses:
            businessIds.append(b.id)

        bankEntries = BankEntry.select(AND(BankEntry.q.debit == self.amount,IN(BankEntry.q.business,businessIds),BusinessEntry.q.userId == session.getUserId()))
        for e in bankEntries:
            e.trackerId = self.id

    #pandas does not support update statements, use SQLObj to select then update ( less efficient :( )
    def markByBusiness(self):
        # params = [
        #     {'name': 'tracker', 'value': [str(self.id)]},
        #     {'name': 'business', 'value': [str(self.businessId)]}
        # ]
        #db.runUpdate(self.Q_MARKBANKENTRYBYBUSINESS, params)
        #db.runUpdate(self.Q_MARKCREDITENTRYBYBUSINESS, params)

        bankEntries = BankEntry.selectBy(business=self.businessId, userId=session.getUserId())
        for e in bankEntries:
            e.trackerId = self.id

        creditEntries = CreditEntry.selectBy(business=self.businessId, userId=session.getUserId())
        for c in creditEntries:
            c.trackerId = self.id




