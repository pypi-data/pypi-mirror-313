from nomad_media_cli.helpers.utils import initialize_sdk
import click
import sys

@click.command()
@click.option("--session_id", required=True, help="The ID of the session.")
@click.option("--content_id", required=True, help="The ID of the content.")
@click.option("--content_definition_id", required=True, help="The ID of the content definition.")
@click.option("--deactivate", required=True, help="The deactivate flag.")
@click.pass_context
def deactivate_content_user_track(ctx, session_id, content_id, content_definition_id, deactivate):
    """Deactivate a content user track"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        nomad_sdk.deactivate_content_user_track(session_id, content_id, content_definition_id, deactivate)
        click.echo("Content user track deactivated successfully")

    except Exception as e:
        click.echo({ "error": f"Error deactivating content user track: {e}" })
        sys.exit(1)