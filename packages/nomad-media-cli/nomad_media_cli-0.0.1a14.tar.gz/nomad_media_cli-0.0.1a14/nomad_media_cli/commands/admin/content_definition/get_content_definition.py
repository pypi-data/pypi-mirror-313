import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--content_definition_id", required=True, help="The ID of the content definition to retrieve.")
@click.pass_context
def get_content_definition(ctx, content_definition_id):
    """Get content definition by id"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.get_content_definition(content_definition_id)
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error getting content definition: {e}"})
        sys.exit(1)