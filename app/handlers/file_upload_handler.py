import json
import os

from app.helpers.logger import log, log_error


def handler(event, context):
    if len(event['Records']) != 0:
        for sqsRecord in event['Records']:
            payload = json.loads(sqsRecord['body'])

            log('file_upload_handler', 'payload', {
                'payload': payload,
                'record': sqsRecord['receiptHandle']
            })
