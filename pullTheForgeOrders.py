#!/usr/local/bin/python
import sys
import pandas as pd
import aiohttp
import asyncio
from io import StringIO
import time
from motor.motor_asyncio import AsyncIOMotorClient
import utils.mongodbData as mdb
from items_dict import items
from updateEtags import updateEtags

header = {
    "In-Game-Name": "XiT Statik Daphiti",
    "Discord-Name": "xit_statik",
    "email": "mullins097956@gmail.com",
    "application": "EVE-AWS",
    "If-None-Match": ""
}

df = pd.read_csv('current_forge_etags.csv', header=0, usecols=['url', 'etag'])

async def fetch(session, url, header):
    async with session.get(url, headers=header) as response:
        if response.status == 200:
            return await response.text()
        else:
            print(f"Error: {response.status}: {url}")
            return None

async def get_names_from_ids(ids):
    url = "https://esi.evetech.net/latest/universe/names/?datasource=tranquility"
    ids = [int(id) for id in ids]
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
    await updateEtags()
    start = time.time()
    db = mdb.mongoData('eve-orders-the-forge') 
    dfs = []
    tasks = []
    urls = [f"https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=all&page={i}" for i in range(1, len(df) + 1)] 

    async with aiohttp.ClientSession() as session:
        for url, etag in zip(urls, df['etag']):  
            header["If-None-Match"] = etag
            tasks.append(asyncio.create_task(fetch(session, url, header)))

        responses = await asyncio.gather(*tasks)

        for response_text in responses:
            if response_text:
                dfs.append(pd.read_json(StringIO(response_text)))

    if dfs:  
        main_df = pd.concat(dfs, ignore_index=True)
        main_df = main_df.sort_values(by=['type_id'])
        type_ids = main_df['type_id'].unique()  

        # Convert the values of the dictionary to a set (assuming they are integers)
        item_values = set(items.keys())

        # Get unique type_ids as integers
        type_ids = main_df['type_id'].unique()

        # Find items in type_ids that are not in item_values
        missing_type_ids = [type_id for type_id in type_ids if type_id not in item_values]


        print(f"Missing type_ids: {missing_type_ids}, len: {len(missing_type_ids)}")
        if missing_type_ids:
            id_name_mapping = await get_names_from_ids(list(missing_type_ids))  # Don't forget to pass the session here
            for entity in id_name_mapping:
                type_id = entity.get('id')  # Keep the ID as an integer, don't convert to string
                type_name = entity.get('name').upper().replace(" ", "_").replace("'", "").replace("\\", "").replace("/", "")  # Formatting the name
                items[type_id] = type_name  # Set the item name as the key and the ID as the value

        with open('items_dict.py', 'w') as file:
            file.write('items = {\n')
            for k, v in items.items():
                file.write(f"    {k}: '{v}',\n")  # Write the item's name and ID without quotes around the value
            file.write('}\n')
            
        print(f'unique ids in this fetch: {len(type_ids)}')
        async def push_single_document(type_id):
            type_name = items.get(type_id)
            temp_df = main_df[main_df['type_id'] == type_id]
            await db.pushData(temp_df, type_name)

        tasks = [push_single_document(type_id) for type_id in type_ids]
        await asyncio.gather(*tasks)

    end = time.time()
    print(f"Execution time: {end - start}")

# Run the main coroutine using asyncio's event loop
asyncio.run(main())
