import pandas as pd
import utilities
import numpy as np
from ItemIdEnum import item
import pathlib
import s3PullData
import asyncio
import aiohttp
import itemPrices
import pathlib
import pyarrow as pa
from pathlib import Path
from RegionIdEnum import region
from s3PullData import PullData
# Converts CSV file to Pickle file type with the new name
async def fileToPickle():   
  puller = PullData()
  for directory in puller.getS3ObjectList():
    if str(directory).endswith(".v3.csv.bz2"):
      print(directory)
      data = await puller.getFileData(str(directory))
      new_name = "new-the-forge-historical2-" + directory.name[0:33] + ".pkl"
      data.to_pickle(new_name)
asyncio.run(fileToPickle())

# Reads the pickle file and prints off the data filtered by region_id 
def pickleRead():
  puller = PullData()
  for directory in puller.getS3ObjectList():
    if str(directory).endswith(".pkl"):
      path = pathlib.Path(directory)
      data = pd.read_pickle(path)
      #print(data.loc[data['region_id'] == region.THE_FORGE.value])
#pickleRead()      
