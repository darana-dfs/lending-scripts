import boto3
import json

def table_exists(table_name, dynamodb_client):
    try:
        dynamodb_client.describe_table(TableName=table_name)
        return True
    except dynamodb_client.exceptions.ResourceNotFoundException:
        return False
    
def create_table(table_params, dynamodb_client):
    table_name = table_params['TableName']
    if table_exists(table_name, dynamodb_client):
        print(f"Table {table_name} already exists, skipping...")
        return
    
    print(f"Creating {table_name}...")
    print(json.dumps(table_params, indent=4))
    table = dynamodb_client.create_table(**table_params)
    print(f"Table {table_name} successdfully succeeded.")
    return table

def put_item(table_name, item, dynamodb_client):
    pk = item['pk']['S']
    sk = item['sk']['S']
    
    print(f"Putting ({pk}, {sk}) in table {table_name}...")
    print(json.dumps(item, indent=4))
    dynamodb_client.put_item(
        TableName=table_name,
        Item=item,
    )

    print(f"Put item ({pk}, {sk}) in table {table_name} succeeded.")