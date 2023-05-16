import dash
from dash import html, dcc, Input, Output
from app import app
import pandas as pd
import plotly.express as px

from __init__ import make_card, make_2c_table, risk_exposure_card

data = pd.read_csv('exec.csv')

layout = html.Div([
    html.Div(id = 'dummy'),
    html.Div([
        html.P('Executive Summary Dashboard', id = 'title-text')
    ], id = 'title-block'),

    html.Div([
        html.Div([

        ], id = 'cards'),
        
        html.Div([
            dcc.Graph(id = 'trends-fig')
        ], id = 'trends'),

        html.Div([
            make_2c_table(title = 'Projects', names = ['Total', 'cost (NOK)'], values = ['41', '200K']),
        ], id = 'table1'),

        html.Div([
            make_2c_table(title = 'Status', names = ['Not started', 'Ongoing', 'Completed'], values = ['24%', '64%', '12%'])
        ], id = 'table2'),
        html.Div([
            html.Div([
                html.P('Risk Exposure', id = 'exposure-title-text')
            ],id = 'exposure-title'),
            html.Div([
                html.Div([
                    html.Div([
                        html.P(''),
                    ]),
                    html.Div([
                        html.P('Score'),
                    ]),
                    html.Div([
                        html.P('Appetite'),
                    ]),
                ], className = 'exposure-row'),
                html.Div([
                    html.Div(html.P('Risk 1'), className = 'risk-exposure-name'),
                    html.Div([
                        risk_exposure_card('h')
                    ]),
                    html.Div([html.P('☓')], className = 'appetite')
                ], className = 'exposure-row'),
                html.Div([
                    html.Div(html.P('Risk 2'), className = 'risk-exposure-name'),
                    html.Div([
                        risk_exposure_card('m')
                    ]),
                    html.Div([html.P('✓')], className = 'appetite')
                ], className = 'exposure-row'),
                html.Div([
                    html.Div(html.P('Risk 3'), className = 'risk-exposure-name'),
                    html.Div([
                        risk_exposure_card('l')
                    ]),
                    html.Div([html.P('✓')], className = 'appetite')
                ], className = 'exposure-row'),
                html.Div([
                    html.Div(html.P('Risk 4'), className = 'risk-exposure-name'),
                    html.Div([
                        risk_exposure_card('h')
                    ]),
                    html.Div([html.P('☓')], className = 'appetite')
                ], className = 'exposure-row')
            ], id = 'exposure-content')
        ], id = 'risk-exposure')
    ], id = 'main1')
])


@dash.callback(
    Output('cards', 'children'),
    Input('dummy', 'children')
)
def create_cards(dummy):
    children = []
    max_date = data['Date'].max()
    for title in data['variable'].unique():
        value = float(data['value'][(data['variable'] == title) & (data['Date'] == max_date)])
        card = make_card(title = title, value = value)
        children.append(card)
    return children


@dash.callback(
    Output('trends-fig', 'figure'),
    Input('dummy', 'chidren')
)
def update_trends_fig(dummy):
    dff = data
    fig = px.line(dff, x = 'Date', y = 'value', color = 'variable')
    fig.update_layout(margin = dict(t = 10, b = 10, l = 10, r = 10), legend = dict(orientation = 'h', x = 0.5, xanchor = 'center', y = -0.1))
    return fig