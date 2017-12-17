import boto3
from botocore.vendored import requests
import json
import os

API_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"
SNS_TOPIC = os.environ['SNS_TOPIC']

def get_current_price(REQUEST_URL):
    response = requests.get(REQUEST_URL)
    content = bytes.decode(response.content)

    json_content = json.loads(content)
    currentprice = json_content['bpi']['USD']['rate']
    formatted_price = currentprice[:currentprice.find('.')+3]
    return formatted_price

#Publish to SNS
def lambda_handler(event, context):
	sns_topic = boto3.resource('sns').Topic(SNS_TOPIC)
	sns_topic.publish(Message=get_current_price(API_URL))
