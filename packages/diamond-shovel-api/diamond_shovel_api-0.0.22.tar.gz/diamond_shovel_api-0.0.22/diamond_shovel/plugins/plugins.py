import configparser
import io
import pathlib
from contextlib import contextmanager
from typing import Generator


plugins: dict[str, dict]

class PluginInitContext:
    @property
    def config(self) -> configparser.ConfigParser:
        ...

    @property
    def data_folder(self) -> pathlib.Path:
        ...

    @contextmanager
    def open_resource(self, name: str) -> Generator[io.IOBase, None, None]:
        ...

    def extract_resource(self, name: str, replace: bool = False) -> None:
        ...
