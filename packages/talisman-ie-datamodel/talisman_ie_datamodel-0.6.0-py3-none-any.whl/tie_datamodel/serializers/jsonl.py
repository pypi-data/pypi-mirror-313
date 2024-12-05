import json
from abc import abstractmethod
from pathlib import Path
from typing import Iterable, TextIO

from tdm import TalismanDocument, TalismanDocumentModel

from tp_interfaces.helpers.io import check_path_absense
from tp_interfaces.serializers.abstract import AbstractPathSerializer, AbstractSerializer


class JSONLinesPathSerializer(AbstractPathSerializer):
    def __init__(self, serializer: 'AbstractJSONLinesSerializer'):
        self._serializer = serializer

    def serialize(self, docs: Iterable[TalismanDocument], path: Path, *, rewrite: bool = False):
        if not rewrite:
            check_path_absense(path)

        with path.open("w", encoding="utf-8") as f:
            for doc in docs:
                self._serializer.serialize(doc, f)
                f.write("\n")


class AbstractJSONLinesSerializer(AbstractSerializer):

    def serialize(self, doc: TalismanDocument, stream: TextIO):
        self._check_stream(stream)
        line = json.dumps(self._doc_to_dict(doc), sort_keys=True, ensure_ascii=False)
        stream.write(line)

    @abstractmethod
    def _doc_to_dict(self, doc: TalismanDocument) -> dict:
        pass


class TDMSerializer(AbstractJSONLinesSerializer):

    def _doc_to_dict(self, doc: TalismanDocument) -> dict:
        model: TalismanDocumentModel = TalismanDocumentModel.serialize(doc)
        return model.dict(exclude_none=True)
