import boto3
import sys
import os
import pandas as pd
import csv
import io
import asyncio
import numpy as np
import pathlib
from ItemIdEnum import item
from io import StringIO
import dask.dataframe as dd

class PullData():
    def __init__(self) -> None:    
        self.bucketName = 'eve-market-order-history'
        
    async def getItemData(self, itemId: int, regionId: int) -> pd.DataFrame:
        # Using Dask to read CSV files directly from S3
        # Construct S3 file paths for the first 30 files
        file_list = dd.read_csv(f's3://{self.bucketName}/2021/2021-07-10/*.csv.bz2', storage_options={ 'use_ssl': True},blocksize=None,assume_missing=True).compute() # type: ignore

        # # Now we can perform comparison on the Dask dataframe
        result_df = file_list[(file_list['type_id'] == itemId) & (file_list['region_id'] == regionId)]
        
        return result_df
        
    def getObjectList(self) -> list:
        s3 = boto3.resource('s3')
        objectLists = []
        bucket = s3.Bucket(self.bucketName)
        for object in bucket.objects.all():
            path = pathlib.Path(object.key)
            if not path.name.endswith('.tmp'):
                objectLists.append(path)
            
        return objectLists
