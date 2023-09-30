import json
from ItemIdEnum import item
from RegionIdEnum import region
import logging
import pathlib 
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import os


class PushData():
    def __init__(self) -> None:
        self.session = boto3.Session()
        self.s3_client = boto3.client('s3')
        
    def listAllBuckets(self) -> list:
        s3 = self.session.resource('s3')
        for bucket in s3.buckets.all():
            print(bucket.name)
        return s3.buckets.all()
    
    def pushCsvToS3(self, pathToData: pathlib.Path,bucketName: str ) -> bool:
        for subpath in pathToData.rglob('*.bz2'):  
            try:
                self.s3_client.upload_file(subpath, bucketName, f'{subpath.parents[1].name}/{subpath.name}')
            except ClientError as e:
                logging.error(e)
                return False
            print(f'Done pushing: {subpath}')
        return True
            
    def createS3Bucket(self,bucketName: str) -> bool:
        try:
            self.s3_client.create_bucket(Bucket=bucketName)
        except ClientError as e:
            logging.error(e)
            return False
        return True
    
    def createBucketDir(self,bucketName: str, dirName: str) -> bool:
        s3 = self.session.resource('s3')
        bucket = s3.Bucket(bucketName)
        try:
            bucket.put_object(Key=dirName)
        except ClientError as e:
            logging.error(e)
            return False
        return True
    
    def pushFolderToS3(self,pathToData: pathlib.Path, bucketName: str,dirName: str) -> bool:
        exist = self.createBucketDir(bucketName,dirName)
        if exist:
            for subpath in pathToData.rglob('*'): 
                if subpath.is_file():
                    try:
                        self.s3_client.upload_file(subpath, bucketName, f'{dirName}/{subpath.name}')
                    except ClientError as e:
                        logging.error(e)
                        return False
                    print(f'Done pushing: {subpath}')
        return True
                
        
        
        
# --------------------------

def main():
    path = pathlib.Path("D:\\Code\\eve-aws\\LSTM_models\\")
    test = PushData()
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    # test.createS3Bucket("eve-market-order-history")
    test.pushFolderToS3(path, "eve-model-history",dt_string)

if __name__ == "__main__":
    main()