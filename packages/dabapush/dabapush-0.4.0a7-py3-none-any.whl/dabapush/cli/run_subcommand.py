"""Some module documentation
"""

from typing import List

import click
from loguru import logger as log

from dabapush.Dabapush import Dabapush


@click.command(help="Run dabapush job in the current working directory.")
@click.argument("targets", nargs=-1)
@click.pass_context
def run(ctx, targets: List[str]) -> None:
    """run verb

    Parameters
    ----------
    ctx :
        param targets: List[str]:
    targets :
        List[str]:
    targets: List[str] :


    Returns
    -------

    """
    db: Dabapush = ctx.obj
    log.debug(f"Running DabaPush job in {db.working_dir}")
    # log.debug(f'Using this global configuration {db.global_config}')
    # log.debug(f'Using this local configuration {db.config}')

    db.job_run(targets)
