import collections
import json
import os


def check_file(filepath):
    return os.path.isfile(filepath)


def read_json_configuration(route):
    with open(route, "r") as f:
        config = json.load(f)
    return config


def check_key(data, key, stype="dict"):
    if key not in data:
        if stype == "dict":
            data[key] = collections.OrderedDict()
        elif stype == "list":
            data[key] = []
        elif stype == "int":
            data[key] = 0
