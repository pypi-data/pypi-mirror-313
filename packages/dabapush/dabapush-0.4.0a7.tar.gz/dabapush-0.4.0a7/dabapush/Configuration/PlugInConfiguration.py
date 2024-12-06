"""PlugInConfiguration module.
"""

import abc
from uuid import uuid4

import yaml

# pylint: disable=W0622


class PlugInConfiguration(yaml.YAMLObject):
    """Abstract Base class for all PlugInConfigurations."""

    yaml_tag = "!dabapush:PluginConfiguration"

    def __init__(self, name: str, id: str or None) -> None:
        super().__init__()

        self.name = name
        self.id = id if id is not None else str(uuid4())

    @abc.abstractmethod
    def get_instance(self) -> object or None:
        """Get a configured instance of the appropriate reader or writer plugin."""
