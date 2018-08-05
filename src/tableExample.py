import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

import sqlalchemy
from sqlalchemy import create_engine
import psycopg2


#Refactor data extraction to separate file
#Format fields per data type
#Step 2 : monthly input/output graph in 3 variants: income vs expenses, savings, total
#Step 1 : combined table from all sources
#Step 3 : start marking recurring expenses
#Step 4 : mark expenses by type
#Step 5 : rename expense (save the new name, re-use when recurring)

#Am I better off getting the data via REST API or directly from DB?
#It seems more direct to use the DB, I see no need for the overhead of APIs just yet
def getData():
    # Create your connection.
    #cnx = builder()(db='mintdb', user='postgres')
    connectionString = "postgres://postgres@localhost:5432/mintdb"
    cnx = create_engine(connectionString)
    df = pd.read_sql_query("SELECT * FROM data_entry", cnx)
    return df

data = getData()

def generate_table(dataframe, max_rows=200):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


app = dash.Dash()

app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

app.layout = html.Div(children=[
    html.H4(children='Bank Report - Work In Pogress'),
    generate_table(data)
])

if __name__ == '__main__':
    app.run_server(debug=True)