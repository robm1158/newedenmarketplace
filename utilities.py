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

def seperateJitaDataTocsv(df: pd.DataFrame, path: pathlib.Path, regionId: int) -> None:
    newCSVName = path.parent.joinpath("the-forge-historical-" + path.name)
    df[df['region_id'] == regionId].to_csv(newCSVName, index=False)
    
def seperateItemDataTocsv(df: pd.DataFrame, path: pathlib.Path, item: item) -> None:
    newCSVName = path.parent.joinpath(item.name+'-' + path.name)

    df[df['type_id'] == item.value].to_csv(newCSVName, index=False)
    
def combineItemcsv(path: pathlib.Path, item: item) -> None:
    df_merged = pd.DataFrame()
    newCSVName = pathlib.Path()
    for file in path.rglob(item.name + "*.csv*"):
        if str(file.suffix) == ".bz2":
            df = pd.read_csv(file)
            df_merged = pd.concat([df_merged,df])
        newCSVName = path.parent.joinpath("merged-"+item.name+'-' + file.name)
    df_merged.to_csv(newCSVName, index=False)
