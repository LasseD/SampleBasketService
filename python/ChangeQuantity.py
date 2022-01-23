import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Ensure that the lambda function can be called using a GET method from an API gateway, as well as directly:
    if 'customer_id' not in event:
        event = event['queryStringParameters']

    # Get the input parameters from the event:
    customer_id = event['customer_id']
    set_nr = event['set_nr']
    quantity = event['quantity']
    method = event['method']

    # Find out what the existing basket content is:
    response = client.get_item(
        TableName='Basket',
        Key={'customer_id':{'S':customer_id}}
        )

    if 'Item' in response: # There is already a basket for the user:
        item = response['Item']
        content = item['content']['M']
        print("existing content in basket: " + json.dumps(content, indent=2))
    else: # Otherwise, create a new basket:
        if quantity > 0:
            content = {'M': {set_nr: {'N': str(quantity)}}}
        else: # Edge case: empty basket from the start:
            content = {'M': {}}
        print("Creating new basket for customer " + customer_id)
        response = client.put_item(
            TableName = 'Basket',
            Item = {
                'customer_id': {'S': customer_id},
                'content': content
            }
        )
        return response

    # Check if we should add, remove, or overwrite the value:
    args = {
        'TableName': 'Basket',
        'Key': {'customer_id':{'S':customer_id}},
        'ExpressionAttributeNames': {'#sn': set_nr}
    }
    
    if method == "add" and set_nr in content:
        args['ExpressionAttributeValues'] = {':q': {'N': str(quantity)}}
        args['UpdateExpression'] = "SET content.#sn = content.#sn + :q"
    elif quantity == 0:
        args['UpdateExpression']= "REMOVE content.#sn"
    else:
        args['ExpressionAttributeValues'] = {':q': {'N': str(quantity)}}
        args['UpdateExpression']= "SET content.#sn=:q"

    response = client.update_item(**args)

    return {
        "statusCode": response["ResponseMetadata"]["HTTPStatusCode"],
        "body": json.dumps(response)
    }
