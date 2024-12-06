"""This module contains the abstract base class for all reader plugins."""

import abc
from pathlib import Path
from typing import Iterator

import ujson
from loguru import logger as log
from tqdm.auto import tqdm

from ..Configuration.ReaderConfiguration import ReaderConfiguration
from ..Record import Record

# pylint: disable=I1101


class Reader(abc.ABC):
    """Abstract base class for all reader plugins.

    **BEWARE**: readers and writers are never to be instanced directly by the user but rather will
    be obtained by calling `get_instance()` on their specific Configuration-counterparts.

    Args:
        config (ReaderConfiguration): The configuration for the reader.
    """

    def __init__(self, config: ReaderConfiguration):
        """
        Parameters
        ----------
        config : ReaderConfiguration
            Configuration file for the reader. In concrete classes it will
            be a subclass of ReaderConfiguration.
        """
        self.config = config
        self.back_log = []
        # initialize file log
        if not Path(".dabapush/").exists():
            Path(".dabapush/").mkdir()

        self.log_path = Path(f".dabapush/{config.name}.jsonl")

    @abc.abstractmethod
    def read(self) -> Iterator[Record]:
        """Subclasses **must** implement this abstract method and implement
        their reading logic here.

        Returns
        -------
        type: Iterator[Record]
            Generator which _should_ be one item per element.
        """

    @property
    @abc.abstractmethod
    def records(self) -> Iterator[Record]:
        """Subclasses **must** implement this abstract method and implement
        their reading logic here.

        Returns
        -------
        type: Iterator[Record]
            Generator which _should_ be one item per element.
        """


class FileReader(Reader):
    """Reader to read files from a path.

    It matches files in the path-tree against the pattern.
    """

    @abc.abstractmethod
    def read(self) -> Iterator[Record]:
        """Reads all files matching the pattern in the read_path."""

    @property
    def records(self) -> Iterator[Record]:
        """Generator for all files matching the pattern in the read_path."""
        if self.log_path.exists():
            log.debug(
                f"Found log file for {self.config.name} at {self.log_path}. Loading..."
            )
            with self.log_path.open("rt", encoding="utf8") as f:
                self.back_log = [Record(**ujson.loads(_)) for _ in f.readlines()]
        else:
            self.log_path.touch()

        yield from (
            Record(
                uuid=str(a),
                payload=a,
                event_handlers={"on_done": [self.log]},
            )
            for a in tqdm(list(Path(self.config.read_path).rglob(self.config.pattern)))
        )

    def log(self, record: Record):
        """Log the record to the persistent record log file."""
        with self.log_path.open("a", encoding="utf8") as f:
            for sub_record in record.walk_tree(only_leafs=True):
                ujson.dump(sub_record.to_log(), f)
                f.write("\n")
                log.debug(f"Done with {record.uuid}")
