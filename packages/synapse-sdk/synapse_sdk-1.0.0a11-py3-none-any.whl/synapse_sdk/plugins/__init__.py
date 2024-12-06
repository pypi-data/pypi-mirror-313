import os

from dotenv import load_dotenv

from synapse_sdk.plugins.cli import cli


def init():
    load_dotenv(os.path.join(os.getcwd(), '.env'))
    cli(obj={}, auto_envvar_prefix='SYNAPSE_PLUGIN')


__all__ = ['init']
