import dash_core_components as dcc
import dash_html_components as html

# TODO: figure out how to display the signin button
# TODO: use this as index and redirect to multipage on click. Fallback here on failed authorization

signin = html.Div(id='mypage', children=[
    #html.Div('<div class="g-signin2" data-onsuccess="onSignIn"></div>')
    #html.Button(className='g-signin2', children='Signin with Google'),
    dcc.Link(id='googlesignin', children=['Sign in with Google'], href='/')
    # , children=[
    #     html.Img(src=app.get_asset_url('googlesignin.png'))
    # ])
    # dcc.Link(html.Img(src='src/assets/googlesignin.png'),href='/')
])


layout = html.Div(children=[
    html.H2('You are now signed in')
])

