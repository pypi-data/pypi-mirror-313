from nomad_media_cli.helpers.utils import initialize_sdk
import click
import json
import sys

@click.command()
@click.option("--content_id", required=True, help="The ID of the content.")
@click.option("--content_definition_id", required=True, help="The ID of the content definition.")
@click.pass_context
def get_content_user_track_touch(ctx, content_id, content_definition_id):
    """Get the user track touch for a content"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk.get_content_user_track_touch(content_id, content_definition_id)
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({ "error": f"Error getting content user track touch: {e}" })
        sys.exit(1)