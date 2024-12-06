from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_library.map_util import (add_to_set, add_to_dict, get_item_from_dict, remove_from_dict)
from ...fable_library.option import (value as value_2, default_arg)
from ...fable_library.range import range_big_int
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.seq import (initialize, delay, collect, singleton, reduce, map, iterate_indexed, iterate, length, max, find, try_find, try_pick, choose, to_list, exists)
from ...fable_library.string_ import replace
from ...fable_library.util import (equals, IEnumerable_1, int32_to_string, ignore, compare_primitives, get_enumerator)
from ..Cells.fs_cell import (FsCell, DataType)
from ..Cells.fs_cells_collection import (FsCellsCollection, Dictionary_tryGet, FsCellsCollection__GetCellsInColumn_Z524259A4, FsCellsCollection__TryGetCell_Z37302880)
from ..fs_address import (FsAddress__get_RowNumber, FsAddress__ctor_Z37302880, FsAddress__get_ColumnNumber)
from ..fs_column import FsColumn
from ..fs_row import FsRow
from ..Ranges.fs_range import (FsRange__FirstRow, FsRange__ctor_6A2513BC)
from ..Ranges.fs_range_address import (FsRangeAddress__get_FirstAddress, FsRangeAddress__ctor_7E77A4A0, FsRangeAddress__get_LastAddress, FsRangeAddress__Union_6A2513BC, FsRangeAddress, FsRangeAddress__Copy)
from ..Ranges.fs_range_base import (FsRangeBase__get_RangeAddress, FsRangeBase__ColumnCount, FsRangeBase__set_RangeAddress_6A2513BC, FsRangeBase, FsRangeBase_reflection)
from ..Ranges.fs_range_column import (FsRangeColumn__ctor_Z524259A4, FsRangeColumn__ctor_6A2513BC, FsRangeColumn__get_Index, FsRangeColumn)
from ..Ranges.fs_range_row import FsRangeRow
from .fs_table_field import (FsTableField, FsTableField__get_Column, FsTableField__ctor_6547009B, FsTableField__get_Name, FsTableField__ctor_726EFFB, FsTableField__get_Index, FsTableField__HeaderCell_10EBE01C, FsTableField__ctor_Z18115A39, FsTableField__set_Index_Z524259A4)

def _expr192() -> TypeInfo:
    return class_type("FsSpreadsheet.FsTable", None, FsTable, FsRangeBase_reflection())


