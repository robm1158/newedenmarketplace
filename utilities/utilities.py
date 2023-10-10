from scipy import stats
import numpy as np
import pandas as pd
import pathlib
from RegionIdEnum import region
from ItemIdEnum import item

def removeOutliers(df: pd.DataFrame) -> pd.DataFrame:
    dfzscores = ((df['price'] - df['price'].mean()) / df['price'].std()).abs()
    df['z_score'] = dfzscores
    dfLen = len(df)
    
    threshold = np.inf #100000

    while ((dfLen/len(df)) - 1 < 0.1):
        threshold = df['z_score'].mean()*3
        df = df[df['z_score'] < threshold]
        dfzscores = ((df['price'] - df['price'].mean()) / df['price'].std()).abs()
        df['z_score'] = pd.Series(dfzscores)
    return df

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
        newCSVName = path.parent.joinpath("merged-"+ file.name)
    df_merged.to_csv(newCSVName, index=False)
