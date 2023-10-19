import sys
sys.path.append('/root/code/eve-aws/utils')
import pandas as pd
import utils.utilities
import matplotlib.pyplot as plt
import numpy as np
from utils.ItemIdEnum import item
import pathlib
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from utils.mongodbData import mongoData
import aiohttp
from io import StringIO
import time

header = {
    "In-Game-Name": "XiT Statik Daphiti",
    "Discord-Name": "xit_statik",
    "email": "mullins097956@gmail.com",
    "application": "EVE-AWS",
    "If-None-Match":""
}

df = pd.read_csv('/root/code/current_forge_etags.csv', header=0, usecols=['url', 'etag'])

async def fetch(session, url, header):
    async with session.get(url, headers=header) as response:
        if response.status == 200:
            text = await response.text()
            return text
        else:
            print(f"Error: {response.status}")
            return None  # or handle it in a way you prefer

async def main():
    start = time.time()
    dfs = []
    tasks = []
    url = f"https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=all"

    async with aiohttp.ClientSession() as session:
        for etag in df['etag']:
            header["If-None-Match"] = etag
            task = asyncio.create_task(fetch(session, url, header))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        for response_text in responses:
            if response_text:  # check if not None
                df_temp = pd.read_json(StringIO(response_text))
                dfs.append(df_temp)

    main_df = pd.concat(dfs, ignore_index=True)
    end = time.time()
    print(main_df)
    print(end-start)

# Run the main coroutine using asyncio's event loop
asyncio.run(main())

