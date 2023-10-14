from scipy import stats
import numpy as np
import pandas as pd
import pathlib
from RegionIdEnum import region
from ItemIdEnum import item
import matplotlib.pyplot as plt
import numpy as np
import itemPrices as ip
from ItemIdEnum import item
import pathlib
import s3PullData as s3PullData
import asyncio
import gc
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import json
from typing import List, Dict, Union
import utils

def removeOutliers(df: pd.DataFrame) -> pd.DataFrame:
    dfzscores = ((df['price'] - df['price'].mean()) / df['price'].std()).abs()
    df['z_score'] = dfzscores
    dfLen = len(df)
    
    threshold = np.inf #100000

    while ((dfLen/len(df)) - 1 < 0.1):
        threshold = df['z_score'].mean()*3
        df = df[df['z_score'] < threshold]
        dfzscores = ((df['price'] - df['price'].mean()) / df['price'].std()).abs()
        df['z_score'] = pd.Series(dfzscores)
    return df

def convertFromZuluTime(df: pd.DataFrame) -> pd.DataFrame:
    df['issued'] = pd.DatetimeIndex(df['issued'])
    return df

def seperateJitaDataTocsv(df: pd.DataFrame, path: pathlib.Path, regionId: int) -> None:
    newCSVName = path.parent.joinpath("the-forge-historical-" + path.name)
    df[df['region_id'] == regionId].to_csv(newCSVName, index=False)
    
def seperateItemDataTocsv(df: pd.DataFrame, path: pathlib.Path, item: item) -> None:
    newCSVName = path.parent.joinpath(item.name+'-' + path.name)

    df[df['type_id'] == item.value].to_csv(newCSVName, index=False)
    
def combineItemcsv(path: pathlib.Path, item: item) -> None:
    df_merged = pd.DataFrame()
    newCSVName = pathlib.Path()
    for file in path.rglob(item.name + "*.csv*"):
        if str(file.suffix) == ".bz2":
            df = pd.read_csv(file)
            df_merged = pd.concat([df_merged,df])
        newCSVName = path.parent.joinpath("merged-"+ file.name)
    df_merged.to_csv(newCSVName, index=False)

def extract_types_for_market_group(data: list, target_id: int) -> List[Dict[str, Union[str, int, float]]]:
    """
    Recursively search and extract type details from a nested market group structure 
    based on a target market group ID.
    
    Parameters:
        data (list): Nested structure of market groups.
        target_id (int): The target market group ID to search for.
    
    Returns:
        list: A list of dictionaries containing the details of types for the given market group ID.
    """
    
    # Iterate over each market group in the provided data
    for entry in data:
        # Check if the current entry's market group ID matches the target ID
        if entry["market_group_id"] == target_id:
            # If a match is found, extract all types associated with this market group
            return extract_all_types(entry)
        
        # If the entry has children, recursively search through them
        types_from_children = extract_types_for_market_group(entry.get("children", []), target_id)
        
        # If types are found in a child, return them
        if types_from_children:
            return types_from_children
    
    # If no matching market group ID is found, return an empty list
    return []

def extract_all_types(data: dict) -> List[Dict[str, Union[str, int, float]]]:
    """
    Recursively extract all type details from a market group entry.
    
    Parameters:
        data (dict): A single market group entry.
    
    Returns:
        list: A list of dictionaries containing type details.
    """
    
    # Extract types from the current entry
    entries = [{"name": data["name"], "type_id": type_id, "percent_profit": None, "item_name": item(type_id).name} 
               for type_id in data.get("types", [])]
    
    # If the entry has children, recursively extract types from them
    for child in data.get("children", []):
        entries.extend(extract_all_types(child))
    
    return entries

async def fetch_data_for_types(all_entries):
    """
    Fetch data for each type ID asynchronously and create a DataFrame.
    
    Parameters:
        all_entries (list): A list of dictionaries containing type details.
    
    Returns:
        DataFrame: A combined DataFrame containing the fetched data for each type ID.
    """
    
    data_frames = []
    
    # Iterate over each type entry and fetch data
    for entry in all_entries:
        type_id = entry["type_id"]
        data = await ip.getItemsPriceHistory(type_id, 10000002)  # Replace with your desired region_id
        
        if data:
            # Extract the most recent data entry
            last_entry = data[-1]
            
            # Calculate the percent profit and update the entry dictionary
            entry.update(last_entry)
            entry["percent_profit"] = (entry['average'] - entry['lowest']) / entry['lowest'] * 100
            
            # Create a DataFrame for the current entry and add it to the list
            df = pd.DataFrame([entry])
            data_frames.append(df)
    
    # Combine all individual dataframes into one DataFrame
    combined_df = pd.concat(data_frames, ignore_index=True)
    
    return combined_df

# The find_name_by_market_group_id function has already been commented above.

