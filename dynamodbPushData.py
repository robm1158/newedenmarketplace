import boto3
import json
import requests
from typing import Dict
from decimal import Decimal
from createNewTable import CreateNewTable
import itemPrices
from ItemIdEnum import item
from RegionIdEnum import region
import logging

class pushData:
    def __init__(self) -> None:
        self.dynamodb = boto3.resource('dynamodb')
        self.newTable = CreateNewTable()

    def pushPriceHistoryToDynamo(self,tableName: str)->None:
        response = self.newTable.createPriceHistoryTable(tableName)
        if response == 200:
            logging.info(f'Create new table {tableName}')
            table = self.dynamodb.Table(tableName)
            table.wait_until_exists()
            logging.info("Done waiting")
            itemjson = itemPrices.getItemsPriceHistory(item[tableName].value,region.THE_FORGE.value)
            jsondata = json.loads(itemjson, parse_float=Decimal)
            with table.batch_writer() as batch:
                for myDict in jsondata:
                    response = batch.put_item(Item = myDict)

        else:
            logging.info("[pushPriceHistoryToDynamo] Just update the table")
            table = self.dynamodb.Table(tableName)
            itemjson = itemPrices.getItemsPriceHistory(item[tableName].value,region.THE_FORGE.value)
            jsondata = json.loads(itemjson, parse_float=Decimal)
            with table.batch_writer() as batch:
                for myDict in jsondata:
                    response = batch.put_item(Item = myDict)

        logging.info(f'[pushPriceHistoryToDynamo] Finished pushing the {tableName} table')
        logging.info(f'[pushPriceHistoryToDynamo] Response code {response}')

    def pushItemOrdersToDynamo(self,tableName: str)->None:
        stringName = tableName+"_ORDERS"
        response = self.newTable.createItemOrderTable(stringName)
        print(stringName)
        print(response)
        if response == 200:
            logging.info(f'[pushItemOrdersToDynamo] Create new table {stringName}')
            table = self.dynamodb.Table(stringName)
            table.wait_until_exists()
            logging.info("Done waiting")
            itemjson = itemPrices.getAllItemOrderHistory(item[tableName].value,region.THE_FORGE.value)
            jsondata = json.loads(itemjson, parse_float=Decimal)
            with table.batch_writer() as batch:
                for myDict in jsondata:
                    response = batch.put_item(Item = myDict)
        else:
            logging.info("Just update the table")
            table = self.dynamodb.Table(stringName)
            itemjson = itemPrices.getAllItemOrderHistory(item[tableName].value,region.THE_FORGE.value)
            jsondata = json.loads(itemjson, parse_float=Decimal)
            with table.batch_writer() as batch:
                for myDict in jsondata:
                    response = batch.put_item(Item = myDict)


        logging.info(f'[pushItemOrdersToDynamo] Finished pushing the {tableName}_ORDERS table')
        logging.info(f'[pushItemOrdersToDynamo] Response code {response}')