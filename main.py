import json
import dynamodbPushData
import RegionIdEnum
import ItemIdEnum
import asyncio
import aiohttp
import itemPrices

# async def push_to_dynamo(i, dynamodb):
#     async with aiohttp.ClientSession() as session:
#         # Assuming that pushItemOrdersToDynamo is an asynchronous function
#         await dynamodb.pushItemOrdersToDynamo(str(i.name), session)

# async def main():
#     dynamodb = dynamodbPushData.pushData()
#     tasks = []

#     for i in list(ItemIdEnum.item):
#         task = asyncio.ensure_future(push_to_dynamo(i, dynamodb))
#         tasks.append(task)

#     await asyncio.gather(*tasks)

# def lambda_handler(event, context):
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
    
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Done getting Item Orders!')
#     }

# def test():
#     itemjson = itemPrices.getAllItemOrderHistory(ItemIdEnum.item["DEPLETED_URANIUM_S"].value,RegionIdEnum.region.THE_FORGE.value)
#     jsondata = json.loads(itemjson, parse_float=Decimal)
#     for myDict in jsondata:
#         print(myDict)

# if __name__ == "__main__":
#     test()
#     main()

# async def main():
#     region_id = RegionIdEnum.region.THE_FORGE.value  # Replace with your region ID
#     # type_ids = [34, 35, 36]  # Replace with your list of type_ids

#     tasks = [itemPrices.getAllItemOrderHistory(type_id.value, region_id) for type_id in ItemIdEnum.item]
#     results = await asyncio.gather(*tasks)

#     for i, result in enumerate(results):
#         print(f"Result for type_id : {result}")

async def main():
    # List of type_ids
    type_ids = ItemIdEnum.item
    region_id = RegionIdEnum.region.THE_FORGE.value

    # Gather all asynchronous calls into one, effectively running them concurrently
    results = await asyncio.gather(*(itemPrices.getItemsPriceHistory(type_id.value, region_id) for type_id in type_ids))
    print(results)



# Run the event loop
if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())


# for i in ItemIdEnum.item:
#     print(i.value)
