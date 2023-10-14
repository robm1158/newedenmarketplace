from typing import Dict
import aiohttp
import asyncio
import json
from decimal import Decimal
import requests
from tqdm import tqdm

async def fetch(type_id: int, region_id: int, retries=3, backoff=1):
    for i in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://esi.evetech.net/latest/markets/{region_id}/history/?datasource=tranquility&type_id={type_id}") as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"Error fetching data for type_id {type_id}: {response.status}")
                        return {}
        except aiohttp.client_exceptions.ServerDisconnectedError:
            if i < retries - 1:  # i is zero indexed
                print("waiting to retry...")
                await asyncio.sleep(backoff)
                backoff *= 2
            else:
                raise


# an async function that kicks off requests to EVE ESI/API and returns that items price history
async def getItemsPriceHistory(type_id: int, region_id: int) -> Dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://esi.evetech.net/latest/markets/{region_id}/history/?datasource=tranquility&type_id={type_id}") as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Error fetching data for type_id {type_id}: {response.status}")
                return {}

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
        async with session.get(f"https://evetycoon.com/api/v1/market/groups") as response:
            data = await response.json()
            return data
        

# async def fetch(session, url):
#     async with session.get(url) as response:
#         return await response.json()

async def unravelGroupsAsync(data: list) -> list:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for group in data:
            url = f"https://esi.evetech.net/latest/markets/groups/{group['marketGroupID']}/?datasource=tranquility&language=en"
            tasks.append(fetch(session, url))
        
        results = await asyncio.gather(*tasks)

        # Adjusting the structure of results
        structured_results = []
        for group, result in zip(data, results):  # Zip the original data with results for simultaneous iteration
            image_name = group.get('iconFile', f"/Icons/items/{result.get('icon_id', 'default')}.png").split('/')[-1]  # This will give you just the image name
            image_name = "/items/" + image_name
            structured_entry = {
                "market_group_id": result['market_group_id'],
                "marketGroupName": result['name'],
                "description": result['description'],
                "parent_group_id": result.get('parent_group_id', None),
                "iconID": group.get('iconID', None),  # Using iconID from the original data
                "iconFile": image_name,  # Use iconFile from the original data or build it from result's icon_id
                "types": result.get('types', [])
            }
            structured_results.append(structured_entry)

        return structured_results



def unravelGroups(data: list):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(unravelGroupsAsync(data))
    return result


def construct_hierarchy(data):
    def find_children(parent_id):
        children = []
        for item in data:
            if item.get('parent_group_id') == parent_id:
                child = {
                    "description": item["description"],
                    "market_group_id": item["market_group_id"],
                    "name": item["marketGroupName"],
                    "iconFile": item["iconFile"],
                    "types": item["types"]
                }
                child['children'] = find_children(item["market_group_id"])
                children.append(child)
        return children

    # Only root items are those that don't have a 'parent_group_id' 
    # or their 'parent_group_id' value doesn't exist in any other item's 'marketGroupID'.
    root_items = [item for item in data if not item.get('parent_group_id') or not any(x['market_group_id'] == item['parent_group_id'] for x in data)]
    hierarchy = []

    for root in root_items:
        root_data = {
            "description": root["description"],
            "market_group_id": root["market_group_id"],
            "name": root["marketGroupName"],
            "iconFile": root["iconFile"],
            "types": root["types"],
            "children": find_children(root["market_group_id"])
        }
        hierarchy.append(root_data)
    return hierarchy
