"""Dabapush is the main application class of this project."""

from pathlib import Path
from typing import Dict, List

import yaml
from loguru import logger as log

from dabapush.Configuration import Registry
from dabapush.Configuration.ProjectConfiguration import ProjectConfiguration
from dabapush.Configuration.Registry import list_all_readers, list_all_writers


class Dabapush:
    """This is the main class for this application.

    Parameters
    ----------
    working_dir : Path
        The working directory of the application
    """

    def __init__(
        self,
        working_dir: Path = Path(),
    ):
        self.working_dir = working_dir.resolve()
        self.config = None
        if not self.project_read():
            self.project_init()
        log.debug(f"Staring DabaPush instance with {self.config}")

    def update_reader_targets(self, name: str) -> None:
        """

        Parameters
        ----------
        name :
            str:
        name :
            str:
        name: str :


        Returns
        -------

        """

    # PROJECT specific methods
    def project_init(self):
        """Initialize a new project in the current directory"""
        self.config = ProjectConfiguration()

    def project_write(self):
        """Write the current configuration to the project
        configuration file in the current directory.
        """
        if self.config is not None:
            conf_path = self.working_dir / "dabapush.yml"
            log.debug(f"writing the following project configuration: {self.config}")
            with conf_path.open("w") as file:
                yaml.dump(self.config, file)

    def project_read(self) -> bool:
        """Read the project configuration file in the current directory

        Parameters
        ----------

        Returns
        -------
        type
            bool: Indicates whether loading was successful

        """
        # attach all plugins once, so they can be used inside the configuration.
        for reader in Registry.list_all_readers():
            Registry.get_reader(reader)
        for writer in Registry.list_all_writers():
            Registry.get_writer(writer)
        # read the configuration file
        conf_path = self.working_dir / "dabapush.yml"
        if conf_path.exists():
            with conf_path.open("r") as file:
                self.config = yaml.full_load(file)
            return True
        return False

    # READER specific methods
    def reader_add(self, reader: str, name: str):
        """add a reader to the current project

        Parameters
        ----------
        reader :
            str:
        name :
            str:

        Returns
        -------

        """
        self.config.add_reader(reader, name)

    def reader_list(self):
        """Lists all available readers"""
        return list_all_readers()

    def reader_rm(self, name: str):
        """remove a reader from the current configuration"""
        if name in self.config.readers:
            del self.config.readers[name]
        else:
            log.warning(f"Cannot delete {name} as it does not exist.")

    def reader_update(self, name: str, config: Dict[str, str]):
        """update a reader's configuration"""
        obj = self.config.readers[name] if name in self.config.readers else None

        if obj is not None:
            for k, v in config.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)
                else:
                    log.warning(f"key {k} not valid in type: {obj.__class__.__name__}")

    # WRITER specific methods
    def writer_add(self, kind: str, name: str):
        """add a reader to the current project"""
        self.config.add_writer(kind, name)

    def writer_rm(self, name: str):
        """remove a reader from the current configuration"""
        if name in self.config.readers:
            del self.config.readers[name]
        else:
            log.warning(f"Cannot delete {name} as it does not exist.")

    def writer_update(self, name: str, config: Dict[str, str]):
        """update a reader's configuration"""
        obj = self.config.writers[name] if name in self.config.readers else None

        if obj is not None:
            for k, v in config.items():
                if hasattr(obj, k):
                    setattr(obj, k, v)
                else:
                    log.warning(f"key {k} not valid in type: {obj.__class__.__name__}")

    def writer_list(self):
        """Lists all available readers"""
        return list_all_writers()

    # JOB specific methods
    def job_run(self, targets: List[str]):
        """runs the job(s) configured in the current directory

        Parameters
        ----------
        targets :
            List[str]:

        Returns
        -------

        """
        if len(self.config.readers) == 0:
            log.error("No jobs are configured. Nothing to run.")
            return
        # single dispatch all jobs
        if len(targets) == 1 and targets[0] == "all":
            log.debug(f'Running all jobs: {", ".join(self.config.readers)}.')
            for target in self.config.readers:
                self.__dispatch_job__(target)

        # run multiple jobs
        else:
            for target in targets:
                if target in self.config.readers:
                    self.__dispatch_job__(target)
                else:
                    # run specific jop
                    log.error(
                        f"Target {target} is not configured. Consider adding it yourself."
                    )

    def __dispatch_job__(self, target: str) -> None:
        # find all candidate files
        # process them accordingly
        # finish
        log.info(f"Dispatching job for {target}")
        reader = self.config.readers[target].get_instance()
        writer = self.config.writers[target].get_instance()
        writer.write(reader.read())

    def job_update(self):
        """update the current job's targets"""
