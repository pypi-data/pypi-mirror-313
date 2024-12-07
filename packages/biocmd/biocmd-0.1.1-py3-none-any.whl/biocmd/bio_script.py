import json
from . import local_config
from . import request

def create_script(workflowcode, step, type, script):
    if local_config.check():
        data = {
            "workflowCode" : workflowcode,
            "step" : step,
            "type" : type,
            "script" : script
        }
        response = request.post("script", "create", json.dumps(data))
        if not response:
            return
        if response["code"] == 0:
            print("[Biolab] Script " + workflowcode + "_" + step + "#"  + script  + " registered successful")
        else:
            print("[Biolab] Script " + workflowcode + "_" + step + "#"  + script  + " already registered")


def list_script(workflowcode):
    if local_config.check():
        data = [workflowcode];
        if not workflowcode:
            data = []
        response = request.post("script", "list", json.dumps(data))
        if not response:
            return
        if not response['data']:
            print("No scripts configured")
            return
        for script in response['data']:
            print(script)