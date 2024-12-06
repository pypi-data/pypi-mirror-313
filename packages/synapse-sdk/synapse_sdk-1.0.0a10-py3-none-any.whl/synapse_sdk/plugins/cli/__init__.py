import click

from synapse_sdk.i18n import gettext as _

from .publish import publish
from .run import run


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug

    if debug:
        click.echo(_('Debug mode is "on"'))


cli.add_command(run)
cli.add_command(publish)
