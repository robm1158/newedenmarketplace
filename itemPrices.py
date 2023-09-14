from typing import Dict
import aiohttp
import json
from decimal import Decimal


async def getItemsPriceHistory(type_id: int, region_id: int) -> Dict:
    connector = aiohttp.TCPConnector(limit_per_host=20)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(f"https://esi.evetech.net/latest/markets/{region_id}/history/?datasource=tranquility&type_id={type_id}") as response:
            data = await response.json()
            return json.dumps(data)


async def getAllItemOrderHistory(type_id: int, region_id: int) -> Dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://esi.evetech.net/latest/markets/{region_id}/orders/?datasource=tranquility&order_type=all&page=1&type_id={type_id}") as response:
            data = await response.json()
            return json.dumps(data)


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