
# TODO: make this an SQLObject ?
# TODO: use seesion.currentUser.Id in all queries to import, save or load data
# No need to store the user info, I get it all from Google when I authenticate the session
# All I need is a predictable hash so I can tag all the data, but no use for a users table
class User:
    id = None  # hash of google Id
    googleId = None
    email = None
    name = None
    picture = None

    def __init__(self,tokenInfo):
        self.googleId = tokenInfo['sub']
        self.email = tokenInfo['email']
        self.name = tokenInfo['name']
        self.picture = tokenInfo['picture']
        self.id = self.hash(self.googleId)

    def hash(self,input):
        return input  #TODO: use an actual hash
