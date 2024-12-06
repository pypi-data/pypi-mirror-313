import click
import json
import sys

@click.command()
@click.option("--tag", required=True, multiple=True, help="tag name")
@click.pass_context
def set_tags(ctx , tag):
    """Set the default tag"""

    config_path = ctx.obj.get("config_path")

    try:
        with open(config_path, "r") as file:
            config = json.load(file)
        
        config["tag"] = ",".join(tag)

        with open(config_path, "w") as file:
            json.dump(config, file, indent=4)
    
    except Exception as e:
        click.echo({ "error": f"Error setting tag: {e}" })       
        sys.exit(1)