from nomad_media_cli.helpers.utils import initialize_sdk

import click
import json
import sys

@click.command()
@click.option("--id", help="Can be an assetId (file), an assetId (folder), a collectionId, a savedSearchId (lower priority).")
@click.option("--path", help="Is the objectKey (which defaults to the default content bucket) or the url to the folder.")
@click.pass_context
def list_assets(ctx, id, path):
    """List assets"""
    
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:        
        filter = None
        if id: 
            filter = [{
                "fieldName": "uuidSearchField",
                "operator": "equals",
                "values": id
            }]
        elif path:
            if "::" not in path:
                if not "bucket" in ctx.obj:
                    click.echo("Please provide a valid path or set the default bucket.")
                    sys.exit(1)
                path = f"{ctx.obj['bucket']}::{path}"

            filter = [{
                "fieldName": "url",
                "operator": "equals",
                "values": path
            }]
        else:
            click.echo("Please provide an id or path.")
            sys.exit(1)

        results = nomad_sdk.search(None, None, 5, filter, 
            [
                { 
                    "fieldName": "identifiers.url", 
                    "sortType": "ascending"
                }
            ], 
            [
                { "name": "id"},
                { "name": "identifiers.name"},
                { "name": "identifiers.url"},
                { "name": "identifiers.fullUrl"},
                { "name": "identifiers.assetTypeDisplay"},
                { "name": "identifiers.mediaTypeDisplay"},
                { "name": "identifiers.contentLength"}
            ], None, None, None, None, None, None, None, None, None)
        
        click.echo(json.dumps(results["items"], indent=4))
    
    except Exception as e:
        click.echo({ "error": f"Error listing assets: {e}" })
        sys.exit(1)