from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.array_ import (iterate_indexed, map)
from ...fable_modules.fable_library.int32 import op_unary_negation_int32
from ...fable_modules.fable_library.list import (cons, is_empty, tail as tail_1, head, FSharpList, empty, of_seq, exists, pick, map_indexed)
from ...fable_modules.fable_library.map import (of_array, try_find)
from ...fable_modules.fable_library.map_util import (get_item_from_dict, add_to_dict, remove_from_dict)
from ...fable_modules.fable_library.mutable_map import Dictionary
from ...fable_modules.fable_library.option import value as value_2
from ...fable_modules.fable_library.range import range_big_int
from ...fable_modules.fable_library.seq import (max_by, try_find_index, filter, to_array, head as head_1, to_list)
from ...fable_modules.fable_library.seq2 import Array_groupBy
from ...fable_modules.fable_library.set import (of_array as of_array_1, FSharpSet__Contains)
from ...fable_modules.fable_library.string_ import (to_console, printf)
from ...fable_modules.fable_library.types import (Array, Int32Array, to_string)
from ...fable_modules.fable_library.util import (compare_primitives, safe_hash, equals, IEnumerable_1, compare, ignore, get_enumerator, dispose, max, number_hash, equal_arrays, array_hash)
from ..Helper.collections_ import (Dictionary_tryFind, List_tryPickAndRemove)
from .composite_cell import CompositeCell
from .composite_column import CompositeColumn
from .composite_header import CompositeHeader

def get_column_count(headers: Array[CompositeHeader]) -> int:
    return len(headers)


def get_row_count(values: Any) -> int:
    if len(values) == 0:
        return 0

    else: 
        def projection(tuple: tuple[int, int], values: Any=values) -> int:
            return tuple[1]

        class ObjectExpr723:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        return 1 + max_by(projection, values.keys(), ObjectExpr723())[1]



def box_hash_values(col_count: int, values: Any) -> Any:
    hash_1: int = 0
    row_count: int = get_row_count(values) or 0
    for col in range(0, (col_count - 1) + 1, 1):
        for row in range(0, (row_count - 1) + 1, 1):
            hash_1 = (((-1640531527 + safe_hash(get_item_from_dict(values, (col, row)))) + (hash_1 << 6)) + (hash_1 >> 2)) or 0
    return hash_1


def _007CIsUniqueExistingHeader_007C__007C(existing_headers: IEnumerable_1[CompositeHeader], input: CompositeHeader) -> int | None:
    if ((((input.tag == 3) or (input.tag == 2)) or (input.tag == 1)) or (input.tag == 0)) or (input.tag == 13):
        return None

    elif input.tag == 12:
        def _arrow724(h: CompositeHeader, existing_headers: Any=existing_headers, input: Any=input) -> bool:
            return True if (h.tag == 12) else False

        return try_find_index(_arrow724, existing_headers)

    elif input.tag == 11:
        def _arrow725(h_1: CompositeHeader, existing_headers: Any=existing_headers, input: Any=input) -> bool:
            return True if (h_1.tag == 11) else False

        return try_find_index(_arrow725, existing_headers)

    else: 
        def _arrow726(h_2: CompositeHeader, existing_headers: Any=existing_headers, input: Any=input) -> bool:
            return equals(h_2, input)

        return try_find_index(_arrow726, existing_headers)



def try_find_duplicate_unique(new_header: CompositeHeader, existing_headers: IEnumerable_1[CompositeHeader]) -> int | None:
    active_pattern_result: int | None = _007CIsUniqueExistingHeader_007C__007C(existing_headers, new_header)
    if active_pattern_result is not None:
        index: int = active_pattern_result or 0
        return index

    else: 
        return None



def try_find_duplicate_unique_in_array(existing_headers: IEnumerable_1[CompositeHeader]) -> FSharpList[dict[str, Any]]:
    def loop(i_mut: int, duplicate_list_mut: FSharpList[dict[str, Any]], header_list_mut: FSharpList[CompositeHeader], existing_headers: Any=existing_headers) -> FSharpList[dict[str, Any]]:
        while True:
            (i, duplicate_list, header_list) = (i_mut, duplicate_list_mut, header_list_mut)
            (pattern_matching_result, header, tail) = (None, None, None)
            if is_empty(header_list):
                pattern_matching_result = 0

            elif is_empty(tail_1(header_list)):
                pattern_matching_result = 0

            else: 
                pattern_matching_result = 1
                header = head(header_list)
                tail = tail_1(header_list)

            if pattern_matching_result == 0:
                return duplicate_list

            elif pattern_matching_result == 1:
                has_duplicate: int | None = try_find_duplicate_unique(header, tail)
                i_mut = i + 1
                duplicate_list_mut = cons({
                    "HeaderType": header,
                    "Index1": i,
                    "Index2": value_2(has_duplicate)
                }, duplicate_list) if (has_duplicate is not None) else duplicate_list
                header_list_mut = tail
                continue

            break

    def predicate(x: CompositeHeader, existing_headers: Any=existing_headers) -> bool:
        return not x.IsTermColumn

    return loop(0, empty(), of_seq(filter(predicate, existing_headers)))


