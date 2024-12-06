from __future__ import annotations
from collections.abc import Callable
from math import pow
from typing import Any
from ..fable_library.char import (char_code_at, is_letter, is_digit)
from ..fable_library.int32 import parse
from ..fable_library.long import (op_addition, from_integer, to_int)
from ..fable_library.reflection import (TypeInfo, class_type)
from ..fable_library.reg_exp import create
from ..fable_library.seq import iterate
from ..fable_library.string_ import (to_text, printf, to_fail)
from ..fable_library.system_text import (StringBuilder__ctor, StringBuilder__Append_244C7CD6)
from ..fable_library.types import (uint32, to_string, int64)
from ..fable_library.util import ignore

CellReference_indexRegex: Any = create("([A-Z]*)(\\d*)")

def CellReference_colAdressToIndex(column_adress: str) -> uint32:
    length: int = len(column_adress) or 0
    sum: uint32 = uint32(0)
    for i in range(0, (length - 1) + 1, 1):
        c_1: str
        c: str = column_adress[(length - 1) - i]
        c_1 = c.upper()
        factor: uint32
        value: float = pow(26.0, i)
        factor = int(value+0x100000000 if value < 0 else value)
        sum = sum + (((int(char_code_at(c_1, 0)+0x100000000 if char_code_at(c_1, 0) < 0 else char_code_at(c_1, 0))) - uint32(64)) * factor)
    return sum


def CellReference_indexToColAdress(i: uint32) -> str:
    def loop(index_mut: uint32, acc_mut: str, i: Any=i) -> str:
        while True:
            (index, acc) = (index_mut, acc_mut)
            if index == uint32(0):
                return acc

            else: 
                mod26: uint32 = (index - uint32(1)) % uint32(26)
                index_mut = (index - uint32(1)) // uint32(26)
                acc_mut = chr((int(char_code_at("A", 0)+0x100000000 if char_code_at("A", 0) < 0 else char_code_at("A", 0))) + mod26) + acc
                continue

            break

    return loop(i, "")


def CellReference_ofIndices(column: uint32, row: uint32) -> str:
    arg: str = CellReference_indexToColAdress(column)
    return to_text(printf("%s%i"))(arg)(row)


def CellReference_toIndices(reference: str) -> tuple[uint32, uint32]:
    char_part: Any = StringBuilder__ctor()
    num_part: Any = StringBuilder__ctor()
    def action(c: str, reference: Any=reference) -> None:
        if is_letter(c):
            ignore(StringBuilder__Append_244C7CD6(char_part, c))

        elif is_digit(c):
            ignore(StringBuilder__Append_244C7CD6(num_part, c))

        else: 
            to_fail(printf("Reference %s does not match Excel A1-style"))(reference)


    iterate(action, reference)
    return (CellReference_colAdressToIndex(to_string(char_part)), parse(to_string(num_part), 511, True, 32))


def CellReference_toColIndex(reference: str) -> uint32:
    return CellReference_toIndices(reference)[0]


def CellReference_toRowIndex(reference: str) -> uint32:
    return CellReference_toIndices(reference)[1]


def CellReference_setColIndex(col_i: uint32, reference: str) -> str:
    return CellReference_ofIndices(col_i, CellReference_toIndices(reference)[1])


def CellReference_setRowIndex(row_i: uint32, reference: str) -> str:
    return CellReference_ofIndices(CellReference_toIndices(reference)[0], row_i)


def CellReference_moveHorizontal(amount: int, reference: str) -> str:
    tupled_arg_1: tuple[uint32, uint32]
    tupled_arg: tuple[uint32, uint32] = CellReference_toIndices(reference)
    def _arrow52(__unit: None=None, amount: Any=amount, reference: Any=reference) -> uint32:
        value: int64 = op_addition(from_integer(tupled_arg[0], False, 6), from_integer(amount, False, 2))
        return int(to_int(value)+0x100000000 if to_int(value) < 0 else to_int(value))

    tupled_arg_1 = (_arrow52(), tupled_arg[1])
    return CellReference_ofIndices(tupled_arg_1[0], tupled_arg_1[1])


def CellReference_moveVertical(amount: int, reference: str) -> str:
    tupled_arg_1: tuple[uint32, uint32]
    tupled_arg: tuple[uint32, uint32] = CellReference_toIndices(reference)
    def _arrow53(__unit: None=None, amount: Any=amount, reference: Any=reference) -> uint32:
        value: int64 = op_addition(from_integer(tupled_arg[1], False, 6), from_integer(amount, False, 2))
        return int(to_int(value)+0x100000000 if to_int(value) < 0 else to_int(value))

    tupled_arg_1 = (tupled_arg[0], _arrow53())
    return CellReference_ofIndices(tupled_arg_1[0], tupled_arg_1[1])


def _expr54() -> TypeInfo:
    return class_type("FsSpreadsheet.FsAddress", None, FsAddress)


class FsAddress:
    def __init__(self, row_number: int, column_number: int, fixed_row: bool, fixed_column: bool) -> None:
        self._fixedRow: bool = fixed_row
        self._fixedColumn: bool = fixed_column
        self._rowNumber: int = row_number or 0
        self._columnNumber: int = column_number or 0
        self._trimmedAddress: str = ""


FsAddress_reflection = _expr54

