import click

@click.command()
@click.pass_context
def list_config_path(ctx):
    """List the configuration path"""
    
    click.echo({ "path": ctx.obj["config_path"] })