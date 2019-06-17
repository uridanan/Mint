# Extend the GoogleOAuth class to make the response available

from flask import Flask, session, abort, redirect, url_for, Response
from dash_google_auth import GoogleOAuth
from flask_dance.contrib.google import google

# TODO: make this a member of the class and override init
# TODO: write a HOW TO guide and sample app and add as separate project in GITHUB
SIGNIN = 'signin'

class MyGoogleOAuth(GoogleOAuth):
    def is_authorized(self):
        if not google.authorized:
            # send to google login
            return False

        self.resp = google.get("/oauth2/v2/userinfo")
        assert self.resp.ok, self.resp.text

        self.email = session['email'] = self.resp.json().get('email')
        self.id = session['id'] = self.resp.json().get('id')
        self.name = session['name'] = self.resp.json().get('name')
        self.picture = session['picture'] = self.resp.json().get('picture')
        if self.email in self.authorized_emails:
            # send to index
            return True
        else:
            # unauthorized email
            return False  #self.login_fail()

    def login_fail(self):
        #return abort(403)
        return redirect(SIGNIN)
        #return redirect(url_for(SIGNIN))


    def login_request(self):
        # send to google auth page
        # TODO: this is where I need to redirect to my login page
        #dcc.Location(id='url', refresh=False),
        return redirect(url_for("google.login"))

    def auth_wrapper(self, f):
        def wrap(*args, **kwargs):
            if not self.is_authorized():  # and kwargs.get('path','/') != SIGNIN:
                return self.login_fail()
                #return self.login_request()  #Response(status=403)

            response = f(*args, **kwargs)
            return response
        return wrap

    def index_auth_wrapper(self, original_index):
        def wrap(*args, **kwargs):
            if self.is_authorized():
                return original_index(*args, **kwargs)
            else:
                return self.login_fail()
                #return self.login_request()
        return wrap

    def getResp(self):
        return self.resp

    def getEmail(self):
        return self.email

    def logout(self):
        if 'google_oauth_token' in session:
            del session['google_oauth_token']
        return redirect(SIGNIN)
