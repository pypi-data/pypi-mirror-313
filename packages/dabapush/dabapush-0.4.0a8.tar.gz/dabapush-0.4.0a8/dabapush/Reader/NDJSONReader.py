"""NDJSON Writer plug-in for dabapush"""

# pylint: disable=R,I1101
from typing import Iterator, List

import ujson

from ..Configuration.ReaderConfiguration import ReaderConfiguration
from ..Record import Record
from ..utils import flatten
from .Reader import FileReader


def read_and_split(
    record: Record,
    flatten_records: bool = False,
) -> List[Record]:
    """Reads a file and splits it into records by line."""
    with record.payload.open("rt", encoding="utf8") as file:
        children = [
            Record(
                uuid=f"{str(record.uuid)}:{str(line_number)}",
                payload=(
                    ujson.loads(line)
                    if not flatten_records
                    else flatten(ujson.loads(line))
                ),
                source=record,
            )
            for line_number, line in enumerate(file)
        ]
        record.children.extend(children)

    return children


class NDJSONReader(FileReader):
    """Reader to read ready to read NDJSON data.
    It matches files in the path-tree against the pattern and reads all
    files and all lines in these files as JSON.

    Attributes
    ----------
    config: NDJSONRreaderConfiguration
        The configuration file used for reading
    """

    def __init__(self, config: "NDJSONReaderConfiguration") -> None:
        super().__init__(config)
        self.config = config

    def read(self) -> Iterator[Record]:
        """reads multiple NDJSON files and emits them line by line"""

        for file_record in self.records:
            filtered_records = filter(
                lambda x: x not in self.back_log,
                file_record.split(
                    func=read_and_split, flatten_records=self.config.flatten_dicts
                ),
            )
            yield from filtered_records


class NDJSONReaderConfiguration(ReaderConfiguration):
    """Read new line delimited JSON files.

    Attributes
    ----------
    flatten_dicts: bool
        whether to flatten those nested dicts

    """

    yaml_tag = "!dabapush:NDJSONReaderConfiguration"
    """internal tag for pyYAML
    """

    def __init__(
        self,
        name,
        id=None,  # pylint: disable=W0622
        read_path: str = ".",
        pattern: str = "*.ndjson",
        flatten_dicts=True,
    ) -> None:
        """
        Parameters
        ----------
        name: str
            target pipeline name
        id : UUID
            ID of the instance (default value = None, is set by super class)
        read_path: str
            path to directory to read
        pattern: str
            filename pattern to match files in `read_path` against
        flatten_dicts: bool
            whether nested dictionaries are flattend (for details see `dabapush.utils.flatten`)

        """
        super().__init__(name, id=id, read_path=read_path, pattern=pattern)
        self.flatten_dicts = flatten_dicts

    def get_instance(self) -> NDJSONReader:  # pylint: disable=W0221
        """Get a configured instance of NDJSONReader

        Returns
        -------
        type: NDJSONReader
            Configured instance of NDJSONReader
        """
        return NDJSONReader(self)
