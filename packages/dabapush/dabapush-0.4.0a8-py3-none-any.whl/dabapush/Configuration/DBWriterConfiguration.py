from .WriterConfiguration import WriterConfiguration


class DBWriterConfiguration(WriterConfiguration):
    def __init__(
        self,
        name,
        id=None,
        chunk_size: int = 2000,
        user: str = "postgres",
        password: str = "password",
        dbname: str = "public",
        host: str = "localhost",
        port: int = 5432,
    ) -> None:
        super().__init__(name, id, chunk_size)

        self.dbuser = user
        self.dbpass = password
        self.dbname = dbname
        self.hostname = host
        self.port = port