def SanityChecks_validateColumnIndex(index: int, column_count: int, allow_append: bool) -> None:
    if index < 0:
        raise Exception("Cannot insert CompositeColumn at index < 0.")

    def _arrow727(__unit: None=None, index: Any=index, column_count: Any=column_count, allow_append: Any=allow_append) -> bool:
        x: int = index or 0
        y: int = column_count or 0
        return (compare(x, y) > 0) if allow_append else (compare(x, y) >= 0)

    if _arrow727():
        raise Exception(("Specified index is out of table range! Table contains only " + str(column_count)) + " columns.")



def SanityChecks_validateRowIndex(index: int, row_count: int, allow_append: bool) -> None:
    if index < 0:
        raise Exception("Cannot insert CompositeColumn at index < 0.")

    def _arrow728(__unit: None=None, index: Any=index, row_count: Any=row_count, allow_append: Any=allow_append) -> bool:
        x: int = index or 0
        y: int = row_count or 0
        return (compare(x, y) > 0) if allow_append else (compare(x, y) >= 0)

    if _arrow728():
        raise Exception(("Specified index is out of table range! Table contains only " + str(row_count)) + " rows.")



def SanityChecks_validateColumn(column: CompositeColumn) -> None:
    ignore(column.Validate(True))


def SanityChecks_validate(headers: Array[CompositeHeader], values: Any, raise_exception: bool) -> bool:
    is_valid: bool = True
    en: Any = get_enumerator(values)
    while en.System_Collections_IEnumerator_MoveNext() if is_valid else False:
        matchValue: tuple[int, int]
        copy_of_struct: Any = en.System_Collections_Generic_IEnumerator_1_get_Current()
        match_value = copy_of_struct[0]
        cell: CompositeCell
        copy_of_struct_1: Any = en.System_Collections_Generic_IEnumerator_1_get_Current()
        cell = copy_of_struct_1[1]
        header: CompositeHeader = headers[match_value[0]]
        header_is_data: bool = header.IsDataColumn
        header_is_freetext: bool = (not header.IsDataColumn) if (not header.IsTermColumn) else False
        cell_is_not_freetext: bool = not cell.is_free_text
        if (cell_is_not_freetext if (not cell.is_data) else False) if header_is_data else False:
            def _arrow729(message: str, headers: Any=headers, values: Any=values, raise_exception: Any=raise_exception) -> None:
                raise Exception(message)

            def _arrow731(__unit: None=None, headers: Any=headers, values: Any=values, raise_exception: Any=raise_exception) -> Callable[[str], None]:
                clo: Callable[[str], None] = to_console(printf("%s"))
                def _arrow730(arg: str) -> None:
                    clo(arg)

                return _arrow730

            (_arrow729 if raise_exception else _arrow731())(((("Invalid combination of header `" + str(header)) + "` and cell `") + str(cell)) + "`. Data header should contain either Data or Freetext cells.")
            is_valid = False

        if cell_is_not_freetext if header_is_freetext else False:
            def _arrow732(message_1: str, headers: Any=headers, values: Any=values, raise_exception: Any=raise_exception) -> None:
                raise Exception(message_1)

            def _arrow734(__unit: None=None, headers: Any=headers, values: Any=values, raise_exception: Any=raise_exception) -> Callable[[str], None]:
                clo_1: Callable[[str], None] = to_console(printf("%s"))
                def _arrow733(arg_1: str) -> None:
                    clo_1(arg_1)

                return _arrow733

            (_arrow732 if raise_exception else _arrow734())(((("Invalid combination of header `" + str(header)) + "` and cell `") + str(cell)) + "`. Freetext header should not contain non-freetext cells.")
            is_valid = False

    return is_valid


