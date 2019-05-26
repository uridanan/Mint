import sqlobject
from sqlobject import *
import src.connection
from src.myString import myString

# This class encapsulates methods to manipulate data entries
# Including import / export methods


class user(SQLObject):
    id = DateCol(default=None)
    name = StringCol(default=None)
    email = StringCol(default=None)
    picture = StringCol(default=None)
    token = StringCol(default=None)

    def isLoggedIn(self):
        return self.token is None

    def logout(self):
        self.token = None

    def login(self,token):
        self.id = self.token.json().get('id')
        #...
        #Actually, create new user or fetch from DB
        #When creating new, add to authorized emails


