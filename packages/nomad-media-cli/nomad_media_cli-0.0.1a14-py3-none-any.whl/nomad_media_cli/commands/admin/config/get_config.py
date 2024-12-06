from nomad_media_cli.helpers.utils import initialize_sdk
import click
import json
import sys

@click.command()
@click.option("--config_type", required=True, type=int, help="The type of config to get. 1 - Admin, 2 - Lambda, 3 - Groundtruth")
@click.pass_context
def get_config(ctx, config_type):
    """Get the configuration"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        if config_type < 1 or config_type > 3:
            click.echo({ "error": "Invalid config type. Must be 1, 2, or 3." })
            sys.exit(1)        

        result = nomad_sdk.get_config(config_type)
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({ "error": f"Error getting configuration: {e}" })
        sys.exit(1)