def Unchecked_tryGetCellAt(column: int, row: int, cells: Any) -> CompositeCell | None:
    return Dictionary_tryFind((column, row), cells)


def Unchecked_setCellAt(column_index: int, row_index: int, c: CompositeCell, cells: Any) -> None:
    cells[column_index, row_index] = c


def Unchecked_addCellAt(column_index: int, row_index: int, c: CompositeCell, cells: Any) -> None:
    add_to_dict(cells, (column_index, row_index), c)


def Unchecked_moveCellTo(from_col: int, from_row: int, to_col: int, to_row: int, cells: Any) -> None:
    match_value: CompositeCell | None = Dictionary_tryFind((from_col, from_row), cells)
    if match_value is None:
        pass

    else: 
        c: CompositeCell = match_value
        ignore(remove_from_dict(cells, (from_col, from_row)))
        value_1: None = Unchecked_setCellAt(to_col, to_row, c, cells)
        ignore(None)



def Unchecked_removeHeader(index: int, headers: Array[CompositeHeader]) -> None:
    headers.pop(index)


def Unchecked_removeColumnCells(index: int, cells: Any) -> None:
    enumerator: Any = get_enumerator(cells)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            active_pattern_result: tuple[tuple[int, int], CompositeCell] = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            c: int = active_pattern_result[0][0] or 0
            if c == index:
                ignore(remove_from_dict(cells, (c, active_pattern_result[0][1])))


    finally: 
        dispose(enumerator)



def Unchecked_removeColumnCells_withIndexChange(index: int, column_count: int, row_count: int, cells: Any) -> None:
    for col in range(index, (column_count - 1) + 1, 1):
        for row in range(0, (row_count - 1) + 1, 1):
            if col == index:
                ignore(remove_from_dict(cells, (col, row)))

            elif col > index:
                Unchecked_moveCellTo(col, row, col - 1, row, cells)



def Unchecked_removeRowCells(row_index: int, cells: Any) -> None:
    enumerator: Any = get_enumerator(cells)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            active_pattern_result: tuple[tuple[int, int], CompositeCell] = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            r: int = active_pattern_result[0][1] or 0
            if r == row_index:
                ignore(remove_from_dict(cells, (active_pattern_result[0][0], r)))


    finally: 
        dispose(enumerator)



def Unchecked_removeRowCells_withIndexChange(row_index: int, column_count: int, row_count: int, cells: Any) -> None:
    for row in range(row_index, (row_count - 1) + 1, 1):
        for col in range(0, (column_count - 1) + 1, 1):
            if row == row_index:
                ignore(remove_from_dict(cells, (col, row)))

            elif row > row_index:
                Unchecked_moveCellTo(col, row, col, row - 1, cells)



def Unchecked_getEmptyCellForHeader(header: CompositeHeader, colum_cell_option: CompositeCell | None=None) -> CompositeCell:
    match_value: bool = header.IsTermColumn
    if match_value:
        (pattern_matching_result,) = (None,)
        if colum_cell_option is None:
            pattern_matching_result = 0

        elif colum_cell_option.tag == 0:
            pattern_matching_result = 0

        elif colum_cell_option.tag == 2:
            pattern_matching_result = 1

        else: 
            pattern_matching_result = 2

        if pattern_matching_result == 0:
            return CompositeCell.empty_term()

        elif pattern_matching_result == 1:
            return CompositeCell.empty_unitized()

        elif pattern_matching_result == 2:
            raise Exception("[extendBodyCells] This should never happen, IsTermColumn header must be paired with either term or unitized cell.")


    else: 
        return CompositeCell.empty_free_text()



