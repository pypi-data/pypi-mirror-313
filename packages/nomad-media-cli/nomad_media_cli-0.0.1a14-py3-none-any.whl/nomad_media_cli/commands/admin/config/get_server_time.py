from nomad_media_cli.helpers.utils import initialize_sdk
import click
import json
import sys

@click.command()
@click.pass_context
def get_server_time(ctx):
    """Get the server time"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.get_server_time()
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({ "error": f"Error getting server time: {e}" })
        sys.exit(1)