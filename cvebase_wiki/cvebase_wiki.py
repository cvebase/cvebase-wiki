import click
from cvebase_wiki.lint import lint
from cvebase_wiki.edit import edit


@click.group()
def cli():
    pass


cli.add_command(lint)
cli.add_command(edit)