def Unchecked_addColumn(new_header: CompositeHeader, new_cells: Array[CompositeCell], index: int, force_replace: bool, only_headers: bool, headers: Array[CompositeHeader], values: Any) -> None:
    number_of_new_columns: int = 1
    index_1: int = index or 0
    has_duplicate_unique: int | None = try_find_duplicate_unique(new_header, headers)
    if (has_duplicate_unique is not None) if (not force_replace) else False:
        raise Exception(((("Invalid new column `" + str(new_header)) + "`. Table already contains header of the same type on index `") + str(value_2(has_duplicate_unique))) + "`")

    if has_duplicate_unique is not None:
        number_of_new_columns = 0
        index_1 = value_2(has_duplicate_unique) or 0

    match_value: int = get_column_count(headers) or 0
    match_value_1: int = get_row_count(values) or 0
    start_col_count: int = match_value or 0
    if has_duplicate_unique is not None:
        Unchecked_removeHeader(index_1, headers)

    headers.insert(index_1, new_header)
    if (has_duplicate_unique is None) if (index_1 < start_col_count) else False:
        def _arrow735(x: int, y: int, new_header: Any=new_header, new_cells: Any=new_cells, index: Any=index, force_replace: Any=force_replace, only_headers: Any=only_headers, headers: Any=headers, values: Any=values) -> int:
            return compare_primitives(x, y)

        last_column_index: int = max(_arrow735, start_col_count - 1, 0) or 0
        for column_index in range(last_column_index, index_1 - 1, -1):
            for row_index in range(0, match_value_1 + 1, 1):
                Unchecked_moveCellTo(column_index, row_index, column_index + number_of_new_columns, row_index, values)

    if not only_headers:
        if has_duplicate_unique is not None:
            Unchecked_removeColumnCells(index_1, values)

        def _arrow737(tupled_arg: tuple[int, int, CompositeCell], new_header: Any=new_header, new_cells: Any=new_cells, index: Any=index, force_replace: Any=force_replace, only_headers: Any=only_headers, headers: Any=headers, values: Any=values) -> Callable[[Any], None]:
            def _arrow736(values_1: Any) -> None:
                value: None = add_to_dict(values_1, (tupled_arg[0], tupled_arg[1]), tupled_arg[2])
                ignore(None)

            return _arrow736

        def _arrow739(tupled_arg_1: tuple[int, int, CompositeCell], new_header: Any=new_header, new_cells: Any=new_cells, index: Any=index, force_replace: Any=force_replace, only_headers: Any=only_headers, headers: Any=headers, values: Any=values) -> Callable[[Any], None]:
            def _arrow738(cells: Any) -> None:
                Unchecked_setCellAt(tupled_arg_1[0], tupled_arg_1[1], tupled_arg_1[2], cells)

            return _arrow738

        f: Callable[[tuple[int, int, CompositeCell], Any], None] = _arrow737 if (index_1 >= start_col_count) else _arrow739
        def action(row_index_3: int, cell_1: CompositeCell, new_header: Any=new_header, new_cells: Any=new_cells, index: Any=index, force_replace: Any=force_replace, only_headers: Any=only_headers, headers: Any=headers, values: Any=values) -> None:
            f((index_1, row_index_3, cell_1))(values)

        iterate_indexed(action, new_cells)



def Unchecked_fillMissingCells(headers: Array[CompositeHeader], values: Any) -> None:
    row_count: int = get_row_count(values) or 0
    column_count: int = get_column_count(headers) or 0
    def projection(tuple: tuple[int, int], headers: Any=headers, values: Any=values) -> int:
        return tuple[0]

    class ObjectExpr741:
        @property
        def Equals(self) -> Callable[[int, int], bool]:
            def _arrow740(x: int, y: int) -> bool:
                return x == y

            return _arrow740

        @property
        def GetHashCode(self) -> Callable[[int], int]:
            return number_hash

    class ObjectExpr742:
        @property
        def Compare(self) -> Callable[[int, int], int]:
            return compare_primitives

    column_key_groups: Any = of_array(Array_groupBy(projection, to_array(values.keys()), ObjectExpr741()), ObjectExpr742())
    for column_index in range(0, (column_count - 1) + 1, 1):
        header: CompositeHeader = headers[column_index]
        match_value: Array[tuple[int, int]] | None = try_find(column_index, column_key_groups)
        if match_value is None:
            default_cell_1: CompositeCell = Unchecked_getEmptyCellForHeader(header, None)
            for row_index_1 in range(0, (row_count - 1) + 1, 1):
                Unchecked_addCellAt(column_index, row_index_1, default_cell_1.Copy(), values)

        elif len(match_value) == row_count:
            col_1: Array[tuple[int, int]] = match_value

        else: 
            col_2: Array[tuple[int, int]] = match_value
            default_cell: CompositeCell = Unchecked_getEmptyCellForHeader(header, get_item_from_dict(values, head_1(col_2)))
            def _arrow743(tuple_1: tuple[int, int], headers: Any=headers, values: Any=values) -> int:
                return tuple_1[1]

            class ObjectExpr744:
                @property
                def Compare(self) -> Callable[[int, int], int]:
                    return compare_primitives

            row_keys: Any = of_array_1(map(_arrow743, col_2, Int32Array), ObjectExpr744())
            for row_index in range(0, (row_count - 1) + 1, 1):
                if not FSharpSet__Contains(row_keys, row_index):
                    Unchecked_addCellAt(column_index, row_index, default_cell.Copy(), values)




