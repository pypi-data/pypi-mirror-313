import click
from sqlfluff.cli.commands import lint as sqlfluff_lint
from sqlfluff.cli.commands import fix as sqlfluff_fix

from click_default_group import DefaultGroup

import importlib.resources

CONFIG_FILE_NAME = "my.sqlfluff"

def get_config_path():
    """Retrieve the path to the dang.sqlfluff file."""
    with importlib.resources.path("dang_sqlfluffer.config", CONFIG_FILE_NAME) as config_path:
        return str(config_path)


@click.group(cls=DefaultGroup, default="lint", default_if_no_args=True)
@click.version_option()
def cli():
    "my convenient opinionated wrapper around sqlfluff"
    pass


@cli.command(
    cls=type(sqlfluff_fix),
    name=sqlfluff_fix.name,
    help=sqlfluff_fix.help,
    params=sqlfluff_fix.params,
)
@click.pass_context
def fix(ctx, *args, **kwargs):
    """Fix a SQL file using the dang-sqlfluff configuration."""
    kwargs['extra_config_path'] = get_config_path()

    click.echo(kwargs['extra_config_path'])
    ctx.invoke(sqlfluff_fix, *args, **kwargs)

if __name__ == "__main__":
    cli()


@cli.command(
    cls=type(sqlfluff_lint),
    name=sqlfluff_lint.name,
    help=sqlfluff_lint.help,
    params=sqlfluff_lint.params,
)
@click.pass_context
def lint(ctx, *args, **kwargs):
    """Lint a SQL file using the dang-sqlfluff configuration."""
    kwargs['extra_config_path'] = get_config_path()

    click.echo(kwargs['extra_config_path'])
    ctx.invoke(sqlfluff_lint, *args, **kwargs)

if __name__ == "__main__":
    cli()
