import json
from . import local_config
from . import request

def create_config(type, key, value):
    if local_config.check():
        data = {
            "type" : type,
            "key" : key,
            "value" : value
        };
        if key not in ['server','parallel','outputDir']:
            print("[Biolab] The key only support ['server','parallel','outputDir'] currently")
            return
        response = request.post("config", "create", json.dumps(data))
        if not response:
            return
        if response['code'] == 0:
            print("[Biolab] The config " + type + "_" + key + " registered successful")
        else:
            print("[Biolab] The config " + type + "_" + key + " already registered")


def list_config():
    if local_config.check():
        data = {};
        response = request.post("config", "list", json.dumps(data))
        if not response:
            return
        if not response['data']:
            print("No system configs configured")
            return
        for config in response['data']:
            print(config)