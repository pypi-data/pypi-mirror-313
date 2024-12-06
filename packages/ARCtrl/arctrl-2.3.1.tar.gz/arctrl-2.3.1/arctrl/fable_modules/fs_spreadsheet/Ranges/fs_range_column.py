from __future__ import annotations
from typing import Any
from ...fable_library.list import FSharpList
from ...fable_library.range import range_big_int
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.seq import (to_list, map)
from ...fable_library.util import IEnumerable_1
from ..Cells.fs_cell import FsCell
from ..Cells.fs_cells_collection import FsCellsCollection
from ..fs_address import (FsAddress__ctor_Z37302880, FsAddress__get_ColumnNumber, FsAddress__set_ColumnNumber_Z524259A4, FsAddress__get_RowNumber)
from .fs_range_address import (FsRangeAddress, FsRangeAddress__ctor_7E77A4A0, FsRangeAddress__get_FirstAddress, FsRangeAddress__get_LastAddress, FsRangeAddress__Copy)
from .fs_range_base import (FsRangeBase, FsRangeBase_reflection, FsRangeBase__get_RangeAddress, FsRangeBase__Cell_Z3407A44B, FsRangeBase__Cells_Z2740B3CA)

def _expr164() -> TypeInfo:
    return class_type("FsSpreadsheet.FsRangeColumn", None, FsRangeColumn, FsRangeBase_reflection())


class FsRangeColumn(FsRangeBase):
    def __init__(self, range_address: FsRangeAddress) -> None:
        super().__init__(range_address)
        pass


FsRangeColumn_reflection = _expr164

def FsRangeColumn__ctor_6A2513BC(range_address: FsRangeAddress) -> FsRangeColumn:
    return FsRangeColumn(range_address)


def FsRangeColumn__ctor_Z524259A4(index: int) -> FsRangeColumn:
    return FsRangeColumn__ctor_6A2513BC(FsRangeAddress__ctor_7E77A4A0(FsAddress__ctor_Z37302880(0, index), FsAddress__ctor_Z37302880(0, index)))


def FsRangeColumn__get_Index(self_1: FsRangeColumn) -> int:
    return FsAddress__get_ColumnNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(self_1)))


def FsRangeColumn__set_Index_Z524259A4(self_1: FsRangeColumn, i: int) -> None:
    FsAddress__set_ColumnNumber_Z524259A4(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(self_1)), i)
    FsAddress__set_ColumnNumber_Z524259A4(FsRangeAddress__get_LastAddress(FsRangeBase__get_RangeAddress(self_1)), i)


def FsRangeColumn__Cell_Z4232C216(self_1: FsRangeColumn, row_index: int, cells_collection: FsCellsCollection) -> FsCell:
    return FsRangeBase__Cell_Z3407A44B(self_1, FsAddress__ctor_Z37302880((row_index - FsAddress__get_RowNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(self_1)))) + 1, 1), cells_collection)


def FsRangeColumn__FirstCell_Z2740B3CA(self_1: FsRangeColumn, cells: FsCellsCollection) -> FsCell:
    return FsRangeBase__Cell_Z3407A44B(self_1, FsAddress__ctor_Z37302880(1, 1), cells)


def FsRangeColumn__Cells_Z2740B3CA(self_1: FsRangeColumn, cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
    return FsRangeBase__Cells_Z2740B3CA(self_1, cells_collection)


def FsRangeColumn_fromRangeAddress_6A2513BC(range_address: FsRangeAddress) -> FsRangeColumn:
    return FsRangeColumn__ctor_6A2513BC(range_address)


def FsRangeColumn__Copy(self_1: FsRangeColumn) -> FsRangeColumn:
    return FsRangeColumn__ctor_6A2513BC(FsRangeAddress__Copy(FsRangeBase__get_RangeAddress(self_1)))


def FsRangeColumn_copy_Z7F7BA1C4(range_column: FsRangeColumn) -> FsRangeColumn:
    return FsRangeColumn__Copy(range_column)


def FsSpreadsheet_FsRangeAddress__FsRangeAddress_toRangeColumns_Static_6A2513BC(range_address: FsRangeAddress) -> IEnumerable_1[FsRangeColumn]:
    columns: FSharpList[int] = to_list(range_big_int(FsAddress__get_ColumnNumber(FsRangeAddress__get_FirstAddress(range_address)), 1, FsAddress__get_ColumnNumber(FsRangeAddress__get_LastAddress(range_address))))
    fst_row: int = FsAddress__get_RowNumber(FsRangeAddress__get_FirstAddress(range_address)) or 0
    lst_row: int = FsAddress__get_RowNumber(FsRangeAddress__get_LastAddress(range_address)) or 0
    def mapping(c: int, range_address: Any=range_address) -> FsRangeColumn:
        return FsRangeColumn__ctor_6A2513BC(FsRangeAddress__ctor_7E77A4A0(FsAddress__ctor_Z37302880(fst_row, c), FsAddress__ctor_Z37302880(lst_row, c)))

    return map(mapping, columns)


__all__ = ["FsRangeColumn_reflection", "FsRangeColumn__ctor_Z524259A4", "FsRangeColumn__get_Index", "FsRangeColumn__set_Index_Z524259A4", "FsRangeColumn__Cell_Z4232C216", "FsRangeColumn__FirstCell_Z2740B3CA", "FsRangeColumn__Cells_Z2740B3CA", "FsRangeColumn_fromRangeAddress_6A2513BC", "FsRangeColumn__Copy", "FsRangeColumn_copy_Z7F7BA1C4", "FsSpreadsheet_FsRangeAddress__FsRangeAddress_toRangeColumns_Static_6A2513BC"]

