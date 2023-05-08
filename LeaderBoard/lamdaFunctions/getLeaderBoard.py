import boto3

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Define the table name and attribute to query
    table_name = 'my-table-name'
    attribute_name = 'my-attribute-name'

    # Define the query parameters
    query_params = {
        'TableName': table_name,
        'KeyConditionExpression': 'attribute_exists({})'.format(attribute_name),
        'ScanIndexForward': False,
        'Limit': 5
    }

    # Query the table
    response = dynamodb.query(**query_params)

    # Print the results
    items = response['Items']
    print(items)

    # Return a response
    return {
        'statusCode': 200,
        'body': 'Query successful'
    }