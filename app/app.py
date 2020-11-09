import boto3
import json
import logging
import os

from base64 import b64decode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


INFO_CHANNEL = os.environ['InfoChannel']
INFO_TOPIC_ARN = os.environ['InfoTopicArn']
ISSUE_CHANNEL = os.environ['IssueChannel']
ISSUE_TOPIC_ARN = os.environ['IssueTopicArn']
# 
HOOK_URL = os.environ['hookUrl']

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    topicArn = event['Records'][0]['Sns']['TopicArn']
    if topicArn == INFO_TOPIC_ARN:
        SLACK_CHANNEL = INFO_CHANNEL
    elif topicArn == ISSUE_TOPIC_ARN:
        SLACK_CHANNEL = ISSUE_CHANNEL
    else: 
        SLACK_CHANNEL = INFO_CHANNEL

    text = event['Records'][0]['Sns']['Message']
    logger.info("text: " + str(text))

    slack_message = {
        'channel': SLACK_CHANNEL,
        'text': str(text)
    }
    logger.info("slack_message: " + str(slack_message))

    req = Request(HOOK_URL, json.dumps(slack_message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)