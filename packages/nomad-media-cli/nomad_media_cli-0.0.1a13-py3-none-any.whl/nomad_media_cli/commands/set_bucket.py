import click
import json
import sys

@click.command()
@click.option("--bucket", required=True, help="Bucket name")
@click.pass_context
def set_bucket(ctx , bucket):
    """Set the default bucket"""

    config_path = ctx.obj.get("config_path")

    try:
        with open(config_path, "r") as file:
            config = json.load(file)
        
        config["bucket"] = bucket

        with open(config_path, "w") as file:
            json.dump(config, file, indent=4)
    
    except Exception as e:
        click.echo({ "error": f"Error setting bucket: {e}" })       
        sys.exit(1)