"""read data from a tegracli group collection.

More info on tegracli [here](https://github.com/Leibniz-HBI/tegracli/).
"""
# pylint: disable=R,W0622,W0221
from pathlib import Path
from typing import Generator

import ujson
from loguru import logger as log

from ..Configuration.ReaderConfiguration import ReaderConfiguration
from ..utils import flatten
from .Reader import Reader


class TegracliReader(Reader):
    """reads a tegracli group collection

    params:
      config: NDJSONRreaderConfiguration
        The configuration file used for reading
    """

    def __init__(self, config: "TegracliReaderConfiguration") -> None:
        super().__init__(config)
        self.config = config

    def read(self) -> Generator[dict, None, None]:
        """reads multiple ndjson files and emits them line by line"""
        read_path = Path(self.config.read_path)
        with (read_path / "profiles.jsonl").open("r", encoding="utf8") as profiles:
            for profile in profiles:
                user = ujson.loads(profile)
                log.debug(f"Processing user {user.get('username') or ''}")
                try:
                    with (read_path / f"{user['id']}.jsonl").open(
                        "r", encoding="utf8"
                    ) as messages:
                        for line in messages:
                            data = ujson.loads(line)
                            data["user"] = user
                            log.trace(f"Persisting message: {data}")
                            if self.config.flatten_dicts is True:
                                yield flatten(data)
                            else:
                                yield data

                except FileNotFoundError as error:
                    log.error(f"No such file {error.filename}. Skipping.")
                    continue


class TegracliReaderConfiguration(ReaderConfiguration):
    """Read new line delimited JSON files.

    Attributes
    ----------
    flatten_dicts: bool
        wether to flatten those nested dictioniaries

    """

    yaml_tag = "!dabapush:TegracliReaderConfiguration"
    """internal tag for pyYAML
    """

    def __init__(
        self,
        name,
        id=None,
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

    def get_instance(self) -> TegracliReader:
        """Get a configured instance of TegracliReader"""
        return TegracliReader(self)
