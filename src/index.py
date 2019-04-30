import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output



#Am I better off getting the data via REST API or directly from DB?
#It seems more direct to use the DB, I see no need for the overhead of APIs just yet

# https://dash.plot.ly/external-resources
# https://github.com/plotly/dash/pull/171

from flask import session
from src.app import app
from src.ui import overview, monthly, recurring


# This layout displays a sidebar and page content
# Create each layout in a separate dedicated file
app.layout = html.Div(children=[
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


@app.callback(
    Output('user', 'children'),
    [Input('user', 'value')]
)
def on_load(value):
    email = session['email']
    id = session['id']
    name = session['name']
    picture = session['picture']
    layout = html.Table([
        html.Tr([
            html.Td([html.Img(src=picture,width=64,height=64)]),
            html.Td([html.P(name),html.P('Logout')])
            ])
        ])
    return layout

@app.callback(Output('content', 'children'),[dash.dependencies.Input('url', 'pathname')])
def display_page(pageName):
    if pageName == '/overview' or pageName == '/':
        return overview.layout
    elif pageName == '/monthly':
        return monthly.layout
    elif pageName == '/recurring':
        return recurring.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True,host='localhost')