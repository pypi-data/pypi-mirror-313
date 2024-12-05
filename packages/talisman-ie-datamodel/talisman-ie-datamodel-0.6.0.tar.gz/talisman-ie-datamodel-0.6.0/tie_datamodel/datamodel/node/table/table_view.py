from abc import ABCMeta
from typing import Callable, Iterable, Iterator

from tdm import TalismanDocument
from tdm.abstract.datamodel import AbstractNode
from tdm.datamodel.nodes import TableNode, TextNode
from typing_extensions import Self

from tie_datamodel.datamodel.node.table.abstract import AbstractTableView


class TableView(AbstractTableView, metaclass=ABCMeta):
    __slots__ = ("_table_node", "_document", "_table_structure", "_header_indices", "_columns_number", "_rows_number")

    def __init__(
            self,
            table_node: TableNode,
            document: TalismanDocument,
            header_indices: Iterable[int] | None = None,
            transposition: bool | None = False
    ):
        self._table_node = table_node
        self._document = document

        # Get table structure
        table_structure, cell_metadata_headers = self._get_table_structure(table_node, document)
        # Transpose table if necessary
        self._table_structure = self._transpose(table_structure) if transposition else table_structure

        # If there are no header indices in config then we take them from table itself (cell node metadata)
        self._header_indices = tuple(header_indices) if header_indices is not None else cell_metadata_headers

        self._columns_number = len(self._table_structure[0]) if self._table_structure else 0
        self._rows_number = len(self._table_structure)

    @staticmethod
    def _get_table_structure(table_node: TableNode, document: TalismanDocument) -> \
            tuple[tuple[tuple[AbstractNode | None, ...], ...], tuple[int, ...]]:
        # TODO: implement processing of different node types (now cell is atomic and represents TextNode)
        table_structure, cell_metadata_headers = [], []
        for index, row in enumerate(document.child_nodes(table_node)):
            cells = []
            for cell in document.child_nodes(row):
                if cell.metadata.header and index not in cell_metadata_headers:
                    cell_metadata_headers.append(index)
                nodes = document.child_nodes(cell)  # get all nodes in current cell
                item = None
                if nodes:
                    if isinstance(nodes[0], TextNode):
                        item = nodes[0] if nodes[0].content else None
                cells.append(item)
            table_structure.append(tuple(cells))
        return tuple(table_structure), tuple(cell_metadata_headers)

    @staticmethod
    def _transpose(table_structure: tuple[tuple[AbstractNode | None, ...], ...]) -> tuple[tuple[AbstractNode | None, ...], ...]:
        return tuple(zip(*table_structure))

    def _validate_indices(self, row: int | None = None, column: int | None = None):
        if row is not None and (row < 0 or row >= self.rows_number):
            raise ValueError(f"Row index should be in range [0, {self.rows_number})!")
        if column is not None and (column < 0 or column >= self.columns_number):
            raise ValueError(f"Column index should be in range [0, {self.columns_number})!")

    @property
    def table_node(self) -> TableNode:
        return self._table_node

    @property
    def document(self) -> TalismanDocument:
        return self._document

    @property
    def table_structure(self) -> tuple[tuple[AbstractNode | None, ...], ...]:
        return self._table_structure

    @property
    def columns_number(self) -> int:
        return self._columns_number

    @property
    def rows_number(self) -> int:
        return self._rows_number

    @property
    def header_indices(self) -> tuple[int, ...]:
        return self._header_indices

    @property
    def header(self) -> tuple[tuple[AbstractNode | None, ...], ...]:
        return tuple(self.row(idx) for idx in self.header_indices)

    def _column_iterator(self, column: int, *, include_header: bool = False, row_start: int = 0, row_end: int | None = None,
                         cell_filter: Callable[[int, int], bool] = lambda row, column: True) -> Iterator[AbstractNode | None]:
        """
        Iterates table over specified column from row_start to row_end (defaults to table size).
        Cells for which cell_filter returns False are ignored.
        """
        if row_end is None:
            row_end = self.rows_number - 1
        step = 1 if row_start < row_end else -1
        for row in range(row_start, row_end + step, step):
            if cell_filter(row, column):
                if include_header:
                    yield self.cell(row, column)
                else:
                    if row not in self.header_indices:
                        yield self.cell(row, column)

    def _row_iterator(self, row: int, *, column_start: int = 0, column_end: int | None = None,
                      cell_filter: Callable[[int, int], bool] = lambda row, column: True) -> Iterator[AbstractNode | None]:
        """
        Iterates table over specified row from column_start to column_end (defaults to table size).
        Cells on which cell_filter returns False are ignored.
        """
        if column_end is None:
            column_end = self.columns_number - 1
        step = 1 if column_start < column_end else -1
        for column in range(column_start, column_end + step, step):
            if cell_filter(row, column):
                yield self.cell(row, column)

    def column(self, column: int, *, include_header: bool = False) -> tuple[AbstractNode | None, ...]:
        return tuple(self._column_iterator(column, include_header=include_header))

    def row(self, row: int) -> tuple[AbstractNode | None, ...]:
        return tuple(self._row_iterator(row))

    def cell(self, row: int, column: int) -> AbstractNode | None:
        self._validate_indices(row, column)
        return self._table_structure[row][column]

    def with_header(self, rows: Iterable[int], transposition: bool | None = False) -> Self:
        return TableView(self.table_node, self.document, tuple(rows), transposition)
