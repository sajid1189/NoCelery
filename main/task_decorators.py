import json
import os
import functools
import boto3
import inspect
from django.conf import settings

from main.models import Foo
from main.utils import filepath_to_module


def task(func):
    sqs = boto3.client("sqs", region_name="eu-central-1")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if settings.EAGER_TASKS:
            func(*args, **kwargs)
            return
        message = dict()
        relative_path = os.path.relpath(inspect.getfile(func), settings.BASE_DIR)
        relative_path = filepath_to_module(relative_path)
        message["path"] = relative_path
        message["func_name"] = func.__name__
        message["args"] = args
        message["kwargs"] = kwargs

        response = sqs.send_message(
            QueueUrl=settings.SQS_QUEUES["q1"]["url"],
            MessageBody=json.dumps(message),
        )

    return wrapper

