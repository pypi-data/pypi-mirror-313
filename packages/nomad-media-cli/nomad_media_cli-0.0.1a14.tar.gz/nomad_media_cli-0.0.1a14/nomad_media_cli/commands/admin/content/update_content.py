from nomad_media_cli.helpers.utils import initialize_sdk
import click
import json
import sys

@click.command()
@click.option("--content_id", required=True, help="The id of the content to retrieve.")
@click.pass_context
def get_content(ctx, content_id):
    """Get content by id"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.get_content(content_id)
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({ "error": f"Error getting content: {e}" })
        sys.exit(1)