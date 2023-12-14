import json
import os

from app.helpers.logger import log, log_error
from app.lib.models.file_batch import FileBatch

def handler(event, context):
    log('file_upload_handler', 'payload', {
        'event': event,
        'queue_in_use': os.getenv('SQS_XLS_FILE_QUEUE')
    })

    if 'Records' in event:
        for sqsRecord in event['Records']:
            payload = json.loads(sqsRecord['body'])

            log('file_upload_handler', 'payload', {
                'payload': payload,
                'record': sqsRecord['receiptHandle']
            })

            file_batch = FileBatch(payload)
            file_batch.perform()
