from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_library.reflection import (TypeInfo, class_type)
from ..fable_library.seq import (length, min_by, max_by, map, exists)
from ..fable_library.util import (IEnumerable_1, compare_primitives, ignore, get_enumerator, IEnumerator, to_iterator)
from .Cells.fs_cell import FsCell
from .Cells.fs_cells_collection import (FsCellsCollection__ctor, FsCellsCollection__GetCellsInRow_Z524259A4, FsCellsCollection, FsCellsCollection__Add_Z21F271A4, FsCellsCollection__Add_2E78CE33)
from .fs_address import (FsAddress__ctor_Z37302880, FsAddress__get_ColumnNumber, FsAddress__get_RowNumber, FsAddress__set_RowNumber_Z524259A4)
from .Ranges.fs_range_address import (FsRangeAddress__ctor_7E77A4A0, FsRangeAddress__get_FirstAddress, FsRangeAddress__get_LastAddress, FsRangeAddress__Copy, FsRangeAddress)
from .Ranges.fs_range_base import (FsRangeBase__Cells_Z2740B3CA, FsRangeBase__get_RangeAddress, FsRangeBase__Cell_Z3407A44B, FsRangeBase, FsRangeBase_reflection)

def _expr173() -> TypeInfo:
    return class_type("FsSpreadsheet.FsRow", None, FsRow, FsRangeBase_reflection())


