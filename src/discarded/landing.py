#! /usr/bin/env python

# Example app

import os

import dash_core_components as dcc
import dash_html_components as html

from dash import Dash
from dash.dependencies import Input, Output
from flask import Flask, url_for, render_template
from src.discarded.environment import env
from src.discarded.myGoogleOAuth import MyGoogleOAuth
from src.discarded import signin

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


# @server.route("/landing")
# def MyDashApp():
#     return app.index()


#
# @app.callback(
#     Output('welcome', 'children'),
#     [Input('placeholder', 'value')]
# )
# def on_load(value):
#     resp = auth.getResp()
#     email = auth.getEmail()
#     return "Welcome, {}!".format(session['email'])

appLayout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.H1(id='title', children='Welcome to Clarity'),
    html.Div(id='content',className='content'),
])

# signinLayout = html.Div(children=[
#     dcc.Location(id='url', refresh=False),
#     html.H1(id='title', children='Welcome to Clarity'),
#     html.Div(id='content',className='content', children=[
#         dcc.Link(id='googlesignin', children=['Sign in with Google'], href='/')
#     ]),
# ])


# def serve_layout():
#     if flask.has_request_context():
#         return signin.signin
#     return appLayout
#
#
# app.layout = serve_layout

app.layout = appLayout

@app.callback(Output('content', 'children'), [Input('url', 'pathname')])
def display_app(pageName):
    if pageName == '/signin':
        return signin.signin
    else:
        return signin.layout


@app.callback(Output('googlesignin', 'href'), [Input('url', 'pathname')])
def display_app(pageName):
    if pageName == '/signin':
        return url_for("google.login")
    else:
        return '/'


# @server.route("/")
# def MyDashApp():
#     return app.index()


@server.route("/signin")
def signin():
    return render_template('signin.html')


# TODO: use serve layout to dynamically change the layout - didn't work
# TODO: use route and HTML to display signin. Figure out how to send googleId back to app and reroute into the app

# https://dash.plot.ly/urls
if __name__ == '__main__':
    app.run_server(debug=True,host='localhost')


# from flask import Flask, redirect, url_for, render_template, request, abort
# app = Flask(__name__)
#
# @app.route('/')
# def index():
#    return render_template('log_in.html')
#
# @app.route('/login',methods = ['POST', 'GET'])
# def login():
#    if request.method == 'POST':
#       if request.form['username'] == 'admin' :
#          return redirect(url_for('success'))
#       else:
#          abort(401)
#    else:
#       return redirect(url_for('index'))
#
# @app.route('/success')
# def success():
#    return 'logged in successfully'
#
# if __name__ == '__main__':
#    app.run(debug = True)