from nomad_media_cli.helpers.utils import initialize_sdk
import click
import json
import sys

@click.command()
@click.pass_context
def create_content_definition(ctx):
    """Create a new content definition"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.create_content_definition()
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({ "error": f"Error creating content definition: {e}" })
        sys.exit(1)