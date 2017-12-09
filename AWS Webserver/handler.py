import json
import sys
import imageParser

import boto3
dynamodb = boto3.resource('dynamodb',region_name='us-east-2')

def parseImage(event, context):
    data = json.loads(event['body'])
    print(data)
    encoded_image = data["image"]
    hashed_email = data["email"]

    # parse image
    purchase = imageParser.imageRecognition(base64=encoded_image)
    purchase["image"] = encoded_image
    purchase["email"] = hashed_email
    print(purchase)

    response = {
        "statusCode": 200,
        "body": json.dumps(purchase)
    }
    print(purchase)

    return response

