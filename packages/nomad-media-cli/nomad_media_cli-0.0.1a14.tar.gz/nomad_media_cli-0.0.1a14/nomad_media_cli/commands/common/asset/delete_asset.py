from nomad_media_cli.helpers.utils import initialize_sdk
import click
import sys

@click.command()
@click.option("--id", required=True, help="The id of the asset to delete.")
@click.pass_context
def delete_asset(ctx, id):
    """Delete an asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        nomad_sdk.delete_asset(id)
        click.echo(f"Asset deleted successfully: {id}")

    except Exception as e:
        click.echo({ "error": f"Error deleting asset: {e}" })
        sys.exit(1)