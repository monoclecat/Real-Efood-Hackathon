import json
import sys
import image_parser
import sys

try:
  import unzip_requirements
except ImportError:
  pass

import boto3
dynamodb = boto3.resource('dynamodb',region_name='us-east-2')

# def updateDynamo(user,purchase):
#     table = boto3.resource('dynamodb',region_name='us-east-2')
#     response = table.update_item(
#         Key={
#             'UserId': user
#         },
#         UpdateExpression="set uule = :u",
#         ExpressionAttributeValues={
#             ':u': uule,
#         },
#         ReturnValues="UPDATED_NEW"
#     )
#     if (response["ResponseMetadata"]["HTTPStatusCode"] == 200):
#         print('updated uule parameter')
#     else:
#         print('updated uule failed')
#
#     return response['Attributes']

def parseImage(event, context):
    print(sys.path)
    data = json.loads(event['body'])
    print(data)
    encoded_image = data["image"]
    hashed_email = data["email"]

    # parse image
    purchase = image_parser.parse_receipt(base64_data=encoded_image)
    purchase["image"] = encoded_image
    purchase["email"] = hashed_email
    print(purchase)

    response = {
        "statusCode": 200,
        "body": json.dumps(purchase)
    }
    print(purchase)

    return response

