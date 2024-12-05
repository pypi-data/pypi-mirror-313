import json
from os import PathLike
from pathlib import Path
from typing import Iterator

from tdm import DefaultDocumentFactory, TalismanDocument
from tdm.datamodel.nodes import TextNode

from tie_datamodel.datamodel.node.text import CoreferenceChain, Mention, TIETextNode
from tp_interfaces.helpers.io import check_path_existence
from tp_interfaces.readers.abstract import AbstractReader


class RuCoCoDocumentReader(AbstractReader):
    def __init__(self, path_to_dir: PathLike):
        self._path = Path(path_to_dir)

    def read(self) -> Iterator[TalismanDocument]:
        check_path_existence(self._path)
        for path_doc in self._path.glob("*.json"):
            yield self.read_doc(path_doc)

    @staticmethod
    def read_doc(path_doc: Path) -> TalismanDocument:
        doc_id = path_doc.stem
        node_id = path_doc.stem
        with path_doc.open("r", encoding="utf-8") as f:
            doc_json = json.load(f)

        raw_text = doc_json['text']

        node = TIETextNode.wrap(TextNode(raw_text, node_id))

        chains = [CoreferenceChain([Mention(node, start, end) for start, end in chain]) for chain in doc_json['entities']]

        return DefaultDocumentFactory.create_document(id_=doc_id).with_main_root(node.with_chains(chains), update=True)
