import os
import flask
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input

# dash-example folder contain a ready-to-pushed demo Dash dashboard chart.
# it contain a virtualenv folder 'venv' which contain all the python dependencies 
# the dependencies will be downloaded base on the list of package described in the requirement.txt file
# the .gitignore file contain the list of files and folder that would not be push to Heroku

server = flask.Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df = pd.read_csv('https://trello-attachments.s3.amazonaws.com/5bd586986a1afd42ce16e477/5ee2fa032e551158843f1905/8fb59309ca45eef878cc9c34197f4750/pop-median-rent.csv')

app.layout = html.Div(
    children=[
    html.H1(children='Dashboard for Property Analysis'),

    html.Div(children='''
        Population vs median rental in Australian major cities:
    '''
    ),

    dcc.Graph(
        id='pop-vs-median-rent',
        figure={
            'data': [
                dict(
                    x=df[df['StateCode'] == i]['EstimatedPopulation'],
                    y=df[df['StateCode'] == i]['MedianWeeklyRent'],
                    text=df[df['StateCode'] == i]['City'],
                    mode='markers',
                    opacity=0.6,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.StateCode.unique()
            ],
            'layout': dict(
                xaxis={'type': 'log', 'title': 'Estimated population'}, #confiture x-axis
                yaxis={'title': 'Average Median Weekly Rent' , 'range' : [200,500]}, #confiture y-axis
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])
@app.callback(dash.dependencies.Output('display-value', 'children'),[dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
if __name__ == '__main__':
    app.run_server(debug=True)