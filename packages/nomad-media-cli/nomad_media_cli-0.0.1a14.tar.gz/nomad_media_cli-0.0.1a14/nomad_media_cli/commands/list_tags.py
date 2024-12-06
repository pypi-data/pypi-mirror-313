from nomad_media_cli.helpers.utils import initialize_sdk

import click
import json
import sys

@click.command()
@click.option("--size", default=10, type=int, help="The number of results shown. Default is 10.")
@click.option("--offset", type=int, help="The offset of the page.")
@click.pass_context
def list_tags(ctx, size, offset):
    """List tags"""    
    
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:    
        filter = [{
            "fieldName": "contentDefinitionId",
            "operation": "equals",
            "values": "c806783c-f127-48ae-90c9-32175f4e1fff"
        }]

        results = nomad_sdk.search(None, offset, size, filter, None, None, None, None, None, None, None, None, None, None, None)

        result_names = [result["title"] for result in results["items"]]
        
        click.echo(json.dumps(result_names, indent=4))

    except Exception as e:
        click.echo({ "error": f"Error listing tags: {e}" })
        sys.exit(1)