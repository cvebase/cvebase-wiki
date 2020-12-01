import click
import editor
from cvebased.repo import compile_cve, check_cve_exists


@click.command()
@click.option(
    '-r',
    '--repo',
    type=click.Path(exists=True),
    required=True,
    help='path to cvebase.com repo'
)
@click.option(
    '-t',
    '--type',
    'type_',
    type=click.Choice(['cve', 'researcher'], case_sensitive=False),
    required=True,
    help=''
)
@click.argument('name', nargs=1)
def edit(repo, type_, name: str) -> None:
    """Edit a file in cvebase.com repo"""
    if type_ == 'cve':
        data = {'id': name}
        exists, path_to_cve = check_cve_exists(repo, data['id'])
        if not exists:
            compile_cve(repo, data)

        with open(path_to_cve, 'r') as fp:
            editor.edit(filename=fp.name)
    elif type_ == 'researcher':
        pass

