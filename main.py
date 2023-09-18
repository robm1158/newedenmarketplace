import json
import dynamodbPushData
import RegionIdEnum
import ItemIdEnum
import asyncio
import aiohttp
import itemPrices

# # 

# async def main2():
#     # List of type_ids
#     type_ids = ItemIdEnum.item
#     region_id = RegionIdEnum.region.THE_FORGE.value

#     # Gather all asynchronous calls into one, effectively running them concurrently
#     results = await asyncio.gather(*(itemPrices.getItemsPriceHistory(type_id.value, region_id) for type_id in type_ids))

#     print(results)

# async def main():
#     manager =  dynamodbPushData.PushData()
    
#     table_names = list(ItemIdEnum.item)

#     # Run pushPriceHistoryToDynamo concurrently for all table names
#     await asyncio.gather(*(manager.pushItemOrdersToDynamo(str(table_name.name)) for table_name in table_names))


# # Run the event loop
# if __name__ == "__main__":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     asyncio.run(main())