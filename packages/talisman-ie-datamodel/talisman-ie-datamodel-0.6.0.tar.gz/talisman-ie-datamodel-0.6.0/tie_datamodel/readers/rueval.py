import logging
from collections import defaultdict
from os import PathLike
from pathlib import Path
from typing import Iterator

from tdm import DefaultDocumentFactory, TalismanDocument
from tdm.datamodel.nodes import TextNode

from tie_datamodel.datamodel.node.text import CoreferenceChain, Mention, TIETextNode
from tp_interfaces.readers.abstract import AbstractReader

logger = logging.getLogger(__name__)


class RuevalReader(AbstractReader):
    """Right now this reader will read only coreference chain content from the RuEval corpus -
    more functionality to be added as necessary"""

    def __init__(self, path_to_rueval: PathLike):
        self._path = Path(path_to_rueval)
        if not self._path.is_dir():
            raise Exception("Path is not a directory; please provide a path to the directory containing RuEval")
        self.chains_dir = self._path / "Chains"
        self.texts_dir = self._path / "Texts"

    def read(self) -> Iterator[TalismanDocument]:
        for directory in self.chains_dir, self.texts_dir:
            if not directory.exists() or not directory.is_dir():
                raise Exception(f"Path {directory} does not contain a {directory.name} directory")
        for text_doc in self.texts_dir.iterdir():
            if not (self.chains_dir / text_doc.name).exists():
                logger.warning(f"Cannot find chains annotation for file {text_doc.stem}")
            yield self.read_doc(text_doc)

    def read_doc(self, text_path: Path):
        doc_id = text_path.stem
        raw_text = text_path.read_text(encoding="utf16")
        node = TIETextNode.wrap(TextNode(raw_text, doc_id))

        chains = defaultdict(list)
        for chain in (self.chains_dir / text_path.name).read_text().splitlines():
            _, start, length, chain_id = map(int, chain.split())
            chains[chain_id].append(Mention(node, start, start + length))

        return DefaultDocumentFactory.create_document(id_=doc_id) \
            .with_main_root(node.with_chains(map(CoreferenceChain, chains.values())), update=True)
