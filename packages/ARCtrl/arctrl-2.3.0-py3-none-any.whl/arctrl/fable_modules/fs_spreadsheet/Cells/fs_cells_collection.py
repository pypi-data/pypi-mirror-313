from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_library.map_util import (get_item_from_dict, add_to_dict, remove_from_dict, add_to_set)
from ...fable_library.option import some
from ...fable_library.range import range_big_int
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.seq import (map, iterate, is_empty, max, collect, delay, empty, singleton, min, min_by)
from ...fable_library.util import (ignore, IEnumerable_1, compare_primitives)
from ..fs_address import (FsAddress__get_RowNumber, FsAddress__get_ColumnNumber, FsAddress, FsAddress__ctor_Z37302880)
from .fs_cell import FsCell

def Dictionary_tryGet(k: Any, dict_1: Any) -> Any | None:
    if k in dict_1:
        return some(get_item_from_dict(dict_1, k))

    else: 
        return None



def _expr148() -> TypeInfo:
    return class_type("FsSpreadsheet.FsCellsCollection", None, FsCellsCollection)


class FsCellsCollection:
    def __init__(self, __unit: None=None) -> None:
        self._columnsUsed: Any = dict([])
        self._deleted: Any = dict([])
        self._rowsCollection: Any = dict([])
        self._maxColumnUsed: int = 0
        self._maxRowUsed: int = 0
        self._rowsUsed: Any = dict([])
        self._count: int = 0


FsCellsCollection_reflection = _expr148

def FsCellsCollection__ctor(__unit: None=None) -> FsCellsCollection:
    return FsCellsCollection(__unit)


def FsCellsCollection__get_Count(this: FsCellsCollection) -> int:
    return this._count


def FsCellsCollection__set_Count_Z524259A4(this: FsCellsCollection, count: int) -> None:
    this._count = count or 0


def FsCellsCollection__get_MaxRowNumber(this: FsCellsCollection) -> int:
    return this._maxRowUsed


def FsCellsCollection__get_MaxColumnNumber(this: FsCellsCollection) -> int:
    return this._maxColumnUsed


def FsCellsCollection__Copy(this: FsCellsCollection) -> FsCellsCollection:
    def mapping(c: FsCell, this: Any=this) -> FsCell:
        return c.Copy()

    return FsCellsCollection_createFromCells_Z21F271A4(map(mapping, FsCellsCollection__GetCells(this)))


def FsCellsCollection_copy_Z2740B3CA(cells_collection: FsCellsCollection) -> FsCellsCollection:
    return FsCellsCollection__Copy(cells_collection)


def FsCellsCollection_IncrementUsage_71185086(dictionary: Any, key: int) -> None:
    match_value: int | None = Dictionary_tryGet(key, dictionary)
    if match_value is None:
        add_to_dict(dictionary, key, 1)

    else: 
        count: int = match_value or 0
        dictionary[key] = count + 1



def FsCellsCollection_DecrementUsage_71185086(dictionary: Any, key: int) -> bool:
    match_value: int | None = Dictionary_tryGet(key, dictionary)
    if match_value is None:
        return False

    elif match_value > 1:
        count_1: int = match_value or 0
        dictionary[key] = count_1 - 1
        return False

    else: 
        ignore(remove_from_dict(dictionary, key))
        return True



def FsCellsCollection_createFromCells_Z21F271A4(cells: IEnumerable_1[FsCell]) -> FsCellsCollection:
    fcc: FsCellsCollection = FsCellsCollection__ctor()
    FsCellsCollection__Add_Z21F271A4(fcc, cells)
    return fcc


def FsCellsCollection__Clear(this: FsCellsCollection) -> FsCellsCollection:
    this._count = 0
    this._rowsUsed.clear()
    this._columnsUsed.clear()
    this._rowsCollection.clear()
    this._maxRowUsed = 0
    this._maxColumnUsed = 0
    return this


