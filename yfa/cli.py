import click
from yfa import __version__


@click.group()
@click.version_option(version=__version__)
def yfa_cli():
    """Command-line interface to YFA."""
    from .logging import configure_logging

    configure_logging()


@yfa_cli.command()
def migrate_core():
    pass


@yfa_cli.command()
def migrate_all_tenants():
    pass


@yfa_cli.command()
@click.option("--user-id")
def migrate_tenant(user_id):
    pass


def entrypoint():
    """The entry that the CLI is executed from"""
    from .exceptions import YFAException

    try:
        yfa_cli()
    except YFAException as e:
        click.secho(f"ERROR: {e}", bold=True, fg="red")


if __name__ == "__main__":
    entrypoint()
