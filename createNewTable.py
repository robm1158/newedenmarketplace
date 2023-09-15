import aioboto3
from botocore.exceptions import ClientError
import json
import requests
import typing
from decimal import Decimal
import logging
import boto3

class CreateNewTable:
    def __init__(self) -> None:
        self.dynamodb = boto3.resource('dynamodb')
        self.session = aioboto3.Session()
    
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
                    'WriteCapacityUnits': 10
                }
            )
            logging.info("[createPriceHistoryTable]: New table created")
            return 200
        except ClientError  as err:
            logging.warning(f"[createPriceHistoryTable]: {err.response['message']} : Status: {err.response['ResponseMetadata']['HTTPStatusCode']}")
            # pass
            return err.response['ResponseMetadata']['HTTPStatusCode']

            
    def createItemOrderTable(self, tableName: str) -> int:
        response = None
        try:
            response = self.dynamodb.create_table(
                TableName=tableName,
                KeySchema=[
                    {
                        'AttributeName': 'issued', # It is called issued in the esi pull
                        'KeyType': 'HASH'  # Hash Key
                    },
                    {
                        'AttributeName': 'order_id', 
                        'KeyType': 'RANGE'  # Sort Key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'issued',
                        'AttributeType': 'S'  # string data type
                    },
                    {
                        'AttributeName': 'order_id',
                        'AttributeType': 'N'  # number data type
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 10
                }
            )
            logging.info(f'[createItemOrderTable]: New table {tableName}_ORDERS created')
            return 200
        except ClientError  as err:
            logging.warning(f"[createItemOrderTable]: {err.response['message']} : Status: {err.response['ResponseMetadata']['HTTPStatusCode']}")
            pass
            return err.response['ResponseMetadata']['HTTPStatusCode']
        
    def enableAutoScaling(self, table_name: str) -> None:
            # Using boto3 to create autoscaling client
            autoscaling = boto3.client('application-autoscaling')
            
            # Registering the DynamoDB table for autoscaling
            autoscaling.register_scalable_target(
                ServiceNamespace='dynamodb',
                ResourceId=f'table/{table_name}',
                ScalableDimension='dynamodb:table:WriteCapacityUnits',
                MinCapacity=1,
                MaxCapacity=10
            )

            # Defining the scaling policy
            autoscaling.put_scaling_policy(
                PolicyName=f'WriteAutoScalingPolicy-{table_name}',
                ServiceNamespace='dynamodb',
                ResourceId=f'table/{table_name}',
                ScalableDimension='dynamodb:table:WriteCapacityUnits',
                PolicyType='TargetTrackingScaling',
                TargetTrackingScalingPolicyConfiguration={
                    'TargetValue': 70.0,
                    'PredefinedMetricSpecification': {
                        'PredefinedMetricType': 'DynamoDBWriteCapacityUtilization'
                    },
                    'ScaleOutCooldown': 30,
                    'ScaleInCooldown': 30
                }
            )
