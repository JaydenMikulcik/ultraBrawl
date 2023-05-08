import boto3

def lambda_handler(event, context):
    # Define the table name and key
    table_name = 'my-table-name'
    key = {'my-key': {'S': 'my-value'}}  # Replace with your own key-value pair

    # Create a DynamoDB client
    dynamodb = boto3.client('dynamodb')

    # Check if the table exists
    try:
        dynamodb.describe_table(TableName=table_name)
    except dynamodb.exceptions.ResourceNotFoundException:
        # Table does not exist
        return {
            'statusCode': 404,
            'body': 'Table does not exist'
        }

    # Increment the item's value if it exists, otherwise create it
    try:
        response = dynamodb.update_item(
            TableName=table_name,
            Key=key,
            UpdateExpression='SET my-value = my-value + :incr',
            ExpressionAttributeValues={':incr': {'N': '1'}},
            ReturnValues='UPDATED_NEW'
        )
        count = response['Attributes']['my-value']['N']
        return {
            'statusCode': 200,
            'body': f'Item updated. New count: {count}'
        }
    except dynamodb.exceptions.ResourceNotFoundException:
        # Item does not exist, create it with a count of 1
        dynamodb.put_item(
            TableName=table_name,
            Item={**key, 'my-value': {'N': '1'}}
        )
        return {
            'statusCode': 200,
            'body': 'Item created with count of 1'
        }