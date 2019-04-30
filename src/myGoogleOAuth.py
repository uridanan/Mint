# Extend the GoogleOAuth class to make the response available

from flask import Flask, session, abort
from dash_google_auth import GoogleOAuth
from flask_dance.contrib.google import google


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
            return abort(403)

    def getResp(self):
        return self.resp

    def getEmail(self):
        return self.email
