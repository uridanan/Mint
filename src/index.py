import src.db.connection
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
        html.Div(id='user', children=[
            html.Table(className='user', children=[
                html.Tr(className='user', children=[
                    html.Td(className='user', children=[html.Img(id="userPic",src="")]),
                    html.Td(className='user', children=[
                        html.P(id='userName',children=""),
                        dcc.Link(id='logout', children='Logout', href='revoke')
                    ])
                ])
            ])
        ]),
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
    Output('userPic', 'src'),
    [Input('user', 'value')]
)
def on_load(value):
    picture = ''
    if session.currentUser is not None:
        picture = session.currentUser.picture
    return picture

@app.callback(
    Output('userName', 'children'),
    [Input('user', 'value')]
)
def on_load(value):
    name = ''
    if session.currentUser is not None:
        name = session.currentUser.name
    return name


hostName = env['SERVER']['host']
if __name__ == '__main__':
    app.run_server(debug=True,host=hostName)

