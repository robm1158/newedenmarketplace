import json
from ItemIdEnum import item
from RegionIdEnum import region
import logging
import pathlib 
import boto3
from botocore.exceptions import ClientError


class PushData():
    def __init__(self) -> None:
        self.session = boto3.Session()
        self.s3_client = boto3.client('s3')
        
    def listAllBuckets(self) -> list:
        s3 = self.session.resource('s3')
        for bucket in s3.buckets.all():
            print(bucket.name)
        return s3.buckets.all()
    
    def pushToS3(self, pathToData: pathlib,bucketName: str ) -> bool:
        for subpath in pathToData.rglob('*.bz2'):  
            try:
                response = self.s3_client.upload_file(subpath, bucketName, f'{subpath.parents[1].name}/{subpath.name}')
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
# --------------------------

def main():
    path = pathlib.Path("/root/code/data/")
    test = PushData()

    # test.createS3Bucket("eve-market-order-history")
    test.pushToS3(path, "eve-market-order-history")

if __name__ == "__main__":
    main()