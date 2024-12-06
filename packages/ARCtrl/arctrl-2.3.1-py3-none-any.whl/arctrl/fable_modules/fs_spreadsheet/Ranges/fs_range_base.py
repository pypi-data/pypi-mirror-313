from __future__ import annotations
from typing import Any
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.string_ import (to_fail, printf)
from ...fable_library.util import (equals, ignore, IEnumerable_1)
from ..Cells.fs_cell import FsCell
from ..Cells.fs_cells_collection import (FsCellsCollection__get_MaxRowNumber, FsCellsCollection__get_MaxColumnNumber, FsCellsCollection__TryGetCell_Z37302880, FsCellsCollection__Add_2E78CE33, FsCellsCollection, FsCellsCollection__GetCells_7E77A4A0)
from ..fs_address import (FsAddress, FsAddress__get_RowNumber, FsAddress__get_ColumnNumber, FsAddress__ctor_Z4C746FC0, FsAddress__get_FixedRow, FsAddress__get_FixedColumn)
from .fs_range_address import (FsRangeAddress, FsRangeAddress__Extend_6D30B323, FsRangeAddress__get_FirstAddress, FsRangeAddress__get_LastAddress)

def _expr145() -> TypeInfo:
    return class_type("FsSpreadsheet.FsRangeBase", None, FsRangeBase)


class FsRangeBase:
    def __init__(self, range_address: FsRangeAddress) -> None:
        self._sortRows: Any = None
        self._sortColumns: Any = None
        self._rangeAddress: FsRangeAddress = range_address
        _id: int
        FsRangeBase.IdCounter = (FsRangeBase.IdCounter + 1) or 0
        _id = FsRangeBase.IdCounter


FsRangeBase_reflection = _expr145

def FsRangeBase__ctor_6A2513BC(range_address: FsRangeAddress) -> FsRangeBase:
    return FsRangeBase(range_address)


def FsRangeBase__cctor(__unit: None=None) -> None:
    FsRangeBase.IdCounter = 0


FsRangeBase__cctor()

def FsRangeBase__Extend_6D30B323(this: FsRangeBase, address: FsAddress) -> None:
    FsRangeAddress__Extend_6D30B323(this._rangeAddress, address)


def FsRangeBase__get_RangeAddress(this: FsRangeBase) -> FsRangeAddress:
    return this._rangeAddress


def FsRangeBase__set_RangeAddress_6A2513BC(this: FsRangeBase, range_adress: FsRangeAddress) -> None:
    if not equals(range_adress, this._rangeAddress):
        old_address: FsRangeAddress = this._rangeAddress
        this._rangeAddress = range_adress



def FsRangeBase__Cell_Z3407A44B(this: FsRangeBase, cell_address_in_range: FsAddress, cells: FsCellsCollection) -> FsCell:
    abs_row: int = ((FsAddress__get_RowNumber(cell_address_in_range) + FsAddress__get_RowNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this)))) - 1) or 0
    abs_column: int = ((FsAddress__get_ColumnNumber(cell_address_in_range) + FsAddress__get_ColumnNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this)))) - 1) or 0
    if True if (abs_row <= 0) else (abs_row > 1048576):
        arg: int = FsCellsCollection__get_MaxRowNumber(cells) or 0
        to_fail(printf("Row number must be between 1 and %i"))(arg)

    if True if (abs_column <= 0) else (abs_column > 16384):
        arg_1: int = FsCellsCollection__get_MaxColumnNumber(cells) or 0
        to_fail(printf("Column number must be between 1 and %i"))(arg_1)

    cell: FsCell | None = FsCellsCollection__TryGetCell_Z37302880(cells, abs_row, abs_column)
    if cell is None:
        absolute_address: FsAddress = FsAddress__ctor_Z4C746FC0(abs_row, abs_column, FsAddress__get_FixedRow(cell_address_in_range), FsAddress__get_FixedColumn(cell_address_in_range))
        new_cell: FsCell = FsCell.create_empty_with_adress(absolute_address)
        FsRangeBase__Extend_6D30B323(this, absolute_address)
        value: None = FsCellsCollection__Add_2E78CE33(cells, abs_row, abs_column, new_cell)
        ignore(None)
        return new_cell

    else: 
        return cell



def FsRangeBase__Cells_Z2740B3CA(this: FsRangeBase, cells: FsCellsCollection) -> IEnumerable_1[FsCell]:
    return FsCellsCollection__GetCells_7E77A4A0(cells, FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this)), FsRangeAddress__get_LastAddress(FsRangeBase__get_RangeAddress(this)))


def FsRangeBase__ColumnCount(this: FsRangeBase) -> int:
    return (FsAddress__get_ColumnNumber(FsRangeAddress__get_LastAddress(this._rangeAddress)) - FsAddress__get_ColumnNumber(FsRangeAddress__get_FirstAddress(this._rangeAddress))) + 1


def FsRangeBase__RowCount(this: FsRangeBase) -> int:
    return (FsAddress__get_RowNumber(FsRangeAddress__get_LastAddress(this._rangeAddress)) - FsAddress__get_RowNumber(FsRangeAddress__get_FirstAddress(this._rangeAddress))) + 1


__all__ = ["FsRangeBase_reflection", "FsRangeBase__Extend_6D30B323", "FsRangeBase__get_RangeAddress", "FsRangeBase__set_RangeAddress_6A2513BC", "FsRangeBase__Cell_Z3407A44B", "FsRangeBase__Cells_Z2740B3CA", "FsRangeBase__ColumnCount", "FsRangeBase__RowCount"]

