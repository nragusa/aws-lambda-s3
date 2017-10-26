# Overview

The following repository contains two AWS Lambda functions which leverage the AWS Serverless Application Model framework. The intent of these functions were to demonstrate retrieving an object from S3, modify the file, then upload the file back to S3. There are two functions which accomplish this in different ways.

## GetWeather

This function uses the [OpenWeatherMap API](https://openweathermap.org/api) to download weather data for Boston, MA and Cupertino, CA. It requires an [API key](http://openweathermap.org/appid) to be passed as a parameter in the template in order to work. If a successful connection is made to the weather service, it downloads an object from S3 (defaults to weather/weather.json), appends the latest information to the file, then uploads the file back to S3. The function is executed every 15 minutes from CloudWatch Events.

## AddUsersEditor

This function is fronted by an API Gateway endpoint which simply proxies data to the Lambda function. The function expects a username to be passed in the URI (e.g. https://my-endpoint/Stage/username) and a JSON body like the following:
```
{"age": 20, "editor": "visual studio code"}
```
You can call this API Gateway endpoint using an HTTP PUT. 

The function will parse this data, download an object from S3, append the latest data to the file, then upload the file back to S3. 

# Getting Started

## OpenWeatherMap API Key
In order for these functions to work, you first need to get an [API key](http://openweathermap.org/appid) from OpenWeatherMap. Getting one is free and easy to use!

Once you get a key, write this down as you'll need to pass it as a parameter to the template.

## Install AWS CLI

Installing the AWS CLI is pretty straightforward. Follow the [online docs](http://docs.aws.amazon.com/cli/latest/userguide/installing.html) to get this up and running for Linux, MacOS, or Windows.

## Package and Deploy

Clone this repository change to the repository's directory. Run the following, being sure to specify an S3 bucket you own. This bucket will be used to store the Lambda functions:
```
$ aws cloudformation package \
    --template-file template.yaml \
    --s3-bucket bucket-name \
    --output-template-file package.yaml
```

Now deploy the stack, being sure to specify your OpenWeatherMap API key:
```
$ aws cloudformation deploy \
    --template-file package.yaml \
    --stack-name my-new-stack \
    --parameter-overrides MyWeatherApiKey=myapikeyfromopenweathermap
    --capabilities CAPABILITY_IAM
```