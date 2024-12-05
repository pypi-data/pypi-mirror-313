import logging
from os import PathLike
from pathlib import Path
from typing import Iterator

from tdm import DefaultDocumentFactory, TalismanDocument
from tdm.datamodel.nodes import TextNode

from tp_interfaces.helpers.io import check_path_existence
from tp_interfaces.readers.abstract import AbstractReader

logger = logging.getLogger(__name__)


def walk_recursively(path: Path) -> Iterator[Path]:
    return iter(sorted(p for p in path.rglob("*") if p.is_file()))


def relative_path_name_provider(file_path: Path, original_path: Path):
    return str(file_path.relative_to(original_path))


class RawTextReader(AbstractReader):
    def __init__(self, path: PathLike, name_provider=relative_path_name_provider, path_walker=walk_recursively):
        self._path = Path(path)
        self._name_provider = name_provider
        self._path_walker = path_walker

    def read(self) -> Iterator[TalismanDocument]:
        check_path_existence(self._path)
        for file_path in self._path_walker(self._path):
            if file_path.suffix != ".txt":
                logger.warning(f"skipping {file_path}, ends not with .txt")
                continue

            yield self.read_file(file_path, self._name_provider(file_path, self._path))

    @staticmethod
    def read_file(path: Path, doc_name: str) -> TalismanDocument:
        check_path_existence(path)
        with path.open("r", encoding="utf-8") as f:
            return DefaultDocumentFactory.create_document(id_=doc_name).with_nodes([TextNode(f.read(), doc_name)])
