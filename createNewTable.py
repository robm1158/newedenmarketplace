import boto3
from botocore.exceptions import ClientError
import json
import requests
import typing
from decimal import Decimal

class CreateNewTable:
    def __init__(self) -> None:
        self.dynamodb = boto3.resource('dynamodb')
    
    def createPriceHistoryTable(self, tableName: str) -> int:
        try:
            response = self.dynamodb.create_table(
                TableName=tableName,
                KeySchema=[
                    {
                        'AttributeName': 'date',
                        'KeyType': 'HASH'  # Hash Key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'date',
                        'AttributeType': 'S'  # string data type
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 50
                }
            )
            print("[createNewTable]: New table created")
            return 200
        except ClientError  as err:
            if err.response['ResponseMetadata']['HTTPStatusCode'] == 400:
                print(f"[createNewTable]: {err.response['message']} Table already created")
            else:
                print(f"[createNewTable]: {err.response['message']}")
            return err.response['ResponseMetadata']['HTTPStatusCode']
            
    def createItemOrderTable(self, tableName: str) -> int:
        try:
            response = self.dynamodb.create_table(
                TableName=tableName,
                KeySchema=[
                    {
                        'AttributeName': 'date', # It is called issued in the esi pull
                        'KeyType': 'HASH'  # Hash Key
                    },
                    {
                        'AttributeName': 'order_id', 
                        'KeyType': 'RANGE'  # Sort Key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'date',
                        'AttributeType': 'S'  # string data type
                    },
                    {
                        'AttributeName': 'order_id',
                        'AttributeType': 'N'  # string data type
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 50
                }
            )
            print(f'[createNewTable]: New table {tableName} created')
            return 200
        except ClientError  as err:
            if err.response['ResponseMetadata']['HTTPStatusCode'] == 400:
                print(f"[createNewTable]: {err.response['message']} Table already created")
            else:
                print(f"[createNewTable]: Error msg {err.response['message']}")
            return err.response['ResponseMetadata']['HTTPStatusCode']
