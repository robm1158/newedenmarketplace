import boto3
import json
import requests
from typing import Dict
from decimal import Decimal
from createNewTable import CreateNewTable
import itemPrices
from ItemIdEnum import item
from RegionIdEnum import region


def getItemsPriceHistory(type_id: int,region_id: int) -> Dict:
    response = requests.get(f"https://esi.evetech.net/latest/markets/{region_id}/history/?datasource=tranquility&type_id={type_id}")
    return json.dumps(response.json())

dynamodb = boto3.resource('dynamodb','us-east-1')
print(item.TRITANIUM.value)
newTable = CreateNewTable()
newTable.createPriceHistoryTable("TRITANIUM","TRITANIUM")
# table = dynamodb.Table("TRITANIUM")
# jsonstuff = getItemsPriceHistory(item.TRITANIUM.value,region.THE_FORGE.value)
# jsondata = json.loads(jsonstuff, parse_float=Decimal)
# def pushPriceHistoryToDynamo():

# for myDict in jsondata:
# #     print(myDict)
#     # myDict.update({'TRITANIUM':34})
#     # print(myDict)
#     table.put_item(Item = myDict)
