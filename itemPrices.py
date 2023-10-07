from typing import Dict
import aiohttp
import json
from decimal import Decimal
import requests

# an async function that kicks off requests to EVE ESI/API and returns that items price history
async def getItemsPriceHistory(type_id: int, region_id: int) -> Dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://esi.evetech.net/latest/markets/{region_id}/history/?datasource=tranquility&type_id={type_id}") as response:
            data = await response.json()
            return json.dumps(data) # type: ignore

# An async function that kicks off requests to EVE ESI/API that returns that items current orders
async def getAllItemOrderHistory(type_id: int, region_id: int) -> Dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://esi.evetech.net/latest/markets/{region_id}/orders/?datasource=tranquility&order_type=all&page=1&type_id={type_id}") as response:
            data = await response.json()
            return json.dumps(data)  # type: ignore

# Not yet tested or in production
async def getRegionOrderIds(region_id: int) -> list:
    idList = []
    pageNum = 1

    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(f"https://esi.evetech.net/latest/markets/{region_id}/types/?datasource=tranquility&page={pageNum}") as response:
                if response.status == 404:
                    break

                data = await response.json()
                idList.append(data)

                pageNum += 1

    return idList

def getSellItemOrderHistory(type_id: int,region_id: int) -> Dict:
    response = requests.get(f"https://esi.evetech.net/latest/markets/{region_id}/orders/?datasource=tranquility&order_type=sell&page=1&type_id={type_id}")
    return json.dumps(response.json())

def getBuysItemOrderHistory(type_id: int,region_id: int) -> Dict:
    response = requests.get(f"https://esi.evetech.net/latest/markets/{region_id}/orders/?datasource=tranquility&order_type=buy&page=1&type_id={type_id}")
    return json.dumps(response.json())