import os
import boto3
import itertools

from boto3.dynamodb.conditions import Key


class DynamodbGateway:
    @classmethod
    def query_index_by_partition_key(cls, index_name, table_name, partition_key_name, partition_key_query_value):
        client = boto3.client('dynamodb')

        response = client.query(
            TableName=table_name,
            IndexName=index_name,
            KeyConditionExpression=f"{partition_key_name} = :value",
            ExpressionAttributeValues={
                ':value': {'S': partition_key_query_value}
            }
        )

        return response.get('Items')
    
    @classmethod
    def scan_table_begins_with(cls, table_name, scan_kwargs):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)

        response = table.scan(**scan_kwargs)

        return {
            "items": response['Items']
        }

    @classmethod
    def get_item(cls, table_name, expression_key):

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)

        response = table.get_item(
            Key=expression_key
        )

        if 'Item' not in response:
            return {}

        return response['Item']

    @classmethod
    def create_item(cls, table_name, default_item):

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)

        table.put_item(
            Item=default_item
        )

        return "CREATED"
    
    @classmethod
    def batch_create_item(cls, table_name, items):

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)

        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

        return "CREATED"

    @classmethod
    def update_item(cls, table_name, expression_key, expressions):

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)

        table.update_item(
            Key=expression_key,
            UpdateExpression=expressions['update_expression'],
            ExpressionAttributeValues=expressions['expression_attribute_values'],
            ExpressionAttributeNames=expressions['expression_attribute_names'],
            ReturnValues="UPDATED_NEW"
        )

        return "UPDATED"

    @classmethod
    def scan_with_pagination(cls, table_name, scan_kwargs):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)

        response = table.scan(**scan_kwargs)
        
        return {
            "items": response['Items'],
            "last_evaluated_key": response["LastEvaluatedKey"] if "LastEvaluatedKey" in response else None
        }

    @classmethod
    def query_by_partition_key(cls, table_name, partition_key, partition_value):
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)

        response = table.query(
            KeyConditionExpression=Key(partition_key).eq(partition_value)
        )

        if 'Items' not in response:
            return {}

        return response['Items']