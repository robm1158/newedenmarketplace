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
#

path = pathlib.Path('/root/code/data/market-orders-2021-06-19_16-50-12.v3.csv.bz2')
data = pd.read_csv(path)
#print(data)

region_index = data.columns.get_loc('region_id')
#print(region_index)
#print(region_index)
newData = pd.DataFrame(columns=data.columns)
print(newData)
for row in data.values:
  if row[region_index] == region.THE_FORGE.value:
    newData.loc[len(newData)] = row.tolist()
  
newCSVName = path.parent.joinpath('the-forge-historical-' + str(path.name))
newData.to_csv(newCSVName, index=False)      
print(newData)
    
#the-forge-historical-market-orders-2021-06-19_16-50-12.v3.csv.bz2
