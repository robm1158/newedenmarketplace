import json
import asyncio
import aioboto3
from concurrent.futures import ThreadPoolExecutor
from createNewTable import CreateNewTable
import itemPrices
from ItemIdEnum import item
from RegionIdEnum import region
import logging

class pushData:
    def __init__(self) -> None:
        self.dynamodb = aioboto3.resource('dynamodb')
        self.newTable = CreateNewTable()

    async def pushPriceHistoryToDynamo(self, tableName: str) -> None:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self.newTable.createPriceHistoryTable, tableName)

        if response == 200:
            logging.info(f'Create new table {tableName}')
            table = await self.dynamodb.Table(tableName)
            await table.wait_until_exists()
            logging.info("Done waiting")
            itemjson = await itemPrices.getItemsPriceHistory(item[tableName].value, region.THE_FORGE.value)
            jsondata = json.loads(itemjson)
            async with table.batch_writer() as batch:
                for myDict in jsondata:
                    await batch.put_item(Item=myDict)
        else:
            logging.info("[pushPriceHistoryToDynamo] Just update the table")
            table = await self.dynamodb.Table(tableName)
            itemjson = await itemPrices.getItemsPriceHistory(item[tableName].value, region.THE_FORGE.value)
            jsondata = json.loads(itemjson)
            async with table.batch_writer() as batch:
                for myDict in jsondata:
                    await batch.put_item(Item=myDict)
        
        logging.info(f'[pushPriceHistoryToDynamo] Finished pushing the {tableName} table')

    async def pushItemOrdersToDynamo(self, tableName: str) -> None:
        loop = asyncio.get_event_loop()
        stringName = tableName + "_ORDERS"
        response = await loop.run_in_executor(None, self.newTable.createItemOrderTable, stringName)

        if response == 200:
            logging.info(f'[pushItemOrdersToDynamo] Create new table {stringName}')
            table = await self.dynamodb.Table(stringName)
            await table.wait_until_exists()
            logging.info("Done waiting")
            itemjson = await itemPrices.getAllItemOrderHistory(item[tableName].value, region.THE_FORGE.value)
            jsondata = json.loads(itemjson)
            async with table.batch_writer() as batch:
                for myDict in jsondata:
                    await batch.put_item(Item=myDict)
        else:
            logging.info("Just update the table")
            table = await self.dynamodb.Table(stringName)
            itemjson = await itemPrices.getAllItemOrderHistory(item[tableName].value, region.THE_FORGE.value)
            jsondata = json.loads(itemjson)
            async with table.batch_writer() as batch:
                for myDict in jsondata:
                    await batch.put_item(Item=myDict)
        
        logging.info(f'[pushItemOrdersToDynamo] Finished pushing the {tableName}_ORDERS table')