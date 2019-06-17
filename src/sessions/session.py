from src.user import User
from src.sessions.environment import env
from src.sessions.googleOAuth import GoogleOAuth

# Use authenticated token info to lookup user in the db and return user data (open a session)
# If user not found, add it to the db
class Session:
    oAuth = None
    db = None
    currentUser = None
    token = None

    def __init__(self):
        clientId = env['GOOGLE_OAUTH']['client_id']
        self.oAuth = GoogleOAuth(clientId)
        self.currentUser = None
        self.token = None

    def authenticate(self,token):
        self.currentUser = None
        tokenInfo = self.oAuth.verifyToken(token)
        if tokenInfo is not None:
            self.currentUser = self.getUser(tokenInfo)
            self.token = token
        return self.currentUser

    def getUser(self,tokenInfo):
        #If user not found in DB, create new
        return User(tokenInfo)

    def logout(self):
        self.currentUser = None
        self.oAuth.revokeToken(self.token)

