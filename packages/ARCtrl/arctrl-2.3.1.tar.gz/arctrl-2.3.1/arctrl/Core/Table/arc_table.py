from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.array_ import (map as map_1, initialize, iterate_indexed, iterate as iterate_2, sort_descending, map_indexed, indexed, sort_by)
from ...fable_modules.fable_library.list import (FSharpList, is_empty, iterate as iterate_1, append)
from ...fable_modules.fable_library.map_util import (add_to_dict, get_item_from_dict)
from ...fable_modules.fable_library.mutable_map import Dictionary
from ...fable_modules.fable_library.option import (default_arg, map as map_2, value as value_3)
from ...fable_modules.fable_library.range import range_big_int
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.seq import (to_array, delay, map, iterate, remove_at, collect, singleton, empty, try_find_index, length, filter, choose, indexed as indexed_1, to_list, append as append_1, fold, item)
from ...fable_modules.fable_library.seq2 import Array_groupBy
from ...fable_modules.fable_library.string_ import (to_fail, printf, join)
from ...fable_modules.fable_library.system_text import (StringBuilder__ctor, StringBuilder__AppendLine_Z721C83C5)
from ...fable_modules.fable_library.types import (Array, to_string, Int32Array)
from ...fable_modules.fable_library.util import (ignore, equal_arrays, array_hash, IEnumerable_1, get_enumerator, dispose, equals, compare_primitives, safe_hash, compare_arrays)
from ..Helper.collections_ import ResizeArray_map
from ..Helper.hash_codes import (box_hash_array, box_hash_seq)
from ..ontology_annotation import OntologyAnnotation
from .arc_table_aux import (SanityChecks_validate, get_column_count, get_row_count, Unchecked_tryGetCellAt, SanityChecks_validateColumnIndex, SanityChecks_validateRowIndex, Unchecked_setCellAt, try_find_duplicate_unique, SanityChecks_validateColumn, Unchecked_addColumn, Unchecked_fillMissingCells, Unchecked_removeHeader, Unchecked_removeColumnCells, try_find_duplicate_unique_in_array, Unchecked_removeColumnCells_withIndexChange, Unchecked_moveColumnTo, Unchecked_getEmptyCellForHeader, Unchecked_addRow, Unchecked_addRows, Unchecked_removeRowCells_withIndexChange, Unchecked_extendToRowCount, Unchecked_alignByHeaders, box_hash_values)
from .composite_cell import CompositeCell
from .composite_column import CompositeColumn
from .composite_header import CompositeHeader

def _expr865() -> TypeInfo:
    return class_type("ARCtrl.ArcTable", None, ArcTable)


