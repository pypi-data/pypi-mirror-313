from __future__ import annotations
from typing import Any
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.string_ import (to_text, printf)
from ...fable_library.util import int32_to_string
from ..fs_address import (FsAddress__get_RowNumber, FsAddress__ctor_Z37302880, FsAddress__get_ColumnNumber)
from .fs_range_address import (FsRangeAddress, FsRangeAddress__get_FirstAddress, FsRangeAddress__ctor_7E77A4A0, FsRangeAddress__get_LastAddress)
from .fs_range_base import (FsRangeBase, FsRangeBase_reflection, FsRangeBase__get_RangeAddress)
from .fs_range_row import (FsRangeRow__ctor_6A2513BC, FsRangeRow)

def _expr165() -> TypeInfo:
    return class_type("FsSpreadsheet.FsRange", None, FsRange, FsRangeBase_reflection())


class FsRange(FsRangeBase):
    def __init__(self, range_address: FsRangeAddress, style_value: Any=None) -> None:
        super().__init__(range_address)
        pass


FsRange_reflection = _expr165

def FsRange__ctor_Z1F5897D9(range_address: FsRangeAddress, style_value: Any=None) -> FsRange:
    return FsRange(range_address, style_value)


def FsRange__ctor_6A2513BC(range_address: FsRangeAddress) -> FsRange:
    return FsRange__ctor_Z1F5897D9(range_address, None)


def FsRange__ctor_65705F1F(range_base: FsRangeBase) -> FsRange:
    return FsRange__ctor_Z1F5897D9(FsRangeBase__get_RangeAddress(range_base), None)


def FsRange__Row_Z524259A4(self_1: FsRange, row: int) -> FsRangeRow:
    if True if (row <= 0) else (((row + FsAddress__get_RowNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(self_1)))) - 1) > 1048576):
        raise Exception(int32_to_string(row), to_text(printf("Row number must be between 1 and %i"))(1048576))

    return FsRangeRow__ctor_6A2513BC(FsRangeAddress__ctor_7E77A4A0(FsAddress__ctor_Z37302880((FsAddress__get_RowNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(self_1))) + row) - 1, FsAddress__get_ColumnNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(self_1)))), FsAddress__ctor_Z37302880((FsAddress__get_RowNumber(FsRangeAddress__get_FirstAddress(FsRangeBase__get_RangeAddress(self_1))) + row) - 1, FsAddress__get_ColumnNumber(FsRangeAddress__get_LastAddress(FsRangeBase__get_RangeAddress(self_1))))))


def FsRange__FirstRow(self_1: FsRange) -> FsRangeRow:
    return FsRange__Row_Z524259A4(self_1, 1)


__all__ = ["FsRange_reflection", "FsRange__ctor_6A2513BC", "FsRange__ctor_65705F1F", "FsRange__Row_Z524259A4", "FsRange__FirstRow"]

