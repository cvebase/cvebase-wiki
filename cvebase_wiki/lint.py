import click
import os
from rich.progress import Progress, TaskID
from concurrent.futures import ThreadPoolExecutor
from cvebased.repo import counttree, scantree, parse_md, write_md
from typing import Callable

progress = Progress()


@click.command()
@click.option(
    '-r',
    '--repo',
    type=click.Path(exists=True),
    help='path to cvebase.com repo'
)
def lint(repo: str) -> None:
    """Lint files in cvebase.com repo"""

    path_to_cves = os.path.join(repo, "cve")
    path_to_researchers = os.path.join(repo, "researcher")

    with progress:
        task1 = progress.add_task("[cyan]Linting CVEs...", start=False)
        task2 = progress.add_task("[cyan]Linting Researchers...", start=False)
        with ThreadPoolExecutor() as pool:
            progress.update(task1, total=counttree(path_to_cves, '.md'))
            progress.start_task(task1)
            for entry in scantree(path_to_cves, '.md'):
                try:
                    pool.submit(process_md, task1, entry.path, check_cve_front_matter)
                except Exception as e:
                    print(e)
                    continue

            progress.update(task2, total=counttree(path_to_researchers, '.md'))
            progress.start_task(task2)
            for entry in scantree(path_to_researchers, '.md'):
                try:
                    pool.submit(process_md, task2, entry.path, check_researcher_front_matter)
                except Exception as e:
                    print(e)
                    continue


def check_cve_front_matter(y: dict) -> dict:
    required_keys = ['id']
    optional_keys = ['pocs', 'courses', 'writeups']
    all_keys = required_keys + optional_keys
    for k in required_keys:
        if k not in y.keys():
            raise Exception(f"{k} missing")

    for k in optional_keys:
        if k in y:
            if len(y[k]) == 0:
                raise Exception(f"key {k} defined but empty")
            # dedupe and sort
            y[k] = dedupe_sort(y[k])

    for k in y.keys():
        if k not in all_keys:
            raise Exception(f"undefined key {k}")

    return y


def process_md(task_id: TaskID, filepath: str, check_front_matter_fn: Callable) -> None:
    with open(filepath, 'r') as f:
        try:
            file_str = f.read()
            ex_yaml, ex_md = parse_md(file_str)
            mod_yaml = check_front_matter_fn(ex_yaml)
            write_md(filepath, mod_yaml, ex_md, file_str)
        except Exception as e:
            print(e)
        finally:
            f.close()
            progress.update(task_id, advance=1)


def check_researcher_filename(filepath: str, alias: str) -> str:
    """Check researcher alias matches existing filepath
    and rename file is researcher alias does not match filename"""

    ex_filename = filepath.split('/')[-1].split('.')[0]
    if alias != ex_filename:
        filepath_base = "/".join(filepath.split('/')[0:-1])
        filepath = os.path.join(filepath_base, f"{alias}.md")
    return filepath


def check_researcher_front_matter(y: dict) -> dict:
    keys = ['name', 'alias', 'cves']
    for k in keys:
        if k not in y.keys():
            raise Exception(f"{k} missing")

    if len(y['cves']) < 1:
        raise Exception("no cves defined in cves field")

    y['cves'] = dedupe_sort(y['cves'])

    return y


def dedupe_sort(in_list: list) -> list:
    out_list = list(dict.fromkeys(in_list))
    out_list.sort()
    return out_list
