import boto3
import json
import requests
from typing import Dict
from decimal import Decimal
from createNewTable import CreateNewTable


def getItemsPriceHistory(type_id: int,region_id=10000002) -> Dict:
    response = requests.get(f"https://esi.evetech.net/latest/markets/{region_id}/history/?datasource=tranquility&type_id={type_id}")
    return json.dumps(response.json())

dynamodb = boto3.resource('dynamodb','us-east-1')
# dynamodb.create_table(TableName="tester")

newTable = CreateNewTable()
newTable.createPriceHistoryTable("TRITANIUM","TRITANIUM")
table = dynamodb.Table("TRITANIUM")
jsonstuff = getItemsPriceHistory(34)
jsondata = json.loads(jsonstuff, parse_float=Decimal)

for myDict in jsondata:
#     print(myDict)
    # myDict.update({'TRITANIUM':34})
    # print(myDict)
    table.put_item(Item = myDict)
