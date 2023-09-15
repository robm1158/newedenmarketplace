import json
import asyncio
import aioboto3
from createNewTable import CreateNewTable
import itemPrices
from ItemIdEnum import item
from RegionIdEnum import region
import logging
from decimal import Decimal

class PushData:
    def __init__(self) -> None:
        self.session = aioboto3.Session()
        self.newTable = CreateNewTable()

    async def pushPriceHistoryToDynamo(self, table_name: str) -> None:
        async with self.session.resource('dynamodb') as dynamodb:
            response = await asyncio.to_thread(self.newTable.createPriceHistoryTable, table_name)

            if response == 200:
                logging.info(f'Creating new table {table_name}')
                table = await dynamodb.Table(table_name)
                await table.wait_until_exists()
                self.newTable.enableAutoScaling(table_name)
            else:
                table = await dynamodb.Table(table_name)

            await self.updatePriceHistoryTable(table, table_name, item[table_name].value)
            logging.info(f'Finished pushing the {table_name} table')

    async def pushItemOrdersToDynamo(self, table_name: str) -> None:
        string_name = f"{table_name}_ORDERS"
        response = await asyncio.to_thread(self.newTable.createItemOrderTable, string_name)

        async with self.session.resource('dynamodb') as dynamodb:
            if response == 200:
                logging.info(f'Creating new table {string_name}')
                table = await dynamodb.Table(string_name)
                await table.wait_until_exists()
                self.newTable.enableAutoScaling(string_name)
            else:
                table = await dynamodb.Table(string_name)

            await self.updateItemOrderTable(table, string_name, item[table_name].value)
            logging.info(f'Finished pushing the {string_name} table')

    async def updatePriceHistoryTable(self, table, table_name, item_id):
        itemjson = await itemPrices.getItemsPriceHistory(item_id, region.THE_FORGE.value)
        jsondata = json.loads(itemjson, parse_float=Decimal)

        async with table.batch_writer() as batch:
            for myDict in jsondata:
                await batch.put_item(Item=myDict)

    async def updateItemOrderTable(self, table, table_name, item_id):
        itemjson = await itemPrices.getAllItemOrderHistory(item_id, region.THE_FORGE.value)
        jsondata = json.loads(itemjson, parse_float=Decimal)

        async with table.batch_writer() as batch:
            for myDict in jsondata:
                await batch.put_item(Item=myDict)