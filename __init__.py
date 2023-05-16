import dash
from dash import html


def make_card(title, value):
    if value >= 3:
        color = 'green'
    elif 3 > value >= 2:
        color = 'orange'
    elif value < 2:
        color = 'red' 

    card_layout = html.Div([
        html.Div(
            html.P(title, className = 'card-title-text'), 
            className = 'card-title'
        ),
        html.Div([
            html.P(
            value,
            className = 'value'
            )
        ], className = 'card-body', style = {"background-color": color})
    ], className = 'exec-card')

    return card_layout




def make_2c_table(title:str, names:list, values:list):
    body_list = []
    for i in range(len(names)):
        body_list.append(html.Div(names[i], className = 'cell'))
        body_list.append(html.Div(values[i], className = 'cell'))
    table_layout = html.Div([
        html.P(title, className = 'table-title'),
        html.Div(children = body_list, className = 'table-body', style = {"display": 'grid', "grid-template-columns": 'repeat(2, 1fr)', "grid-template-rows": f'repeat({len(names)}, 1fr)'})
    ], className = 'table-layout')
    return table_layout


def create_colored_card(value):
    if value:
        if value >= 3:
            color = 'green'
        elif 3 > value >= 2:
            color = 'orange'
        elif value < 2:
            color = 'red' 
        else:
            color = 'white'
        
        return html.Div(value, className = 'cap-inner', style = {"background-color": color})

def cn(value):
    if value:
        if type(value) == str:
            color = 'black'
        elif value >= 3:
            color = 'green'
        elif 3 > value >= 2:
            color = 'orange'
        elif value < 2:
            color = 'red' 
        else:
            color = 'white'
        
        return html.Div(html.P(value), className = 'cap-inner', style = {"color": color})

def make_capability_row(values:list):
    title = values[0]
    score = values[1]
    target = values[2]
    coverage = values[3]
    stage1 = values[4]
    stage2 = values[5]
    stage3 = values[6]
    stage4 = values[7]
    stage5 = values[8]



    row = html.Button(children = [
        html.Div(html.P(title, className = 'capability-txt'), className = 'capability-text-container'),
        create_colored_card(score),
        create_colored_card(target),
        html.Div(
            html.P(coverage), className = 'coverage'
        ),
        create_colored_card(stage1),
        create_colored_card(stage2),
        create_colored_card(stage3),
        create_colored_card(stage4),
        create_colored_card(stage5),
    ], className = 'cap-button', id = f'{title}-box', n_clicks = 0)
    return row




def metric_view(data):
    elements = [
        html.Div('Metrics list', className = 'cell-a'),
        html.Div('Value', className = 'cell-a'),
        html.Div('Effectiveness', className = 'cell-a'),
        html.Div('Coverage', className = 'cell-a'),
    ]
    for i in range(len(data)):
        row = list(data.iloc[i])
        for i in row:
            elements.append(html.Div([i], className = 'cell-a-1'))

    view = html.Div(
        children = elements, 
        className = 'metric-view',
        style = {"display": 'grid', "grid-template-columns": "40% 20% 20% 20%", "grid-template-rows": f'repeat({len(data)+1}, 1fr)'})
    return view


def risk_exposure_card(value):
    value = value.upper()
    if value == 'H':
        color = '#ff0000'
    elif value == 'L':
        color = '#008000'
    elif value == 'M':
        color = '#ffc000'
    children = html.Div([html.P(value)], className = 'exposure_card', style = {'background-color': color})
    return children

def create_risk_card(name, val1, val2, symbol):
    val1 = val1.upper()
    val2 = val2.upper()
    if symbol == 'no-change':
        symbol = '—'
    elif symbol == 'down':
        symbol = '↓'
    elif symbol == 'up':
        symbol = '↑'

    children = html.Div([
        html.Div([
            html.P(name)
        ], className = 'risk-title-container'),
        html.Div([
            html.Div([
                html.P('Current', className = 'risk-normal-text'),
                risk_exposure_card(val1)
            ], className = 'risk-col'),
            html.Div([
                html.P('Trend', className = 'risk-normal-text'),
                html.Div([
                    html.P(symbol, className = 'symbol')
                ], className = 'symbol-container'),
            ], className = 'risk-col'),
            html.Div([
                html.P('Target', className = 'risk-normal-text'),
                risk_exposure_card(val2)
            ], className = 'risk-col'),
        ], className= 'risk-card-inner'),
    ], className = 'risk-card')

    return children