import os
import json

def set_config(server,port,token):
    config = {
        "server": server,
        "port": port,
        "token": token
    }
    home_dir = os.path.expanduser('~')
    config_path = os.path.join(home_dir, '.biocmd.conf');

    print("[Biolab] Config write in [", config_path, "] successful!")    # 配置服务端信息
    with open(config_path, 'w') as file:
        file.write(json.dumps(config,indent=4));

def load_config():
    home_dir = os.path.expanduser('~')
    config_path = os.path.join(home_dir, '.biocmd.conf');
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config_string = f.read()
            return json.loads(config_string)
    else:
        print("[Biolab] Use 'biocmd local' command to set 'server','port' and 'token' first");
        return {}

def check():
    config = load_config();
    if len(config) == 0:
        return False;
    if "server" not in config or "port" not in config:
        print("[Biolab] 'server','port' and 'token' must be configured, use config command first")
        return False;
    return True;