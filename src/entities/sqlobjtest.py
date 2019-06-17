from sqlobject import *


class Person(SQLObject):
    #_connection = conn
    firstName = StringCol()
    middleInitial = StringCol(length=1, default=None)
    lastName = StringCol()


#Person.createTable(ifNotExists=True)

#p1 = Person(firstName='John', middleInitial='F', lastName='Doe')
p2 = Person.get(1)
p2.middleInitial = 'K'