def Unchecked_extendToRowCount(row_count: int, headers: Array[CompositeHeader], values: Any) -> None:
    column_count: int = get_column_count(headers) or 0
    previous_row_count: int = get_row_count(values) or 0
    for column_index in range(0, (column_count - 1) + 1, 1):
        last_value: CompositeCell = get_item_from_dict(values, (column_index, previous_row_count - 1))
        for row_index in range(previous_row_count - 1, (row_count - 1) + 1, 1):
            Unchecked_setCellAt(column_index, row_index, last_value, values)


def Unchecked_addRow(index: int, new_cells: Array[CompositeCell], headers: Array[CompositeHeader], values: Any) -> None:
    row_count: int = get_row_count(values) or 0
    column_count: int = get_column_count(headers) or 0
    increase_row_indices: None
    if index < row_count:
        def _arrow745(x: int, y: int, index: Any=index, new_cells: Any=new_cells, headers: Any=headers, values: Any=values) -> int:
            return compare_primitives(x, y)

        last_row_index: int = max(_arrow745, row_count - 1, 0) or 0
        for row_index in range(last_row_index, index - 1, -1):
            for column_index in range(0, (column_count - 1) + 1, 1):
                Unchecked_moveCellTo(column_index, row_index, column_index, row_index + 1, values)

    else: 
        increase_row_indices = None

    def action(column_index_1: int, cell: CompositeCell, index: Any=index, new_cells: Any=new_cells, headers: Any=headers, values: Any=values) -> None:
        Unchecked_setCellAt(column_index_1, index, cell, values)

    set_new_cells: None = iterate_indexed(action, new_cells)


def Unchecked_addRows(index: int, new_rows: Array[Array[CompositeCell]], headers: Array[CompositeHeader], values: Any) -> None:
    row_count: int = get_row_count(values) or 0
    column_count: int = get_column_count(headers) or 0
    num_new_rows: int = len(new_rows) or 0
    increase_row_indices: None
    if index < row_count:
        def _arrow746(x: int, y: int, index: Any=index, new_rows: Any=new_rows, headers: Any=headers, values: Any=values) -> int:
            return compare_primitives(x, y)

        last_row_index: int = max(_arrow746, row_count - 1, 0) or 0
        for row_index in range(last_row_index, index - 1, -1):
            for column_index in range(0, (column_count - 1) + 1, 1):
                Unchecked_moveCellTo(column_index, row_index, column_index, row_index + num_new_rows, values)

    else: 
        increase_row_indices = None

    current_row_index: int = index or 0
    for idx in range(0, (len(new_rows) - 1) + 1, 1):
        def action(column_index_1: int, cell: CompositeCell, index: Any=index, new_rows: Any=new_rows, headers: Any=headers, values: Any=values) -> None:
            Unchecked_setCellAt(column_index_1, current_row_index, cell, values)

        set_new_cells: None = iterate_indexed(action, new_rows[idx])
        current_row_index = (current_row_index + 1) or 0


def Unchecked_compositeHeaderMainColumnEqual(ch1: CompositeHeader, ch2: CompositeHeader) -> bool:
    return to_string(ch1) == to_string(ch2)


def Unchecked_moveColumnTo(row_count: int, from_col: int, to_col: int, headers: Array[CompositeHeader], values: Any) -> None:
    pattern_input: tuple[int, int, int] = ((-1, from_col + 1, to_col)) if (from_col < to_col) else ((1, from_col - 1, to_col))
    shift_start: int = pattern_input[1] or 0
    shift_end: int = pattern_input[2] or 0
    shift: int = pattern_input[0] or 0
    header: CompositeHeader = headers[from_col]
    with get_enumerator(to_list(range_big_int(shift_start, op_unary_negation_int32(shift), shift_end))) as enumerator:
        while enumerator.System_Collections_IEnumerator_MoveNext():
            c: int = enumerator.System_Collections_Generic_IEnumerator_1_get_Current() or 0
            headers[c + shift] = headers[c]
    headers[to_col] = header
    for r in range(0, (row_count - 1) + 1, 1):
        cell: CompositeCell = get_item_from_dict(values, (from_col, r))
        with get_enumerator(to_list(range_big_int(shift_start, op_unary_negation_int32(shift), shift_end))) as enumerator_1:
            while enumerator_1.System_Collections_IEnumerator_MoveNext():
                c_1: int = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current() or 0
                values[c_1 + shift, r] = get_item_from_dict(values, (c_1, r))
        values[to_col, r] = cell


