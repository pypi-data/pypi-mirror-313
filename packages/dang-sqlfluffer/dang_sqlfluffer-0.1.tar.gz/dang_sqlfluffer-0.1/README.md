# dang-sqlfluffer

[![PyPI](https://img.shields.io/pypi/v/dang-sqlfluffer.svg)](https://pypi.org/project/dang-sqlfluffer/)
[![Changelog](https://img.shields.io/github/v/release/dannguyen/dang-sqlfluffer?include_prereleases&label=changelog)](https://github.com/dannguyen/dang-sqlfluffer/releases)
[![Tests](https://github.com/dannguyen/dang-sqlfluffer/actions/workflows/test.yml/badge.svg)](https://github.com/dannguyen/dang-sqlfluffer/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/dannguyen/dang-sqlfluffer/blob/master/LICENSE)

my convenient opinionated wrapper around sqlfluff


# Current status

Invoke either lint or fix; lint is default.

```sh
# default behavior is to lint using config/my.sqlfluff
$ echo 'select 1 as id, 2 hello, 3 world order by id' | dang-sqlfluff -

== [stdin] FAIL                                                                                                                      L:   1 | P:   1 | CP01 | Keywords must be upper case.
                       | [capitalisation.keywords]
L:   1 | P:   1 | LT09 | Select targets should be on a new line unless there is
                       | only one select target. [layout.select_targets]
L:   1 | P:  10 | CP01 | Keywords must be upper case.
                       | [capitalisation.keywords]
L:   1 | P:  19 | AL02 | Implicit/explicit aliasing of columns.
                       | [aliasing.column]
L:   1 | P:  28 | AL02 | Implicit/explicit aliasing of columns.
                       | [aliasing.column]
L:   1 | P:  34 | CP01 | Keywords must be upper case.
                       | [capitalisation.keywords]
L:   1 | P:  40 | CP01 | Keywords must be upper case.
                       | [capitalisation.keywords]
All Finished 📜 🎉!
```






# Boilerplate

## Installation

Install this tool using `pip`:
```bash
pip install dang-sqlfluffer
```
## Usage

For help, run:
```bash
dang-sqlfluff --help
```
You can also use:
```bash
python -m dang_sqlfluffer --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd dang-sqlfluffer
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
