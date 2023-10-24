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
    await db.checkConnection()
    
    path = pathlib.Path("/root/code/market-history/data.everef.net/market-history/2023/")

    dfs = []
    main_df =None
    for csv in path.rglob("*.csv.bz2"):
            df = pd.read_csv(csv)
            filtered_df =  df[df["region_id"] == 10000002]
            if not filtered_df.empty:
                dfs.append(filtered_df)
                
            if dfs:
                main_df = pd.concat(dfs, ignore_index=True)
    
    for key in items.keys():
        filtered_df = main_df[(main_df["type_id"] == key)]
        await db.pushData(filtered_df, items[key])
        print(items[key])
        print(filtered_df)
                        
    
            
asyncio.run(main())