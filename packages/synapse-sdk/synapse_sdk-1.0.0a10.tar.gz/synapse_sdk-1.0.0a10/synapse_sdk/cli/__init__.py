import click

from synapse_sdk.cli.create_plugin import create_plugin


@click.group()
def cli():
    pass


cli.add_command(create_plugin)
