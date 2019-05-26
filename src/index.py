import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output



#Am I better off getting the data via REST API or directly from DB?
#It seems more direct to use the DB, I see no need for the overhead of APIs just yet

# https://dash.plot.ly/external-resources
# https://github.com/plotly/dash/pull/171

from flask import session, redirect
from src.app import app, auth
from src.ui import overview, monthly, recurring
from src import signin

# This layout displays a sidebar and page content
# Create each layout in a separate dedicated file
appLayout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='sidebar',className='sidebar',children=[
        html.Div(id='user'),
        dcc.Link('Overview', href='overview'),
        dcc.Link('Monthly Reports', href='monthly'),
        dcc.Link('Recurring Expenses', href='recurring'),
        dcc.Link('About', href='about')
        ]),
    html.Div(id='content',className='content'),
])

app.layout = appLayout


@app.callback(
    Output('user', 'children'),
    [Input('user', 'value')]
)
def on_load(value):
    email = auth.getEmail()  #session['email']
    id = auth.getResp().json().get('id')  #session['id']
    name = auth.getResp().json().get('name')  #session['name']
    picture = auth.getResp().json().get('picture')  #session['picture']
    layout = html.Table([
        html.Tr([
            html.Td([html.Img(src=picture,width=64,height=64)]),
            html.Td([html.P(name),dcc.Link('Logout', href='logout')])
            ])
        ])
    return layout

@app.callback(Output(app.layout, 'children'),[dash.dependencies.Input('url', 'pathname')])
def display_app(pageName):
    if pageName == '/logout':
        auth.logout()
        return signin.layout
    else:
        return appLayout

@app.callback(Output('content', 'children'),[dash.dependencies.Input('url', 'pathname')])
def display_page(pageName):
    if pageName == '/overview' or pageName == '/':
        return overview.layout
    elif pageName == '/monthly':
        return monthly.layout
    elif pageName == '/recurring':
        return recurring.layout
    else:
        return '/logout'


if __name__ == '__main__':
    app.run_server(debug=True,host='localhost')