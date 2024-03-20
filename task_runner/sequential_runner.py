import sys
from pathlib import Path

import boto3
import importlib
import os
import django
import json
import argparse
import logging
from django.conf import settings

logging.basicConfig(
    level=logging.INFO,
    filename="sequential_runner.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NoCelery.settings")

django.setup()


def main(queue_url):
    sqs = boto3.client("sqs")

    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=5,
                AttributeNames=["All"],
                MessageAttributeNames=["All"],
            )
            if "Messages" in response:
                for message in response["Messages"]:
                    message_j = json.loads(message["Body"])
                    module = importlib.import_module(message_j["path"])
                    func = getattr(module, message_j["func_name"])
                    res = func.__wrapped__(*message_j["args"], **message_j["kwargs"])
                    logging.info(f"func call executed successfully. returned {res}")
                    sqs.delete_message(
                        QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"]
                    )
                    logging.info(
                        f"successfully processed and deleted message {message}"
                    )
            else:
                logging.warning("Empty response.")
        except Exception as e:
            logging.error(f"error occurred when processing message {message} -> {e}")
            raise e



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--qn", help="Queue name.")
    args = parser.parse_args()
    queue_url = settings.SQS_QUEUES[args.qn]["url"]
    main(queue_url)
