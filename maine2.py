import sys
sys.path.append('/root/code/eve-aws/utils')
import pandas as pd
import utils
import matplotlib.pyplot as plt
import numpy as np
from ItemIdEnum import item
import pathlib
import s3PullData
import asyncio
import mongodbData as mdb
import itemPrices as ip
import datetime as dt


async def process_item(db, item):
    result = await ip.fetch(item.value, 10000002)
    df = pd.DataFrame().from_dict(result)
    await db.pushData_with_retry(df, item.name)

async def main():
    start = dt.datetime.now()
    db = mdb.mongodbData('eve-historical-daily-the-forge')
    await db.checkConnection()
    
    # Create tasks for processing items concurrently
    tasks = [process_item(db, items) for items in item]
    
    # Run tasks concurrently
    await asyncio.gather(*tasks)
    end = dt.datetime.now()
    print(end-start)

# Run the main coroutine using asyncio's event loop
asyncio.run(main())
