"""A writer that persists records in NDJSON format."""

from pathlib import Path

import ujson
from loguru import logger as log

from ..Configuration.FileWriterConfiguration import FileWriterConfiguration
from .Writer import Writer

# pylint: disable=R0913,R0917


class NDJSONWriter(Writer):
    """A writer that persists records in NDJSON format."""

    def __init__(self, config: "NDJSONWriterConfiguration"):
        super().__init__(config=config)
        self.config = config

    def persist(self):
        """Persist the buffer to the file and flush."""

        last_rows = self.buffer
        self.buffer = []

        _file: Path = Path(self.config.path) / self.config.make_file_name()

        with _file.open("a", encoding="utf8") as file:
            for row in last_rows:
                ujson.dump(  # pylint: disable=I1101
                    row.payload, file, ensure_ascii=False
                )
                file.write("\n")
        log.info(f"Persisted {len(last_rows)} records")

        return len(last_rows)


class NDJSONWriterConfiguration(FileWriterConfiguration):
    """Configuration for the NDJSONWriter."""

    yaml_tag = "!dabapush:NDJSONWriterConfiguration"

    def __init__(
        self,
        name,
        id=None,  # pylint: disable=W0622
        chunk_size: int = 2000,
        path: str = ".",
        name_template: str = "${date}_${time}_${name}.${type}",
    ) -> None:
        super().__init__(name, id, chunk_size, path, name_template)
        self.type = "ndjson"

    def get_instance(self):  # pylint: disable=W0221
        """Get a configured instance of NDJSONWriter"""
        return NDJSONWriter(self)
