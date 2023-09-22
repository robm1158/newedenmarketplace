import json
import dynamodbPushData
import RegionIdEnum
import ItemIdEnum
import asyncio
import aiohttp
import itemPrices
import pandas as pd
import pathlib
from RegionIdEnum import region

# for directory in pathlib.Path("/root/code/data/").iterdir():
#   if str(directory) != "/root/code/data/index.html.tmp": 
#     data = pd.read_csv(directory)
#     print(data)

# How the file name should appear once reconstructed:
# #the-forge-historical-market-orders-2021-06-19_16-50-12.v3.csv.bz2

path = pathlib.Path('/root/code/data/market-orders-2021-06-19_16-50-12.v3.csv.bz2')
data = pd.read_csv(path)

newCSVName = path.parent.joinpath("the-forge-historical2-" + path.name)
print(data.loc[data['region_id'] == region.THE_FORGE.value])
data.loc[data['region_id'] == region.THE_FORGE.value].to_csv(newCSVName, index=False)






