import json
import boto3
 
client = boto3.client('lambda')
 
def lambda_handler(event, context):
    if 'customer_id' not in event:
        event = event['queryStringParameters']
    
    customer_id = event['customer_id']
    set_nr = event['set_nr'];

    ChangeQuantityParams = {
        "customer_id": customer_id,
        "set_nr" : set_nr,
        "quantity": 0,
        "method": "set"
    }
 
    response = client.invoke(
        FunctionName = 'arn:aws:lambda:eu-west-1:539601493679:function:ChangeQuantity',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(ChangeQuantityParams)
    )

    return {
        "statusCode": response["ResponseMetadata"]["HTTPStatusCode"],
        "body": "Remove From Basket Invoked"
    }
