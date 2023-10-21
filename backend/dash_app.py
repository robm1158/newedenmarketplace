import sys
sys.path.append('/root/code/eve-aws/utils')
print(sys.path)
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import requests
from app import app as flask_app
from utils.ItemIdEnum import item
from flask_cors import CORS


# Create Dash app and associate with Flask app
dash_app = Dash(__name__, server=flask_app, url_base_pathname='/dashboard/')
CORS(dash_app.server)
# Layout of the app
dash_app.layout = html.Div(
    [
        dcc.Graph(id='item-graph'),
        html.Div(id='item-name-div', style={'display': 'none'}),  # This is a hidden div to store the selected item name
    ]
)



# @dash_app.callback(
#     Output('item-graph', 'figure'),
#     [Input('item-name-div', 'children')]  # Adjusted to take the name from the hidden div
# )
# def update_graph(selected_item):
#     response = requests.get(f'http://127.19.0.2:5000/get_item/{selected_item}')
#     df = pd.read_json(response.text)
    
#     fig = px.scatter(df, x='issued', y='price', title=f'Price trend for {selected_item}')
    
#     return fig

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True)