def FsAddress__ctor_Z4C746FC0(row_number: int, column_number: int, fixed_row: bool, fixed_column: bool) -> FsAddress:
    return FsAddress(row_number, column_number, fixed_row, fixed_column)


def FsAddress__ctor_Z668C30D9(row_number: int, column_letter: str, fixed_row: bool, fixed_column: bool) -> FsAddress:
    return FsAddress__ctor_Z4C746FC0(row_number, int(CellReference_colAdressToIndex(column_letter)), fixed_row, fixed_column)


def FsAddress__ctor_Z37302880(row_number: int, column_number: int) -> FsAddress:
    return FsAddress__ctor_Z4C746FC0(row_number, column_number, False, False)


def FsAddress__ctor_Z721C83C5(cell_address_string: str) -> FsAddress:
    pattern_input: tuple[uint32, uint32] = CellReference_toIndices(cell_address_string)
    return FsAddress__ctor_Z37302880(int(pattern_input[1]), int(pattern_input[0]))


def FsAddress__get_ColumnNumber(self_1: FsAddress) -> int:
    return self_1._columnNumber


def FsAddress__set_ColumnNumber_Z524259A4(self_1: FsAddress, col_i: int) -> None:
    self_1._columnNumber = col_i or 0


def FsAddress__get_RowNumber(self_1: FsAddress) -> int:
    return self_1._rowNumber


def FsAddress__set_RowNumber_Z524259A4(self_1: FsAddress, row_i: int) -> None:
    self_1._rowNumber = row_i or 0


def FsAddress__get_Address(self_1: FsAddress) -> str:
    return CellReference_ofIndices(int(self_1._columnNumber+0x100000000 if self_1._columnNumber < 0 else self_1._columnNumber), int(self_1._rowNumber+0x100000000 if self_1._rowNumber < 0 else self_1._rowNumber))


def FsAddress__set_Address_Z721C83C5(self_1: FsAddress, address: str) -> None:
    pattern_input: tuple[uint32, uint32] = CellReference_toIndices(address)
    self_1._rowNumber = int(pattern_input[1]) or 0
    self_1._columnNumber = int(pattern_input[0]) or 0


def FsAddress__get_FixedRow(self_1: FsAddress) -> bool:
    return False


def FsAddress__get_FixedColumn(self_1: FsAddress) -> bool:
    return False


def FsAddress__Copy(this: FsAddress) -> FsAddress:
    col_no: int = FsAddress__get_ColumnNumber(this) or 0
    return FsAddress__ctor_Z4C746FC0(FsAddress__get_RowNumber(this), col_no, FsAddress__get_FixedRow(this), FsAddress__get_FixedColumn(this))


def FsAddress_copy_6D30B323(address: FsAddress) -> FsAddress:
    return FsAddress__Copy(address)


def FsAddress__UpdateIndices_Z37302880(self_1: FsAddress, row_index: int, col_index: int) -> None:
    self_1._columnNumber = col_index or 0
    self_1._rowNumber = row_index or 0


def FsAddress_updateIndices(row_index: int, col_index: int, address: FsAddress) -> FsAddress:
    FsAddress__UpdateIndices_Z37302880(address, row_index, col_index)
    return address


def FsAddress__ToIndices(self_1: FsAddress) -> tuple[int, int]:
    return (self_1._rowNumber, self_1._columnNumber)


def FsAddress_toIndices_6D30B323(address: FsAddress) -> tuple[int, int]:
    return FsAddress__ToIndices(address)


def FsAddress__Compare_6D30B323(self_1: FsAddress, address: FsAddress) -> bool:
    if (FsAddress__get_FixedColumn(self_1) == FsAddress__get_FixedColumn(address)) if ((FsAddress__get_RowNumber(self_1) == FsAddress__get_RowNumber(address)) if ((FsAddress__get_ColumnNumber(self_1) == FsAddress__get_ColumnNumber(address)) if (FsAddress__get_Address(self_1) == FsAddress__get_Address(address)) else False) else False) else False:
        return FsAddress__get_FixedRow(self_1) == FsAddress__get_FixedRow(address)

    else: 
        return False



def FsAddress_compare(address1: FsAddress, address2: FsAddress) -> bool:
    return FsAddress__Compare_6D30B323(address1, address2)


__all__ = ["CellReference_indexRegex", "CellReference_colAdressToIndex", "CellReference_indexToColAdress", "CellReference_ofIndices", "CellReference_toIndices", "CellReference_toColIndex", "CellReference_toRowIndex", "CellReference_setColIndex", "CellReference_setRowIndex", "CellReference_moveHorizontal", "CellReference_moveVertical", "FsAddress_reflection", "FsAddress__ctor_Z668C30D9", "FsAddress__ctor_Z37302880", "FsAddress__ctor_Z721C83C5", "FsAddress__get_ColumnNumber", "FsAddress__set_ColumnNumber_Z524259A4", "FsAddress__get_RowNumber", "FsAddress__set_RowNumber_Z524259A4", "FsAddress__get_Address", "FsAddress__set_Address_Z721C83C5", "FsAddress__get_FixedRow", "FsAddress__get_FixedColumn", "FsAddress__Copy", "FsAddress_copy_6D30B323", "FsAddress__UpdateIndices_Z37302880", "FsAddress_updateIndices", "FsAddress__ToIndices", "FsAddress_toIndices_6D30B323", "FsAddress__Compare_6D30B323", "FsAddress_compare"]

