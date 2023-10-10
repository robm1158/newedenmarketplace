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
import mongodbData as mdb
import ItemIdEnum as item
import plotly.express as px
import plotly.graph_objects as go



pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 17)
pd.set_option('display.width', 250)

async def main():
    db = mdb.mongoData('eve-historical-data')
    db.checkConnection()
    # collectionList = db.getCollectionList()
    # for item in collectionList:
    #     print(item)
        # data = db.pullData(item)
        # print(data)
    data = db.pullData('PLAGIOCLASE')
    sorted_df = data.sort_values(by='issued', ascending=True)
    sorted_df['issued'] = pd.to_datetime(sorted_df['issued'])

    fig = go.Figure(data=go.Scatter(x=sorted_df['issued'], y=sorted_df['price'], mode='lines'))
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True)),
                    xaxis_title="Issued Date",
                    yaxis_title="Price Value",
                    title="PLAGIOCLASE Price Over Time")
    fig.show()

# # Run the main coroutine using asyncio's event loop
asyncio.run(main())




