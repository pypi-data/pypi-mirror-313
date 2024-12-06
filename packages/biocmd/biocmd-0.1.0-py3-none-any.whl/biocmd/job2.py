import json
from . import local_config
from . import request

def create_task(workflowcode, step, uniqueNo):
    if local_config.check():
        data = {
            "workflowCode" : workflowcode,
            "step" : step,
            "uniqueNo" : uniqueNo
        }
        response = request.post("task", "create", json.dumps(data))
        if not response:
            return
        code = response["code"]
        if code == 0:
            print("[Biolab] Task " + workflowcode + "_" + step + "_"  + uniqueNo  + " create successful")
        elif code == 5003:
            print("[Biolab] The workflow [" + workflowcode + "_" + step + "] missing script")
        elif code == 5004:
            print("[Biolab] The workflow [" + workflowcode + "_" + step + "] missing input template")
        elif code == 5005:
            print("[Biolab] The workflow [" + workflowcode + "_" + step + "] missing input files")
        elif code == 5006:
            print("[Biolab] The task [" + workflowcode + "_" + step + "_" + uniqueNo + "] pre task not all completed")
        elif code == 5007:
            print("[Biolab] The task [" + workflowcode + "_" + step + "_" + uniqueNo + "] already exist")
        elif code == 5008:
            print("[Biolab] The workflow [" + workflowcode + "_" + step + "] not exist")

def list_task(workflowcode):
    if local_config.check():
        data = [workflowcode]
        if not workflowcode:
            data = []
        response = request.post("task", "list", json.dumps(data))
        if not response:
            return
        if not response['data']:
            print("No tasks created")
            return
        for script in response['data']:
            print(script)