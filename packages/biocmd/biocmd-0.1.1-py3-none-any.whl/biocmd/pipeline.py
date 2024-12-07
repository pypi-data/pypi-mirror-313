import json
from . import local_config
from . import request

def create_workflow(workflowname, workflowcode, step, preStep):
    if local_config.check():
        data = {
            "workflowName" : workflowname,
            "workflowCode" : workflowcode,
            "step" : step,
            "preStep" : json.dumps(list(preStep))
        };
        response = request.post("workflow", "create", json.dumps(data))
        if not response:
            return
        if response["code"] == 0:
            print("[Biolab] Workflow " + workflowname + "#" + workflowcode + "_" + step + " registered successful !")
        else:
            print("[Biolab] Workflow " + workflowname + "#" + workflowcode + "_" + step + " already registered")



def list_workflow(workflowcode):
    if local_config.check():
        data = [workflowcode]
        if not workflowcode:
            data = []
        # print(list(unique_no))
        response = request.post("workflow", "list", json.dumps(data))
        if not response:
            return
        if not response['data']:
            print("No workflow configured")
            return
        for workflow in response["data"]:
            print(workflow)