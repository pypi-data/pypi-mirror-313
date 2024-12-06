from nomad_media_cli.helpers.utils import initialize_sdk

import click
import json
import sys

@click.command()
@click.pass_context
def list_buckets(ctx):
    """List buckets"""    
    
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:    
        filter = [{
            "fieldName": "assetType",
            "operation": "equals",
            "values": 5
        }]

        results = nomad_sdk.search(None, None, None, filter, None, None, None, None, None, None, None, None, None, None, None)

        result_names = [result["identifiers"]["name"] for result in results["items"]]
        
        click.echo(json.dumps(result_names, indent=4))

    except Exception as e:
        click.echo({ "error": f"Error listing buckets: {e}" })
        sys.exit(1)