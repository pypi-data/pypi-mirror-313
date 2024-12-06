from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.fable_library.array_ import (skip, map, try_item)
from ...fable_modules.fable_library.list import (of_array, singleton as singleton_1, FSharpList, map as map_2)
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.range import range_big_int
from ...fable_modules.fable_library.seq import (to_array, delay, map as map_1, exists, to_list, append, singleton)
from ...fable_modules.fable_library.types import (Array, to_string)
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.fs_spreadsheet.Cells.fs_cell import FsCell
from ...fable_modules.fs_spreadsheet.fs_column import FsColumn
from ...Core.Table.composite_cell import CompositeCell
from ...Core.Table.composite_column import CompositeColumn
from ...Core.Table.composite_header import (IOType, CompositeHeader)
from .composite_cell import to_string_cells as to_string_cells_1
from .composite_header import (from_string_cells, to_string_cells)

def fix_deprecated_ioheader(string_cell_col: Array[str]) -> Array[str]:
    if len(string_cell_col) == 0:
        raise Exception("Can\'t fix IOHeader Invalid column, neither header nor values given")

    values: Array[str] = skip(1, string_cell_col, None)
    match_value: IOType = IOType.of_string(string_cell_col[0])
    if match_value.tag == 4:
        return string_cell_col

    elif match_value.tag == 0:
        string_cell_col[0] = to_string(CompositeHeader(11, IOType(0)))
        return string_cell_col

    else: 
        string_cell_col[0] = to_string(CompositeHeader(12, match_value))
        return string_cell_col



def from_string_cell_columns(columns: Array[Array[str]]) -> CompositeColumn:
    def mapping(c: Array[str], columns: Any=columns) -> str:
        return c[0]

    pattern_input: tuple[CompositeHeader, Callable[[Array[str]], CompositeCell]] = from_string_cells(map(mapping, columns, None))
    l: int = len(columns[0]) or 0
    def _arrow1245(__unit: None=None, columns: Any=columns) -> IEnumerable_1[CompositeCell]:
        def _arrow1244(i: int) -> CompositeCell:
            def mapping_1(c_1: Array[str]) -> str:
                return c_1[i]

            return pattern_input[1](map(mapping_1, columns, None))

        return map_1(_arrow1244, range_big_int(1, 1, l - 1))

    cells: Array[CompositeCell] = to_array(delay(_arrow1245))
    return CompositeColumn.create(pattern_input[0], cells)


def from_fs_columns(columns: Array[FsColumn]) -> CompositeColumn:
    def mapping_1(c: FsColumn, columns: Any=columns) -> Array[str]:
        c.ToDenseColumn()
        def mapping(c_1: FsCell, c: Any=c) -> str:
            return c_1.ValueAsString()

        return map(mapping, to_array(c.Cells), None)

    return from_string_cell_columns(map(mapping_1, columns, None))


def to_string_cell_columns(column: CompositeColumn) -> FSharpList[FSharpList[str]]:
    def predicate(c: CompositeCell, column: Any=column) -> bool:
        return c.is_unitized

    has_unit: bool = exists(predicate, column.Cells)
    is_term: bool = column.Header.IsTermColumn
    def predicate_1(c_1: CompositeCell, column: Any=column) -> bool:
        return c_1.is_data

    is_data: bool = exists(predicate_1, column.Cells) if column.Header.IsDataColumn else False
    header: Array[str] = to_string_cells(has_unit, column.Header)
    def mapping(cell: CompositeCell, column: Any=column) -> Array[str]:
        return to_string_cells_1(is_term, has_unit, cell)

    cells: Array[Array[str]] = map(mapping, column.Cells, None)
    def get_cell_or_default(ri: int, ci: int, cells_1: Array[Array[str]], column: Any=column) -> str:
        return default_arg(try_item(ci, cells_1[ri]), "")

    if has_unit:
        def _arrow1251(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow1250(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow1249(i: int) -> str:
                    return get_cell_or_default(i, 0, cells)

                return map_1(_arrow1249, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[0]), delay(_arrow1250))

        def _arrow1254(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow1253(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow1252(i_1: int) -> str:
                    return get_cell_or_default(i_1, 1, cells)

                return map_1(_arrow1252, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[1]), delay(_arrow1253))

        def _arrow1257(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow1256(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow1255(i_2: int) -> str:
                    return get_cell_or_default(i_2, 2, cells)

                return map_1(_arrow1255, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[2]), delay(_arrow1256))

        def _arrow1260(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow1259(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow1258(i_3: int) -> str:
                    return get_cell_or_default(i_3, 3, cells)

                return map_1(_arrow1258, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[3]), delay(_arrow1259))

        return of_array([to_list(delay(_arrow1251)), to_list(delay(_arrow1254)), to_list(delay(_arrow1257)), to_list(delay(_arrow1260))])

    elif is_term:
        def _arrow1266(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow1265(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow1264(i_4: int) -> str:
                    return get_cell_or_default(i_4, 0, cells)

                return map_1(_arrow1264, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[0]), delay(_arrow1265))

        def _arrow1269(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow1268(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow1267(i_5: int) -> str:
                    return get_cell_or_default(i_5, 1, cells)

                return map_1(_arrow1267, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[1]), delay(_arrow1268))

        def _arrow1272(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow1271(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow1270(i_6: int) -> str:
                    return get_cell_or_default(i_6, 2, cells)

                return map_1(_arrow1270, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[2]), delay(_arrow1271))

        return of_array([to_list(delay(_arrow1266)), to_list(delay(_arrow1269)), to_list(delay(_arrow1272))])

    elif is_data:
        def _arrow1278(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow1277(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow1276(i_7: int) -> str:
                    return get_cell_or_default(i_7, 0, cells)

                return map_1(_arrow1276, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[0]), delay(_arrow1277))

        def _arrow1281(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow1280(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow1279(i_8: int) -> str:
                    return get_cell_or_default(i_8, 1, cells)

                return map_1(_arrow1279, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[1]), delay(_arrow1280))

        def _arrow1284(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow1283(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow1282(i_9: int) -> str:
                    return get_cell_or_default(i_9, 2, cells)

                return map_1(_arrow1282, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[2]), delay(_arrow1283))

        return of_array([to_list(delay(_arrow1278)), to_list(delay(_arrow1281)), to_list(delay(_arrow1284))])

    else: 
        def _arrow1287(__unit: None=None, column: Any=column) -> IEnumerable_1[str]:
            def _arrow1286(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow1285(i_10: int) -> str:
                    return cells[i_10][0]

                return map_1(_arrow1285, range_big_int(0, 1, len(column.Cells) - 1))

            return append(singleton(header[0]), delay(_arrow1286))

        return singleton_1(to_list(delay(_arrow1287)))



def to_fs_columns(column: CompositeColumn) -> FSharpList[FSharpList[FsCell]]:
    def mapping_1(c: FSharpList[str], column: Any=column) -> FSharpList[FsCell]:
        def mapping(s: str, c: Any=c) -> FsCell:
            return FsCell(s)

        return map_2(mapping, c)

    return map_2(mapping_1, to_string_cell_columns(column))


__all__ = ["fix_deprecated_ioheader", "from_string_cell_columns", "from_fs_columns", "to_string_cell_columns", "to_fs_columns"]

