import json
import importlib
from django.conf import settings
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NoCelery.settings")
# django.setup()
# message = '{"path": "main/tasks.py", "args": [5, 6], "kwargs": {}}'
# message_j = json.loads(message)
#
# module_path = message_j["path"]
# module_path.replace
# module_path = module_path.replace("/", ".")
# module = importlib.import_module('main.tasks')
# func = getattr(module, "add")
# res = func.__wrapped__(*message_j["args"], **message_j["kwargs"])
# res

#
# def filepath_to_module(filepath):
#     # Convert the file path to the platform-specific separator
#     filepath = os.path.normpath(filepath)
#
#     # Get the base filename without the extension
#     module_name = os.path.splitext(os.path.basename(filepath))[0]
#
#     # Get the directory path and convert it to a module path
#     dir_path = os.path.dirname(filepath)
#     module_path = dir_path.replace(os.path.sep, ".")
#
#     # Return the module name and path
#     return module_name + "." + module_path
#
#
import argparse

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", help="Your name")
    parser.add_argument("--age", help="Your age")

    args = parser.parse_args()
    name = args.name
    print(name)
    print(args.age)
