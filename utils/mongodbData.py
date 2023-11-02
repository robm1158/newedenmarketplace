import sys
import os
sys.path.append('/root/code/eve-aws/utils')
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from passwordsEnum import passwords
from ItemIdEnum import item
import pandas as pd
from json import loads, dumps
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from pymongo import DESCENDING


class mongoData():
    CLIENT = None
    def __init__(self, dbName:str) -> None:
        """
        Initialize the mongoData class with the specified database name.

        Parameters:
            dbName (str): The name of the MongoDB database.
        """
        MONGO_USER = os.environ.get("MONGO_USER")
        MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
        self.uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@evestoragecluster.4jc1x.mongodb.net/?retryWrites=true&w=majority&maxPoolSize=200"
        self.syncClient = MongoClient(self.uri)
        # If CLIENT is not instantiated, create it
        if mongoData.CLIENT is None:
            mongoData.CLIENT = AsyncIOMotorClient(self.uri)
        # Create a new asynchronous client and connect to the server
        # self.client = AsyncIOMotorClient(self.uri)
        self.dbName = dbName

    async def pushData(self, data: pd.DataFrame, collectionName: str, use_time_for_id=False) -> None:
        """
        Asynchronously push data from a pandas DataFrame to the specified MongoDB collection.

        Parameters:
            data (pd.DataFrame): The data to be pushed to MongoDB.
            collectionName (str): The name of the collection to push the data to.
        """
        await self.createCollection(collectionName)
        db = self.CLIENT[self.dbName]
        collection = db[collectionName]
        result = data.to_dict(orient="list")  # Convert DataFrame to list of dicts
        
        result['_id'] = datetime.now().isoformat()  # Unique string based on the current time

        await collection.insert_one(result)
        # print(f"Finished Pushing {collectionName} Data")
    

    async def checkConnection(self):
        """
        Asynchronously check if a connection to the MongoDB server is established by pinging it.
        """
        try:
            await self.CLLIENT.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    async def createCollection(self, collectionName: str) -> None:
        """
        Asynchronously create a collection with the specified name in the database.

        Parameters:
            collectionName (str): The name of the collection to be created.
        """
        if collectionName in await self.CLIENT[self.dbName].list_collection_names():
            # print("Collection already exists")
            pass
        else:   
            db = self.CLIENT[self.dbName]
            collection = db[collectionName]
            print(f"Created Collection {collectionName}")

    async def getCollectionList(self) -> list:
        """
        Asynchronously retrieve a list of all collection names in the database.

        Returns:
            list: A list containing the names of all collections in the database.
        """
        db = self.CLIENT[self.dbName]
        collection_names = await db.list_collection_names()
        return collection_names
    
   
    async def pullData(self, collectionName: str):
        """
        Asynchronously pull data from the specified MongoDB collection and return it as a pandas DataFrame.

        Parameters:
            collectionName (str): The name of the collection to pull data from.

        Returns:
            pd.DataFrame: The pulled data in a pandas DataFrame format.
        """
        db = self.CLIENT[self.dbName]
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
        """
        Asynchronously delete the specified database from the MongoDB server.

        Parameters:
            dbName (str): The name of the database to be deleted.
        """
        await self.CLIENT.drop_database(dbName)
        print(f"Deleted {dbName}")
        
    async def pullAllCollectionDocuments(self, collectionName: str) -> None:
        """
        Asynchronously pull all documents from the specified MongoDB collection.

        Parameters:
            collectionName (str): The name of the collection to pull documents from.

        Returns:
            list: A list containing all documents from the specified collection.
        """
        def ensure_list(value):
            """Convert scalar values to single-item list or return the value if it's already a list-like."""
            if value is None:
                return [None]
            elif isinstance(value, (list, pd.Series)):
                return value
            else:
                return [value]
        db = self.CLIENT[self.dbName]
        collection = db[collectionName]
        documents = await collection.find({}).to_list(length=None)
        
        df = pd.DataFrame(columns=['date','average','highest',
                          'lowest','order_count','volume','item_name'])

        for document in documents:

            date_data = ensure_list(document.get('date'))
            average_data = ensure_list(document.get('average'))
            highest_data = ensure_list(document.get('highest'))
            lowest_data = ensure_list(document.get('lowest'))
            order_count_data = ensure_list(document.get('order_count'))
            volume_data = ensure_list(document.get('volume'))
            item_name = collectionName
        
            df1 = pd.DataFrame({
                'date': date_data,
                'average': average_data,
                'highest': highest_data,
                'lowest': lowest_data,
                'order_count': order_count_data,
                'volume': volume_data,
                'item_name': item_name
                })
            df = pd.concat([df, df1])

        return df
    
    def syncPullAllCollectionDocuments(self, collectionName: str) -> None:
        """
        Pull all documents from the specified MongoDB collection.

        Parameters:
            collectionName (str): The name of the collection to pull documents from.

        Returns:
            DataFrame: A dataframe containing all documents from the specified collection.
        """
        def ensure_list(value):
            """Convert scalar values to single-item list or return the value if it's already a list-like."""
            if value is None:
                return [None]
            elif isinstance(value, (list, pd.Series)):
                return value
            else:
                return [value]

        db = self.syncClient[self.dbName]
        collection = db[collectionName]
        
        # Use pymongo's find method directly
        documents = list(collection.find({}))

        df = pd.DataFrame(columns=['date','average','highest',
                        'lowest','order_count','volume','item_name'])

        for document in documents:

            date_data = ensure_list(document.get('date'))
            average_data = ensure_list(document.get('average'))
            highest_data = ensure_list(document.get('highest'))
            lowest_data = ensure_list(document.get('lowest'))
            order_count_data = ensure_list(document.get('order_count'))
            volume_data = ensure_list(document.get('volume'))
            item_name = collectionName

            df1 = pd.DataFrame({
                'date': date_data,
                'average': average_data,
                'highest': highest_data,
                'lowest': lowest_data,
                'order_count': order_count_data,
                'volume': volume_data,
                'item_name': item_name
                })
            df = pd.concat([df, df1])

        return df

    def syncPullLastDocument(self, collectionName: str) -> dict:
        """
        Pull the last document from the specified MongoDB collection.

        Parameters:
            collectionName (str): The name of the collection to pull the last document from.

        Returns:
            dict: The last document in the specified collection.
        """
        db = self.syncClient[self.dbName]
        collection = db[collectionName]

        # Sort by the 'date' field (or replace 'date' with your custom field name)
        last_document = collection.find_one(sort=[("_id", DESCENDING)])
        
        # Convert the result to a DataFrame
        df = pd.DataFrame(last_document)
        df = df.drop(columns=['_id'])
        # df = df.explode('order_id')
        # df = df.explode('issued')
        # df = df.explode('is_buy_order')
        # df = df.explode('price')
        # df = df.explode('system_id')
        return df


# The main function and its calls are commented out, but it serves to:
# - Establish a connection to MongoDB.
# - Fetch data from an S3 bucket using the s3PullData module.
# - Push this data to the MongoDB instance.
# async def main():
#     puller = s3PullData.PullData()
#     db = mongoData('eve-market-order-history-the-forge')
#     await db.checkConnection()
#     for object in puller.getS3ObjectList():
#         for items in item:
#             print(f'================== {items.name} ==================')
#             object = object.replace('\\', '/')
#             print(object)
#             result = await puller.getItemData(items.value, regionId=10000002, path=object)
#             await db.pushData(result, items.name)
# asyncio.run(main())
