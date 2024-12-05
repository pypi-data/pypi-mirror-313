from os import PathLike
from pathlib import Path

from tdm import DefaultDocumentFactory, TalismanDocument
from tdm.abstract.datamodel import FactStatus
from tdm.datamodel.mentions import TextNodeMention
from tdm.datamodel.nodes import TextNode
from tdm.datamodel.values import StringValue

from tp_interfaces.domain.model.types import AtomValueType
from tp_interfaces.helpers.datamodel.fact import mentioned_fact_factory
from .abstract import AbstractJSONLinesReader


class DoccanoReader(AbstractJSONLinesReader):

    def __init__(self, filepath: PathLike):
        super().__init__(Path(filepath))

    def _convert_to_doc(self, json_dict: dict) -> TalismanDocument:
        node_id = json_dict['id']
        node = TextNode(json_dict['text'], node_id)
        facts = []
        for s, e, l in json_dict['labels']:
            facts.extend(mentioned_fact_factory(AtomValueType(l, StringValue, id=l))(TextNodeMention(node, s, e), FactStatus.APPROVED))
        return DefaultDocumentFactory.create_document(id_=node_id) \
            .with_main_root(node, update=True) \
            .with_facts(facts, update=True)
