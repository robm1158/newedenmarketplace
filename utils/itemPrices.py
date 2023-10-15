from typing import Dict
import aiohttp
import json
from decimal import Decimal
import asyncio


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
            try:
                data = await response.json()
            except aiohttp.client_exceptions.ContentTypeError:
                print(f"Failed to decode JSON for type_id {type_id}. URL: {response.url}")
                data = None

            return json.dumps(data)  # type: ignore

async def fetch_page(session, url) -> tuple:
    """Fetch a single page from the API."""
    async with session.get(url) as response:
        content_type = response.headers.get('Content-Type')
        
        # If not JSON or 500, treat as end of pagination
        if response.status == 500 or (content_type and 'application/json' not in content_type):
            return None, response.headers
        
        return await response.json(), response.headers

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

    async with aiohttp.ClientSession() as session:
        # Fetch the first page to get total number of pages from the headers
        _, headers = await fetch_page(session, f"https://esi.evetech.net/latest/markets/{region_id}/types/?datasource=tranquility&page=1")
        print(headers)
        total_pages = int(headers.get('X-Pages', 1))

        tasks = [fetch_page(session, f"https://esi.evetech.net/latest/markets/{region_id}/types/?datasource=tranquility&page={i}") for i in range(1, total_pages + 1)]
        results = await asyncio.gather(*tasks)

        for page, _ in results:
            if page is not None:
                idList.extend(page)

    return idList