class FsTable(FsRangeBase):
    def __init__(self, name: str, range_address: FsRangeAddress, show_totals_row: bool | None=None, show_header_row: bool | None=None) -> None:
        super().__init__(range_address)
        self._name: str = replace(name.strip(), " ", "_")
        self._lastRangeAddress: FsRangeAddress = range_address
        self._showTotalsRow: bool = default_arg(show_totals_row, False)
        self._showHeaderRow: bool = default_arg(show_header_row, True)
        self._fieldNames: Any = dict([])
        self._uniqueNames: Any = set([])

    @property
    def Name(self, __unit: None=None) -> str:
        this: FsTable = self
        return this._name

    def GetFieldNames(self, cells_collection: FsCellsCollection) -> Any:
        this: FsTable = self
        if equals(this._lastRangeAddress, FsRangeBase__get_RangeAddress(this)) if ((not equals(this._lastRangeAddress, None)) if (not equals(this._fieldNames, None)) else False) else False:
            return this._fieldNames

        else: 
            this._lastRangeAddress = FsRangeBase__get_RangeAddress(this)
            return this._fieldNames


    def GetFields(self, cells_collection: FsCellsCollection) -> IEnumerable_1[FsTableField]:
        this: FsTable = self
        def _arrow184(i: int) -> FsTableField:
            return this.GetFieldAt(i, cells_collection)

        return initialize(FsRangeBase__ColumnCount(this), _arrow184)

    @property
    def ShowHeaderRow(self, __unit: None=None) -> bool:
        this: FsTable = self
        return this._showHeaderRow

    @ShowHeaderRow.setter
    def ShowHeaderRow(self, show_header_row: bool) -> None:
        this: FsTable = self
        this._showHeaderRow = show_header_row

    def HeadersRow(self, __unit: None=None) -> FsRangeRow:
        this: FsTable = self
        return None if (not this.ShowHeaderRow) else FsRange__FirstRow(FsRange__ctor_6A2513BC(FsRangeBase__get_RangeAddress(this)))

    def TryGetHeaderRow(self, cells_collection: FsCellsCollection) -> FsRow | None:
        this: FsTable = self
        match_value: bool = this.ShowHeaderRow
        if match_value:
            row_index: int = FsAddress__get_RowNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this))) or 0
            return FsRow(FsRangeAddress__ctor_7E77A4A0(FsAddress__ctor_Z37302880(row_index, FsAddress__get_ColumnNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this)))), FsAddress__ctor_Z37302880(row_index, FsAddress__get_ColumnNumber(FsRangeAddress__get_LastAddress(FsRangeBase__get_RangeAddress(this))))), cells_collection)

        else: 
            return None


    def GetHeaderRow(self, cells_collection: FsCellsCollection) -> FsRow:
        this: FsTable = self
        match_value: FsRow | None = this.TryGetHeaderRow(cells_collection)
        if match_value is None:
            raise Exception(("Error. Unable to get header row for table \"" + this.Name) + "\" as `ShowHeaderRow` is set to `false`.")

        else: 
            return match_value


    def GetColumns(self, cells_collection: FsCellsCollection) -> IEnumerable_1[FsColumn]:
        this: FsTable = self
        def _arrow186(__unit: None=None) -> IEnumerable_1[FsColumn]:
            def _arrow185(i: int) -> IEnumerable_1[FsColumn]:
                return singleton(FsColumn(FsRangeAddress__ctor_7E77A4A0(FsAddress__ctor_Z37302880(FsAddress__get_RowNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this))), i), FsAddress__ctor_Z37302880(FsAddress__get_RowNumber(FsRangeAddress__get_LastAddress(FsRangeBase__get_RangeAddress(this))), i)), cells_collection))

            return collect(_arrow185, range_big_int(FsAddress__get_ColumnNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this))), 1, FsAddress__get_ColumnNumber(FsRangeAddress__get_LastAddress(FsRangeBase__get_RangeAddress(this)))))

        return delay(_arrow186)

    def GetRows(self, cells_collection: FsCellsCollection) -> IEnumerable_1[FsRow]:
        this: FsTable = self
        def _arrow188(__unit: None=None) -> IEnumerable_1[FsRow]:
            def _arrow187(i: int) -> IEnumerable_1[FsRow]:
                return singleton(FsRow(FsRangeAddress__ctor_7E77A4A0(FsAddress__ctor_Z37302880(i, FsAddress__get_ColumnNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this)))), FsAddress__ctor_Z37302880(i, FsAddress__get_ColumnNumber(FsRangeAddress__get_LastAddress(FsRangeBase__get_RangeAddress(this))))), cells_collection))

            return collect(_arrow187, range_big_int(FsAddress__get_RowNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this))), 1, FsAddress__get_RowNumber(FsRangeAddress__get_LastAddress(FsRangeBase__get_RangeAddress(this)))))

        return delay(_arrow188)

    def RescanRange(self, __unit: None=None) -> None:
        this: FsTable = self
        def mapping(v: FsTableField) -> FsRangeAddress:
            return FsRangeBase__get_RangeAddress(FsTableField__get_Column(v))

        FsRangeBase__set_RangeAddress_6A2513BC(this, reduce(FsRangeAddress__Union_6A2513BC, map(mapping, this._fieldNames.values())))

    @staticmethod
    def rescan_range(table: FsTable) -> FsTable:
        table.RescanRange()
        return table

    def GetUniqueName(self, original_name: str, initial_offset: int, enforce_offset: bool) -> str:
        this: FsTable = self
        name: str = original_name + (int32_to_string(initial_offset) if enforce_offset else "")
        if name in this._uniqueNames:
            i: int = initial_offset or 0
            name = original_name + int32_to_string(i)
            while name in this._uniqueNames:
                i = (i + 1) or 0
                name = original_name + int32_to_string(i)

        ignore(add_to_set(name, this._uniqueNames))
        return name

    @staticmethod
    def get_unique_names(original_name: str, initial_offset: int, enforce_offset: bool, table: FsTable) -> str:
        return table.GetUniqueName(original_name, initial_offset, enforce_offset)

    def InitFields(self, field_names: IEnumerable_1[str]) -> None:
        this: FsTable = self
        def action(i: int, fn: str) -> None:
            table_field: FsTableField = FsTableField__ctor_6547009B(fn, i, FsRangeColumn__ctor_Z524259A4(i))
            add_to_dict(this._fieldNames, fn, table_field)

        iterate_indexed(action, field_names)

    @staticmethod
    def init_fields(field_names: IEnumerable_1[str], table: FsTable) -> FsTable:
        table.InitFields(field_names)
        return table

    def AddFields(self, table_fields: IEnumerable_1[FsTableField]) -> None:
        this: FsTable = self
        def action(tf: FsTableField) -> None:
            add_to_dict(this._fieldNames, FsTableField__get_Name(tf), tf)

        iterate(action, table_fields)

    @staticmethod
    def add_fields(table_fields: IEnumerable_1[FsTableField], table: FsTable) -> FsTable:
        table.AddFields(table_fields)
        return table

    def Field(self, name: str, cells_collection: FsCellsCollection) -> FsTableField:
        this: FsTable = self
        match_value: FsTableField | None = Dictionary_tryGet(name, this._fieldNames)
        if match_value is None:
            def _arrow190(__unit: None=None) -> int:
                s: IEnumerable_1[int] = map(FsTableField__get_Index, this._fieldNames.values())
                class ObjectExpr189:
                    @property
                    def Compare(self) -> Callable[[int, int], int]:
                        return compare_primitives

                return 0 if (length(s) == 0) else max(s, ObjectExpr189())

            def _arrow191(__unit: None=None) -> FsRangeAddress:
                offset: int = len(this._fieldNames) or 0
                return FsRangeAddress__ctor_7E77A4A0(FsAddress__ctor_Z37302880(FsAddress__get_RowNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this))), FsAddress__get_ColumnNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this))) + offset), FsAddress__ctor_Z37302880(FsAddress__get_RowNumber(FsRangeAddress__get_LastAddress(FsRangeBase__get_RangeAddress(this))), FsAddress__get_ColumnNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this))) + offset))

            new_field: FsTableField = FsTableField__ctor_726EFFB(name, _arrow190() + 1, FsRangeColumn__ctor_6A2513BC(_arrow191()), None, None)
            if this.ShowHeaderRow:
                value: None = FsTableField__HeaderCell_10EBE01C(new_field, cells_collection, True).SetValueAs(name)
                ignore(None)

            add_to_dict(this._fieldNames, name, new_field)
            this.RescanRange()
            return new_field

        else: 
            return match_value


    def GetField(self, name: str, cells_collection: FsCellsCollection) -> FsTableField:
        this: FsTable = self
        name_1: str = replace(name, "\r\n", "\n")
        try: 
            return get_item_from_dict(this.GetFieldNames(cells_collection), name_1)

        except Exception as match_value:
            raise Exception(("The header row doesn\'t contain field name \'" + name_1) + "\'.")


    @staticmethod
    def get_field(name: str, cells_collection: FsCellsCollection, table: FsTable) -> FsTableField:
        return table.GetField(name, cells_collection)

    def GetFieldAt(self, index: int, cells_collection: FsCellsCollection) -> FsTableField:
        this: FsTable = self
        try: 
            def predicate(ftf: FsTableField) -> bool:
                return FsTableField__get_Index(ftf) == index

            return find(predicate, this.GetFieldNames(cells_collection).values())

        except Exception as match_value:
            raise Exception(("FsTableField with index " + str(index)) + " does not exist in the FsTable.")


    def GetFieldIndex(self, name: str, cells_collection: FsCellsCollection) -> int:
        this: FsTable = self
        return FsTableField__get_Index(this.GetField(name, cells_collection))

    def RenameField(self, old_name: str, new_name: str) -> None:
        this: FsTable = self
        match_value: FsTableField | None = Dictionary_tryGet(old_name, this._fieldNames)
        if match_value is None:
            raise Exception("The FsTabelField does not exist in this FsTable", "oldName")

        else: 
            field: FsTableField = match_value
            ignore(remove_from_dict(this._fieldNames, old_name))
            add_to_dict(this._fieldNames, new_name, field)


    @staticmethod
    def rename_field(old_name: str, new_name: str, table: FsTable) -> FsTable:
        table.RenameField(old_name, new_name)
        return table

    def TryGetHeaderCellOfColumnAt(self, cells_collection: FsCellsCollection, col_index: int) -> FsCell | None:
        this: FsTable = self
        fst_row_index: int = FsAddress__get_RowNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this))) or 0
        def predicate(c: FsCell) -> bool:
            return c.RowNumber == fst_row_index

        return try_find(predicate, FsCellsCollection__GetCellsInColumn_Z524259A4(cells_collection, col_index))

    @staticmethod
    def try_get_header_cell_of_column_index_at(cells_collection: FsCellsCollection, col_index: int, table: FsTable) -> FsCell | None:
        return table.TryGetHeaderCellOfColumnAt(cells_collection, col_index)

    def TryGetHeaderCellOfColumn(self, cells_collection: FsCellsCollection, column: FsRangeColumn) -> FsCell | None:
        this: FsTable = self
        return this.TryGetHeaderCellOfColumnAt(cells_collection, FsRangeColumn__get_Index(column))

    @staticmethod
    def try_get_header_cell_of_column(cells_collection: FsCellsCollection, column: FsRangeColumn, table: FsTable) -> FsCell | None:
        return table.TryGetHeaderCellOfColumn(cells_collection, column)

    def GetHeaderCellOfColumnAt(self, cells_collection: FsCellsCollection, col_index: int) -> FsCell:
        this: FsTable = self
        return value_2(this.TryGetHeaderCellOfColumnAt(cells_collection, col_index))

    @staticmethod
    def get_header_cell_of_column_index_at(cells_collection: FsCellsCollection, col_index: int, table: FsTable) -> FsCell:
        return table.GetHeaderCellOfColumnAt(cells_collection, col_index)

    def GetHeaderCellOfColumn(self, cells_collection: FsCellsCollection, column: FsRangeColumn) -> FsCell:
        this: FsTable = self
        return value_2(this.TryGetHeaderCellOfColumn(cells_collection, column))

    @staticmethod
    def get_header_cell_of_column(cells_collection: FsCellsCollection, column: FsRangeColumn, table: FsTable) -> FsCell:
        return table.GetHeaderCellOfColumn(cells_collection, column)

    def GetHeaderCellOfTableField(self, cells_collection: FsCellsCollection, table_field: FsTableField) -> FsCell:
        this: FsTable = self
        return FsTableField__HeaderCell_10EBE01C(table_field, cells_collection, this.ShowHeaderRow)

    @staticmethod
    def get_header_cell_of_table_field(cells_collection: FsCellsCollection, table_field: FsTableField, table: FsTable) -> FsCell:
        return table.GetHeaderCellOfTableField(cells_collection, table_field)

    def TryGetHeaderCellOfTableFieldAt(self, cells_collection: FsCellsCollection, table_field_index: int) -> FsCell | None:
        this: FsTable = self
        def chooser(tf: FsTableField) -> FsCell | None:
            if FsTableField__get_Index(tf) == table_field_index:
                return FsTableField__HeaderCell_10EBE01C(tf, cells_collection, this.ShowHeaderRow)

            else: 
                return None


        return try_pick(chooser, this._fieldNames.values())

    @staticmethod
    def try_get_header_cell_of_table_field_index_at(cells_collection: FsCellsCollection, table_field_index: int, table: FsTable) -> FsCell | None:
        return table.TryGetHeaderCellOfTableFieldAt(cells_collection, table_field_index)

    def GetHeaderCellOfTableFieldAt(self, cells_collection: FsCellsCollection, table_field_index: int) -> FsCell:
        this: FsTable = self
        return value_2(this.TryGetHeaderCellOfTableFieldAt(cells_collection, table_field_index))

    @staticmethod
    def get_header_cell_of_table_field_index_at(cells_collection: FsCellsCollection, table_field_index: int, table: FsTable) -> FsCell:
        return table.GetHeaderCellOfTableFieldAt(cells_collection, table_field_index)

    def TryGetHeaderCellByFieldName(self, cells_collection: FsCellsCollection, field_name: str) -> FsCell | None:
        this: FsTable = self
        match_value: FsTableField | None = Dictionary_tryGet(field_name, this._fieldNames)
        return None if (match_value is None) else FsTableField__HeaderCell_10EBE01C(match_value, cells_collection, this.ShowHeaderRow)

    @staticmethod
    def try_get_header_cell_by_field_name(cells_collection: FsCellsCollection, field_name: str, table: FsTable) -> FsCell | None:
        return table.TryGetHeaderCellByFieldName(cells_collection, field_name)

    def GetDataCellsOfColumnAt(self, cells_collection: FsCellsCollection, col_index: int) -> IEnumerable_1[FsCell]:
        this: FsTable = self
        def chooser(ri: int) -> FsCell | None:
            return FsCellsCollection__TryGetCell_Z37302880(cells_collection, ri, col_index)

        return choose(chooser, to_list(range_big_int(FsAddress__get_RowNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(this))) + 1, 1, FsAddress__get_RowNumber(FsRangeAddress__get_LastAddress(FsRangeBase__get_RangeAddress(this))))))

    @staticmethod
    def get_data_cells_of_column_index_at(cells_collection: FsCellsCollection, col_index: int, table: FsTable) -> IEnumerable_1[FsCell]:
        return table.GetDataCellsOfColumnAt(cells_collection, col_index)

    def Copy(self, __unit: None=None) -> FsTable:
        this: FsTable = self
        ra: FsRangeAddress = FsRangeAddress__Copy(FsRangeBase__get_RangeAddress(this))
        return FsTable(this.Name, ra, False, this.ShowHeaderRow)

    @staticmethod
    def copy(table: FsTable) -> FsTable:
        return table.Copy()

    def RescanFieldNames(self, cells_collection: FsCellsCollection) -> None:
        this: FsTable = self
        if this.ShowHeaderRow:
            old_field_names: Any = this._fieldNames
            this._fieldNames = dict([])
            cell_pos: int = 0
            with get_enumerator(this.GetHeaderRow(cells_collection)) as enumerator:
                while enumerator.System_Collections_IEnumerator_MoveNext():
                    cell: FsCell = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                    name: str = cell.ValueAsString()
                    match_value: FsTableField | None = Dictionary_tryGet(name, old_field_names)
                    if match_value is None:
                        if (name is None) != (name == ""):
                            name = this.GetUniqueName("Column", cell_pos + 1, True)
                            value: None = cell.SetValueAs(name)
                            ignore(None)
                            cell.DataType = DataType(0)

                        if name in this._fieldNames:
                            raise Exception(("The header row contains more than one field name \'" + name) + "\'.")

                        add_to_dict(this._fieldNames, name, FsTableField__ctor_Z18115A39(name, cell_pos))
                        cell_pos = (cell_pos + 1) or 0

                    else: 
                        table_field: FsTableField = match_value
                        FsTableField__set_Index_Z524259A4(table_field, cell_pos)
                        add_to_dict(this._fieldNames, name, table_field)
                        cell_pos = (cell_pos + 1) or 0


        else: 
            col_count: int = FsRangeBase__ColumnCount(this) or 0
            for i in range(1, col_count + 1, 1):
                def predicate(v: FsTableField) -> bool:
                    return FsTableField__get_Index(v) == (i - 1)

                if not exists(predicate, this._fieldNames.values()):
                    name_1: str = "Column" + int32_to_string(i)
                    add_to_dict(this._fieldNames, name_1, FsTableField__ctor_Z18115A39(name_1, i - 1))




FsTable_reflection = _expr192

def FsTable__ctor_30096B47(name: str, range_address: FsRangeAddress, show_totals_row: bool | None=None, show_header_row: bool | None=None) -> FsTable:
    return FsTable(name, range_address, show_totals_row, show_header_row)


__all__ = ["FsTable_reflection"]

