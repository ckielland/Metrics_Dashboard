import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, callback_context
import json
import executive_summary, management, error404
import dash_bootstrap_components as dbc

from __init__ import make_card  
import pandas as pd

data = pd.read_csv('exec.csv')


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None,
                     plot_bgcolor="rgba( 0, 0, 0, 0)",
                     paper_bgcolor="rgba( 0, 0, 0, 0)",)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)

    return fig

config = {'displaylogo': False,
         'modeBarButtonsToAdd':['drawline',
                                'drawopenpath',
                                'drawclosedpath',
                                'drawcircle',
                                'drawrect',
                                'eraseshape'
                               ]}




app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server
app.title = 'Prototype'

app.layout = html.Div([
    html.Div(id='blank'), 
    dcc.Store(id='style'), 
    dcc.Location(id='url', refresh=False), 
    html.Div([
        html.Div([
            html.Div(
                className="menu", id='menu'),
        ], id='menuspace'),
        html.Div([
                html.H1('', id='dashboardtitle')
        ],className='dashboardtitle', id='title'),
    ], id = 'top_section'),
    html.Div(id='page-content', children=[])
], id='layout')


@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return executive_summary.layout
    elif pathname == '/executive_summary':
        return executive_summary.layout
    elif pathname == '/management':
        return management.layout

    else:
        return error404.layout


@app.callback(Output('style', 'data'),
            [Input('url', 'pathname')])
def efine_styles(pathname):
    styles =[None]*2
    if pathname == '/':
        styles[0] = {'background-color': 'black', 'color': 'white'}
    elif pathname == '/executive_summary':
        styles[0] = {'background-color': 'black', 'color': 'white'}
    elif pathname == '/management':
        styles[1] = {'background-color': 'black', 'color': 'white'}
    else:
        styles=[None]*2
    return styles



@app.callback(Output('menu', 'children'),
            [Input('style', 'data')])
def change_styles(styles):
    children=[
        dcc.Link(html.Div(['Executive Summary'], className='button_'), className='link', id='page_1', style= styles[0], href='/executive_summary'),
        dcc.Link(html.Div(['Management'], className='button_'), className='link', id='page_2', style= styles[1], href='/management'),]
        
            
    return children



app.clientside_callback(
    """
    function(pathname) {
        if (pathname === '/') {
            document.title = 'Executive Summary'
        } else if (pathname === '/executive_summary') {
            document.title = 'Executive Summary'
        }else if (pathname === '/management') {
            document.title = 'Management'
        }else {
            document.title = 'Page not found'
        }
    }
    """,
    Output('blank', 'children'), 
    Input('url', 'pathname')
)




if __name__ == "__main__":
    app.run_server(debug=True)