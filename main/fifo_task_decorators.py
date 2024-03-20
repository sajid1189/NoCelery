import json
import os
import functools
import boto3
import inspect
from django.conf import settings
from main.utils import filepath_to_module


def fifo_task(func):
    sqs = boto3.client("sqs", region_name="eu-central-1")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if settings.EAGER_TASKS:
            func(*args, **kwargs)
            return
        relative_path = os.path.relpath(inspect.getfile(func), settings.BASE_DIR)
        relative_path = filepath_to_module(relative_path)

        message = {
            "path": relative_path,
            "func_name": func.__name__,
            "args": args,
            "kwargs": kwargs,
        }
        message_payload = json.dumps(message)
        response = sqs.send_message(
            QueueUrl=settings.SQS_QUEUES["q2"]["url"],
            MessageBody=json.dumps(message),
            # MessageDeduplicationId=str(hash(message_payload)),
            MessageGroupId="invoice_approval"
        )

    return wrapper
