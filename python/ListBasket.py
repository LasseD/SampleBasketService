import boto3
import json

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    if 'customer_id' not in event:
        event = event['queryStringParameters']
        
    customer_id = event['customer_id']

    # Find out what the existing basket content is:
    response = client.get_item(
        TableName='Basket',
        Key={'customer_id':{'S':customer_id}}
        )

    if 'Item' in response: # There is already a bbasket for the user:
        item = response['Item']
        content = item['content']['M']
    else: # Otherwise, create a new basket:
        content = {}

    # Compress the DyndamoDB entries from "N":val to just val:
    for k, v in content.items():
        content[k] = v['N']

    response = {
        "statusCode": 200,
        "body": json.dumps(content)
    }
    
    return response
