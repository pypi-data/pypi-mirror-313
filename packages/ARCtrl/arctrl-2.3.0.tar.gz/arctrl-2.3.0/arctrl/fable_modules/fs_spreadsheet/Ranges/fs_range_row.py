from __future__ import annotations
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.util import IEnumerable_1
from ..Cells.fs_cell import FsCell
from ..Cells.fs_cells_collection import FsCellsCollection
from ..fs_address import (FsAddress__ctor_Z37302880, FsAddress__get_RowNumber, FsAddress__set_RowNumber_Z524259A4, FsAddress__get_ColumnNumber)
from .fs_range_address import (FsRangeAddress, FsRangeAddress__ctor_7E77A4A0, FsRangeAddress__get_FirstAddress, FsRangeAddress__get_LastAddress)
from .fs_range_base import (FsRangeBase, FsRangeBase_reflection, FsRangeBase__get_RangeAddress, FsRangeBase__Cell_Z3407A44B, FsRangeBase__Cells_Z2740B3CA)

def _expr147() -> TypeInfo:
    return class_type("FsSpreadsheet.FsRangeRow", None, FsRangeRow, FsRangeBase_reflection())


class FsRangeRow(FsRangeBase):
    def __init__(self, range_address: FsRangeAddress) -> None:
        super().__init__(range_address)
        pass


FsRangeRow_reflection = _expr147

def FsRangeRow__ctor_6A2513BC(range_address: FsRangeAddress) -> FsRangeRow:
    return FsRangeRow(range_address)


def FsRangeRow__ctor_Z524259A4(index: int) -> FsRangeRow:
    return FsRangeRow__ctor_6A2513BC(FsRangeAddress__ctor_7E77A4A0(FsAddress__ctor_Z37302880(index, 0), FsAddress__ctor_Z37302880(index, 0)))


def FsRangeRow__get_Index(self_1: FsRangeRow) -> int:
    return FsAddress__get_RowNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(self_1)))


def FsRangeRow__set_Index_Z524259A4(self_1: FsRangeRow, i: int) -> None:
    FsAddress__set_RowNumber_Z524259A4(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(self_1)), i)
    FsAddress__set_RowNumber_Z524259A4(FsRangeAddress__get_LastAddress(FsRangeBase__get_RangeAddress(self_1)), i)


def FsRangeRow__Cell_Z4232C216(self_1: FsRangeRow, column_index: int, cells: FsCellsCollection) -> FsCell:
    return FsRangeBase__Cell_Z3407A44B(self_1, FsAddress__ctor_Z37302880(1, (column_index - FsAddress__get_ColumnNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(self_1)))) + 1), cells)


def FsRangeRow__Cells_Z2740B3CA(self_1: FsRangeRow, cells: FsCellsCollection) -> IEnumerable_1[FsCell]:
    return FsRangeBase__Cells_Z2740B3CA(self_1, cells)


__all__ = ["FsRangeRow_reflection", "FsRangeRow__ctor_Z524259A4", "FsRangeRow__get_Index", "FsRangeRow__set_Index_Z524259A4", "FsRangeRow__Cell_Z4232C216", "FsRangeRow__Cells_Z2740B3CA"]