def FsCellsCollection__Add_2E78CE33(this: FsCellsCollection, row: int, column: int, cell: FsCell) -> None:
    cell.RowNumber = row or 0
    cell.ColumnNumber = column or 0
    this._count = (this._count + 1) or 0
    FsCellsCollection_IncrementUsage_71185086(this._rowsUsed, row)
    FsCellsCollection_IncrementUsage_71185086(this._columnsUsed, column)
    def _arrow149(__unit: None=None, this: Any=this, row: Any=row, column: Any=column, cell: Any=cell) -> Any:
        match_value: Any | None = Dictionary_tryGet(row, this._rowsCollection)
        if match_value is None:
            columns_collection_1: Any = dict([])
            add_to_dict(this._rowsCollection, row, columns_collection_1)
            return columns_collection_1

        else: 
            return match_value


    add_to_dict(_arrow149(), column, cell)
    if row > this._maxRowUsed:
        this._maxRowUsed = row or 0

    if column > this._maxColumnUsed:
        this._maxColumnUsed = column or 0

    match_value_1: Any | None = Dictionary_tryGet(row, this._deleted)
    if match_value_1 is None:
        pass

    else: 
        del_hash: Any = match_value_1
        ignore(del_hash.delete(column))



def FsCellsCollection_addCellWithIndeces(row_index: int, col_index: int, cell: FsCell, cells_collection: FsCellsCollection) -> None:
    FsCellsCollection__Add_2E78CE33(cells_collection, row_index, col_index, cell)


def FsCellsCollection__Add_Z334DF64D(this: FsCellsCollection, cell: FsCell) -> None:
    FsCellsCollection__Add_2E78CE33(this, FsAddress__get_RowNumber(cell.Address), FsAddress__get_ColumnNumber(cell.Address), cell)


def FsCellsCollection_addCell(cell: FsCell, cells_collection: FsCellsCollection) -> FsCellsCollection:
    FsCellsCollection__Add_Z334DF64D(cells_collection, cell)
    return cells_collection


def FsCellsCollection__Add_Z21F271A4(this: FsCellsCollection, cells: IEnumerable_1[FsCell]) -> None:
    def action(arg: FsCell, this: Any=this, cells: Any=cells) -> None:
        value: None = FsCellsCollection__Add_Z334DF64D(this, arg)
        ignore(None)

    iterate(action, cells)


def FsCellsCollection_addCells(cells: IEnumerable_1[FsCell], cells_collection: FsCellsCollection) -> FsCellsCollection:
    FsCellsCollection__Add_Z21F271A4(cells_collection, cells)
    return cells_collection


def FsCellsCollection__ContainsCellAt_Z37302880(this: FsCellsCollection, row_index: int, col_index: int) -> bool:
    match_value: Any | None = Dictionary_tryGet(row_index, this._rowsCollection)
    if match_value is None:
        return False

    else: 
        cols_collection: Any = match_value
        return cols_collection.has(col_index)



def FsCellsCollection_containsCellAt(row_index: int, col_index: int, cells_collection: FsCellsCollection) -> bool:
    return FsCellsCollection__ContainsCellAt_Z37302880(cells_collection, row_index, col_index)


def FsCellsCollection__RemoveCellAt_Z37302880(this: FsCellsCollection, row: int, column: int) -> None:
    this._count = (this._count - 1) or 0
    row_removed: bool = FsCellsCollection_DecrementUsage_71185086(this._rowsUsed, row)
    column_removed: bool = FsCellsCollection_DecrementUsage_71185086(this._columnsUsed, column)
    if (row == this._maxRowUsed) if row_removed else False:
        class ObjectExpr151:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        this._maxRowUsed = (max(this._rowsUsed.keys(), ObjectExpr151()) if (not is_empty(this._rowsUsed.keys())) else 0) or 0

    if (column == this._maxColumnUsed) if column_removed else False:
        class ObjectExpr152:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        this._maxColumnUsed = (max(this._columnsUsed.keys(), ObjectExpr152()) if (not is_empty(this._columnsUsed.keys())) else 0) or 0

    match_value: Any | None = Dictionary_tryGet(row, this._deleted)
    if match_value is None:
        del_hash_3: Any = set([])
        ignore(add_to_set(column, del_hash_3))
        add_to_dict(this._deleted, row, del_hash_3)

    else: 
        def _arrow153(__unit: None=None, this: Any=this, row: Any=row, column: Any=column) -> bool:
            del_hash: Any = match_value
            return del_hash.has(column)

        if _arrow153():
            del_hash_1: Any = match_value

        else: 
            del_hash_2: Any = match_value
            ignore(add_to_set(column, del_hash_2))


    match_value_1: Any | None = Dictionary_tryGet(row, this._rowsCollection)
    if match_value_1 is None:
        pass

    else: 
        columns_collection: Any = match_value_1
        ignore(remove_from_dict(columns_collection, column))
        if len(columns_collection) == 0:
            ignore(remove_from_dict(this._rowsCollection, row))




