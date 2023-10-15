import sys
sys.path.append('/root/code/eve-aws/')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import utils.itemPrices as ip
import utils.ItemIdEnum as item
import utils.RegionIdEnum as region
import asyncio
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import json
from typing import List, Dict, Union
import utils.mongodbData as mdb
import utils.utilities as utils
import aiohttp

def check_values_exist(values: list) -> list:
    not_exist = []
    enum_values = [e.value for e in item.item]
    for val in values:
        if val not in enum_values:
            not_exist.append(val)
    return not_exist

async def fetch_and_push(id, db):
    
    # Check if the ID is a valid enum member
    if id not in [e.value for e in item.item]:
        print(f"ID {id} not found in the enum. Skipping...")
        return

    # Fetching item order history for the given id
    result = await ip.getAllItemOrderHistory(id, region.region.THE_FORGE.value)
    result = json.loads(result)

    print(result)
    if isinstance(result, dict) and all(isinstance(val, (int, float, str)) for val in result.values()):
        # This handles the case where result is a dictionary of scalar values
        df = pd.DataFrame([result])
    else:
        df = pd.DataFrame(result)

    # Pushing the data to MongoDB
    await db.pushData(df, item.item(id).name)  # Note: Using `item(id).name` directly, assuming id is valid.


async def pullTheForgeOrders():
    """
    Asynchronously pull all order IDs for The Forge region from the EVE Online ESI API.
    """
    # Pull all order IDs for The Forge region
    orderIds = await ip.getRegionOrderIds(region.region.THE_FORGE.value)
    db = mdb.mongoData('eve-orders-the-forge')
    
    # Check which orderIds don't exist in the enum
    missing_ids = check_values_exist(orderIds)
    
    # Use asyncio.gather to fetch and push data concurrently only for IDs that exist in the enum
    valid_ids = set(orderIds) - set(missing_ids)
    await asyncio.gather(*(fetch_and_push(id, db) for id in valid_ids))
    if missing_ids:
        print(f"The following IDs are missing from the enum: {missing_ids}")
    # await db.deleteDB('eve-orders-the-forge')

    


asyncio.run(pullTheForgeOrders())