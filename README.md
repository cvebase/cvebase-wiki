# cvebase-wiki

cvebase's command line tool for interacting with cvebase.com wiki data.

* [Visit cvebase.com web app](https://www.cvebase.com/)
* [View wiki repo on GitHub (cvebase/cvebase.com)](https://github.com/cvebase/cvebase.com)

## Installation

```
python3 -m pip install cvebase-wiki --upgrade
```

## Usage

Lint all CVE & Researcher markdown files.

```
cvebase-wiki lint -r <path to cvebase.com repo>
```

Edit CVE file. Looks for ${EDITOR} env variable, then system editor in order: vim, emacs, nano.

```
cvebase-wiki edit -t <path to cvebase.com repo> -t cve CVE-2020-14882
```
