
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from passwordsEnum import passwords
from ItemIdEnum import item
import pathlib
import s3PullData
import asyncio
import pandas as pd
from json import loads, dumps
from motor.motor_asyncio import AsyncIOMotorClient

class mongodbData():
    def __init__(self, dbName:str) -> None:
        self.uri = f"mongodb+srv://{passwords.mongoUser.value}:{passwords.mongoPassword.value}@serverlessinstance0.drbmrdi.mongodb.net/?retryWrites=true&w=majority"
        
        # Create a new client and connect to the server
        self.client = AsyncIOMotorClient(self.uri)
        self.dbName = dbName

    async def checkConnection(self):
        try:
            await self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    async def createCollection(self, collectionName: str) -> None:
        print(collectionName in await self.client[self.dbName].list_collection_names())
        if collectionName in await self.client[self.dbName].list_collection_names():
            print("Collection already exists")
        else:   
            db = self.client[self.dbName]
            collection = db[collectionName]
            print("Created Collection")

    async def getCollectionList(self) -> list:
        db = self.client[self.dbName]
        collection_names = await db.list_collection_names()
        return collection_names
    
    async def pushData(self, data: pd.DataFrame, collectionName: str) -> None:
        await self.createCollection(collectionName)
        db = self.client[self.dbName]
        collection = db[collectionName]
        result = data.to_dict(orient="list")
        await collection.insert_one(result)
        print("Finished Pushing Data")
    
    async def pullData(self, collectionName: str):
        db = self.client[self.dbName]
        collection = db[collectionName]

        documents = collection.find({}, {"issued": 1, "price": 1, "is_buy_order": 1, "_id": 0})
        df = pd.DataFrame(list(documents))
        all_data = []
        for idx, row in df.iterrows():
            issued = list(row['issued'].values())
            price = list(row['price'].values())
            for i, p in zip(issued, price):
                all_data.append({'issued': i, 'price': p})

        flattened_df = pd.DataFrame(all_data)

        return flattened_df

    async def deleteDB(self, dbName: str) -> None:
        await self.client.drop_database(dbName)
        print(f"Deleted {dbName}")


async def main():
    puller = s3PullData.PullData()
    db = mongoData('eve-market-order-history-the-forge')
    await db.checkConnection()

    for object in puller.getS3ObjectList():
        for items in item:
            print(f'================== {items.name} ==================')
            object = object.replace('\\', '/')
            print(object)
            result = await puller.getItemData(items.value, regionId=10000002, path=object)
            await db.pushData(result, items.name)

        
asyncio.run(main())