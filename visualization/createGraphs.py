import sys
sys.path.append('/root/code/eve-aws/')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import utils.itemPrices as ip
import utils.ItemIdEnum as item
import asyncio
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import json
from typing import List, Dict, Union
import utils.mongodbData as mdb
import utils.utilities as utils



class graphs():
    def __init__(self,dbName='eve-historical-daily-the-forge') -> None:
        self.db = mdb.mongoData(dbName)
    async def createBubbleGraph(self,type_id = 7):
        type_id = 7
        
        # Load JSON data
        with open("marketGroups.json", "r") as f:
            market_data = json.load(f)
        name = utils.find_name_by_market_group_id(market_data, type_id)
        # Extract types for a specific market group id
        all_entries = utils.extract_types_for_market_group(market_data, type_id)

        # Fetch data for these types (This is an asynchronous function)
        combined_df = await utils.fetch_data_for_types(all_entries)
        combined_df['adjusted_volume'] = np.sqrt(combined_df['volume'])
        combined_df = combined_df.sort_values(by='percent_profit', ascending=False)
        # Print or save the data
        print(combined_df)
        
        fig = px.scatter(combined_df, x='order_count', y='percent_profit', color='name', 
                        size='adjusted_volume', hover_data=['item_name','volume','average'],
                        text='item_name')
        fig.update_layout(
            legend_title_text='Group Types',
            title=f"{name} Percent Profit vs Total Order Count",
            xaxis_title="Total Order Count Per Day",
            yaxis=dict(
                title="Relative Percent Profit",
                gridwidth=2,
            )
        )
        # fig.update_traces(marker=dict(sizeref=(combined_df['volume'].max() /100)))
        fig.show()

    async def createHistoryGraph(self,collectionName = item.item.TRITANIUM.name) -> None:
        
        df = await self.db.pullAllCollectionDocuments(item.item.TRITANIUM.name)
        df = df.drop_duplicates()
 
        # Create a line trace for average price
        line_trace = go.Scatter(x=df['date'], y=df["average"], mode='lines', name='Average Price')

        # Create a bar trace for volume, and set it to the secondary y-axis
        bar_trace = go.Bar(x=df['date'], y=df["volume"], name='Volume', yaxis='y2')

        # Create a figure and add traces
        fig = go.Figure(data=[line_trace, bar_trace])
        # Buttons for toggling
        buttons = [
            dict(label="Both",
                method="update",
                args=[{"visible": [True, True]}, {"title": "Average Price and Volume"}]),
            dict(label="Line Only",
                method="update",
                args=[{"visible": [True, False]}, {"title": "Average Price"}]),
            dict(label="Bar Only",
                method="update",
                args=[{"visible": [False, True]}, {"title": "Volume"}])
]
        # Update layout to include the secondary y-axis
        fig.update_layout(
            bargap=0.5,
            legend_title_text='Item Name',
            title=f"{collectionName} Year History",
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            fixedrange=False,
            type="date"
            ),
            yaxis=dict(
                title="Price [ISK]",
                gridwidth=2,
            ),
            yaxis2=dict(
                title="Volume",
                overlaying='y',
                side='right'
            ),
            updatemenus=[
                dict(type="buttons",
             showactive=True,
             buttons=buttons)]
        )

        fig.show()
        

graph = graphs()
asyncio.run(graph.createHistoryGraph())