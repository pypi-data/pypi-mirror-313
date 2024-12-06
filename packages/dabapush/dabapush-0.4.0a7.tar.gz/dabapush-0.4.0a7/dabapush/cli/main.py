"""Entrypoint for Dabapush CLI"""

import click
from loguru import logger as log

from dabapush.Dabapush import Dabapush

from .create_subcommand import create
from .reader_subcommand import reader
from .run_subcommand import run
from .update_subcommand import update
from .writer_subcommand import writer
from dabapush import __version__

_log_levels_ = {
    0: "CRITICAL",
    1: "ERROR",
    2: "WARNING",
    3: "INFO",
    4: "DEBUG",
}


@click.group()
@click.option(
    "--logfile",
    "-l",
    type=click.File("at", encoding="utf8"),
    help="File to log in, defaults to stdout.",
    default="-",
)
@click.option(
    "--json",
    "-j",
    is_flag=True,
    help="Output log in JSON format, defaults to False.",
    default=False,
)
@click.option(
    "--verbose",
    "-v",
    count=True,
    help="Increases verbosity, maximally vvvv.",
    default=0,
)
@click.pass_context
@click.version_option(__version__)
def cli(ctx: click.Context, logfile, json, verbose):
    """Dabapush"""
    # prepare log options
    log.remove()
    log_level = _log_levels_.get(verbose, "CRITICAL")
    log.add(logfile, level=log_level, serialize=json)

    # prepare context
    ctx.ensure_object(Dabapush)

    db: Dabapush = ctx.obj
    log.debug(f"Starting DabaPush in {db.working_dir}.")


cli.add_command(reader)
cli.add_command(writer)
cli.add_command(run)
cli.add_command(create)
cli.add_command(update)
