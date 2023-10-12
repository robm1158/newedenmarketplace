import sys
sys.path.append('/root/code/eve-aws/utils')
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

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 17)
pd.set_option('display.width', 250)

def save_to_file(data, filename='marketGroups.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Saved to {filename}")

async def main():
    data = await getGroups()
    # print(data)
    result = await unravelGroupsAsync(data)
    # # print(result)
    
    data1 = construct_hierarchy(result)
    save_to_file(data1)
    # print(data1)

# Run the main coroutine using asyncio's event loop
asyncio.run(main())

