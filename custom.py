import os
import boto3
import json
from botocore.exceptions import ClientError
from botocore.vendored import requests

S3_BUCKET = os.environ['S3_BUCKET']
S3_EDITORS_KEY = os.environ['S3_EDITORS_KEY']
S3_WEATHER_KEY = os.environ['S3_WEATHER_KEY']

def main(event, context):
    s3 = boto3.client('s3')
    try:
        response = s3.put_object(
            Bucket=S3_BUCKET,
            Key=S3_EDITORS_KEY
        )
        response = s3.put_object(
            Bucket=S3_BUCKET,
            Key=S3_WEATHER_KEY
        )
        sendResponse(event, '', 'SUCCESS')
    except ClientError as error:
        print('Problem adding empty object: {}'.format(error))
        sendResponse(event, error, 'FAILED')

def sendResponse(event, reason, status):
    response = {
        'Status': status,
        'Reason': reason,
        'PhysicalResourceId': 'physical-resource-id',
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId']
    }
    print(response)
    try:
        cfn_response = requests.put(event['ResponseURL'], data=json.dumps(response))
        print(cfn_response.status_code, cfn_response.text)
    except requests.exceptions.RequestException as error:
        print('Problem connecting to CloudFormation: {}'.format(error))
    return
