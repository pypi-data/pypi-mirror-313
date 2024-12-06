import click
import json
import sys

@click.command()
@click.option("--service-api-url", help="API URL for the service")
@click.option("--api-type", default="admin", type=click.Choice(['admin', 'portal']), help="API type (i.e. admin, portal )")
@click.pass_context
def update_config(ctx, service_api_url, api_type):
    """Update the configuration"""
    
    config_path = ctx.obj["config_path"]

    try:
        with open(config_path, "r") as file:
            config = json.load(file)
        
        if service_api_url:
            config["serviceApiUrl"] = service_api_url
        if api_type:
            config["apiType"] = api_type

        with open(config_path, "w") as file:
            json.dump(config, file, indent=4)
    
    except Exception as e:
        click.echo({ "error": f"Error updating configuration: {e}" })
        sys.exit(1)