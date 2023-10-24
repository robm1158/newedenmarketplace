import sys
import pandas as pd
import aiohttp
import asyncio
from io import StringIO
import time
from motor.motor_asyncio import AsyncIOMotorClient
import utils.mongodbData as mdb
from items_dict import items
import pathlib


async def main():
    db = mdb.mongoData('eve-historical-daily-the-forge')
    await db.deleteDB('eve-historical-daily-the-forge')
    # await db.checkConnection()
    
    # path = pathlib.Path("/root/code/market-history/data.everef.net/market-history/2022/")
    # for key in items.keys():
    #     dfs = []
    #     print(items[key])
        # for csv in path.rglob("*.csv.bz2"):
    # df = pd.read_csv("/root/code/market-history/data.everef.net/market-history/2022/market-history-2022-12-31.csv.bz2")
    # print(df[(df["type_id"] == 34) & (df["region_id"] == 10000002)])
        #     filtered_df = df[df["type_id"] == key]
        #     if not filtered_df.empty:
        #         dfs.append(filtered_df)
        # if dfs:
        #     main_df = pd.concat(dfs, ignore_index=True).sort_values(by=['date'])
        #     await db.pushData(main_df, items[key])
        #     print(items[key])
        #     print(main_df)
            
# Run the main coroutine using asyncio's event loop
asyncio.run(main())
