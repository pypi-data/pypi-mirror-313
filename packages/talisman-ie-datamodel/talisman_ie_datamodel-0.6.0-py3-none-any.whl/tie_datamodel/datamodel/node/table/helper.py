from collections import defaultdict
from typing import Iterable

from tdm.abstract.datamodel import AbstractFact, AbstractNode, AbstractNodeMention, FactStatus
from tdm.datamodel.facts import AtomValueFact, ConceptFact, MentionFact, PropertyFact, RelationFact
from tdm.datamodel.mentions import TextNodeMention
from tdm.datamodel.nodes import TableCellNode, TableCellNodeMetadata, TableNode, TableRowNode, TextNode


def generate_concept_facts(
        cpt_type: str,
        props: dict[str, tuple[str, TextNode | AbstractNodeMention]],
        relations: dict[str, Iterable[AbstractFact]] = None
) -> Iterable[AbstractFact]:
    if relations is None:
        relations = {}
    result = []
    cpt = ConceptFact(FactStatus.NEW, cpt_type)
    result.append(cpt)
    for prop_type, (value_type, value_mention) in props.items():
        value, mention = generate_value_facts(value_type, value_mention)
        result.extend([value, mention, PropertyFact(FactStatus.NEW, prop_type, cpt, value)])
    for rel_type, (target, *other) in relations.items():
        result.append(target)
        result.append(RelationFact(FactStatus.NEW, rel_type, cpt, target))
        result.extend(other)
    return result


def generate_value_facts(value_type: str, mention: TextNode | AbstractNodeMention) -> tuple[AtomValueFact, MentionFact]:
    if isinstance(mention, TextNode):
        mention = TextNodeMention(mention, 0, len(mention.content))
    value = AtomValueFact(FactStatus.NEW, value_type)
    mention = MentionFact(FactStatus.NEW, mention, value)
    return value, mention


def generate_table_nodes(
        table: Iterable[Iterable[str]]
) -> tuple[TableNode, dict[AbstractNode, Iterable[AbstractNode]], tuple[tuple[TextNode, ...], ...]]:
    root: TableNode = TableNode()
    structure: dict[AbstractNode, list[AbstractNode]] = defaultdict(list)
    cells: list[list[TextNode]] = []

    for i, row in enumerate(table):
        row_node = TableRowNode()
        structure[root].append(row_node)
        row_nodes = []
        for cell in row:
            cell_node = TableCellNode(metadata=TableCellNodeMetadata(header=(i == 0)))
            structure[row_node].append(cell_node)
            text_node = TextNode(cell)
            structure[cell_node].append(text_node)
            row_nodes.append(text_node)
        if i != 0:
            cells.append(row_nodes)

    return root, structure, tuple(tuple(row) for row in cells)
