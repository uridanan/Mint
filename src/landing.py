#! /usr/bin/env python

# Example app

import os

import dash_core_components as dcc
import dash_html_components as html

from dash import Dash
from dash.dependencies import Input, Output
from flask import Flask, session, abort
from src.environment import env

from dash_google_auth import GoogleOAuth
from flask_dance.contrib.google import (
    make_google_blueprint,
    google,
)


# configure app
server = Flask(__name__)
app = Dash(
    __name__,
    server=server,
    url_base_pathname='/',
    auth='auth',
)
app.config['suppress_callback_exceptions']=True
#
# # configure google oauth using environment variables
# server.secret_key = env['SERVER']['secret_key']
# server.config["GOOGLE_OAUTH_CLIENT_ID"] = env['GOOGLE_OAUTH']['client_id'] #os.environ["GOOGLE_OAUTH_CLIENT_ID"]
# server.config["GOOGLE_OAUTH_CLIENT_SECRET"] = env['GOOGLE_OAUTH']['client_secret'] #os.environ["GOOGLE_OAUTH_CLIENT_SECRET"]
#
# # allow for insecure transport for local testing (remove in prod)
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
#
# # designate list of authorized emails
# authorized_emails = env['GOOGLE_OAUTH']['authorized_emails']
#
# auth = MyGoogleOAuth(
#     app,
#     authorized_emails,
# )


@server.route("/")
def MyDashApp():
    return app.index()

@server.route("/landing")
def MyDashApp():
    return app.index()

import src.signin

app.layout = src.signin.layout
#
# @app.callback(
#     Output('welcome', 'children'),
#     [Input('placeholder', 'value')]
# )
# def on_load(value):
#     resp = auth.getResp()
#     email = auth.getEmail()
#     return "Welcome, {}!".format(session['email'])

if __name__ == '__main__':
    app.run_server(host='localhost')