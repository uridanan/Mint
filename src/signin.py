import dash_core_components as dcc
import dash_html_components as html
import src.dbAccess as db
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from src.app import app


# TODO: figure out how to display the signin button
# TODO: use this as index and redirect to multipage on click. Fallback here on failed authorization

layout = html.Div(children=[
    html.H4(id='title', children='Welcome to Clarity'),
    html.Button(className='g-signin2', children='Signin with Google'),
    #html.Img(src='googlesignin.png'),
    # dcc.Link(html.Img(src='src/assets/googlesignin.png'),href='/')
])

