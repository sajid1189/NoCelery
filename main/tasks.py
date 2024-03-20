import json
import os
import functools
import boto3
import inspect
from django.conf import settings

from main.models import Foo



def filepath_to_module(filepath):
    # Convert the file path to the platform-specific separator
    filepath = os.path.normpath(filepath)

    # Get the base filename without the extension
    module_name = os.path.splitext(os.path.basename(filepath))[0]

    # Get the directory path and convert it to a module path
    dir_path = os.path.dirname(filepath)
    module_path = dir_path.replace(os.path.sep, ".")

    # Return the module name and path
    return module_path + "." +module_name


def task(func):
    # Initialize SQS client
    sqs = boto3.client("sqs", region_name="eu-central-1")

    # Define the URL of your FIFO queue

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
            QueueUrl=settings.SQS_QUEUES["q2"]["url"],
            MessageBody=json.dumps(message),
        )

    return wrapper


@task
def add(x, y):
    print("I am adding")
    return x + y

@task
def incr_foo(f_id, d):
    f = Foo.objects.get(id=f_id)
    f.value += 100
    f.save()
    print("updated on ", d)

def test_func(a=1, b=2):
    print(a, b)
