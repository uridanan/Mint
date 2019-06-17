
# TODO: make this an SQLObject
class User:
    id = None # hash of google Id
    googleId = None
    email = None
    name = None
    picture = None

    def __init__(self,tokenInfo):
        self.googleId = tokenInfo['sub']
        self.email = tokenInfo['email']
        self.name = tokenInfo['name']
        self.picture = tokenInfo['picture']
        self.id = self.googleId  # for now, later we'll use a hash so we don't store GoogleIds in the DB