class ArcTable:
    def __init__(self, name: str, headers: Array[CompositeHeader], values: Any) -> None:
        valid: bool = SanityChecks_validate(headers, values, True)
        self.name_004021: str = name
        self.headers_004022: Array[CompositeHeader] = headers
        self.values_004023: Any = values

    @property
    def Headers(self, __unit: None=None) -> Array[CompositeHeader]:
        this: ArcTable = self
        return this.headers_004022

    @Headers.setter
    def Headers(self, new_headers: Array[CompositeHeader]) -> None:
        this: ArcTable = self
        ignore(SanityChecks_validate(new_headers, this.values_004023, True))
        this.headers_004022 = new_headers

    @property
    def Values(self, __unit: None=None) -> Any:
        this: ArcTable = self
        return this.values_004023

    @Values.setter
    def Values(self, new_values: Any) -> None:
        this: ArcTable = self
        ignore(SanityChecks_validate(this.headers_004022, new_values, True))
        this.values_004023 = new_values

    @property
    def Name(self, __unit: None=None) -> str:
        this: ArcTable = self
        return this.name_004021

    @Name.setter
    def Name(self, new_name: str) -> None:
        this: ArcTable = self
        this.name_004021 = new_name

    @staticmethod
    def create(name: str, headers: Array[CompositeHeader], values: Any) -> ArcTable:
        return ArcTable(name, headers, values)

    @staticmethod
    def init(name: str) -> ArcTable:
        class ObjectExpr784:
            @property
            def Equals(self) -> Callable[[tuple[int, int], tuple[int, int]], bool]:
                return equal_arrays

            @property
            def GetHashCode(self) -> Callable[[tuple[int, int]], int]:
                return array_hash

        return ArcTable(name, [], Dictionary([], ObjectExpr784()))

    @staticmethod
    def create_from_headers(name: str, headers: Array[CompositeHeader]) -> ArcTable:
        class ObjectExpr785:
            @property
            def Equals(self) -> Callable[[tuple[int, int], tuple[int, int]], bool]:
                return equal_arrays

            @property
            def GetHashCode(self) -> Callable[[tuple[int, int]], int]:
                return array_hash

        return ArcTable.create(name, headers, Dictionary([], ObjectExpr785()))

    @staticmethod
    def create_from_rows(name: str, headers: Array[CompositeHeader], rows: Array[Array[CompositeCell]]) -> ArcTable:
        t: ArcTable = ArcTable.create_from_headers(name, headers)
        t.AddRows(rows)
        return t

    def Validate(self, raise_exception: bool | None=None) -> bool:
        this: ArcTable = self
        raise_exception_1: bool = default_arg(raise_exception, True)
        return SanityChecks_validate(this.Headers, this.Values, raise_exception_1)

    @staticmethod
    def validate(raise_exception: bool | None=None) -> Callable[[ArcTable], bool]:
        def _arrow786(table: ArcTable) -> bool:
            return table.Validate(raise_exception)

        return _arrow786

    @property
    def ColumnCount(self, __unit: None=None) -> int:
        this: ArcTable = self
        return get_column_count(this.Headers)

    @property
    def RowCount(self, __unit: None=None) -> int:
        this: ArcTable = self
        return get_row_count(this.Values)

    @property
    def Columns(self, __unit: None=None) -> Array[CompositeColumn]:
        this: ArcTable = self
        def _arrow788(__unit: None=None) -> IEnumerable_1[CompositeColumn]:
            def _arrow787(i: int) -> CompositeColumn:
                return this.GetColumn(i)

            return map(_arrow787, range_big_int(0, 1, this.ColumnCount - 1))

        return to_array(delay(_arrow788))

    def Copy(self, __unit: None=None) -> ArcTable:
        this: ArcTable = self
        def f(h: CompositeHeader) -> CompositeHeader:
            return h.Copy()

        next_headers: Array[CompositeHeader] = ResizeArray_map(f, this.Headers)
        class ObjectExpr789:
            @property
            def Equals(self) -> Callable[[tuple[int, int], tuple[int, int]], bool]:
                return equal_arrays

            @property
            def GetHashCode(self) -> Callable[[tuple[int, int]], int]:
                return array_hash

        next_values: Any = Dictionary([], ObjectExpr789())
        def action(tupled_arg: tuple[int, int]) -> None:
            ci: int = tupled_arg[0] or 0
            ri: int = tupled_arg[1] or 0
            add_to_dict(next_values, (ci, ri), get_item_from_dict(this.Values, (ci, ri)).Copy())

        iterate(action, this.Values.keys())
        return ArcTable.create(this.Name, next_headers, next_values)

    def TryGetCellAt(self, column: int, row: int) -> CompositeCell | None:
        this: ArcTable = self
        return Unchecked_tryGetCellAt(column, row, this.Values)

    @staticmethod
    def try_get_cell_at(column: int, row: int) -> Callable[[ArcTable], CompositeCell | None]:
        def _arrow790(table: ArcTable) -> CompositeCell | None:
            return table.TryGetCellAt(column, row)

        return _arrow790

    def GetCellAt(self, column: int, row: int) -> CompositeCell:
        this: ArcTable = self
        try: 
            return get_item_from_dict(this.Values, (column, row))

        except Exception as match_value:
            arg_2: str = this.Name
            return to_fail(printf("Unable to find cell for index: (%i, %i) in table %s"))(column)(row)(arg_2)


    @staticmethod
    def get_cell_at(column: int, row: int) -> Callable[[ArcTable], CompositeCell]:
        def _arrow791(table: ArcTable) -> CompositeCell:
            return table.GetCellAt(column, row)

        return _arrow791

    def IterColumns(self, action: Callable[[CompositeColumn], None]) -> None:
        this: ArcTable = self
        for column_index in range(0, (this.ColumnCount - 1) + 1, 1):
            action(this.GetColumn(column_index))

    @staticmethod
    def iter_columns(action: Callable[[CompositeColumn], None]) -> Callable[[ArcTable], ArcTable]:
        def _arrow792(table: ArcTable) -> ArcTable:
            copy: ArcTable = table.Copy()
            copy.IterColumns(action)
            return copy

        return _arrow792

    def IteriColumns(self, action: Callable[[int, CompositeColumn], None]) -> None:
        this: ArcTable = self
        for column_index in range(0, (this.ColumnCount - 1) + 1, 1):
            action(column_index, this.GetColumn(column_index))

    @staticmethod
    def iteri_columns(action: Callable[[int, CompositeColumn], None]) -> Callable[[ArcTable], ArcTable]:
        def _arrow793(table: ArcTable) -> ArcTable:
            copy: ArcTable = table.Copy()
            copy.IteriColumns(action)
            return copy

        return _arrow793

    def UpdateCellAt(self, column_index: int, row_index: int, c: CompositeCell, skip_validation: bool | None=None) -> None:
        this: ArcTable = self
        if not default_arg(skip_validation, False):
            SanityChecks_validateColumnIndex(column_index, this.ColumnCount, False)
            SanityChecks_validateRowIndex(row_index, this.RowCount, False)
            ignore(c.ValidateAgainstHeader(this.Headers[column_index], True))

        Unchecked_setCellAt(column_index, row_index, c, this.Values)

    @staticmethod
    def update_cell_at(column_index: int, row_index: int, cell: CompositeCell, skip_validation: bool | None=None) -> Callable[[ArcTable], ArcTable]:
        def _arrow794(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.UpdateCellAt(column_index, row_index, cell, skip_validation)
            return new_table

        return _arrow794

    def SetCellAt(self, column_index: int, row_index: int, c: CompositeCell, skip_validation: bool | None=None) -> None:
        this: ArcTable = self
        if not default_arg(skip_validation, False):
            SanityChecks_validateColumnIndex(column_index, this.ColumnCount, False)
            ignore(c.ValidateAgainstHeader(this.Headers[column_index], True))

        Unchecked_setCellAt(column_index, row_index, c, this.Values)

    @staticmethod
    def set_cell_at(column_index: int, row_index: int, cell: CompositeCell, skip_validation: bool | None=None) -> Callable[[ArcTable], ArcTable]:
        def _arrow795(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.SetCellAt(column_index, row_index, cell, skip_validation)
            return new_table

        return _arrow795

    def UpdateCellsBy(self, f: Callable[[int, int, CompositeCell], CompositeCell], skip_validation: bool | None=None) -> None:
        this: ArcTable = self
        skip_validation_1: bool = default_arg(skip_validation, False)
        enumerator: Any = get_enumerator(this.Values)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                kv: Any = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                pattern_input: tuple[int, int] = kv[0]
                ri: int = pattern_input[1] or 0
                ci: int = pattern_input[0] or 0
                new_cell: CompositeCell = f(ci, ri, kv[1])
                if not skip_validation_1:
                    ignore(new_cell.ValidateAgainstHeader(this.Headers[ci], True))

                Unchecked_setCellAt(ci, ri, new_cell, this.Values)

        finally: 
            dispose(enumerator)


    @staticmethod
    def update_cells_by(f: Callable[[int, int, CompositeCell], CompositeCell], skip_validation: bool | None=None) -> Callable[[ArcTable], None]:
        def _arrow796(table: ArcTable) -> None:
            new_table: ArcTable = table.Copy()
            new_table.UpdateCellsBy(f, skip_validation)

        return _arrow796

    def UpdateCellBy(self, column_index: int, row_index: int, f: Callable[[CompositeCell], CompositeCell], skip_validation: bool | None=None) -> None:
        this: ArcTable = self
        skip_validation_1: bool = default_arg(skip_validation, False)
        if not skip_validation_1:
            SanityChecks_validateColumnIndex(column_index, this.ColumnCount, False)
            SanityChecks_validateRowIndex(row_index, this.RowCount, False)

        new_cell: CompositeCell = f(this.GetCellAt(column_index, row_index))
        if not skip_validation_1:
            ignore(new_cell.ValidateAgainstHeader(this.Headers[column_index], True))

        Unchecked_setCellAt(column_index, row_index, new_cell, this.Values)

    @staticmethod
    def update_cell_by(column_index: int, row_index: int, f: Callable[[CompositeCell], CompositeCell], skip_validation: bool | None=None) -> Callable[[ArcTable], None]:
        def _arrow797(table: ArcTable) -> None:
            new_table: ArcTable = table.Copy()
            new_table.UpdateCellBy(column_index, row_index, f, skip_validation)

        return _arrow797

    def UpdateHeader(self, index: int, new_header: CompositeHeader, force_convert_cells: bool | None=None) -> None:
        this: ArcTable = self
        force_convert_cells_1: bool = default_arg(force_convert_cells, False)
        SanityChecks_validateColumnIndex(index, this.ColumnCount, False)
        header: CompositeHeader = new_header
        match_value: int | None = try_find_duplicate_unique(header, remove_at(index, this.Headers))
        if match_value is not None:
            raise Exception(((("Invalid input. Tried setting unique header `" + str(header)) + "`, but header of same type already exists at index ") + str(match_value)) + ".")

        c: CompositeColumn = CompositeColumn(new_header, this.GetColumn(index).Cells)
        if c.Validate():
            set_header: None
            this.Headers[index] = new_header

        elif force_convert_cells_1:
            def mapping(c_1: CompositeCell) -> CompositeCell:
                if c_1.is_free_text:
                    return c_1.ToTermCell()

                else: 
                    return c_1


            def mapping_1(c_2: CompositeCell) -> CompositeCell:
                return c_2.ToFreeTextCell()

            converted_cells: Array[CompositeCell] = map_1(mapping, c.Cells, None) if new_header.IsTermColumn else map_1(mapping_1, c.Cells, None)
            this.UpdateColumn(index, new_header, converted_cells)

        else: 
            raise Exception("Tried setting header for column with invalid type of cells. Set `forceConvertCells` flag to automatically convert cells into valid CompositeCell type.")


    @staticmethod
    def update_header(index: int, header: CompositeHeader) -> Callable[[ArcTable], ArcTable]:
        def _arrow798(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.UpdateHeader(index, header)
            return new_table

        return _arrow798

    def AddColumn(self, header: CompositeHeader, cells: Array[CompositeCell] | None=None, index: int | None=None, force_replace: bool | None=None, skip_fill_missing: bool | None=None) -> None:
        this: ArcTable = self
        index_1: int = default_arg(index, this.ColumnCount) or 0
        cells_1: Array[CompositeCell] = default_arg(cells, [])
        force_replace_1: bool = default_arg(force_replace, False)
        SanityChecks_validateColumnIndex(index_1, this.ColumnCount, True)
        SanityChecks_validateColumn(CompositeColumn.create(header, cells_1))
        Unchecked_addColumn(header, cells_1, index_1, force_replace_1, False, this.Headers, this.Values)
        if not equals(skip_fill_missing, True):
            Unchecked_fillMissingCells(this.Headers, this.Values)


    @staticmethod
    def add_column(header: CompositeHeader, cells: Array[CompositeCell] | None=None, index: int | None=None, force_replace: bool | None=None) -> Callable[[ArcTable], ArcTable]:
        def _arrow799(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.AddColumn(header, cells, index, force_replace)
            return new_table

        return _arrow799

    def AddColumnFill(self, header: CompositeHeader, cell: CompositeCell, index: int | None=None, force_replace: bool | None=None) -> None:
        this: ArcTable = self
        def _arrow800(_arg: int) -> CompositeCell:
            return cell.Copy()

        cells: Array[CompositeCell] = initialize(this.RowCount, _arrow800, None)
        this.AddColumn(header, cells, index, force_replace)

    @staticmethod
    def add_column_fill(header: CompositeHeader, cell: CompositeCell, index: int | None=None, force_replace: bool | None=None) -> Callable[[ArcTable], ArcTable]:
        def _arrow801(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.AddColumnFill(header, cell, index, force_replace)
            return new_table

        return _arrow801

    def UpdateColumn(self, column_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None, skip_fill_missing: bool | None=None) -> None:
        this: ArcTable = self
        SanityChecks_validateColumnIndex(column_index, this.ColumnCount, False)
        column: CompositeColumn = CompositeColumn.create(header, cells)
        SanityChecks_validateColumn(column)
        header_1: CompositeHeader = column.Header
        match_value: int | None = try_find_duplicate_unique(header_1, remove_at(column_index, this.Headers))
        if match_value is not None:
            raise Exception(((("Invalid input. Tried setting unique header `" + str(header_1)) + "`, but header of same type already exists at index ") + str(match_value)) + ".")

        Unchecked_removeHeader(column_index, this.Headers)
        Unchecked_removeColumnCells(column_index, this.Values)
        this.Headers.insert(column_index, column.Header)
        def action(row_index: int, v: CompositeCell) -> None:
            Unchecked_setCellAt(column_index, row_index, v, this.Values)

        iterate_indexed(action, column.Cells)
        if not equals(skip_fill_missing, True):
            Unchecked_fillMissingCells(this.Headers, this.Values)


    @staticmethod
    def update_column(column_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> Callable[[ArcTable], ArcTable]:
        def _arrow802(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.UpdateColumn(column_index, header, cells)
            return new_table

        return _arrow802

    def InsertColumn(self, index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> None:
        this: ArcTable = self
        this.AddColumn(header, cells, index, False)

    @staticmethod
    def insert_column(index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> Callable[[ArcTable], ArcTable]:
        def _arrow803(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.InsertColumn(index, header, cells)
            return new_table

        return _arrow803

    def AppendColumn(self, header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> None:
        this: ArcTable = self
        this.AddColumn(header, cells, this.ColumnCount, False)

    @staticmethod
    def append_column(header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> Callable[[ArcTable], ArcTable]:
        def _arrow804(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.AppendColumn(header, cells)
            return new_table

        return _arrow804

    def AddColumns(self, columns: Array[CompositeColumn], index: int | None=None, force_replace: bool | None=None, skip_fill_missing: bool | None=None) -> None:
        this: ArcTable = self
        index_1: int = default_arg(index, this.ColumnCount) or 0
        force_replace_1: bool = default_arg(force_replace, False)
        SanityChecks_validateColumnIndex(index_1, this.ColumnCount, True)
        def mapping(x: CompositeColumn) -> CompositeHeader:
            return x.Header

        duplicates: FSharpList[dict[str, Any]] = try_find_duplicate_unique_in_array(map(mapping, columns))
        if not is_empty(duplicates):
            sb: Any = StringBuilder__ctor()
            ignore(StringBuilder__AppendLine_Z721C83C5(sb, "Found duplicate unique columns in `columns`."))
            def action(x_1: dict[str, Any]) -> None:
                ignore(StringBuilder__AppendLine_Z721C83C5(sb, ((((("Duplicate `" + str(x_1["HeaderType"])) + "` at index ") + str(x_1["Index1"])) + " and ") + str(x_1["Index2"])) + "."))

            iterate_1(action, duplicates)
            raise Exception(to_string(sb))

        def action_1(x_2: CompositeColumn) -> None:
            SanityChecks_validateColumn(x_2)

        iterate_2(action_1, columns)
        def action_2(col: CompositeColumn) -> None:
            nonlocal index_1
            prev_headers_count: int = len(this.Headers) or 0
            Unchecked_addColumn(col.Header, col.Cells, index_1, force_replace_1, False, this.Headers, this.Values)
            if len(this.Headers) > prev_headers_count:
                index_1 = (index_1 + 1) or 0


        iterate_2(action_2, columns)
        if not equals(skip_fill_missing, True):
            Unchecked_fillMissingCells(this.Headers, this.Values)


    @staticmethod
    def add_columns(columns: Array[CompositeColumn], index: int | None=None, skip_fill_missing: bool | None=None) -> Callable[[ArcTable], ArcTable]:
        def _arrow805(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.AddColumns(columns, index, None, skip_fill_missing)
            return new_table

        return _arrow805

    def RemoveColumn(self, index: int) -> None:
        this: ArcTable = self
        SanityChecks_validateColumnIndex(index, this.ColumnCount, False)
        column_count: int = this.ColumnCount or 0
        Unchecked_removeHeader(index, this.Headers)
        Unchecked_removeColumnCells_withIndexChange(index, column_count, this.RowCount, this.Values)

    @staticmethod
    def remove_column(index: int) -> Callable[[ArcTable], ArcTable]:
        def _arrow806(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.RemoveColumn(index)
            return new_table

        return _arrow806

    def RemoveColumns(self, index_arr: Array[int]) -> None:
        this: ArcTable = self
        def _arrow807(index: int) -> None:
            SanityChecks_validateColumnIndex(index, this.ColumnCount, False)

        iterate_2(_arrow807, index_arr)
        def _arrow808(index_1: int) -> None:
            this.RemoveColumn(index_1)

        class ObjectExpr809:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        iterate_2(_arrow808, sort_descending(index_arr, ObjectExpr809()))

    @staticmethod
    def remove_columns(index_arr: Array[int]) -> Callable[[ArcTable], ArcTable]:
        def _arrow810(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.RemoveColumns(index_arr)
            return new_table

        return _arrow810

    def GetColumn(self, column_index: int) -> CompositeColumn:
        this: ArcTable = self
        SanityChecks_validateColumnIndex(column_index, this.ColumnCount, False)
        h: CompositeHeader = this.Headers[column_index]
        def _arrow812(__unit: None=None) -> IEnumerable_1[CompositeCell]:
            def _arrow811(i: int) -> IEnumerable_1[CompositeCell]:
                match_value: CompositeCell | None = this.TryGetCellAt(column_index, i)
                if match_value is not None:
                    return singleton(match_value)

                else: 
                    to_fail(printf("Unable to find cell for index: (%i, %i)"))(column_index)(i)
                    return empty()


            return collect(_arrow811, range_big_int(0, 1, this.RowCount - 1))

        cells: Array[CompositeCell] = to_array(delay(_arrow812))
        return CompositeColumn.create(h, cells)

    @staticmethod
    def get_column(index: int) -> Callable[[ArcTable], CompositeColumn]:
        def _arrow813(table: ArcTable) -> CompositeColumn:
            return table.GetColumn(index)

        return _arrow813

    def TryGetColumnByHeader(self, header: CompositeHeader) -> CompositeColumn | None:
        this: ArcTable = self
        def mapping(i: int) -> CompositeColumn:
            return this.GetColumn(i)

        def predicate(x: CompositeHeader) -> bool:
            return equals(x, header)

        return map_2(mapping, try_find_index(predicate, this.Headers))

    @staticmethod
    def try_get_column_by_header(header: CompositeHeader) -> Callable[[ArcTable], CompositeColumn | None]:
        def _arrow814(table: ArcTable) -> CompositeColumn | None:
            return table.TryGetColumnByHeader(header)

        return _arrow814

    def TryGetColumnByHeaderBy(self, header_predicate: Callable[[CompositeHeader], bool]) -> CompositeColumn | None:
        this: ArcTable = self
        def mapping(i: int) -> CompositeColumn:
            return this.GetColumn(i)

        return map_2(mapping, try_find_index(header_predicate, this.Headers))

    @staticmethod
    def try_get_column_by_header_by(header_predicate: Callable[[CompositeHeader], bool]) -> Callable[[ArcTable], CompositeColumn | None]:
        def _arrow815(table: ArcTable) -> CompositeColumn | None:
            return table.TryGetColumnByHeaderBy(header_predicate)

        return _arrow815

    def GetColumnByHeader(self, header: CompositeHeader) -> CompositeColumn:
        this: ArcTable = self
        match_value: CompositeColumn | None = this.TryGetColumnByHeader(header)
        if match_value is None:
            arg: str = this.Name
            return to_fail(printf("Unable to find column with header in table %s: %O"))(arg)(header)

        else: 
            return match_value


    @staticmethod
    def get_column_by_header(header: CompositeHeader) -> Callable[[ArcTable], CompositeColumn]:
        def _arrow816(table: ArcTable) -> CompositeColumn:
            return table.GetColumnByHeader(header)

        return _arrow816

    def TryGetInputColumn(self, __unit: None=None) -> CompositeColumn | None:
        this: ArcTable = self
        def mapping(i: int) -> CompositeColumn:
            return this.GetColumn(i)

        def predicate(x: CompositeHeader) -> bool:
            return x.is_input

        return map_2(mapping, try_find_index(predicate, this.Headers))

    @staticmethod
    def try_get_input_column(__unit: None=None) -> Callable[[ArcTable], CompositeColumn | None]:
        def _arrow817(table: ArcTable) -> CompositeColumn | None:
            return table.TryGetInputColumn()

        return _arrow817

    def GetInputColumn(self, __unit: None=None) -> CompositeColumn:
        this: ArcTable = self
        match_value: CompositeColumn | None = this.TryGetInputColumn()
        if match_value is None:
            arg: str = this.Name
            return to_fail(printf("Unable to find input column in table %s"))(arg)

        else: 
            return match_value


    @staticmethod
    def get_input_column(__unit: None=None) -> Callable[[ArcTable], CompositeColumn]:
        def _arrow818(table: ArcTable) -> CompositeColumn:
            return table.GetInputColumn()

        return _arrow818

    def TryGetOutputColumn(self, __unit: None=None) -> CompositeColumn | None:
        this: ArcTable = self
        def mapping(i: int) -> CompositeColumn:
            return this.GetColumn(i)

        def predicate(x: CompositeHeader) -> bool:
            return x.is_output

        return map_2(mapping, try_find_index(predicate, this.Headers))

    @staticmethod
    def try_get_output_column(__unit: None=None) -> Callable[[ArcTable], CompositeColumn | None]:
        def _arrow819(table: ArcTable) -> CompositeColumn | None:
            return table.TryGetOutputColumn()

        return _arrow819

    def GetOutputColumn(self, __unit: None=None) -> CompositeColumn:
        this: ArcTable = self
        match_value: CompositeColumn | None = this.TryGetOutputColumn()
        if match_value is None:
            arg: str = this.Name
            return to_fail(printf("Unable to find output column in table %s"))(arg)

        else: 
            return match_value


    @staticmethod
    def get_output_column(__unit: None=None) -> Callable[[ArcTable], CompositeColumn]:
        def _arrow820(table: ArcTable) -> CompositeColumn:
            return table.GetOutputColumn()

        return _arrow820

    def MoveColumn(self, start_col: int, end_col: int) -> None:
        this: ArcTable = self
        if start_col == end_col:
            pass

        elif True if (start_col < 0) else (start_col >= this.ColumnCount):
            to_fail(printf("Cannt move column. Invalid start column index: %i"))(start_col)

        elif True if (end_col < 0) else (end_col >= this.ColumnCount):
            to_fail(printf("Cannt move column. Invalid end column index: %i"))(end_col)

        else: 
            Unchecked_moveColumnTo(this.RowCount, start_col, end_col, this.Headers, this.Values)


    @staticmethod
    def move_column(start_col: int, end_col: int) -> Callable[[ArcTable], ArcTable]:
        def _arrow821(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.MoveColumn(start_col, end_col)
            return new_table

        return _arrow821

    def AddRow(self, cells: Array[CompositeCell] | None=None, index: int | None=None) -> None:
        this: ArcTable = self
        index_1: int = default_arg(index, this.RowCount) or 0
        def _arrow823(__unit: None=None) -> IEnumerable_1[CompositeCell]:
            def _arrow822(column_index: int) -> IEnumerable_1[CompositeCell]:
                return singleton(Unchecked_getEmptyCellForHeader(this.Headers[column_index], Unchecked_tryGetCellAt(column_index, 0, this.Values)))

            return collect(_arrow822, range_big_int(0, 1, this.ColumnCount - 1))

        cells_1: Array[CompositeCell] = to_array(delay(_arrow823)) if (cells is None) else value_3(cells)
        SanityChecks_validateRowIndex(index_1, this.RowCount, True)
        column_count: int = this.ColumnCount or 0
        new_cells_count: int = length(cells_1) or 0
        if column_count == 0:
            raise Exception("Table contains no columns! Cannot add row to empty table!")

        elif new_cells_count != column_count:
            raise Exception(((("Cannot add a new row with " + str(new_cells_count)) + " cells, as the table has ") + str(column_count)) + " columns.")

        for column_index_1 in range(0, (this.ColumnCount - 1) + 1, 1):
            h_1: CompositeHeader = this.Headers[column_index_1]
            SanityChecks_validateColumn(CompositeColumn.create(h_1, [cells_1[column_index_1]]))
        Unchecked_addRow(index_1, cells_1, this.Headers, this.Values)

    @staticmethod
    def add_row(cells: Array[CompositeCell] | None=None, index: int | None=None) -> Callable[[ArcTable], ArcTable]:
        def _arrow824(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.AddRow(cells, index)
            return new_table

        return _arrow824

    def UpdateRow(self, row_index: int, cells: Array[CompositeCell]) -> None:
        this: ArcTable = self
        SanityChecks_validateRowIndex(row_index, this.RowCount, False)
        column_count: int = this.RowCount or 0
        new_cells_count: int = length(cells) or 0
        if column_count == 0:
            raise Exception("Table contains no columns! Cannot add row to empty table!")

        elif new_cells_count != column_count:
            raise Exception(((("Cannot add a new row with " + str(new_cells_count)) + " cells, as the table has ") + str(column_count)) + " columns.")

        def action(i: int, cell: CompositeCell) -> None:
            h: CompositeHeader = this.Headers[i]
            SanityChecks_validateColumn(CompositeColumn.create(h, [cell]))

        iterate_indexed(action, cells)
        def action_1(column_index: int, cell_1: CompositeCell) -> None:
            Unchecked_setCellAt(column_index, row_index, cell_1, this.Values)

        iterate_indexed(action_1, cells)

    @staticmethod
    def update_row(row_index: int, cells: Array[CompositeCell]) -> Callable[[ArcTable], ArcTable]:
        def _arrow825(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.UpdateRow(row_index, cells)
            return new_table

        return _arrow825

    def AppendRow(self, cells: Array[CompositeCell] | None=None) -> None:
        this: ArcTable = self
        this.AddRow(cells, this.RowCount)

    @staticmethod
    def append_row(cells: Array[CompositeCell] | None=None) -> Callable[[ArcTable], ArcTable]:
        def _arrow826(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.AppendRow(cells)
            return new_table

        return _arrow826

    def InsertRow(self, index: int, cells: Array[CompositeCell] | None=None) -> None:
        this: ArcTable = self
        this.AddRow(cells, index)

    @staticmethod
    def insert_row(index: int, cells: Array[CompositeCell] | None=None) -> Callable[[ArcTable], ArcTable]:
        def _arrow827(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.AddRow(cells, index)
            return new_table

        return _arrow827

    def AddRows(self, rows: Array[Array[CompositeCell]], index: int | None=None) -> None:
        this: ArcTable = self
        index_1: int = default_arg(index, this.RowCount) or 0
        SanityChecks_validateRowIndex(index_1, this.RowCount, True)
        def action(row: Array[CompositeCell]) -> None:
            column_count: int = this.ColumnCount or 0
            new_cells_count: int = length(row) or 0
            if column_count == 0:
                raise Exception("Table contains no columns! Cannot add row to empty table!")

            elif new_cells_count != column_count:
                raise Exception(((("Cannot add a new row with " + str(new_cells_count)) + " cells, as the table has ") + str(column_count)) + " columns.")


        iterate_2(action, rows)
        for idx in range(0, (len(rows) - 1) + 1, 1):
            row_1: Array[CompositeCell] = rows[idx]
            for column_index in range(0, (this.ColumnCount - 1) + 1, 1):
                h: CompositeHeader = this.Headers[column_index]
                SanityChecks_validateColumn(CompositeColumn.create(h, [row_1[column_index]]))
        Unchecked_addRows(index_1, rows, this.Headers, this.Values)

    @staticmethod
    def add_rows(rows: Array[Array[CompositeCell]], index: int | None=None) -> Callable[[ArcTable], ArcTable]:
        def _arrow828(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.AddRows(rows, index)
            return new_table

        return _arrow828

    def AddRowsEmpty(self, row_count: int, index: int | None=None) -> None:
        this: ArcTable = self
        def _arrow830(__unit: None=None) -> IEnumerable_1[CompositeCell]:
            def _arrow829(column_index: int) -> IEnumerable_1[CompositeCell]:
                return singleton(Unchecked_getEmptyCellForHeader(this.Headers[column_index], Unchecked_tryGetCellAt(column_index, 0, this.Values)))

            return collect(_arrow829, range_big_int(0, 1, this.ColumnCount - 1))

        row: Array[CompositeCell] = to_array(delay(_arrow830))
        def _arrow831(_arg: int) -> Array[CompositeCell]:
            return row

        rows: Array[Array[CompositeCell]] = initialize(row_count, _arrow831, None)
        this.AddRows(rows, index)

    @staticmethod
    def add_rows_empty(row_count: int, index: int | None=None) -> Callable[[ArcTable], ArcTable]:
        def _arrow832(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.AddRowsEmpty(row_count, index)
            return new_table

        return _arrow832

    def RemoveRow(self, index: int) -> None:
        this: ArcTable = self
        SanityChecks_validateRowIndex(index, this.RowCount, False)
        Unchecked_removeRowCells_withIndexChange(index, this.ColumnCount, this.RowCount, this.Values)

    @staticmethod
    def remove_row(index: int) -> Callable[[ArcTable], ArcTable]:
        def _arrow833(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.RemoveRow(index)
            return new_table

        return _arrow833

    def RemoveRows(self, index_arr: Array[int]) -> None:
        this: ArcTable = self
        def _arrow834(index: int) -> None:
            SanityChecks_validateRowIndex(index, this.RowCount, False)

        iterate_2(_arrow834, index_arr)
        def _arrow835(index_1: int) -> None:
            this.RemoveRow(index_1)

        class ObjectExpr836:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        iterate_2(_arrow835, sort_descending(index_arr, ObjectExpr836()))

    @staticmethod
    def remove_rows(index_arr: Array[int]) -> Callable[[ArcTable], ArcTable]:
        def _arrow837(table: ArcTable) -> ArcTable:
            new_table: ArcTable = table.Copy()
            new_table.RemoveColumns(index_arr)
            return new_table

        return _arrow837

    def GetRow(self, row_index: int, SkipValidation: bool | None=None) -> Array[CompositeCell]:
        this: ArcTable = self
        if not equals(SkipValidation, True):
            SanityChecks_validateRowIndex(row_index, this.RowCount, False)

        def _arrow839(__unit: None=None) -> IEnumerable_1[CompositeCell]:
            def _arrow838(column_index: int) -> CompositeCell:
                return value_3(this.TryGetCellAt(column_index, row_index))

            return map(_arrow838, range_big_int(0, 1, this.ColumnCount - 1))

        return to_array(delay(_arrow839))

    @staticmethod
    def get_row(index: int) -> Callable[[ArcTable], Array[CompositeCell]]:
        def _arrow840(table: ArcTable) -> Array[CompositeCell]:
            return table.GetRow(index)

        return _arrow840

    def Join(self, table: ArcTable, index: int | None=None, join_options: str | None=None, force_replace: bool | None=None, skip_fill_missing: bool | None=None) -> None:
        this: ArcTable = self
        join_options_1: str = default_arg(join_options, "headers")
        force_replace_1: bool = default_arg(force_replace, False)
        skip_fill_missing_1: bool = default_arg(skip_fill_missing, False)
        index_1: int = default_arg(index, this.ColumnCount) or 0
        index_1 = (this.ColumnCount if (index_1 == -1) else index_1) or 0
        SanityChecks_validateColumnIndex(index_1, this.ColumnCount, True)
        only_headers: bool = join_options_1 == "headers"
        columns: Array[CompositeColumn]
        pre: Array[CompositeColumn] = table.Columns
        def mapping_2(c_1: CompositeColumn) -> CompositeColumn:
            units_opt: Array[OntologyAnnotation] | None = c_1.TryGetColumnUnits()
            if units_opt is None:
                return CompositeColumn(c_1.Header, [])

            else: 
                def mapping_1(u: OntologyAnnotation, c_1: Any=c_1) -> CompositeCell:
                    return CompositeCell.create_unitized("", u)

                return CompositeColumn(c_1.Header, map_1(mapping_1, units_opt, None))


        def mapping(c: CompositeColumn) -> CompositeColumn:
            return CompositeColumn(c.Header, [])

        columns = map_1(mapping_2, pre, None) if (join_options_1 == "withUnit") else (pre if (join_options_1 == "withValues") else map_1(mapping, pre, None))
        def mapping_3(x: CompositeColumn) -> CompositeHeader:
            return x.Header

        duplicates: FSharpList[dict[str, Any]] = try_find_duplicate_unique_in_array(map(mapping_3, columns))
        if not is_empty(duplicates):
            sb: Any = StringBuilder__ctor()
            ignore(StringBuilder__AppendLine_Z721C83C5(sb, "Found duplicate unique columns in `columns`."))
            def action(x_1: dict[str, Any]) -> None:
                ignore(StringBuilder__AppendLine_Z721C83C5(sb, ((((("Duplicate `" + str(x_1["HeaderType"])) + "` at index ") + str(x_1["Index1"])) + " and ") + str(x_1["Index2"])) + "."))

            iterate_1(action, duplicates)
            raise Exception(to_string(sb))

        def action_1(x_2: CompositeColumn) -> None:
            SanityChecks_validateColumn(x_2)

        iterate_2(action_1, columns)
        def action_2(col: CompositeColumn) -> None:
            nonlocal index_1
            prev_headers_count: int = len(this.Headers) or 0
            Unchecked_addColumn(col.Header, col.Cells, index_1, force_replace_1, only_headers, this.Headers, this.Values)
            if len(this.Headers) > prev_headers_count:
                index_1 = (index_1 + 1) or 0


        iterate_2(action_2, columns)
        if not skip_fill_missing_1:
            Unchecked_fillMissingCells(this.Headers, this.Values)


    @staticmethod
    def join(table: ArcTable, index: int | None=None, join_options: str | None=None, force_replace: bool | None=None) -> Callable[[ArcTable], ArcTable]:
        def _arrow841(this: ArcTable) -> ArcTable:
            copy: ArcTable = this.Copy()
            copy.Join(table, index, join_options, force_replace)
            return copy

        return _arrow841

    def AddProtocolTypeColumn(self, types: Array[OntologyAnnotation] | None=None, index: int | None=None) -> None:
        this: ArcTable = self
        def mapping_1(array: Array[OntologyAnnotation]) -> Array[CompositeCell]:
            def mapping(Item: OntologyAnnotation, array: Any=array) -> CompositeCell:
                return CompositeCell(0, Item)

            return map_1(mapping, array, None)

        cells: Array[CompositeCell] | None = map_2(mapping_1, types)
        this.AddColumn(CompositeHeader(4), cells, index)

    def AddProtocolVersionColumn(self, versions: Array[str] | None=None, index: int | None=None) -> None:
        this: ArcTable = self
        def mapping_1(array: Array[str]) -> Array[CompositeCell]:
            def mapping(Item: str, array: Any=array) -> CompositeCell:
                return CompositeCell(1, Item)

            return map_1(mapping, array, None)

        cells: Array[CompositeCell] | None = map_2(mapping_1, versions)
        this.AddColumn(CompositeHeader(7), cells, index)

    def AddProtocolUriColumn(self, uris: Array[str] | None=None, index: int | None=None) -> None:
        this: ArcTable = self
        def mapping_1(array: Array[str]) -> Array[CompositeCell]:
            def mapping(Item: str, array: Any=array) -> CompositeCell:
                return CompositeCell(1, Item)

            return map_1(mapping, array, None)

        cells: Array[CompositeCell] | None = map_2(mapping_1, uris)
        this.AddColumn(CompositeHeader(6), cells, index)

    def AddProtocolDescriptionColumn(self, descriptions: Array[str] | None=None, index: int | None=None) -> None:
        this: ArcTable = self
        def mapping_1(array: Array[str]) -> Array[CompositeCell]:
            def mapping(Item: str, array: Any=array) -> CompositeCell:
                return CompositeCell(1, Item)

            return map_1(mapping, array, None)

        cells: Array[CompositeCell] | None = map_2(mapping_1, descriptions)
        this.AddColumn(CompositeHeader(5), cells, index)

    def AddProtocolNameColumn(self, names: Array[str] | None=None, index: int | None=None) -> None:
        this: ArcTable = self
        def mapping_1(array: Array[str]) -> Array[CompositeCell]:
            def mapping(Item: str, array: Any=array) -> CompositeCell:
                return CompositeCell(1, Item)

            return map_1(mapping, array, None)

        cells: Array[CompositeCell] | None = map_2(mapping_1, names)
        this.AddColumn(CompositeHeader(8), cells, index)

    def GetProtocolTypeColumn(self, __unit: None=None) -> CompositeColumn:
        this: ArcTable = self
        return this.GetColumnByHeader(CompositeHeader(4))

    def GetProtocolVersionColumn(self, __unit: None=None) -> CompositeColumn:
        this: ArcTable = self
        return this.GetColumnByHeader(CompositeHeader(7))

    def GetProtocolUriColumn(self, __unit: None=None) -> CompositeColumn:
        this: ArcTable = self
        return this.GetColumnByHeader(CompositeHeader(6))

    def GetProtocolDescriptionColumn(self, __unit: None=None) -> CompositeColumn:
        this: ArcTable = self
        return this.GetColumnByHeader(CompositeHeader(5))

    def GetProtocolNameColumn(self, __unit: None=None) -> CompositeColumn:
        this: ArcTable = self
        return this.GetColumnByHeader(CompositeHeader(8))

    def TryGetProtocolNameColumn(self, __unit: None=None) -> CompositeColumn | None:
        this: ArcTable = self
        return this.TryGetColumnByHeader(CompositeHeader(8))

    def GetComponentColumns(self, __unit: None=None) -> Array[CompositeColumn]:
        this: ArcTable = self
        def mapping(h_1: CompositeHeader) -> CompositeColumn:
            return this.GetColumnByHeader(h_1)

        def predicate(h: CompositeHeader) -> bool:
            return h.is_component

        return map_1(mapping, to_array(filter(predicate, this.Headers)), None)

    @staticmethod
    def SplitByColumnValues(column_index: int) -> Callable[[ArcTable], Array[ArcTable]]:
        def _arrow843(table: ArcTable) -> Array[ArcTable]:
            def mapping_3(i: int, index_group: Array[int]) -> ArcTable:
                headers: Array[CompositeHeader] = list(table.Headers)
                def mapping_2(i_1: int, i: Any=i, index_group: Any=index_group) -> Array[CompositeCell]:
                    return table.GetRow(i_1, True)

                rows: Array[Array[CompositeCell]] = map_1(mapping_2, index_group, None)
                return ArcTable.create_from_rows(table.Name, headers, rows)

            def mapping_1(tupled_arg: tuple[CompositeCell, Array[tuple[int, CompositeCell]]]) -> Array[int]:
                def mapping(tuple_1: tuple[int, CompositeCell], tupled_arg: Any=tupled_arg) -> int:
                    return tuple_1[0]

                return map_1(mapping, tupled_arg[1], Int32Array)

            def projection(tuple: tuple[int, CompositeCell]) -> CompositeCell:
                return tuple[1]

            class ObjectExpr842:
                @property
                def Equals(self) -> Callable[[CompositeCell, CompositeCell], bool]:
                    return equals

                @property
                def GetHashCode(self) -> Callable[[CompositeCell], int]:
                    return safe_hash

            return map_indexed(mapping_3, map_1(mapping_1, Array_groupBy(projection, indexed(table.GetColumn(column_index).Cells), ObjectExpr842()), None), None)

        return _arrow843

    @staticmethod
    def SplitByColumnValuesByHeader(header: CompositeHeader) -> Callable[[ArcTable], Array[ArcTable]]:
        def _arrow844(table: ArcTable) -> Array[ArcTable]:
            def predicate(x: CompositeHeader) -> bool:
                return equals(x, header)

            index: int | None = try_find_index(predicate, table.Headers)
            if index is None:
                return [table.Copy()]

            else: 
                i: int = index or 0
                return ArcTable.SplitByColumnValues(i)(table)


        return _arrow844

    @staticmethod
    def SplitByProtocolREF() -> Callable[[ArcTable], Array[ArcTable]]:
        def _arrow845(table: ArcTable) -> Array[ArcTable]:
            return ArcTable.SplitByColumnValuesByHeader(CompositeHeader(8))(table)

        return _arrow845

    @staticmethod
    def update_reference_by_annotation_table(ref_table: ArcTable, annotation_table: ArcTable) -> ArcTable:
        ref_table_1: ArcTable = ref_table.Copy()
        annotation_table_1: ArcTable = annotation_table.Copy()
        def chooser(tupled_arg: tuple[int, CompositeHeader]) -> int | None:
            if tupled_arg[1].is_protocol_column:
                return None

            else: 
                return tupled_arg[0]


        non_protocol_columns: Array[int] = to_array(choose(chooser, indexed_1(ref_table_1.Headers)))
        ref_table_1.RemoveColumns(non_protocol_columns)
        Unchecked_extendToRowCount(annotation_table_1.RowCount, ref_table_1.Headers, ref_table_1.Values)
        arr: Array[CompositeColumn] = annotation_table_1.Columns
        for idx in range(0, (len(arr) - 1) + 1, 1):
            c: CompositeColumn = arr[idx]
            ref_table_1.AddColumn(c.Header, c.Cells, None, True)
        return ref_table_1

    @staticmethod
    def append(table1: ArcTable, table2: ArcTable) -> ArcTable:
        def get_list(t: ArcTable) -> FSharpList[FSharpList[tuple[CompositeHeader, CompositeCell]]]:
            def _arrow849(__unit: None=None, t: Any=t) -> IEnumerable_1[FSharpList[tuple[CompositeHeader, CompositeCell]]]:
                def _arrow848(row: int) -> FSharpList[tuple[CompositeHeader, CompositeCell]]:
                    def _arrow847(__unit: None=None) -> IEnumerable_1[tuple[CompositeHeader, CompositeCell]]:
                        def _arrow846(col: int) -> tuple[CompositeHeader, CompositeCell]:
                            return (t.Headers[col], get_item_from_dict(t.Values, (col, row)))

                        return map(_arrow846, range_big_int(0, 1, t.ColumnCount - 1))

                    return to_list(delay(_arrow847))

                return map(_arrow848, range_big_int(0, 1, t.RowCount - 1))

            return to_list(delay(_arrow849))

        pattern_input: tuple[Array[CompositeHeader], Any] = Unchecked_alignByHeaders(False, append(get_list(table1), get_list(table2)))
        return ArcTable.create(table1.Name, pattern_input[0], pattern_input[1])

    def __str__(self, __unit: None=None) -> str:
        this: ArcTable = self
        row_count: int = this.RowCount or 0
        def _arrow858(__unit: None=None) -> IEnumerable_1[str]:
            def _arrow857(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow856(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow855(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow850(row_i: int) -> str:
                            return join("\t|\t", map(to_string, this.GetRow(row_i)))

                        def _arrow853(__unit: None=None) -> IEnumerable_1[str]:
                            def _arrow852(__unit: None=None) -> IEnumerable_1[str]:
                                def _arrow851(row_i_1: int) -> str:
                                    return join("\t|\t", map(to_string, this.GetRow(row_i_1)))

                                return map(_arrow851, range_big_int(row_count - 20, 1, row_count - 1))

                            return append_1(singleton("..."), delay(_arrow852))

                        def _arrow854(row_i_2: int) -> str:
                            return join("\t|\t", map(to_string, this.GetRow(row_i_2)))

                        return append_1(map(_arrow850, range_big_int(0, 1, 19)), delay(_arrow853)) if (row_count > 50) else (singleton("No rows") if (row_count == 0) else map(_arrow854, range_big_int(0, 1, row_count - 1)))

                    return append_1(singleton(join("\t|\t", map(to_string, this.Headers))), delay(_arrow855))

                return append_1(singleton("-------------"), delay(_arrow856))

            return append_1(singleton(("Table: " + this.Name) + ""), delay(_arrow857))

        return join("\n", to_list(delay(_arrow858)))

    def StructurallyEquals(self, other: ArcTable) -> bool:
        this: ArcTable = self
        def sort(arg: Any) -> Array[Any]:
            def projection(_arg: Any, arg: Any=arg) -> tuple[int, int]:
                return _arg[0]

            class ObjectExpr859:
                @property
                def Compare(self) -> Callable[[tuple[int, int], tuple[int, int]], int]:
                    return compare_arrays

            return sort_by(projection, list(arg), ObjectExpr859())

        def _arrow862(__unit: None=None) -> bool:
            a: IEnumerable_1[CompositeHeader] = this.Headers
            b: IEnumerable_1[CompositeHeader] = other.Headers
            def folder(acc: bool, e: bool) -> bool:
                if acc:
                    return e

                else: 
                    return False


            def _arrow861(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow860(i: int) -> bool:
                    return equals(item(i, a), item(i, b))

                return map(_arrow860, range_big_int(0, 1, length(a) - 1))

            return fold(folder, True, to_list(delay(_arrow861))) if (length(a) == length(b)) else False

        if _arrow862() if (this.Name == other.Name) else False:
            a_1: IEnumerable_1[Any] = sort(this.Values)
            b_1: IEnumerable_1[Any] = sort(other.Values)
            def folder_1(acc_1: bool, e_1: bool) -> bool:
                if acc_1:
                    return e_1

                else: 
                    return False


            def _arrow864(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow863(i_1: int) -> bool:
                    return equals(item(i_1, a_1), item(i_1, b_1))

                return map(_arrow863, range_big_int(0, 1, length(a_1) - 1))

            return fold(folder_1, True, to_list(delay(_arrow864))) if (length(a_1) == length(b_1)) else False

        else: 
            return False


    def ReferenceEquals(self, other: ArcTable) -> bool:
        this: ArcTable = self
        return this is other

    def __eq__(self, other: Any=None) -> bool:
        this: ArcTable = self
        return this.StructurallyEquals(other) if isinstance(other, ArcTable) else False

    def __hash__(self, __unit: None=None) -> Any:
        this: ArcTable = self
        v_hash: Any = box_hash_values(this.ColumnCount, this.Values)
        return box_hash_array([this.Name, box_hash_seq(this.Headers), v_hash])


ArcTable_reflection = _expr865

def ArcTable__ctor_76CAD84E(name: str, headers: Array[CompositeHeader], values: Any) -> ArcTable:
    return ArcTable(name, headers, values)


__all__ = ["ArcTable_reflection"]

