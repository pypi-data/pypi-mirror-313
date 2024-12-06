from nomad_media_cli.helpers.utils import initialize_sdk

import click
import json
import sys

@click.command()
@click.option("--id", required=True, help="The id of the asset to retrieve.")
@click.pass_context
def get_asset(ctx, id):
    """Get an asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.get_asset(id)
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({ "error": f"Error getting asset: {e}" })
        sys.exit(1)