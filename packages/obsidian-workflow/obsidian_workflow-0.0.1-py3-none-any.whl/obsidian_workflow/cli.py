import click

from .daily import daily_cli


@click.version_option()
@click.group()
def cli():
    "Obsidian tools for automating my obsidian workflow"


cli.add_command(daily_cli)
