import json
from . import local_config
from . import request

def create_env(workflowcode, step, type, key, feature):
    if local_config.check():
        data = {
            "workflowCode" : workflowcode,
            "step" : step,
            "type" : type,
            "key" : key,
            "feature" : feature
        };
        response = request.post("env", "create", json.dumps(data))
        if not response:
            return
        if response['code'] == 0:
            print("[Biolab] The env " + workflowcode + "_" + step + "_" + type + "#" + key + " registered successful")
        else:
            print("[Biolab] The env " + workflowcode + "_" + step + "_" + type + "#" + key + " already registered")


def list_env(workflowcode, step):
    if local_config.check():
        data = {
            "workflowCode" : workflowcode,
            "step" : step
        };
        response = request.post("env", "list", json.dumps(data))
        if not response:
            return
        if not response['data']:
            print("No envs added")
            return
        for env in response['data']:
            print(env)