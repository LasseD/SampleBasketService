import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    customer_id = event['customer_id']

    # Find out what the existing basket content is:
    response = client.get_item(
        TableName='Basket',
        Key={'customer_id':{'S':customer_id}}
        )

    if 'Item' in response: # There is already a basket for the user:
        item = response['Item']
        content = item['content']['M']
    else:
        content = {}

    # Compress the DyndamoDB entries from "N":val to just val:
    for k, v in content.items():
        content[k] = v['N']

    return content
