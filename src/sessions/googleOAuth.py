# To use this file, you need to run
# pip install --upgrade google-auth
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as authRequests

# (Receive token by HTTPS POST)
# ...

class GoogleOAuth:
    client_id = None

    def __init__(self,clientId):
        self.client_id = clientId

    def verifyToken(self,token):
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, authRequests.Request(), self.client_id)

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
            return idinfo
        except ValueError:
            # Invalid token
            return None

    def revokeToken(self,token):
        requests.post('https://accounts.google.com/o/oauth2/revoke',
                      params={'token': token},
                      headers={'content-type': 'application/x-www-form-urlencoded'})