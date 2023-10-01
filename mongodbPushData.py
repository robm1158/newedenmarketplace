
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from passwordsEnum import passwords
from ItemIdEnum import item
import pathlib
import s3PullData
import asyncio
import pandas as pd
from json import loads, dumps

class mongoPushData():
    def __init__(self, dbName:str) -> None:
        self.uri = f"mongodb+srv://{passwords.mongoUser.value}:{passwords.mongoPassword.value}@serverlessinstance0.drbmrdi.mongodb.net/?retryWrites=true&w=majority"

        # Create a new client and connect to the server
        self.client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.dbName = dbName
    
    def checkConnection(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
    
    def createCollection(self, collectionName: str) -> None:
        if collectionName in self.client[self.dbName].list_collection_names():
            print("Collection already exists")
        else:   
            db = self.client[self.dbName]
            collection = db[collectionName]
            print("Created Collection")
    
    
    def pushData(self, data: pd.DataFrame, collectionName: str) -> None:
        self.createCollection(collectionName)
        db = self.client[self.dbName]
        collection = db[collectionName]
        result = data.to_dict(orient="dict")
        collection.insert_one(result)
        print("Finished Pushing Data")
    


async def main():
    puller = s3PullData.PullData()
    db = mongoPushData('eve-historical-data')
    db.checkConnection()
    for items in item:
        for path in puller.getS3ObjectList():
            print(path,items.name)
            result = await puller.getItemData(items.value, regionId=10000002, path=path)
            result.reset_index(inplace=True)
            result.index = result.index.map(str)
            db.pushData(result,items.name)


        
asyncio.run(main())