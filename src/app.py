import os
from src.environment import env
from src.myGoogleOAuth import MyGoogleOAuth
from dash import Dash
from flask import Flask


# How to build a multi-page app
# https://dash.plot.ly/urls
# https://github.com/plotly/dash/issues/133
# Cool Themes: https://1stwebdesigner.com/free-bootstrap-dashboard-templates/

# GOOGLE_OAUTH_CLIENT_ID: set this to the client ID you got from Google.
# GOOGLE_OAUTH_CLIENT_SECRET: set this to the client secret you got from Google.
# OAUTHLIB_RELAX_TOKEN_SCOPE: set this to true. This indicates that it's OK for Google to return different OAuth scopes than requested; Google does that sometimes.
# OAUTHLIB_INSECURE_TRANSPORT: set this to true. This indicates that you're doing local testing, and it's OK to use HTTP instead of HTTPS for OAuth. You should only do this for local testing. Do not set this in production! [oauthlib docs]

#=====================================================================================================================
# Configure server for Google Sign in
#Authorized URI: http://localhost:8050/login/google/authorized
server = Flask(__name__)
server.secret_key = env['SERVER']['secret_key']
server.config["GOOGLE_OAUTH_CLIENT_ID"] = env['GOOGLE_OAUTH']['client_id'] #os.environ["GOOGLE_OAUTH_CLIENT_ID"]
server.config["GOOGLE_OAUTH_CLIENT_SECRET"] = env['GOOGLE_OAUTH']['client_secret'] #os.environ["GOOGLE_OAUTH_CLIENT_SECRET"]

# allow for insecure transport for local testing (remove in prod)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# designate list of authorized emails
authorized_emails = env['GOOGLE_OAUTH']['authorized_emails']
additional_scopes = []


#=====================================================================================================================
# Dash App

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets, server=server, url_base_pathname='/', auth='auth')
# server = app.server
app.config.suppress_callback_exceptions = True
# app.config['suppress_callback_exceptions']=True

auth = MyGoogleOAuth(app, authorized_emails, additional_scopes)


@server.route("/")
def MyDashApp():
    return app.index()


# TODO: create login display in the sidebar
# TODO: figure out what hash to use in the DB
# TODO: figure out how to signout
# TODO: figure out how to create a landing page with a Google Button before authenticating

