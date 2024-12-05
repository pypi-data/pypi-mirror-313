from .brat import BratReader
from .conll import CoNLLFileParser, CoNLLReader, OntoNotesFileParser
from .directory import DirectoryReader
from .docred import DocREDReader
from .jsonl import DoccanoReader, TDMReader
from .jsonl.wlcoref import WlcorefJSONLinesReader
from .raw import RawTextReader
from .rucoco import RuCoCoDocumentReader
from .rueval import RuevalReader
from .tacred import TACREDDocumentReader

readers = {
    'docred': DocREDReader,
    'doccano': DoccanoReader,
    'plain': RawTextReader,
    'conll': lambda path: CoNLLReader(path, CoNLLFileParser.conll_parser()),
    'bionlp': lambda path: CoNLLReader(path, CoNLLFileParser.bionlp_parser()),
    'ontonotes': lambda path: CoNLLReader(path, OntoNotesFileParser()),
    'tacred': TACREDDocumentReader,
    'default': TDMReader,
    'tdm-directory': lambda path: DirectoryReader(lambda x: TDMReader(x), path),
    'brat': BratReader,
    'wlcoref': WlcorefJSONLinesReader,
    'rueval': RuevalReader,
    'rucoco': RuCoCoDocumentReader
}

configurable_readers = {
    'default': TDMReader.from_config,
    'wlcoref': WlcorefJSONLinesReader.from_config,
    'docred': DocREDReader.from_config
}
