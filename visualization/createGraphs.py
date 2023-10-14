import pandas as pd
import utilities
import matplotlib.pyplot as plt
import numpy as np
import itemPrices as ip
from ItemIdEnum import item
import pathlib
import s3PullData
import asyncio
import gc
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import json
from typing import List, Dict, Union
import utils

async def createBubbleGraph(type_id = 7):
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

asyncio.run(createBubbleGraph())