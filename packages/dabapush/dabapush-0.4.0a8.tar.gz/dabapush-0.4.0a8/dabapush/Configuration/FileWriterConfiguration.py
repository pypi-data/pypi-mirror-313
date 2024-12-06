"""FileWriterConfiguration provides a base class for file-based Writers."""

import abc
from datetime import datetime
from string import Template
from typing import Dict, Optional

from loguru import logger as log

from .WriterConfiguration import WriterConfiguration

# pylint: disable=W0221,W0622,R0917,R0913


class FileWriterConfiguration(WriterConfiguration):
    """Abstract class describing configuration items for a file based writer"""

    def __init__(
        self,
        name,
        id=None,
        chunk_size: int = 2000,
        path: str = ".",
        name_template: str = "${date}_${time}_${name}.${type}",
    ) -> None:
        super().__init__(name, id=id, chunk_size=chunk_size)

        self.path = path
        self.name_template = name_template

    def make_file_name(self, additional_keys: Optional[Dict] = None) -> str:
        """Interpolate a fitting file name.

        params:
          additional_keys :
            dict:  (Default value = {})

        returns:
          Interpolated file name as str.
        """
        now = datetime.now()
        available_data = {
            "date": datetime.strftime(now, "%Y-%m-%d"),
            "time": datetime.strftime(now, "%H%M"),
            "chunk_size": self.chunk_size,
            "name": self.name,
            "id": self.id,
            **(additional_keys or {}),
        }

        log.info(f"Available data: {available_data}")

        return Template(self.name_template).substitute(**available_data)

    def set_name_template(self, template: str):
        """Sets the template string.

        params:
          template: str
            Template string to use.
        """
        self.name_template = template

    @abc.abstractmethod
    def get_instance(self) -> object or None:
        """Get configured instance of Writer"""
