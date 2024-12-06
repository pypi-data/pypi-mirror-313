from __future__ import annotations
from ..fable_modules.fable_library.seq import try_pick
from ..fable_modules.fable_library.string_ import (to_fail, printf)
from ..fable_modules.fs_spreadsheet.fs_workbook import FsWorkbook
from ..fable_modules.fs_spreadsheet.fs_worksheet import FsWorksheet
from ..Core.data_map import DataMap
from .DataMapTable.data_map_table import (try_from_fs_worksheet, to_fs_worksheet)

def from_fs_workbook(doc: FsWorkbook) -> DataMap:
    try: 
        data_map_table: DataMap | None = try_pick(try_from_fs_worksheet, doc.GetWorksheets())
        if data_map_table is None:
            raise Exception("No DataMapTable found in workbook")

        else: 
            return data_map_table


    except Exception as err:
        arg: str = str(err)
        return to_fail(printf("Could not parse datamap: \n%s"))(arg)



def to_fs_workbook(data_map: DataMap) -> FsWorkbook:
    doc: FsWorkbook = FsWorkbook()
    sheet: FsWorksheet = to_fs_worksheet(data_map)
    doc.AddWorksheet(sheet)
    return doc


__all__ = ["from_fs_workbook", "to_fs_workbook"]

