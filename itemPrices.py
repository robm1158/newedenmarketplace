from typing import Dict
import aiohttp
import asyncio
import json
from decimal import Decimal
import requests
from tqdm import tqdm

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

async def getGroups() -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://esi.evetech.net/latest/markets/groups/") as response:
            data = await response.json()
            return data
        

async def fetch(session, group):
    url = f"https://esi.evetech.net/latest/markets/groups/{group}/?datasource=tranquility&language=en"
    async with session.get(url) as response:
        return await response.json()

async def unravelGroupsAsync(data: list):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, group) for group in data]
        return await asyncio.gather(*tasks)

def unravelGroups(data: list):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(unravelGroupsAsync(data))
    return result


def construct_hierarchy(data):
    def find_children(parent_id):
        children = []
        for item in tqdm(data, total=100):
            if item.get('parent_group_id') == parent_id:
                child = {
                    "description": item["description"],
                    "market_group_id": item["market_group_id"],
                    "name": item["name"],
                    "types": item["types"]
                }
                child['children'] = find_children(item["market_group_id"])
                children.append(child)
        return children

    root_items = [item for item in data if "parent_group_id" not in item]
    hierarchy = []

    for root in tqdm(root_items, total=100):
        root_data = {
            "description": root["description"],
            "market_group_id": root["market_group_id"],
            "name": root["name"],
            "types": root["types"],
            "children": find_children(root["market_group_id"])
        }
        hierarchy.append(root_data)
    return hierarchy