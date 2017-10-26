import json
import boto3
import os
from botocore.exceptions import ClientError
from botocore.vendored import requests

S3_BUCKET = os.environ['S3_BUCKET']
S3_WEATHER_KEY = os.environ['S3_WEATHER_KEY']
WEATHER_API_KEY = os.environ['WEATHER_API_KEY']

def main(event, context):
    """This calls the OpenWeatherMap API and gets the weather for Boston, MA and Cupertino, CA.
    It appends the response data to an object retrieved from S3, then uploads the object
    back to S3."""
    s3 = boto3.resource('s3')
    try:
        s3.meta.client.download_file(S3_BUCKET, S3_WEATHER_KEY, '/tmp/local.json')
    except ClientError as error:
        print('Error downloading file from S3 {}'.format(error))
        return
    try:
        weather_data_boston = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=02215,us&APPID={}'.format(WEATHER_API_KEY))
        weather_data_cupertino = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=95014,us&APPID={}'.format(WEATHER_API_KEY))
    except requests.exceptions.RequestException as error:
        print('Problem getting weather data: {}'.format(error))
        return
    with open('/tmp/local.json', 'a') as local:
        json.dump(weather_data_boston.json(), local)
        local.write('\n')
        json.dump(weather_data_cupertino.json(), local)
        local.write('\n')
    try:
        s3.meta.client.upload_file('/tmp/local.json', S3_BUCKET, S3_WEATHER_KEY)
        return
    except ClientError as error:
        print('Problem uploading file to S3: {}'.format(error))
        return
