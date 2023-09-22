from scipy import stats
import numpy as np
import pandas as pd
import pathlib
from RegionIdEnum import region
from ItemIdEnum import item

def removeOutliers(df: pd.DataFrame) -> pd.DataFrame:
    zScores = np.abs(stats.zscore(df['price'],nan_policy='omit'))
    threshold = np.mean(zScores)
    return df[(zScores < threshold)]

def convertFromZuluTime(df: pd.DataFrame) -> pd.DataFrame:
    df['issued'] = pd.DatetimeIndex(df['issued'])
    return df

def seperateJitaDataTocsv(df: pd.DataFrame, path: pathlib, regionId: region):
    newCSVName = path.parent.joinpath("the-forge-historical-" + path.name)
    df[df['region_id'] == regionId].to_csv(newCSVName, index=False)
    
def seperateItemDataTocsv(df: pd.DataFrame, path: pathlib, item: item):
    newCSVName = path.parent.joinpath({item.name} + path.name)
    df[df['type_id'] == item.value].to_csv(newCSVName, index=False)