def FsCellsCollection_removeCellAt(row_index: int, col_index: int, cells_collection: FsCellsCollection) -> FsCellsCollection:
    FsCellsCollection__RemoveCellAt_Z37302880(cells_collection, row_index, col_index)
    return cells_collection


def FsCellsCollection__TryRemoveValueAt_Z37302880(this: FsCellsCollection, row_index: int, col_index: int) -> None:
    match_value: Any | None = Dictionary_tryGet(row_index, this._rowsCollection)
    if match_value is None:
        pass

    else: 
        cols_collection: Any = match_value
        try: 
            get_item_from_dict(cols_collection, col_index).Value = ""

        except Exception as match_value_1:
            pass




def FsCellsCollection_tryRemoveValueAt(row_index: int, col_index: int, cells_collection: FsCellsCollection) -> FsCellsCollection:
    FsCellsCollection__TryRemoveValueAt_Z37302880(cells_collection, row_index, col_index)
    return cells_collection


def FsCellsCollection__RemoveValueAt_Z37302880(this: FsCellsCollection, row_index: int, col_index: int) -> None:
    get_item_from_dict(get_item_from_dict(this._rowsCollection, row_index), col_index).Value = ""


def FsCellsCollection_removeValueAt(row_index: int, col_index: int, cells_collection: FsCellsCollection) -> FsCellsCollection:
    FsCellsCollection__RemoveValueAt_Z37302880(cells_collection, row_index, col_index)
    return cells_collection


def FsCellsCollection__GetCells(this: FsCellsCollection) -> IEnumerable_1[FsCell]:
    def mapping(columns_collection: Any, this: Any=this) -> Any:
        return columns_collection.values()

    return collect(mapping, this._rowsCollection.values())


