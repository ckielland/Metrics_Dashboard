import dash
from dash import html, dcc, Input, Output, State, callback_context
import pandas as pd
from __init__ import make_capability_row, metric_view, create_risk_card, cn, create_colored_card, risk_exposure_card
import dash_bootstrap_components as dbc
import plotly.express as px

capability_cards = pd.read_csv('capability_cards.csv')

layout = html.Div([
        dcc.Store(id = 'last_clicked'),
        html.Div(id = 'dummy'),
        html.Div([
            html.P('Management Dashboard', id = 'title-text')
        ], id = 'title-block'),
        html.Div([
            html.Div([
                html.Div([
                    #html.Div([
                        #html.P('Risk', className = 'title-text-risk'),], 
                     #className = 'title-container'),
                    html.Div([
                       create_risk_card('Risk1', 'h', 'm', 'up'),
                       create_risk_card('Risk2', 'l', 'l', 'down'),
                       create_risk_card('Risk3', 'h', 'm', 'no-change'),
                       create_risk_card('Risk4', 'm', 'm', 'down'),
                       create_risk_card('Risk5', 'h', 'm', 'up'),
                       create_risk_card('Risk6', 'm', 'l', 'no-change')

                    ], id = 'risk-inner')
                ], id = 'risk'),
            ], id = 'top-row'),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.P('Threat Exposure', className = 'title-text-risk'),
                    ], className = 'title-container'),
                    html.Div([
                        cn('Threat Scenario'), cn('Exposure'), cn('Identify'), cn('Protect'), cn('Detect'), cn('Respond'), cn('Recover'),
                        cn('Scenario1'), risk_exposure_card('h'), cn(2.1), cn(1.2),cn(2.7),cn(2),cn(1.7),
                        cn('Scenario2'), risk_exposure_card('m'), cn(2.4), cn(1.9),cn(3),cn(2.8),cn(2.6),
                        cn('Scenario3'), risk_exposure_card('m'), cn(1.9), cn(2.8),cn(2.9),cn(1.9),cn(2.5),
                        cn('Scenario4'), risk_exposure_card('h'), cn(2.4), cn(1.2),cn(1),cn(1.5),cn(2.1)
                    ], id = 'threat-exposure-inner')
                ], id = 'threat-exposure'),
                html.Div([
                    html.Div([
                        html.Div(
                            html.P('Capabilities'), className = 'capability-text-container'
                        ),
                        html.Div(
                            html.P('Score'),
                        ),
                        html.Div(
                            html.P('Target'),
                        ),
                        html.Div(
                            html.P('Coverage'),
                        ),
                        html.Div(
                            html.P('Stage1'),
                        ),
                        html.Div(
                            html.P('Stage2'),
                        ),
                        html.Div(
                            html.P('Stage3'),
                        ),
                        html.Div(
                            html.P('Stage4')
                        ),
                        html.Div(
                            html.P('Stage5')
                        ),
                        ], id = 'cap-header'),
                    html.Div([make_capability_row(list(capability_cards.loc[i])) for i in range(len(capability_cards))], id = 'capabilities-inner')
                ], id = 'capabilities'),
            ], id = 'bottom-row'),

        ], id = 'main2'),
        dbc.Modal(
            [
                dbc.ModalBody(id = 'popup-content'),
                dbc.ModalFooter([
                    html.Button('Show trend graph', id = 'show-trend', n_clicks = 0),
                    html.Button("Close", id="close", n_clicks=0),]
                ),
            ],
            id="modal",
            size="xl",
            is_open=False,
        ),
    ])


@dash.callback(
    Output('last_clicked', 'data'),
    [Input(title+'-box', 'n_clicks') for title in list(capability_cards['Capability Names'].unique())]
)
def store_clicked(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0][0:-9]
    return changed_id

@dash.callback(
    Output("modal", "is_open"),
    [Input("last_clicked", "data"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@dash.callback(
    Output('popup-content', 'children'),
    [Input('last_clicked', 'data'),
     Input('show-trend', 'n_clicks')]
)
def update_popup_content(last_clicked, n_clicks):
    if n_clicks % 2 != 0:
        try:
            data = pd.read_csv(f'{last_clicked[:-4]} trends.csv')
            data['value'] = data['value'].apply(lambda x : int(x[:-1]))
            fig = px.line(data, x = 'Date', y = 'value', color = 'variable')
            fig.update_layout(margin = dict(t = 10, b = 10, l = 10, r = 10))
            return dcc.Graph(figure = fig)
        except:
            return 'No data available.'
    if last_clicked:
        try:
            data = pd.read_csv(f"{last_clicked[:-4]}.csv")
            return metric_view(data = data)
        except:
            return 'No data available.'



@dash.callback(
    Output('show-trend', 'children'),
    Input('show-trend', 'n_clicks')
)
def update_button_text(n_clicks):
    if n_clicks %2 == 0:
        text = "Show trend graph"
    else: 
        text = "Show metrics"
    return text