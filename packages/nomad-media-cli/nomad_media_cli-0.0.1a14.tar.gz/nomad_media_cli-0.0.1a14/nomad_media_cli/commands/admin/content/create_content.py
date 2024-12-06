from nomad_media_cli.helpers.utils import initialize_sdk
import click
import json
import sys

@click.command()
@click.option("--content_definition_id", required=True, help="The id of the content definition to create.")
@click.option("--language_id", help="The id of the language to create the content in.")
@click.pass_context
def create_content(ctx, content_definition_id, language_id):
    """Create a new content"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.create_content(content_definition_id, language_id)
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({ "error": f"Error creating content: {e}" })
        sys.exit(1)