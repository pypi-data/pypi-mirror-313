import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--content_management_type", required=False, type=int, help="The type of content management to get. 1; None, 2; DataSelector, 3; FormSelector")
@click.option("--sort_column", required=False, help="The column to sort by.")
@click.option("--is_desc", required=False, type=bool, help="Whether to sort descending.")
@click.option("--page_index", required=False, type=int, help="The page index to get.")
@click.option("--page_size", required=False, type=int, help="The page size to get.")
@click.pass_context
def get_content_definitions(ctx, content_management_type, sort_column, is_desc, page_index, page_size):
    """Get content definitions"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        if content_management_type:
            if content_management_type < 1 or content_management_type > 3:
                click.echo({"error": "Content management type must be 1, 2, or 3."})
                sys.exit(1)     

        result = nomad_sdk.get_content_definitions(content_management_type, sort_column, is_desc, page_index, page_size)
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error getting content definitions: {e}"})
        sys.exit(1)