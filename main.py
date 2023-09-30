import pandas as pd
import utilities
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import sklearn as sk
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
from sklearn.model_selection import TimeSeriesSplit
import seaborn as sns
from statsmodels.graphics.gofplots import qqplot
from scipy.stats import norm, uniform
import createLSTM
from ItemIdEnum import item
import pathlib
import s3PullData
import asyncio



pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 17)
pd.set_option('display.width', 250)

async def main():
    puller = s3PullData.PullData()
    for items in item:
        print(f'================== {items.name} ==================')
        
        result = await puller.getItemData(items.value, regionId=10000002)
        print(len(result))

        createLSTM.createLSTM(items.name, result, 30, 1, 300,64,True,True)
    # utilities.removeOutliers(result)
    # result = await puller.getItemData(22, regionId=10000002)

    # createLSTM.createLSTM(item.ARKONOR.name, result, 30, 1, 300,64,False,False)


# Run the main coroutine using asyncio's event loop
asyncio.run(main())

