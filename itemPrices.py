from mimetypes import init
from typing import Dict
import requests


def getItemsPriceHistory(type_id: int,region_id=10000002) -> Dict:
    response = requests.get(f"https://esi.evetech.net/latest/markets/{region_id}/history/?datasource=tranquility&type_id={type_id}")
    return response.json()

def sendItemPriceHistory(self):
    #ToDo
    return 0

print(getItemsPriceHistory(34))