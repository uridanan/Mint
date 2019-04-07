import dash

# How to build a multi-page app
# https://dash.plot.ly/urls
# https://github.com/plotly/dash/issues/133
# Cool Themes: https://1stwebdesigner.com/free-bootstrap-dashboard-templates/

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True
