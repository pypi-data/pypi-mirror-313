"""Create a new project configuration.
"""

import click
from loguru import logger as log

from dabapush.Configuration import Registry
from dabapush.Configuration.ProjectConfiguration import ProjectConfiguration
from dabapush.Dabapush import Dabapush


# CREATE
@click.command()
@click.option(
    "--interactive/--non-interactive",
    default=True,
    show_default=True,
    help="should we run an interactive prompt to create the configuration?",
)
@click.pass_context
def create(ctx, interactive):
    """

    Parameters
    ----------
    ctx :
        param interactive:
    interactive :


    Returns
    -------

    """
    log.debug(f"Creating project in {ctx.obj.working_dir}")
    # Initialize configuration dict, setup work is already done by
    # db.pr_init, has it has not found a configuration
    db: Dabapush = ctx.obj
    conf: ProjectConfiguration = db.config

    if interactive:
        conf.set_name(click.prompt("project name", type=str))
        conf.set_author(
            click.prompt('author name (split several authors with ";")', type=str)
        )

        man_config = click.confirm("Should we configure readers and writers?")

        while man_config is True:
            thing_to_configure = click.prompt(
                "What do you want to configure?",
                default="Writer",
                type=click.Choice(["Reader", "Writer"]),
            )
            if thing_to_configure not in ["Reader", "Writer"]:
                log.debug("Try again.")
            else:
                if thing_to_configure == "Reader":
                    log.debug("Configuring a Reader")
                    reader_name = click.prompt(
                        "Which Reader should we configure?",
                        type=click.Choice(Registry.list_all_readers()),
                    )
                    if reader_name in Registry.list_all_readers():
                        conf.add_reader(reader_name, "default")
                        log.debug("Success! Found the reader you're looking for!")
                if thing_to_configure == "Writer":
                    writer_name = click.prompt(
                        "Which Writer should we configure?",
                        type=click.Choice(Registry.list_all_writers()),
                    )
                    if writer_name in Registry.list_all_writers():
                        conf.add_writer(writer_name, "default")
                        log.debug("Success! Found the writer you're looking for!")
                man_config = click.confirm("Do another?")

    db.project_write()
