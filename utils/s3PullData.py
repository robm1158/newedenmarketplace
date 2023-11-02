import boto3
# import sys
# import os
import pandas as pd
# import csv
# import io
# import asyncio
# import numpy as np
import pathlib
from ItemIdEnum import item
# from io import StringIO
import dask.dataframe as dd

class PullData():
    def __init__(self) -> None:    
        self.bucketName = 'eve-market-order-history'
        
    async def getItemData(self, itemId: int, regionId: int, path: str) -> pd.DataFrame:
        # Using Dask to read CSV files directly from S3
        # Construct S3 file paths for the first 30 files
        file_list = dd.read_csv(f's3://{self.bucketName}/{path}', storage_options={ 'use_ssl': True},blocksize=None,assume_missing=True) # type: ignore

        # # Now we can perform comparison on the Dask dataframe
        result_df = file_list[(file_list['type_id'] == itemId) & (file_list['region_id'] == regionId)]
        
        return result_df.compute()
        
    def getS3ObjectList(self) -> list:
        s3 = boto3.resource('s3')
        objectLists = []
        bucket = s3.Bucket(self.bucketName)
        for object in bucket.objects.all():
            path = pathlib.Path(object.key)
            if path.name.endswith('.csv.bz2'):
                objectLists.append(str(path))
            
        return objectLists
