from os import PathLike
from pathlib import Path
from typing import Callable

from tp_interfaces.readers.abstract import AbstractReader


class DirectoryReader(AbstractReader):
    def __init__(self, base_reader: Callable[[Path], AbstractReader], path_to_dir: PathLike):
        self._path = Path(path_to_dir)
        self._base_reader = base_reader

    def read(self):
        for file in self._path.iterdir():
            yield from self._base_reader(file).read()
