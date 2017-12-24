import boto3
from botocore.vendored import requests
import json
import os

API_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"
SNS_TOPIC_NAME = "sendSMS"

def get_current_price(REQUEST_URL):
    response = requests.get(REQUEST_URL)
    content = bytes.decode(response.content)

    json_content = json.loads(content)
    currentprice = json_content['bpi']['USD']['rate']
    formatted_price = currentprice[:currentprice.find('.')+3]
    return formatted_price

def get_topic_arn():
	topic_list = boto3.client('sns').list_topics()['Topics']
	for topic in topic_list:
		if SNS_TOPIC_NAME in topic['TopicArn']:
			print(topic['TopicArn'])
			return topic['TopicArn']

#Publish to SNS
def lambda_handler(event, context):
	sns_topic = boto3.resource('sns').Topic(get_topic_arn())
	sns_topic.publish(Message=get_current_price(API_URL))
