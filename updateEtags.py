#!/usr/local/bin/python

import sys
sys.path.append('/root/code/eve-aws/utils')
import pandas as pd
import numpy as np
import time
import aiohttp
import asyncio
import utils.mongodbData as mdb  # Assuming utils is a package with mongodbData module

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return url, response.headers.get('etag').strip('"'), int(response.headers.get('X-Pages'))
            else:
                print(f"Error with {url}: {response.status}")
    except Exception as e:
        print(f"Exception with {url}: {str(e)}")
        return None  # or some error indicator


async def updateEtags():
    db = mdb.mongoData('etag-storage')
    df = pd.read_csv('current_forge_etags.csv', header=0, usecols=['url', 'etag'])
    start = time.time()
    url = f"https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=all"
    tasks = []
    async with aiohttp.ClientSession() as session:
        url, etag, xPages = await fetch(session, url)
        print(xPages)

        if len(df) > xPages:
            n = len(df) - xPages
            df = df.iloc[:-n]
        else:
            print("Here1")
            df = pd.DataFrame(columns=['url', 'etag'])
            
            for i in range(1, xPages+1):
                url = f"https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=all&page={i}"
                print(f"Here {i}")
                tasks.append(fetch(session, url))
            print("gather")
            results = await asyncio.gather(*tasks)
            print("Here2")
            for url, etag, _ in results:
                df.loc[len(df.index)] = [url, etag]

    end = time.time()
    df.index = np.arange(1, len(df) + 1)
    await db.pushData(df, 'the-forge-etags', True)
    print(end-start)
    df.to_csv('current_forge_etags.csv')

# Run the async function
if __name__ == "__main__":
    asyncio.run(updateEtags())
