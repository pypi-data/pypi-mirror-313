from nomad_media_pip.src.nomad_sdk import Nomad_SDK
from nomad_media_cli.helpers.utils import get_config

import click
import json
import sys

@click.command()
@click.option("--username", required=True, help="Username for authentication")
@click.option("--password", required=True, help="Password for authentication")
@click.pass_context
def login(ctx, username, password):
    """Login to the service"""

    get_config(ctx)

    config = ctx.obj["config"]
    config_path = ctx.obj["config_path"]

    try:
        login_config = config.copy()
        login_config["username"] = username
        login_config["password"] = password
        
        nomad_sdk = Nomad_SDK(login_config)
        nomad_sdk.login()
        
        config["token"] = nomad_sdk.token
        config["refresh_token_val"] = nomad_sdk.refresh_token_val
        config["expiration_seconds"] = nomad_sdk.expiration_seconds
        config["id"] = nomad_sdk.id
        
        with open(config_path, "w") as file:
            json.dump(config, file, indent=4)
            
    except Exception as e:
        click.echo({ "error": f"Error logging in: {e}" })
        sys.exit(1)