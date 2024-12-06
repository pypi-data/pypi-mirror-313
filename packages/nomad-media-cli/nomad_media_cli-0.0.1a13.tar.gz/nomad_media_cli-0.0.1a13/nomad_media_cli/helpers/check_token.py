import json

def check_token(config_path, nomad_sdk):
    with open(config_path, "r") as file:
        config = json.load(file)
    
    if config["token"] == nomad_sdk.token:
        return
    
    config["token"] = nomad_sdk.token
    
    with open(config_path, "w") as file:
        json.dump(config, file, indent=4)