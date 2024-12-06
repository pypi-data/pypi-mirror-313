from nomad_media_cli.helpers.utils import initialize_sdk
import click
import json
import sys

@click.command()
@click.option("--id", required=True, help="The id of the asset to get the audit for.")
@click.pass_context
def get_audit(ctx, id):
    """Get the audit for an asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        result = nomad_sdk._get_audit(id)
        if result:
            click.echo(json.dumps(result, indent=4))
        else:
            click.echo("No audit information found.")

    except Exception as e:
        click.echo({ "error": f"Error getting audit: {e}" })
        sys.exit(1)