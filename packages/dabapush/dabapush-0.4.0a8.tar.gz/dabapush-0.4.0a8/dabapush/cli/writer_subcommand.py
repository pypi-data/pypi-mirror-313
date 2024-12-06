"""CLI subcommands for writer manipulation"""

# pylint: disable=W0622
from typing import List

import click

from dabapush.Dabapush import Dabapush


# Writer
@click.group()
def writer():
    """writer command"""


@writer.command()
@click.option(
    "--parameter",
    "-p",
    multiple=True,
    help="supply additional configuration detail in a key value format, e.g. port=1234.",
)
@click.argument("type")
@click.argument("name")
@click.pass_context
def add(ctx: click.Context, parameter: List[str], type: str, name: str):
    """add a writer to a project"""
    params = dict(arg.split("=") for arg in parameter)
    db: Dabapush = ctx.obj
    db.writer_add(type, name)
    db.writer_update(name, params)
    db.project_write()


@writer.command()
@click.argument("name")
@click.pass_context
def remove(ctx: click.Context, name: str):
    """remove a writer from a project"""
    db: Dabapush = ctx.obj
    db.reader_rm(name)


@writer.command()
@click.pass_context
def list(ctx):
    """list all writers"""
    writers = ctx.obj.writer_list()
    for key in writers:
        click.echo(f"- {key}")


@writer.command(help="Configure the writer with given name")
@click.option(
    "--parameter",
    "-p",
    multiple=True,
    type=click.STRING,
    help="add onfiguration in a key value format, e.g. pattern='*.ndjson'.",
)
@click.argument("name")
@click.pass_context
def configure(ctx: click.Context, parameter: List[str], name: str):
    """add configuration to a writer"""

    params = dict(arg.split("=") for arg in parameter)
    db: Dabapush = ctx.obj
    db.writer_update(name, params)
    db.project_write()
