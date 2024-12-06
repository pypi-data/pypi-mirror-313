"""Writer base class for writing records to a destination.

The Writer class is an abstract base class for writing records to a destination.
It provides a write method to consume a queue of records and a persist method to
write the records to the destination.
"""

import abc
from typing import Iterator, List

from loguru import logger as log

from ..Configuration.WriterConfiguration import WriterConfiguration
from ..Record import Record


class Writer:
    """Abstract base class for all writer plugins."""

    def __init__(self, config: WriterConfiguration):
        """Initializes the Writer with the given configuration.

        Args:
           config (WriterConfiguration): The configuration for the writer.
        """
        super().__init__()

        self.config = config
        self.buffer: List[Record] = []

    def __del__(self):
        """Ensures the buffer is flushed before the object is destroyed."""
        self.persist()

    def write(self, queue: Iterator[Record]) -> None:
        """Consumes items from the provided queue.

        Args:
            queue (Iterator[Record]): Items to be consumed.
        """
        for item in queue:
            self.buffer.append(item)
            if len(self.buffer) >= self.config.chunk_size:
                self.persist()
                log.debug(
                    f"Persisted {self.config.chunk_size} records. Setting to done."
                )
                for record in self.buffer:
                    log.debug(f"Setting record {record.uuid} as done.")
                    record.done()
                self.buffer = []

    @abc.abstractmethod
    def persist(self) -> None:
        """Abstract method to persist the records to the destination."""

    @property
    def name(self):
        """Gets the name of the writer.

        Returns:
            str: The name of the writer.
        """
        return self.config.name

    @property
    def id(self):
        """Gets the ID of the writer.

        Returns:
            str: The ID of the writer.
        """
        return self.config.id
