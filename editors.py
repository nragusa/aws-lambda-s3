import json
import boto3
from datetime import datetime
from botocore.exceptions import ClientError
from botocore.vendored import requests
import os
import sys

S3_BUCKET = os.environ['S3_BUCKET']
S3_EDITORS_KEY = os.environ['S3_EDITORS_KEY']

def main(event, context):
    """This function downloads an object from S3, parses data sent to it from
    an API Gateway endpoint, appends this data to the object from S3, then re-uploads
    the file back into S3.
    Returns an appropriate HTTP status code and status message to API Gateway.

    Example invocation:
    req = requests.put('https://my-apigw-endpoint.com/exampleuser', data=json.dumps(
        {'age': '20', 'editor': 'vim'}
    ))
    """
    s3 = boto3.resource('s3')
    try:
        s3.meta.client.download_file(S3_BUCKET, S3_EDITORS_KEY, '/tmp/local.json')
    except ClientError as e:
        print('Error downloading file from S3 {}'.format(e))
        return {'statusCode': 400, 'body': json.dumps({'status': str(e)})}
    try:
        user = event['pathParameters']['user']
        attributes = json.loads(event['body'])
        age = attributes['age']
        editor = attributes['editor']
    except KeyError as error:
        print('Problem getting data from request: {}'.format(error))
        return {'statusCode': 400, 'body': json.dumps({'status': str(error)})}
    with open('/tmp/local.json', 'a') as local:
        data = dict(
            user=user,
            age=age,
            editor=editor,
            now=datetime.now().isoformat(' ')
        )
        json.dump(data, local)
        local.write('\n')
    try:
        s3.meta.client.upload_file('/tmp/local.json', S3_BUCKET, S3_EDITORS_KEY)
        return {'statusCode': 200, 'body': json.dumps({'status': 'success'})}
    except ClientError as error:
        print('Problem uploading file to S3: {}'.format(error))
        return {'statusCode': 400, 'body': json.dumps({'status': str(error)})}