def FsCellsCollection_getCells_Z2740B3CA(cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
    return FsCellsCollection__GetCells(cells_collection)


def FsCellsCollection__GetCells_6611854F(this: FsCellsCollection, row_start: int, column_start: int, row_end: int, column_end: int, predicate: Callable[[FsCell], bool]) -> IEnumerable_1[FsCell]:
    final_row: int = (this._maxRowUsed if (row_end > this._maxRowUsed) else row_end) or 0
    final_column: int = (this._maxColumnUsed if (column_end > this._maxColumnUsed) else column_end) or 0
    def _arrow156(__unit: None=None, this: Any=this, row_start: Any=row_start, column_start: Any=column_start, row_end: Any=row_end, column_end: Any=column_end, predicate: Any=predicate) -> IEnumerable_1[FsCell]:
        def _arrow155(ro: int) -> IEnumerable_1[FsCell]:
            match_value: Any | None = Dictionary_tryGet(ro, this._rowsCollection)
            if match_value is None:
                return empty()

            else: 
                columns_collection: Any = match_value
                def _arrow154(co: int) -> IEnumerable_1[FsCell]:
                    match_value_1: FsCell | None = Dictionary_tryGet(co, columns_collection)
                    (pattern_matching_result, cell_1) = (None, None)
                    if match_value_1 is not None:
                        if predicate(match_value_1):
                            pattern_matching_result = 0
                            cell_1 = match_value_1

                        else: 
                            pattern_matching_result = 1


                    else: 
                        pattern_matching_result = 1

                    if pattern_matching_result == 0:
                        return singleton(cell_1)

                    elif pattern_matching_result == 1:
                        return empty()


                return collect(_arrow154, range_big_int(column_start, 1, final_column))


        return collect(_arrow155, range_big_int(row_start, 1, final_row))

    return delay(_arrow156)


def FsCellsCollection_filterCellsFromTo(row_start: int, column_start: int, row_end: int, column_end: int, predicate: Callable[[FsCell], bool], cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
    return FsCellsCollection__GetCells_6611854F(cells_collection, row_start, column_start, row_end, column_end, predicate)


def FsCellsCollection__GetCells_24D826EF(this: FsCellsCollection, start_address: FsAddress, last_address: FsAddress, predicate: Callable[[FsCell], bool]) -> IEnumerable_1[FsCell]:
    return FsCellsCollection__GetCells_6611854F(this, FsAddress__get_RowNumber(start_address), FsAddress__get_ColumnNumber(start_address), FsAddress__get_RowNumber(last_address), FsAddress__get_ColumnNumber(last_address), predicate)


def FsCellsCollection_filterCellsFromToAddress(start_address: FsAddress, last_address: FsAddress, predicate: Callable[[FsCell], bool], cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
    return FsCellsCollection__GetCells_24D826EF(cells_collection, start_address, last_address, predicate)


def FsCellsCollection__GetCells_Z6C21C500(this: FsCellsCollection, row_start: int, column_start: int, row_end: int, column_end: int) -> IEnumerable_1[FsCell]:
    final_row: int = (this._maxRowUsed if (row_end > this._maxRowUsed) else row_end) or 0
    final_column: int = (this._maxColumnUsed if (column_end > this._maxColumnUsed) else column_end) or 0
    def _arrow159(__unit: None=None, this: Any=this, row_start: Any=row_start, column_start: Any=column_start, row_end: Any=row_end, column_end: Any=column_end) -> IEnumerable_1[FsCell]:
        def _arrow158(ro: int) -> IEnumerable_1[FsCell]:
            match_value: Any | None = Dictionary_tryGet(ro, this._rowsCollection)
            if match_value is None:
                return empty()

            else: 
                columns_collection: Any = match_value
                def _arrow157(co: int) -> IEnumerable_1[FsCell]:
                    match_value_1: FsCell | None = Dictionary_tryGet(co, columns_collection)
                    if match_value_1 is not None:
                        return singleton(match_value_1)

                    else: 
                        return empty()


                return collect(_arrow157, range_big_int(column_start, 1, final_column))


        return collect(_arrow158, range_big_int(row_start, 1, final_row))

    return delay(_arrow159)


def FsCellsCollection_getCellsFromTo(row_start: int, column_start: int, row_end: int, column_end: int, cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
    return FsCellsCollection__GetCells_Z6C21C500(cells_collection, row_start, column_start, row_end, column_end)


def FsCellsCollection__GetCells_7E77A4A0(this: FsCellsCollection, start_address: FsAddress, last_address: FsAddress) -> IEnumerable_1[FsCell]:
    return FsCellsCollection__GetCells_Z6C21C500(this, FsAddress__get_RowNumber(start_address), FsAddress__get_ColumnNumber(start_address), FsAddress__get_RowNumber(last_address), FsAddress__get_ColumnNumber(last_address))


def FsCellsCollection_getCellsFromToAddress(start_address: FsAddress, last_address: FsAddress, cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
    return FsCellsCollection__GetCells_7E77A4A0(cells_collection, start_address, last_address)


def FsCellsCollection__TryGetCell_Z37302880(this: FsCellsCollection, row: int, column: int) -> FsCell | None:
    if True if (row > this._maxRowUsed) else (column > this._maxColumnUsed):
        return None

    else: 
        match_value: Any | None = Dictionary_tryGet(row, this._rowsCollection)
        if match_value is None:
            return None

        else: 
            match_value_1: FsCell | None = Dictionary_tryGet(column, match_value)
            if match_value_1 is None:
                return None

            else: 
                return match_value_1





def FsCellsCollection_tryGetCell(row_index: int, col_index: int, cells_collection: FsCellsCollection) -> FsCell | None:
    return FsCellsCollection__TryGetCell_Z37302880(cells_collection, row_index, col_index)


def FsCellsCollection__GetCellsInColumn_Z524259A4(this: FsCellsCollection, col_index: int) -> IEnumerable_1[FsCell]:
    return FsCellsCollection__GetCells_Z6C21C500(this, 1, col_index, this._maxRowUsed, col_index)


def FsCellsCollection_getCellsInColumn(col_index: int, cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
    return FsCellsCollection__GetCellsInColumn_Z524259A4(cells_collection, col_index)


def FsCellsCollection__GetCellsInRow_Z524259A4(this: FsCellsCollection, row_index: int) -> IEnumerable_1[FsCell]:
    return FsCellsCollection__GetCells_Z6C21C500(this, row_index, 1, row_index, this._maxColumnUsed)


def FsCellsCollection_getCellsInRow(row_index: int, cells_collection: FsCellsCollection) -> IEnumerable_1[FsCell]:
    return FsCellsCollection__GetCellsInRow_Z524259A4(cells_collection, row_index)


def FsCellsCollection__GetFirstAddress(this: FsCellsCollection) -> FsAddress:
    if True if is_empty(this._rowsCollection) else is_empty(this._rowsCollection.keys()):
        return FsAddress__ctor_Z37302880(0, 0)

    else: 
        class ObjectExpr161:
            @property
            def Compare(self) -> Callable[[int, int], int]:
                return compare_primitives

        def _arrow165(__unit: None=None, this: Any=this) -> int:
            def projection(d: Any) -> int:
                class ObjectExpr162:
                    @property
                    def Compare(self) -> Callable[[int, int], int]:
                        return compare_primitives

                return min(d.keys(), ObjectExpr162())

            class ObjectExpr163:
                @property
                def Compare(self) -> Callable[[int, int], int]:
                    return compare_primitives

            d_1: Any = min_by(projection, this._rowsCollection.values(), ObjectExpr163())
            class ObjectExpr164:
                @property
                def Compare(self) -> Callable[[int, int], int]:
                    return compare_primitives

            return min(d_1.keys(), ObjectExpr164())

        return FsAddress__ctor_Z37302880(min(this._rowsCollection.keys(), ObjectExpr161()), _arrow165())



def FsCellsCollection_getFirstAddress_Z2740B3CA(cells: FsCellsCollection) -> FsAddress:
    return FsCellsCollection__GetFirstAddress(cells)


def FsCellsCollection__GetLastAddress(this: FsCellsCollection) -> FsAddress:
    return FsAddress__ctor_Z37302880(FsCellsCollection__get_MaxRowNumber(this), FsCellsCollection__get_MaxColumnNumber(this))


def FsCellsCollection_getLastAddress_Z2740B3CA(cells: FsCellsCollection) -> FsAddress:
    return FsCellsCollection__GetLastAddress(cells)


__all__ = ["Dictionary_tryGet", "FsCellsCollection_reflection", "FsCellsCollection__get_Count", "FsCellsCollection__set_Count_Z524259A4", "FsCellsCollection__get_MaxRowNumber", "FsCellsCollection__get_MaxColumnNumber", "FsCellsCollection__Copy", "FsCellsCollection_copy_Z2740B3CA", "FsCellsCollection_IncrementUsage_71185086", "FsCellsCollection_DecrementUsage_71185086", "FsCellsCollection_createFromCells_Z21F271A4", "FsCellsCollection__Clear", "FsCellsCollection__Add_2E78CE33", "FsCellsCollection_addCellWithIndeces", "FsCellsCollection__Add_Z334DF64D", "FsCellsCollection_addCell", "FsCellsCollection__Add_Z21F271A4", "FsCellsCollection_addCells", "FsCellsCollection__ContainsCellAt_Z37302880", "FsCellsCollection_containsCellAt", "FsCellsCollection__RemoveCellAt_Z37302880", "FsCellsCollection_removeCellAt", "FsCellsCollection__TryRemoveValueAt_Z37302880", "FsCellsCollection_tryRemoveValueAt", "FsCellsCollection__RemoveValueAt_Z37302880", "FsCellsCollection_removeValueAt", "FsCellsCollection__GetCells", "FsCellsCollection_getCells_Z2740B3CA", "FsCellsCollection__GetCells_6611854F", "FsCellsCollection_filterCellsFromTo", "FsCellsCollection__GetCells_24D826EF", "FsCellsCollection_filterCellsFromToAddress", "FsCellsCollection__GetCells_Z6C21C500", "FsCellsCollection_getCellsFromTo", "FsCellsCollection__GetCells_7E77A4A0", "FsCellsCollection_getCellsFromToAddress", "FsCellsCollection__TryGetCell_Z37302880", "FsCellsCollection_tryGetCell", "FsCellsCollection__GetCellsInColumn_Z524259A4", "FsCellsCollection_getCellsInColumn", "FsCellsCollection__GetCellsInRow_Z524259A4", "FsCellsCollection_getCellsInRow", "FsCellsCollection__GetFirstAddress", "FsCellsCollection_getFirstAddress_Z2740B3CA", "FsCellsCollection__GetLastAddress", "FsCellsCollection_getLastAddress_Z2740B3CA"]

