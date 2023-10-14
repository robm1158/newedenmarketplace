from typing import Dict
import aiohttp
import json
from decimal import Decimal

# Define a header with necessary details for API requests.
header = {
    "In-Game-Name": "XiT Statik Daphiti",
    "Discord-Name": "xit_statik",
    "email": "mullins097956@gmail.com",
    "application": "EVE-AWS"
}

async def getItemsPriceHistory(type_id: int, region_id: int) -> Dict:
    """
    Asynchronously fetch the price history for a specific item type in a given region 
    from the EVE Online ESI API.

    Parameters:
        type_id (int): The ID of the item type to fetch the price history for.
        region_id (int): The ID of the region to fetch the price history from.

    Returns:
        Dict: A dictionary containing the price history data for the given item type.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://esi.evetech.net/latest/markets/{region_id}/history/?datasource=tranquility&type_id={type_id}", headers=header) as response:
            data = await response.json()
            return data  # type: ignore

async def getAllItemOrderHistory(type_id: int, region_id: int) -> Dict:
    """
    Asynchronously fetch current orders for a specific item type in a given region 
    from the EVE Online ESI API.

    Parameters:
        type_id (int): The ID of the item type to fetch orders for.
        region_id (int): The ID of the region to fetch orders from.

    Returns:
        Dict: A dictionary containing the order data for the given item type.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://esi.evetech.net/latest/markets/{region_id}/orders/?datasource=tranquility&order_type=all&page=1&type_id={type_id}", headers=header) as response:
            data = await response.json()
            return json.dumps(data)  # type: ignore

async def getRegionOrderIds(region_id: int) -> list:
    """
    Asynchronously fetch a list of order IDs for a given region from the EVE Online ESI API.
    This function paginates through the API until all order IDs are retrieved.

    Parameters:
        region_id (int): The ID of the region to fetch order IDs for.

    Returns:
        list: A list containing all order IDs for the given region.
    """
    idList = []
    pageNum = 1

    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(f"https://esi.evetech.net/latest/markets/{region_id}/types/?datasource=tranquility&page={pageNum}", headers=header) as response:
                # Exit the loop if a 404 status is returned (indicating no further data)
                if response.status == 404:
                    break

                data = await response.json()
                idList.append(data)

                pageNum += 1

    return idList
