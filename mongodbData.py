
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from passwordsEnum import passwords
from ItemIdEnum import item
import pathlib
import s3PullData
import asyncio
import pandas as pd
from json import loads, dumps

class mongoData():
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
    
    def getCollectionList(self) -> list:
        db = self.client[self.dbName]
        collection_names = db.list_collection_names()
        return collection_names
    
    
    def pushData(self, data: pd.DataFrame, collectionName: str) -> None:
        self.createCollection(collectionName)
        db = self.client[self.dbName]
        collection = db[collectionName]
        result = data.to_dict(orient="dict")
        collection.insert_one(result)
        print("Finished Pushing Data")
        
    def pullData(self, collectionName: str):
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

# async def main():
#     db = mongoData('eve-historical-data')
#     db.checkConnection()
#     collectionList = db.getCollectionList()
#     for item in collectionList:
#         print(item)
#         data = db.pullData(item)
#         print(data)


        
# asyncio.run(main())