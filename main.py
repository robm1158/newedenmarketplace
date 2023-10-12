import sys
print(sys.path)
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pathlib
import asyncio
from itemPrices import getGroups
from itemPrices import unravelGroupsAsync
from itemPrices import construct_hierarchy
import json
from tqdm import tqdm
from utils.ItemIdEnum import item

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 17)
pd.set_option('display.width', 250)

def save_to_file(data, filename='final_enum.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Saved to {filename}")
    
def extract_types(data):
    types = []
    for item in data:
        types.extend(item['types'])  # Add types from current item
        types.extend(extract_types(item['children']))  # Recursively get types from children
    return types
async def main():
    # data = await getGroups()
    # # print(data)
    # result = await unravelGroupsAsync(data)
    # # # print(result)
    
    # data1 = construct_hierarchy(result)
    # save_to_file(data1)
    # # print(data1)
    # for items in item:
    #     print(items.name)
    
    # with open('/root/code/eve-aws/marketGroups.json', 'r') as file:
    #     data = json.load(file)
    #     all_types = extract_types(data)
    #     save_to_file(all_types, 'types.txt')
    # if "900" in "_100_AURUM_TOKEN = 32792":
    #     print("yes")
    # else:
    #     print("no")
    
    # type_list = []
    # enum_list = []
    # final_enum_list = []
    # with open('/root/code/eve-aws/types.txt', 'r') as file:
    #     type_list = file.readlines()

    #     # Optionally, if you want to remove newline characters from each string in the list:
    #     type_list = [line.strip() for line in type_list]
    # with open('/root/code/eve-aws/enumList.txt', 'r') as file:
    #     enum_list = file.readlines()
    #     enum_list = [line.strip() for line in enum_list]
        
    # for type in tqdm(type_list, total=100):
    #     for enum in enum_list:
    #         if type in enum:
    #             final_enum_list.append(enum)

    
        
    # print(enum_list)
    # save_to_file(enum_list)


# Run the main coroutine using asyncio's event loop
asyncio.run(main())

