#!/usr/local/bin/python

import sys
sys.path.append('/root/code/eve-aws/utils')
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
import time
from typing import Dict
import aiohttp
import json
from decimal import Decimal
import asyncio
import requests
import utils.mongodbData as mdb

# from utils.passwordsEnum import passwords

async def updateForgeEtags() -> None:
    """
    Asynchronously pull all order IDs for The Forge region from the EVE Online ESI API.
    """
async def fetch(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.text(), response.headers.get('etag').strip('"'), int(response.headers.get('X-Pages'))
        else:
            print(f"Error: {response.status}")
            

async def updateEtags():
    db = mdb.mongoData('etag-storage')
    df = pd.read_csv('/root/code/current_forge_etags.csv', header=0, usecols=['url', 'etag'])
    start = time.time()
    url = f"https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=all"

    async with aiohttp.ClientSession() as session:
        text, etag, xPages = await fetch(session, url)

        if len(df) > xPages:
            n = len(df) - xPages
            df = df.iloc[:-n]
        else:
            df = pd.DataFrame(columns=['url', 'etag'])
            tasks = []
            for i in range(1, xPages+1):
                url = f"https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=all&page={i}"
                tasks.append(fetch(session, url))

            results = await asyncio.gather(*tasks)

            for text, etag, _ in results:
                df.loc[len(df.index)] = [url, etag]

    end = time.time()
    df.index = np.arange(1, len(df) + 1)
    await db.pushData(df,'the-forge-etags',True)
    print(len(df))
    print(end-start)
    df.to_csv('/root/code/current_forge_etags.csv')

# Run the async main function
if __name__ == "__main__":
    asyncio.run(updateEtags())