from flask import Flask,render_template,redirect, request
from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import visdcc
from src.sessions.globals import *


#=====================================================================================================================
# Flask Server
#=====================================================================================================================
server = Flask(__name__)


# Load the signin page
@server.route(routes["SIGNIN"])
def signin():
    return render_template('signin.html')


# Catch POST from the signin page and authenticates the token before creating a session
@server.route(routes["AUTHORIZE"], methods = ['POST'])
def authenticate():
    if request.method == 'POST' and request.form['idtoken'] != '':
        token = request.form['idtoken']
        session.authenticate(token)

    if session.currentUser is not None:
        return redirect(routes['INDEX'])
    else:
        return redirect(routes["SIGNIN"])


# Catch signout from the signin page and revokes the session
# (should not actually happen, used this to debug the signin page)
# Signout from the app happens in app.callback
@server.route(routes["REVOKE"], methods = ['POST'])
def revoke():
    session.logout()
    return redirect(routes["SIGNIN"])


# The main app route. Remember, dash works as a single page app
@server.route("/")
def welcome():
    if session.currentUser is not None:
        return app.index()
    else:
        return redirect(routes["SIGNIN"])


#=====================================================================================================================
# Dash App
#=====================================================================================================================
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets, server=server, url_base_pathname='/')
app.config.suppress_callback_exceptions = True


# Top level layout, includes navigation param and container for the other layouts
app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='pageContent')
])


#=====================================================================================================================
# Layouts
#=====================================================================================================================
# Layout to display in pageContent when user is authorized
# This is where your app content goes
authorizedLayout = html.Div(id='authorizedContent', children='Your app goes here')


# Layout to display when the user is not authorized
# You can use the redirect layout instead to return the user to the signin page
unauthaurizedLayout = html.Div(children=[
    html.H1(id='title', children='Unauthaurized user'),
    html.A(id='signout', href=routes["SIGNIN"], children="Return to signin page")
])


# Use this layout to redirect the user to another page (signin page?)
# Use this to run JS inside dash: https://github.com/jimmybow/visdcc#3-visdccrun_js-
redirectLayout = html.Div(children=[
        visdcc.Run_js(id = 'javascript', run='window.location.replace("'+ routes['SIGNINFULLPATH'] +'");')
        # visdcc.Run_js(id = 'javascript', run='window.location.replace("http://localhost:8050/signin");')
        ])


#=====================================================================================================================
# Callbacks
#=====================================================================================================================

# Load the app layout only for authorized users
# Do not load the app layout when the path is /revoke
@app.callback(
    Output('pageContent', 'children'),
    [Input('url', 'pathname')]
)
def on_load(path):
    if path == '/revoke':
        session.logout()
        return redirectLayout  # unauthaurizedLayout
    if session.currentUser is not None:
        return authorizedLayout  # replace with method passing path as parameter
    else:
        return redirectLayout  # unauthaurizedLayout


# hostName = env['SERVER']['host']
# if __name__ == '__main__':
#     app.run_server(debug=True,host=hostName)


# TODO: beautify HTML layouts
