
from pathlib import Path
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

#the Online version must use relative path o.w. app will crash

dat = pd.read_csv("Kyle.csv")

######### quick clean up to prepare for deployment
dat = dat.loc[:,['Unnamed: 0',
                'DEPT NAME Consultee Dept Name from Lookup', 'Dept_category',
                'STATUS', 'period','TASK']]

dat = dat.rename(columns={'Unnamed: 0': 'id',
                          'DEPT NAME Consultee Dept Name from Lookup':'dept'})

external_stylesheets = ['https://kylechanhy.netlify.app/assets/hacky.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H1(children="📊 Odum Stats Help Desk Analytics: Kyle Chan", className = "header-title"),
    html.P(children="This dahsboard analyzes the types of clients that I have seen in my role as student consultant"
           "at the Odum Institute for Research in Social Science"
           " between 2020 and 2021",
           className ="header-description"),
    html.P(children="Note: If you use the Department Category, be sure to double click to isolate"
           " a particular department. Otherwise the number of categories can be quite overwhelming!"),
    html.P("Category:"),
    dcc.Dropdown(
        id='dropdown',
        value='Dept_category', #default category
        options=[{'value': 'dept', 'label': 'Department'},
                 {'value': 'Dept_category', 'label': 'Department by Category'},
                 {'value': 'STATUS', 'label': 'Affiliate status'},
                 {'value': 'period', 'label': 'Semester'},
                 {'value': 'TASK', 'label': 'Reason for Visit'}
                ], #options. otherwise label = what they see; value = col name
        clearable=False # user must need at least 1 category to be shown
    ),
    dcc.Graph(id="pie-chart"),
])


@app.callback( #Callback - IO
    Output(component_id="pie-chart", component_property="figure"),  #output - affect the figure
    [Input(component_id="dropdown", component_property="value")] #input - define input from dropdown
    )

def generate_chart(dropdown):
    fig = px.pie(dat, names = dropdown, hole=.3)
    fig.update_traces(textinfo="label+percent+value")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
