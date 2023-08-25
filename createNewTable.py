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
                        'KeyType': 'HASH'  # Sort Key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'date',
                        'AttributeType': 'S'  # number data type
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
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