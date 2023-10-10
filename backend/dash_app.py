from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import requests
from app import app as flask_app
import sys
sys.path.append('/root/code/eve-aws/utils')
from utils.ItemIdEnum import item


# Create Dash app and associate with Flask app
dash_app = Dash(__name__, server=flask_app, url_base_pathname='/dashboard/')

# Layout of the app
dash_app.layout = html.Div(
    [
        dcc.Dropdown(
            id='item-dropdown',
            options = [{'label': items.name, 'value': items.name} for items in item],
            value='TRITANIUM'
        ),
        dcc.Graph(id='item-graph'),
    ]
)


@dash_app.callback(
    Output('item-graph', 'figure'),
    [Input('item-dropdown', 'value')]
)
def update_graph(selected_item):
    response = requests.get(f'http://127.19.0.2:5000/get_item/{selected_item}')
    df = pd.read_json(response.text)
    
    fig = px.line(df, x='issued', y='price', title=f'Price trend for {selected_item}')
    
    return fig

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True)