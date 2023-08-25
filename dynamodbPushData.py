import boto3
import json
import requests
from typing import Dict
from decimal import Decimal
from createNewTable import CreateNewTable
import itemPrices
from ItemIdEnum import item
from RegionIdEnum import region

class pushData:
    def __init__(self) -> None:
        self.dynamodb = boto3.resource('dynamodb')
        self.newTable = CreateNewTable()

    def pushPriceHistoryToDynamo(self,tableName: str)->None:
        response = self.newTable.createPriceHistoryTable(tableName)
        print(response)
        if response == 200:
            print(f'Create new table {tableName}')
            table = self.dynamodb.Table(tableName)
            table.wait_until_exists()
            print("Done waiting")
            jsonstuff = itemPrices.getItemsPriceHistory(item[tableName].value,region.THE_FORGE.value)
            jsondata = json.loads(jsonstuff, parse_float=Decimal)
            for myDict in jsondata:
                # print(myDict)
                table.put_item(Item = myDict)
        else:
            print("Just update the table")
            table = self.dynamodb.Table(tableName)
            jsonstuff = itemPrices.getItemsPriceHistory(item[tableName].value,region.THE_FORGE.value)
            jsondata = json.loads(jsonstuff, parse_float=Decimal)
            for myDict in jsondata:
                # print(myDict)
                table.put_item(Item = myDict)
        print(f'Finished pushing the {tableName} table')

