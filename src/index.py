from src.app import *
from src.ui import overview, monthly, recurring


#=====================================================================================================================
# Layout
#=====================================================================================================================
# Main layout, this is where your app goes
# This layout displays a sidebar and page content
# Create each layout in a separate dedicated file
indexLayout = html.Div(id='indexContent', children=[
    html.Div(id='sidebar',className='sidebar',children=[
        html.Div(id='user'),
        dcc.Link('Overview', href='overview'),
        dcc.Link('Monthly Reports', href='monthly'),
        dcc.Link('Recurring Expenses', href='recurring'),
        dcc.Link('About', href='about')
        ]),
    html.Div(id='content',className='content'),
])


#=====================================================================================================================
# Callbacks
#=====================================================================================================================
# Main callback, return a layout with a sidebar and content page
@app.callback(
    Output('authorizedContent', 'children'),
    [Input('url', 'pathname')]
)
def on_load(pageName):
    return indexLayout


# Multi-page callback, return the right layout based on the selected page
@app.callback(
    Output('content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pageName):
    if pageName == '/overview':
        return overview.layout
    elif pageName == '/monthly':
        return monthly.layout
    elif pageName == '/recurring':
        return recurring.layout
    else:
        return overview.layout


# Load the user element and logout link
# This is here as an example. You will want to replace it with your own
@app.callback(
    Output('user', 'children'),
    [Input('user', 'value')]
)
def on_load(value):
    picture = ''
    name = ''

    if session.currentUser is not None:
        email = session.currentUser.email
        id = session.currentUser.id
        name = session.currentUser.name
        picture = session.currentUser.picture

    layout = html.Table([
        html.Tr([
            html.Td([html.Img(src=picture,width=64,height=64)]),
            html.Td([html.P(name),dcc.Link('Logout', href='revoke')])
            ])
        ])

    return layout


#runMyApp()
hostName = env['SERVER']['host']
if __name__ == '__main__':
    app.run_server(debug=True,host=hostName)

