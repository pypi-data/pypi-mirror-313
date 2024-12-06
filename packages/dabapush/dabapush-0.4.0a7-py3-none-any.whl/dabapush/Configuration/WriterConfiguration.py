from .PlugInConfiguration import PlugInConfiguration


class WriterConfiguration(PlugInConfiguration):
    """ """

    yaml_tag = "!dabapush:WriterConfiguration"

    def __init__(self, name, id=None, chunk_size: int = 2000) -> None:
        super().__init__(name, id=id)

        self.chunk_size = chunk_size
