
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import utils.itemPrices as ip
import pathlib
import asyncio
import gc
import utils.mongodbData as mdb
from items_dict import items
from createLSTM import createHistoryLSTM

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 17)
pd.set_option('display.width', 250)


async def main():
    db = mdb.mongoData('eve-historical-daily-the-forge')
    df = await db.pullAllCollectionDocuments(items[34])
    df = df.drop_duplicates()
    df = df.sort_values(by='date')
    df = df.drop(columns=['item_name'])
    createHistoryLSTM(items[34],df,30, 1, 200, 16, True, True)
 

asyncio.run(main())



