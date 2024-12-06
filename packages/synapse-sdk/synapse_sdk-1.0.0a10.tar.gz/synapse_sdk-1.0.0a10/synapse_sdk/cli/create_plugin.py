from pathlib import Path

import click
from cookiecutter.main import cookiecutter


@click.command()
def create_plugin():
    project_root = Path(__file__).parent.parent
    cookiecutter(str(project_root / 'plugins/templates'))
