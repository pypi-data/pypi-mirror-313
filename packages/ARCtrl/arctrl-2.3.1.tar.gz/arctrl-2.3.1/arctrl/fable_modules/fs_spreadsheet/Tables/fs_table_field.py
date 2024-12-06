from __future__ import annotations
from typing import Any
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.seq import skip
from ...fable_library.string_ import (to_fail, printf)
from ...fable_library.util import (equals, IEnumerable_1)
from ..Cells.fs_cell import FsCell
from ..Cells.fs_cells_collection import FsCellsCollection
from ..fs_address import (FsAddress__ctor_Z37302880, FsAddress__get_RowNumber)
from ..Ranges.fs_range_address import (FsRangeAddress__ctor_7E77A4A0, FsRangeAddress__get_FirstAddress, FsRangeAddress__get_LastAddress)
from ..Ranges.fs_range_base import FsRangeBase__get_RangeAddress
from ..Ranges.fs_range_column import (FsRangeColumn, FsRangeColumn__ctor_6A2513BC, FsRangeColumn__FirstCell_Z2740B3CA, FsRangeColumn__Copy, FsRangeColumn__Cells_Z2740B3CA)

def _expr183() -> TypeInfo:
    return class_type("FsSpreadsheet.FsTableField", None, FsTableField)


class FsTableField:
    def __init__(self, name: str, index: int, column: FsRangeColumn, totals_row_label: Any=None, totals_row_function: Any=None) -> None:
        self._totalsRowsFunction: Any = totals_row_function
        self._totalsRowLabel: Any = totals_row_label
        self._column: FsRangeColumn = column
        self._index: int = index or 0
        self._name: str = name
        self._Column: FsRangeColumn = self._column


FsTableField_reflection = _expr183

def FsTableField__ctor_726EFFB(name: str, index: int, column: FsRangeColumn, totals_row_label: Any=None, totals_row_function: Any=None) -> FsTableField:
    return FsTableField(name, index, column, totals_row_label, totals_row_function)


def FsTableField__ctor(__unit: None=None) -> FsTableField:
    return FsTableField__ctor_726EFFB("", 0, None, None, None)


def FsTableField__ctor_Z721C83C5(name: str) -> FsTableField:
    return FsTableField__ctor_726EFFB(name, 0, None, None, None)


def FsTableField__ctor_Z18115A39(name: str, index: int) -> FsTableField:
    return FsTableField__ctor_726EFFB(name, index, None, None, None)


def FsTableField__ctor_6547009B(name: str, index: int, column: FsRangeColumn) -> FsTableField:
    return FsTableField__ctor_726EFFB(name, index, column, None, None)


def FsTableField__get_Column(__: FsTableField) -> FsRangeColumn:
    return __._Column


def FsTableField__set_Column_Z7F7BA1C4(__: FsTableField, v: FsRangeColumn) -> None:
    __._Column = v


def FsTableField__get_Index(this: FsTableField) -> int:
    return this._index


def FsTableField__set_Index_Z524259A4(this: FsTableField, index: int) -> None:
    if index == this._index:
        pass

    else: 
        this._index = index or 0
        if equals(this._column, None):
            pass

        else: 
            ind_diff: int = (index - this._index) or 0
            FsTableField__set_Column_Z7F7BA1C4(this, FsRangeColumn__ctor_6A2513BC(FsRangeAddress__ctor_7E77A4A0(FsAddress__ctor_Z37302880(FsAddress__get_RowNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(FsTableField__get_Column(this)))), this._index + ind_diff), FsAddress__ctor_Z37302880(FsAddress__get_RowNumber(FsRangeAddress__get_LastAddress(FsRangeBase__get_RangeAddress(FsTableField__get_Column(this)))), this._index + ind_diff))))




def FsTableField__get_Name(this: FsTableField) -> str:
    return this._name


def FsTableField__SetName_103577A7(this: FsTableField, name: str, cells_collection: FsCellsCollection, show_header_row: bool) -> None:
    this._name = name
    if show_header_row:
        FsRangeColumn__FirstCell_Z2740B3CA(FsTableField__get_Column(this), cells_collection).SetValueAs(name)



def FsTableField_setName(name: str, cells_collection: FsCellsCollection, show_header_row: bool, table_field: FsTableField) -> FsTableField:
    FsTableField__SetName_103577A7(table_field, name, cells_collection, show_header_row)
    return table_field


def FsTableField__Copy(this: FsTableField) -> FsTableField:
    col: FsRangeColumn = FsRangeColumn__Copy(FsTableField__get_Column(this))
    ind: int = FsTableField__get_Index(this) or 0
    return FsTableField__ctor_726EFFB(FsTableField__get_Name(this), ind, col, None, None)


def FsTableField_copy_Z5343F797(table_field: FsTableField) -> FsTableField:
    return FsTableField__Copy(table_field)


def FsTableField__HeaderCell_10EBE01C(this: FsTableField, cells_collection: FsCellsCollection, show_header_row: bool) -> FsCell:
    if not show_header_row:
        arg: str = this._name
        return to_fail(printf("tried to get header cell of table field \"%s\" even though showHeaderRow is set to zero"))(arg)

    else: 
        return FsRangeColumn__FirstCell_Z2740B3CA(FsTableField__get_Column(this), cells_collection)



def FsTableField_getHeaderCell(cells_collection: FsCellsCollection, show_header_row: bool, table_field: FsTableField) -> FsCell:
    return FsTableField__HeaderCell_10EBE01C(table_field, cells_collection, show_header_row)


def FsTableField__DataCells_Z2740B3CA(this: FsTableField, cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
    return skip(1, FsRangeColumn__Cells_Z2740B3CA(FsTableField__get_Column(this), cells_collection))


def FsTableField_getDataCells(cells_collection: FsCellsCollection, table_field: FsTableField) -> IEnumerable_1[FsCell]:
    return FsTableField__DataCells_Z2740B3CA(table_field, cells_collection)


__all__ = ["FsTableField_reflection", "FsTableField__ctor", "FsTableField__ctor_Z721C83C5", "FsTableField__ctor_Z18115A39", "FsTableField__ctor_6547009B", "FsTableField__get_Column", "FsTableField__set_Column_Z7F7BA1C4", "FsTableField__get_Index", "FsTableField__set_Index_Z524259A4", "FsTableField__get_Name", "FsTableField__SetName_103577A7", "FsTableField_setName", "FsTableField__Copy", "FsTableField_copy_Z5343F797", "FsTableField__HeaderCell_10EBE01C", "FsTableField_getHeaderCell", "FsTableField__DataCells_Z2740B3CA", "FsTableField_getDataCells"]

