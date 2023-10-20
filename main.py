import sys
sys.path.append('/root/code/eve-aws/utils')
import pandas as pd
import utils.utilities
import matplotlib.pyplot as plt
import numpy as np
# from utils.ItemIdEnum import item
import pathlib
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import utils.mongodbData as mdb
import aiohttp
from io import StringIO
import time
from items_dict import items

header = {
    "In-Game-Name": "XiT Statik Daphiti",
    "Discord-Name": "xit_statik",
    "email": "mullins097956@gmail.com",
    "application": "EVE-AWS",
    "If-None-Match":""
}

df = pd.read_csv('current_forge_etags.csv', header=0, usecols=['url', 'etag'])

async def fetch(session, url, header):
    async with session.get(url, headers=header) as response:
        if response.status == 200:
            text = await response.text()
            return text
        else:
            print(f"Error: {response.status}")
            return None  # or handle it in a way you prefer

async def get_names_from_ids(ids):
    url = "https://esi.evetech.net/latest/universe/names/?datasource=tranquility"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=ids) as resp:
            if resp.status == 200:
                return await resp.json()
            raise aiohttp.ClientResponseError(
                resp.request_info,
                resp.history,
                status=resp.status,
                message=resp.reason,
                headers=resp.headers,
            )

async def main():
    start = time.time()
    db = mdb.mongoData('eve-orders-the-forge')
    dfs = []
    tasks = []
    url = f"https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=all"

    async with aiohttp.ClientSession() as session:
        # ... [the rest of your session setup] ...
        
        responses = await asyncio.gather(*tasks)

        for response_text in responses:
            if response_text:  # check if not None
                df_temp = pd.read_json(StringIO(response_text))
                dfs.append(df_temp)

        main_df = pd.concat(dfs, ignore_index=True)

        item_set = set(items.values())

        missing_type_ids = set(id for id in main_df['type_id'] if id not in item_set)

        if missing_type_ids:
            id_name_mapping = await get_names_from_ids(session, list(missing_type_ids))

            for entity in id_name_mapping:
                type_id = entity.get('id')
                type_name = entity.get('name').upper().replace(" ", "_")  # Formatting the name
                items[type_id] = type_name

            with open('items_dict.py', 'w') as file:
                file.write('items = {\n')
                for k, v in items.items():
                    file.write(f"    {k}: '{v}',\n")  # writing each item in the dictionary
                file.write('}\n')

        unique_type_ids = main_df['type_id'].unique()

        for type_id in unique_type_ids:
            temp_df = main_df[main_df['type_id'] == type_id]
            type_name = items.get(type_id, f"UNKNOWN_ITEM_{type_id}")
            await db.pushData(temp_df, type_name)

        print(missing_type_ids)
        end = time.time()
        print(end - start)
    
# Run the main coroutine using asyncio's event loop
asyncio.run(main())

