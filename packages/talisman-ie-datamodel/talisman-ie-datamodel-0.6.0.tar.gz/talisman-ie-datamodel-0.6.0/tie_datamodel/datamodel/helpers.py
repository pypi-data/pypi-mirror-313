from tdm import TalismanDocument
from tdm.utils.node import dfs

from tie_datamodel.datamodel.node.text import Sentence, TIETextNode
from tie_datamodel.datamodel.span import Span

_SEPARATOR = "\n"


def document_nodes_data_merge(document: TalismanDocument) -> tuple[tuple[TIETextNode, ...], str, tuple[Span, ...], tuple[Sentence, ...]]:
    text_nodes: tuple[TIETextNode, ...] = tuple(dfs(document, document.main_root, TIETextNode))
    texts = []
    concat_tokens: list[Span] = []
    concat_sentences: list[Sentence] = []
    pointer = 0
    for node in text_nodes:
        node: TIETextNode
        texts.append(node.content)
        for sentence in node.sentences:
            sentence = sentence.shift(pointer)
            concat_sentences.append(sentence)
            concat_tokens.extend(sentence)
        pointer += len(texts[-1]) + len(_SEPARATOR)
    return text_nodes, _SEPARATOR.join(texts), tuple(concat_tokens), tuple(concat_sentences)
