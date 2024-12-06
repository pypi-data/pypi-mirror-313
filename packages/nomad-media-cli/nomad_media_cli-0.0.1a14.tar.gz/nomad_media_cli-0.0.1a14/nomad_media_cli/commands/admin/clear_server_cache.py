from nomad_media_cli.helpers.utils import initialize_sdk
import click
import sys

@click.command()
@click.pass_context
def clear_server_cache(ctx):
    """Clear the server cache"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        nomad_sdk.clear_server_cache()
        click.echo("Server cache cleared successfully")

    except Exception as e:
        click.echo({ "error": f"Error clearing server cache: {e}" })
        sys.exit(1)