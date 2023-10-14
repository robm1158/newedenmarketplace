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
import utils.s3PullData as s3PullData
import asyncio
import gc
from motor.motor_asyncio import AsyncIOMotorClient
from mongodbData import mongoData



pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 17)
pd.set_option('display.width', 250)

async def main():
    puller = s3PullData.PullData()
    db = mongoData('eve-market-order-history-the-forge')
    await db.deleteDB('eve-market-order-history-the-forge')

# Run the main coroutine using asyncio's event loop
asyncio.run(main())