class FsRow(FsRangeBase):
    def __init__(self, range_address: FsRangeAddress, cells: FsCellsCollection) -> None:
        super().__init__(range_address)
        self.cells_004021: FsCellsCollection = cells

    @staticmethod
    def empty(__unit: None=None) -> FsRow:
        return FsRow(FsRangeAddress__ctor_7E77A4A0(FsAddress__ctor_Z37302880(0, 0), FsAddress__ctor_Z37302880(0, 0)), FsCellsCollection__ctor())

    @staticmethod
    def create_at(index: int, cells: FsCellsCollection) -> FsRow:
        def get_index_by(f: Callable[[Callable[[FsCell], int], IEnumerable_1[FsCell]], FsCell]) -> int:
            if length(FsCellsCollection__GetCellsInRow_Z524259A4(cells, index)) == 0:
                return 1

            else: 
                def _arrow166(c: FsCell, f: Any=f) -> int:
                    return FsAddress__get_ColumnNumber(c.Address)

                return FsAddress__get_ColumnNumber(f(_arrow166)(FsCellsCollection__GetCellsInRow_Z524259A4(cells, index)).Address)


        def _arrow169(projection: Callable[[FsCell], int]) -> Callable[[IEnumerable_1[FsCell]], FsCell]:
            def _arrow168(source_1: IEnumerable_1[FsCell]) -> FsCell:
                class ObjectExpr167:
                    @property
                    def Compare(self) -> Callable[[int, int], int]:
                        return compare_primitives

                return min_by(projection, source_1, ObjectExpr167())

            return _arrow168

        min_col_index: int = get_index_by(_arrow169) or 0
        def _arrow172(projection_1: Callable[[FsCell], int]) -> Callable[[IEnumerable_1[FsCell]], FsCell]:
            def _arrow171(source_2: IEnumerable_1[FsCell]) -> FsCell:
                class ObjectExpr170:
                    @property
                    def Compare(self) -> Callable[[int, int], int]:
                        return compare_primitives

                return max_by(projection_1, source_2, ObjectExpr170())

            return _arrow171

        max_col_index: int = get_index_by(_arrow172) or 0
        return FsRow(FsRangeAddress__ctor_7E77A4A0(FsAddress__ctor_Z37302880(index, min_col_index), FsAddress__ctor_Z37302880(index, max_col_index)), cells)

    @property
    def Cells(self, __unit: None=None) -> IEnumerable_1[FsCell]:
        this: FsRow = self
        return FsRangeBase__Cells_Z2740B3CA(this, this.cells_004021)

    @property
    def Index(self, __unit: None=None) -> int:
        this: FsRow = self
        return FsAddress__get_RowNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this)))

    @Index.setter
    def Index(self, i: int) -> None:
        this: FsRow = self
        FsAddress__set_RowNumber_Z524259A4(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this)), i)
        FsAddress__set_RowNumber_Z524259A4(FsRangeAddress__get_LastAddress(FsRangeBase__get_RangeAddress(this)), i)

    @property
    def MinColIndex(self, __unit: None=None) -> int:
        this: FsRow = self
        return FsAddress__get_ColumnNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this)))

    @property
    def MaxColIndex(self, __unit: None=None) -> int:
        this: FsRow = self
        return FsAddress__get_ColumnNumber(FsRangeAddress__get_LastAddress(FsRangeBase__get_RangeAddress(this)))

    def Copy(self, __unit: None=None) -> FsRow:
        this: FsRow = self
        ra: FsRangeAddress = FsRangeAddress__Copy(FsRangeBase__get_RangeAddress(this))
        def mapping(c: FsCell) -> FsCell:
            return c.Copy()

        cells: IEnumerable_1[FsCell] = map(mapping, this.Cells)
        fcc: FsCellsCollection = FsCellsCollection__ctor()
        FsCellsCollection__Add_Z21F271A4(fcc, cells)
        return FsRow(ra, fcc)

    @staticmethod
    def copy(row: FsRow) -> FsRow:
        return row.Copy()

    @staticmethod
    def get_index(row: FsRow) -> int:
        return row.Index

    def HasCellAt(self, col_index: int) -> bool:
        this: FsRow = self
        def predicate(c: FsCell) -> bool:
            return c.ColumnNumber == col_index

        return exists(predicate, this.Cells)

    @staticmethod
    def has_cell_at(col_index: int, row: FsRow) -> bool:
        return row.HasCellAt(col_index)

    def Item(self, column_index: int) -> FsCell:
        this: FsRow = self
        return FsRangeBase__Cell_Z3407A44B(this, FsAddress__ctor_Z37302880(1, column_index), this.cells_004021)

    @staticmethod
    def item(col_index: int, row: FsRow) -> FsCell:
        return row.Item(col_index)

    def TryItem(self, col_index: int) -> FsCell | None:
        this: FsRow = self
        return this.Item(col_index) if this.HasCellAt(col_index) else None

    @staticmethod
    def try_item(col_index: int, row: FsRow) -> FsCell | None:
        return row.TryItem(col_index)

    def InsertValueAt(self, col_index: int, value: Any) -> None:
        this: FsRow = self
        cell: FsCell = FsCell(value)
        FsCellsCollection__Add_2E78CE33(this.cells_004021, this.Index, col_index, cell)

    @staticmethod
    def insert_value_at(col_index: int, value: IConvertible, row: FsRow) -> FsRow:
        value_1: None = row.InsertValueAt(col_index, value)
        ignore(None)
        return row

    def ToDenseRow(self, __unit: None=None) -> None:
        this: FsRow = self
        for i in range(this.MinColIndex, this.MaxColIndex + 1, 1):
            ignore(this.Item(i))

    @staticmethod
    def to_dense_row(row: FsRow) -> FsRow:
        row.ToDenseRow()
        return row

    @staticmethod
    def create_dense_row_of(row: FsRow) -> FsRow:
        new_row: FsRow = row.Copy()
        new_row.ToDenseRow()
        return new_row

    def GetEnumerator(self, __unit: None=None) -> IEnumerator[FsCell]:
        this: FsRow = self
        return get_enumerator(this.Cells)

    def __iter__(self) -> IEnumerator[FsCell]:
        return to_iterator(self.GetEnumerator())

    def System_Collections_IEnumerable_GetEnumerator(self, __unit: None=None) -> IEnumerator[Any]:
        this: FsRow = self
        return get_enumerator(this)


FsRow_reflection = _expr173

def FsRow__ctor_7678C70A(range_address: FsRangeAddress, cells: FsCellsCollection) -> FsRow:
    return FsRow(range_address, cells)


__all__ = ["FsRow_reflection"]

