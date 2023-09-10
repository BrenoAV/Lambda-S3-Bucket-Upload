import json
import urllib.parse
import boto3

print("Loading lambda function...")

s3 = boto3.client("s3")
ses = boto3.client("ses")

def lambda_handler(event, context):
    
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    print(bucket)
    key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("Content Type: " + response["ContentType"])
        subject = "Email from AWS Trigger"
        body = "A file was uploaded in your bucket"
        message = {"Subject": {"Data": subject}, "Body": {"Html": {"Data":body}}}
        res = ses.send_email(Source="<your_email_here>",
                             Destination={"ToAddresses": ["<your_email_here>"]},
                             Message=message)
        return response["ContentType"]
    
    except Exception as e:
        print(e)