from mimetypes import init
from typing import Dict
import requests
import json
from ItemIdEnum import item
from RegionIdEnum import region
from decimal import Decimal



def getItemsPriceHistory(type_id: int,region_id: int) -> Dict:
    response = requests.get(f"https://esi.evetech.net/latest/markets/{region_id}/history/?datasource=tranquility&type_id={type_id}")
    return json.dumps(response.json())

def getAllItemOrderHistory(type_id: int,region_id: int) -> Dict:
    response = requests.get(f"https://esi.evetech.net/latest/markets/{region_id}/orders/?datasource=tranquility&order_type=all&page=1&type_id={type_id}")
    return json.dumps(response.json())

# This will need to be turned into an async function and even recursive async
def getRegionOrderIds(region_id: int) -> list:
    pageNum = 1
    idList = []
    response = requests.get(f"https://esi.evetech.net/latest/markets/{region_id}/types/?datasource=tranquility&page={pageNum}")
    while response != 404:
        response = requests.get(f"https://esi.evetech.net/latest/markets/{region_id}/types/?datasource=tranquility&page={pageNum}")
        idList.append(response.json())
        pageNum+=1
        # print(pageNum)
    # print(len(idList))
    return idList
# print(getRegionOrderIds(region.THE_FORGE.value))
# itemjson = getAllItemOrderHistory(item["PHASED_PLASMA_L"].value,region.THE_FORGE.value)
# print(type(json.loads(itemjson, parse_float=Decimal)))
# itemjson = getItemsPriceHistory(item["PHASED_PLASMA_L"].value,region.THE_FORGE.value)
# jsondata = json.loads(itemjson, parse_float=Decimal)
# print(type(jsondata))