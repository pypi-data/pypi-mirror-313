from nomad_media_cli.helpers.utils import initialize_sdk

import click
import os
import sys
import threading

@click.command()
@click.option("--source", help="File or folder to upload")
@click.option("--id", help="Parent folder id")
@click.option("--url", help="The Nomad URL of the Asset (file or folder) to list the assets for (bucket::object-key).")
@click.option("--object-key", help="Object-key only of the Asset (file or folder) to list the assets for. This option assumes the default bucket that was previously set with the `set-bucket` command.")
@click.option("-r", "--recursive", is_flag=True, help="Recursively upload a folder")
@click.pass_context
def upload_assets(ctx, source, id, url, object_key, recursive):
    """Upload assets"""
    
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:
        parent_id = None        

        if not source:
            click.echo({ "error": "Please provide a file or folder to upload." })
            sys.exit(1)
            
        if not id and not url and not object_key:
            click.echo({ "error": "Please provide a parent id, url, or object_key." })
            sys.exit(1)
            
        if url and "::" not in url:
            click.echo("Please provide a valid path.")
            sys.exit(1)

        if object_key:
            if "bucket" in ctx.obj:
                url = f"{ctx.obj['bucket']}::{object_key}"
            else:
                click.echo({ "error": "Please set bucket using `set-bucket` or use url." })
                sys.exit(1)
            
        if url:
            parent_id = url
        elif id:
            parent_id = id
            
        if os.path.isdir(source):
            if recursive:
                threads = []
                for root, dirs, files in os.walk(source):
                    folder_name = os.path.basename(root)
                    
                    folder = None
                    while True:
                        nomad_folders = nomad_sdk.search(None, None, None,
                            [
                                {
                                    "fieldName": "assetId",
                                    "operator": "equals",
                                    "values": parent_id
                                },
                                {
                                    "fieldName": "assetType",
                                    "operator": "equals",
                                    "values": 1
                                }
                            ],
                            None, None, None, None, None, None, None, None, None, None, None)
                        
                        if len(nomad_folders["items"]) == 0:
                            break
                        
                        folder = next((nomad_folder for nomad_folder in nomad_folders["items"] if nomad_folder["title"] == folder_name), None)
                        if folder:
                            break
                        
                    if not folder:
                        folder = nomad_sdk.create_folder_asset(parent_id, folder_name)
                        
                    folder_id = folder["id"]
                    parent_id = folder_id

                    for name in files:
                        file_path = os.path.join(root, name)
                        thread = threading.Thread(target=nomad_sdk.upload_asset, args=(None, None, None, "replace", file_path, folder_id, None))
                        thread.start()
                        threads.append(thread)
                        
                for thread in threads:
                    thread.join()
                    
            else:
                click.echo({ "error": "Please use the --recursive option to upload directories." })
                sys.exit(1)
        else:
            nomad_sdk.upload_asset(None, None, None, "replace", source, parent_id, None)
                
    except Exception as e:
        click.echo({ "error": f"Error uploading assets: {e}" })
        sys.exit(1)