def Unchecked_alignByHeaders(keep_order: bool, rows: FSharpList[FSharpList[tuple[CompositeHeader, CompositeCell]]]) -> tuple[Array[CompositeHeader], Any]:
    headers: Array[CompositeHeader] = []
    class ObjectExpr747:
        @property
        def Equals(self) -> Callable[[tuple[int, int], tuple[int, int]], bool]:
            return equal_arrays

        @property
        def GetHashCode(self) -> Callable[[tuple[int, int]], int]:
            return array_hash

    values: Any = Dictionary([], ObjectExpr747())
    def loop(col_i_mut: int, rows_2_mut: FSharpList[FSharpList[tuple[CompositeHeader, CompositeCell]]], keep_order: Any=keep_order, rows: Any=rows) -> tuple[Array[CompositeHeader], Any]:
        while True:
            (col_i, rows_2) = (col_i_mut, rows_2_mut)
            def _arrow748(arg: FSharpList[tuple[CompositeHeader, CompositeCell]], col_i: Any=col_i, rows_2: Any=rows_2) -> bool:
                return not is_empty(arg)

            if not exists(_arrow748, rows_2):
                return (headers, values)

            else: 
                def _arrow749(l: FSharpList[tuple[CompositeHeader, CompositeCell]], col_i: Any=col_i, rows_2: Any=rows_2) -> tuple[CompositeHeader, CompositeCell] | None:
                    return None if is_empty(l) else head(l)

                first_elem: CompositeHeader = pick(_arrow749, rows_2)[0]
                (headers.append(first_elem))
                col_i_mut = col_i + 1
                def mapping(row_i: int, l_1: FSharpList[tuple[CompositeHeader, CompositeCell]], col_i: Any=col_i, rows_2: Any=rows_2) -> FSharpList[tuple[CompositeHeader, CompositeCell]]:
                    if keep_order:
                        if not is_empty(l_1):
                            if Unchecked_compositeHeaderMainColumnEqual(head(l_1)[0], first_elem):
                                add_to_dict(values, (col_i, row_i), head(l_1)[1])
                                return tail_1(l_1)

                            else: 
                                return l_1


                        else: 
                            return empty()


                    else: 
                        def f(tupled_arg: tuple[CompositeHeader, CompositeCell], row_i: Any=row_i, l_1: Any=l_1) -> CompositeCell | None:
                            if Unchecked_compositeHeaderMainColumnEqual(tupled_arg[0], first_elem):
                                return tupled_arg[1]

                            else: 
                                return None


                        pattern_input: tuple[CompositeCell | None, FSharpList[tuple[CompositeHeader, CompositeCell]]] = List_tryPickAndRemove(f, l_1)
                        new_l: FSharpList[tuple[CompositeHeader, CompositeCell]] = pattern_input[1]
                        first_match: CompositeCell | None = pattern_input[0]
                        if first_match is None:
                            return new_l

                        else: 
                            add_to_dict(values, (col_i, row_i), first_match)
                            return new_l



                rows_2_mut = map_indexed(mapping, rows_2)
                continue

            break

    return loop(0, rows)


__all__ = ["get_column_count", "get_row_count", "box_hash_values", "_007CIsUniqueExistingHeader_007C__007C", "try_find_duplicate_unique", "try_find_duplicate_unique_in_array", "SanityChecks_validateColumnIndex", "SanityChecks_validateRowIndex", "SanityChecks_validateColumn", "SanityChecks_validate", "Unchecked_tryGetCellAt", "Unchecked_setCellAt", "Unchecked_addCellAt", "Unchecked_moveCellTo", "Unchecked_removeHeader", "Unchecked_removeColumnCells", "Unchecked_removeColumnCells_withIndexChange", "Unchecked_removeRowCells", "Unchecked_removeRowCells_withIndexChange", "Unchecked_getEmptyCellForHeader", "Unchecked_addColumn", "Unchecked_fillMissingCells", "Unchecked_extendToRowCount", "Unchecked_addRow", "Unchecked_addRows", "Unchecked_compositeHeaderMainColumnEqual", "Unchecked_moveColumnTo", "Unchecked_alignByHeaders"]

