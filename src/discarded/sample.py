#! /usr/bin/env python

# Example app

import os

import dash_core_components as dcc
import dash_html_components as html

from dash import Dash
from dash.dependencies import Input, Output
from flask import Flask, session, abort
from src.discarded.environment import env

from dash_google_auth import GoogleOAuth
from flask_dance.contrib.google import (
    google,
)

class MyGoogleOAuth(GoogleOAuth):
    def is_authorized(self):
        if not google.authorized:
            # send to google login
            return False

        self.resp = google.get("/oauth2/v2/userinfo")
        assert self.resp.ok, self.resp.text

        self.email = session['email'] = self.resp.json().get('email')
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



# configure app
server = Flask(__name__)
app = Dash(
    __name__,
    server=server,
    url_base_pathname='/',
    auth='auth',
)
app.config['suppress_callback_exceptions']=True

# configure google oauth using environment variables
server.secret_key = env['SERVER']['secret_key']
server.config["GOOGLE_OAUTH_CLIENT_ID"] = env['GOOGLE_OAUTH']['client_id'] #os.environ["GOOGLE_OAUTH_CLIENT_ID"]
server.config["GOOGLE_OAUTH_CLIENT_SECRET"] = env['GOOGLE_OAUTH']['client_secret'] #os.environ["GOOGLE_OAUTH_CLIENT_SECRET"]

# allow for insecure transport for local testing (remove in prod)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# designate list of authorized emails
authorized_emails = env['GOOGLE_OAUTH']['authorized_emails']

auth = MyGoogleOAuth(
    app,
    authorized_emails,
)


@server.route("/")
def MyDashApp():
    return app.index()


app.layout = html.Div(children=[
    html.H1(children="Private Dash App"),

    html.Div(id='placeholder', style={'display':'none'}),
    html.Div(id='welcome'),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 6], 'type': 'bar', 'name': 'Montreal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

@app.callback(
    Output('welcome', 'children'),
    [Input('placeholder', 'value')]
)
def on_load(value):
    resp = auth.getResp()
    email = auth.getEmail()
    return "Welcome, {}!".format(session['email'])

if __name__ == '__main__':
    app.run_server(host='localhost')