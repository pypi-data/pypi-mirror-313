import click
import json
import os

@click.command()
@click.option("--service-api-url", required=True, help="API URL for the service")
@click.option("--api-type", default="admin", type=click.Choice(['admin', 'portal']), help="API type (i.e. admin, portal )")
@click.option("--debug-mode", default="false", type=click.Choice(['true', 'false']), help="Enable debug mode")
@click.option("--singleton", default="true", type=click.Choice(['true', 'false']), help="Enable singleton mode")
@click.pass_context
def init(ctx, service_api_url, api_type, debug_mode, singleton):
    """Initialize the SDK and save configuration"""
    
    config_path = ctx.obj["config_path"]
    config_dir = os.path.dirname(config_path)
    os.makedirs(config_dir, exist_ok=True)
    
    config = {
        "serviceApiUrl": service_api_url,
        "apiType": api_type,
        "debugMode": False,
        "singleton": singleton == "true",
        "noLogging": True
    }
    
    try:
        with open(config_path, "w") as file:
            json.dump(config, file, indent=4)
    
    except Exception as e:
        click.echo({ "error": f"Error saving configuration: {e}" })