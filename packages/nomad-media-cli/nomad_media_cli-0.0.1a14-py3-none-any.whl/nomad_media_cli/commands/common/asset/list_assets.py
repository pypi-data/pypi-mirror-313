from nomad_media_cli.helpers.utils import initialize_sdk

import click
import json
import sys

@click.command()
@click.option("--id", help="Can be an assetId (file), an assetId (folder), a collectionId, a savedSearchId (lower priority).")
@click.option("--url", help="The Nomad URL of the Asset (file or folder) to list the assets for (bucket::object-key).")
@click.option("--object-key", help="Object-key only of the Asset (file or folder) to list the assets for. This option assumes the default bucket that was previously set with the `set-bucket` command.")
@click.pass_context
def list_assets(ctx, id, url, object_key):
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
        elif url or object_key:
            if url and "::" not in url:
                click.echo({ "error": "Please provide a valid path or set the default bucket." })               
                sys.exit(1)
            if object_key:
                if "bucket" in ctx.obj:
                    url = f"{ctx.obj['bucket']}::{object_key}"
                else:
                    click.echo({ "error": "Please set bucket using `set-bucket` or use url." })
                    sys.exit(1)

            filter = [{
                "fieldName": "url",
                "operator": "equals",
                "values": url
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