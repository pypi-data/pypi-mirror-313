"""ProjectConfiguration hold all information regarding jobs for a single project."""

# pylint: disable=W0622
from typing import Dict, List, Optional

import yaml
from loguru import logger as log

from dabapush.Configuration.ReaderConfiguration import ReaderConfiguration
from dabapush.Configuration.Registry import get_reader, get_writer
from dabapush.Configuration.WriterConfiguration import WriterConfiguration


class ProjectConfiguration(yaml.YAMLObject):
    """ProjectConfiguration holds necessary configuration information

    A ProjectConfiguration is for reading and writing data as well as the project's meta data
    e.g. author name(s) and email addresses.

    Parameters
    ----------

    Returns
    -------

    """

    yaml_tag = "!dabapush:ProjectConfiguration"

    def __init__(
        self,
        readers: Optional[Dict[str, ReaderConfiguration]] = None,
        writers: Optional[Dict[str, WriterConfiguration]] = None,
        author: str = "",
        name: str = "",
    ) -> None:
        """Initialize a ProjectConfiguration with optional reader and/or writer dicts"""
        super().__init__()

        # store readers if they are passed into the constructor or else initialize
        # new list via default arg
        self.readers: Dict[str, ReaderConfiguration] = readers or {}
        # store writers if they are passed into the constructor or else initialize
        # new list via default arg
        self.writers: Dict[str, WriterConfiguration] = writers or {}

        # initialize project metadata
        self.author = author
        self.name = name

    def add_reader(self, kind: str, name: str) -> None:
        """add a reader configuration to the project

        Parameters
        ----------
        kind :
            str: registry of the configuration to add
        name :
            str: name of the configuration to add
            Returns: Nothing.

        Returns
        -------

        Raises
        ------
        ConfigurationError
            if no local or global configurations are found

        """
        # get constructor from registry
        configuration_constructor = get_reader(kind)
        if configuration_constructor is not None:
            self.readers[name] = configuration_constructor(name)
            log.debug(f'Currently configured readers: {",".join(list(self.readers))}')
        else:
            raise ValueError(f"{kind} not found")

    def remove_reader(self, name: str) -> None:
        """Remove a reader from the configuration.

        Parameters
        ----------
        name :
            str: name of the reader to be removed
        """
        if name in self.readers:
            self.readers.pop(name)

    def list_readers(self) -> List[ReaderConfiguration]:
        """List all configured readers

        Returns: List[Dict]: list of dicts with name- and id-fields

        Parameters
        ----------

        Returns
        -------

        """
        # copy stuff
        return list(self.readers.values())

    def add_writer(self, kind: str, name: str) -> None:
        """Adds a writer to the configuration.

        Parameters
        ----------
        type :
            str: type of the writer to add
        name :
            str: name of the added writer
        """
        # get constructor from registry
        configuration_constructor = get_writer(kind)
        if configuration_constructor is not None:
            self.writers[name] = configuration_constructor(name)
        else:
            raise ValueError(f"{kind} not found")

    def remove_writer(self, name: str):
        """Removes the specified writer from the configuration.

        Parameters
        ----------
        name :
            str:
        """
        if name in self.writers:
            self.writers.pop(name)

    def list_writers(self):
        """list all configured writers."""
        # copy stuff
        return list(self.writers.values())

    def set_name(self, name):
        """Sets the project's name."""
        self.name = name

    def set_author(self, author):
        """Sets the project's authors."""
        self.author = author
