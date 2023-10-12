
import sys
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
import requests
import re

# pd.set_option('display.max_rows', 10)
# pd.set_option('display.max_columns', 17)
# pd.set_option('display.width', 250)
def save_to_file(data, filename='final_enum.txt'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Saved to {filename}")
async def main():
    # puller = s3PullData.PullData()
    # path = '2022/2022-06-10/market-orders-2022-06-10_2*.v3.csv.bz2'
    # # for items in item:
    # print(f'================== {item.TRITANIUM.name} ==================')
    # df = await puller.getItemData(item.TRITANIUM.value, regionId=10000002,path=path)
    # df = utils.removeOutliers(df)
    # df = utils.convertFromZuluTime(df)
    # df = df.drop(columns=['range','universe_id','http_last_modified'])
    # df['issued'] = df['issued'].dt.date
    # fig = px.scatter(df, x='issued', y="price",color='is_buy_order')
    # fig.add_box(x=df['issued'], y=df["price"])
    # fig.show()
    

    # Assuming you've already read type_list and enum_list from files...
    type_list = []
    final_enum_list = []

    # Read type_list from file
    with open('/root/code/eve-aws/types.txt', 'r') as file:
        type_list = [line.strip().replace(',', '') for line in file.readlines()]

    # Read enum_list from file and create a dictionary for efficient look-up
    enum_dict = {}
    pattern = re.compile(r"=\s*(\d+)")
    with open('/root/code/eve-aws/enumList.txt', 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                enum_value = int(match.group(1))
                enum_dict[enum_value] = line.strip()

    # Lookup types in enum_dict
    final_enum_list = [enum_dict[int(type_str)] for type_str in type_list if int(type_str) in enum_dict]

    save_to_file(final_enum_list)



asyncio.run(main())



