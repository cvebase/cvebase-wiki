import click
from cvebase_wiki.lint import lint


@click.group()
def cli():
    pass


cli.add_command(lint)
