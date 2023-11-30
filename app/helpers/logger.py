import os
import json
import traceback


def log(action, content, context=None):
    service = os.environ.get('AWS_LAMBDA_FUNCTION_NAME')
    try:
        entry = {
            'version': 'json',
            'action': action,
            'service': service,
            'body': content,
            'context': context
        }
        print(json.dumps(entry, default=str))
    except:
        print({
            'version': 'raw',
            'action': action,
            'service': service,
            'body': content,
            'context': context,
            'parsing_error': traceback.format_exc()
        })


def log_error(context={}):
    log('app_error', {'traceback': traceback.format_exc()}, context)
