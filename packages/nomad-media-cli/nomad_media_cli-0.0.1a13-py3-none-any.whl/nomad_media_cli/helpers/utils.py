from nomad_media_pip.src.nomad_sdk import Nomad_SDK

import click
import json
import os
import sys

def get_config(ctx):
    config_path = ctx.obj["config_path"]    

    try:
        if os.path.exists(config_path):
            with open(config_path, "r") as file:
                config = json.load(file)
            ctx.obj["config"] = config
        else:
            click.echo({ "error": "No configuration found. Please run 'init' first." })
            sys.exit(1)
    
    except Exception as e:
        click.echo({ "error": f"Error loading configuration: {e}" })
        sys.exit(1)

def initialize_sdk(ctx):
    get_config(ctx)
    config = ctx.obj["config"]

    try:
        if config is not None:
            if not "token" in config:
                click.echo({ "error": "No token found. Please run 'login' first." })
                sys.exit(1)            

            nomad_sdk = Nomad_SDK(config)

            nomad_sdk.token = config.get("token")
            nomad_sdk.refresh_token_val = config.get("refresh_token_val")
            
            ctx.obj["nomad_sdk"] = nomad_sdk
            
        else:
            click.echo({ "error": "No configuration found. Please run 'init' first." })
            sys.exit(1)
            
    except Exception as e:
        click.echo({ "error": f"Error initializing SDK: {e}" })
        sys.exit(1)