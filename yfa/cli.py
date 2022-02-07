import os
import sys
import click
import subprocess
import asyncio

from yfa import __version__


@click.group()
@click.version_option(version=__version__)
def yfa_cli():
    """Command-line interface to YFA."""
    from yfa.logging import configure_logging

    configure_logging()


@yfa_cli.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.option("--db", type=click.Choice(["core", "user"]))
@click.option("--db-name", required=False)
@click.pass_context
def alembic(ctx, db: str, db_name: str = None):
    if db == "user" and not db_name:
        raise Exception("--db-name is mandatory")

    print(f"Type: {db}")
    exec_args = [
        sys.executable,
        "-m", "alembic",
        "--name", db,
        "-c", os.path.join(os.path.dirname(__file__), "alembic.ini"),
        *ctx.args,
    ]
    print(" ".join(exec_args))

    env = {}
    if db_name:
        env["DB_NAME"] = db_name
    subprocess.run(exec_args, env=env)


@yfa_cli.command()
def make_core_db():
    if not click.confirm("This will reset the CoreDB. Do you want to Continue ?"):
        return
    from yfa.database.utils.core_db import make_core_db as _make_core_db
    asyncio.run(_make_core_db())


def entrypoint():
    """The entry that the CLI is executed from"""
    from yfa.exceptions import YFAException

    try:
        yfa_cli()
    except YFAException as e:
        click.secho(f"ERROR: {e}", bold=True, fg="red")


if __name__ == "__main__":
    entrypoint()
