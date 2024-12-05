from typing import Iterator, List

from .abstract import AbstractCoNLLFileParser


class OntoNotesFileParser(AbstractCoNLLFileParser):
    def read_docs(self, f) -> Iterator[List[List[str]]]:
        doc_raw_tokens = []
        empty_lines = 0
        for line in f:
            spl = line.split()
            if spl:
                if empty_lines > 3 and doc_raw_tokens:
                    yield doc_raw_tokens
                    doc_raw_tokens = []
                empty_lines = 0
            else:
                empty_lines += 1
            doc_raw_tokens.append(spl)
        if doc_raw_tokens:
            yield doc_raw_tokens
