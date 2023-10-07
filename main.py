import json
import dynamodbPushData
import RegionIdEnum
import ItemIdEnum
import asyncio
import aiohttp
import itemPrices
import pandas as pd
import pathlib
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from RegionIdEnum import region

# Converts CSV file to Pickle file type with the new name
def fileToPickle():   
  for directory in pathlib.Path("/root/code/data/").iterdir():
    if str(directory).endswith(".v3.csv.bz2"):
      data = pd.read_csv(directory)
      new_name = "new-the-forge-historical2-" + directory.name[0:33] + ".pkl"
      data.to_pickle(new_name)
#fileToPickle()

# Reads the pickle file and prints off the data filtered by region_id 
def pickleRead():
  for directory in pathlib.Path("/root/code/data2/").iterdir():
    if str(directory).endswith(".pkl"):
      path = pathlib.Path(directory)
      data = pd.read_pickle(path)
      #print(data.loc[data['region_id'] == region.THE_FORGE.value])
pickleRead()      





