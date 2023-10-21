import pandas as pd
import utils.utilities as utilities
import matplotlib.pyplot as plt
import numpy as np
import utils.itemPrices as ip
from ItemIdEnum import item
import pathlib
import utils.s3PullData as s3PullData
import asyncio
import gc
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import json
from typing import List, Dict, Union

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 17)
pd.set_option('display.width', 250)

def extract_types_for_market_group(data: list, target_id: int) -> List[Dict[str, Union[str, int, float]]]:
    # Base case
    for entry in data:
        if entry["market_group_id"] == target_id:
            # Call the function recursively to extract all types for the target_id
            return extract_all_types(entry)
        
        # Recursive case
        types_from_children = extract_types_for_market_group(entry.get("children", []), target_id)
        if types_from_children:
            return types_from_children
    return []

def extract_all_types(data: dict) -> List[Dict[str, Union[str, int, float]]]:
    entries = [{"name": data["name"], "type_id": type_id, "percent_profit": None, "item_name": item(type_id).name} for type_id in data.get("types", [])]
    
    for child in data.get("children", []):
        entries.extend(extract_all_types(child))
    return entries

async def fetch_data_for_types(all_entries):
    data_frames = []

    for entry in all_entries:
        type_id = entry["type_id"]
        data = await ip.getItemsPriceHistory(type_id, 10000002)  # Replace with your desired region_id
        if data:
            # Get only the last entry
            last_entry = data[-1]

            # Add the data to the existing entry dictionary
            entry.update(last_entry)
            entry["percent_profit"] = (entry['average'] - entry['lowest']) / entry['lowest'] * 100

            # Create a DataFrame using the entry dictionary and append
            df = pd.DataFrame([entry])
            data_frames.append(df)

    # Combine all the dataframes
    combined_df = pd.concat(data_frames, ignore_index=True)
    return combined_df

def find_name_by_market_group_id(data: list, target_id: int) -> str:
    """
    Recursively search through a nested structure of market groups to find
    the name associated with a specific market group ID.
    
    Parameters:
        data (list): The nested data structure to search through.
        target_id (int): The market group ID to search for.
    
    Returns:
        str: The name associated with the found market group ID or an 
             empty string if not found.
    """
    for entry in data:
        # Check if the current entry's market group ID matches the target ID
        if entry["market_group_id"] == target_id:
            return entry["name"]
        
        # Recursive call: If the entry has children, search through them
        found_name = find_name_by_market_group_id(entry.get("children", []), target_id)
        
        # If the name was found in a child, return it
        if found_name:
            return found_name
    
    # If the function hasn't returned by this point, the ID was not found
    return ""

async def main():
    type_id = 7
    
    # Load JSON data
    with open("marketGroups.json", "r") as f:
        market_data = json.load(f)
    name = find_name_by_market_group_id(market_data, type_id)
    # Extract types for a specific market group id
    all_entries = extract_types_for_market_group(market_data, type_id)

    # Fetch data for these types (This is an asynchronous function)
    combined_df = await fetch_data_for_types(all_entries)
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

asyncio.run(main())



