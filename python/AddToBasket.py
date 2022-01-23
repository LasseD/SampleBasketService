import json
import boto3
 
client = boto3.client('lambda')
 
def lambda_handler(event, context):
    customer_id = event['customer_id']
    set_nr = event['set_nr'];

    ChangeQuantityParams = {
        "customer_id": customer_id,
        "set_nr" : set_nr,
        "quantity": 1,
        "method": "add"
    }
 
    response = client.invoke(
        FunctionName = 'arn:aws:lambda:eu-west-1:539601493679:function:ChangeQuantity',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(ChangeQuantityParams)
    )

    return response['ResponseMetadata']
