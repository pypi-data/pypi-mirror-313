"""This module contains the STDOUTWriter and STDOUTWriterConfiguration classes."""

from ..Configuration.WriterConfiguration import WriterConfiguration
from .Writer import Writer


class STDOUTWriter(Writer):
    """STDOUTWriter writes to stdout."""

    def __init__(self, config: "STDOUTWriterConfiguration"):
        super().__init__(config)

    def persist(self):
        last_rows = self.buffer
        for row in last_rows:
            print(row)


class STDOUTWriterConfiguration(WriterConfiguration):
    """STDOUTWriterConfiguration is the configuration for STDOUTWriter."""

    yaml_tag = "!dabapush:STDOUTWriterConfiguration"

    def get_instance(self):  # pylint: disable=W0221
        """Returns a STDOUTWriter instance."""
        return STDOUTWriter(self)
