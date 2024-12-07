import os
import json

from . import local_config
from . import request

def create_file(basedir):
    if local_config.check():
        if basedir.endswith('/'):
             basedir = basedir[:-1]
        batchNo = os.path.basename(basedir)
        data = [];
        file_address = [];
        for root, dirs, files in os.walk(basedir):
            for file in files:
                if file.endswith('.fq.gz'):
                    sample_no, unique_no = os.path.basename(os.path.dirname(root)), os.path.basename(root)
                    file_path = os.path.join(root, file)
                    found = False
                    for item in data:
                        if item['sampleNo'] == sample_no and item['uniqueNo'] == unique_no:
                            item['address'].append(file_path)
                            file_address = item['address']
                            item['address'] = json.dumps(file_address)
                            found = True
                            break
                    if not found:
                        data.append({'batchNo':batchNo,'sampleNo': sample_no, 'uniqueNo': unique_no,'type':'rawdata', 'address': [file_path]})

        # print(data)
        response = request.post("fileIndex", "createAll", json.dumps(data))
        if not response:
            return
        if response['code'] == 0:
            print("[Biolab] Total", len(data) , "samples register successful")


def list_file(uniqueno):
    if local_config.check():
        response = request.post("fileIndex", "list", json.dumps(uniqueno))
        if not response:
            return
        if not response['data']:
            print("No files added")
            return
        for file in response['data']:
            print(file)