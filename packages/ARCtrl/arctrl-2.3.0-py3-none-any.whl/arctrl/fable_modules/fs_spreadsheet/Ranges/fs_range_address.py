from __future__ import annotations
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.string_ import (to_text, printf, to_console)
from ...fable_library.types import (Array, uint32)
from ..fs_address import (FsAddress, CellReference_toIndices, CellReference_moveHorizontal, FsAddress__ctor_Z721C83C5, FsAddress__get_RowNumber, FsAddress__set_RowNumber_Z524259A4, FsAddress__get_ColumnNumber, FsAddress__set_ColumnNumber_Z524259A4, FsAddress__ctor_Z37302880, FsAddress__get_Address)

def _expr146() -> TypeInfo:
    return class_type("FsSpreadsheet.FsRangeAddress", None, FsRangeAddress)


class FsRangeAddress:
    def __init__(self, first_address: FsAddress, last_address: FsAddress) -> None:
        self.first_address: FsAddress = first_address
        self.last_address: FsAddress = last_address
        self._firstAddress: FsAddress = self.first_address
        self._lastAddress: FsAddress = self.last_address

    def __str__(self, __unit: None=None) -> str:
        self_1: FsRangeAddress = self
        return FsRangeAddress__get_Range(self_1)


FsRangeAddress_reflection = _expr146

def FsRangeAddress__ctor_7E77A4A0(first_address: FsAddress, last_address: FsAddress) -> FsRangeAddress:
    return FsRangeAddress(first_address, last_address)


def Range_ofBoundaries(from_cell_reference: str, to_cell_reference: str) -> str:
    return to_text(printf("%s:%s"))(from_cell_reference)(to_cell_reference)


def Range_toBoundaries(area: str) -> tuple[str, str]:
    a: Array[str] = area.split(":")
    return (a[0], a[1])


def Range_rightBoundary(area: str) -> uint32:
    return CellReference_toIndices(Range_toBoundaries(area)[1])[0]


def Range_leftBoundary(area: str) -> uint32:
    return CellReference_toIndices(Range_toBoundaries(area)[0])[0]


def Range_upperBoundary(area: str) -> uint32:
    return CellReference_toIndices(Range_toBoundaries(area)[0])[1]


def Range_lowerBoundary(area: str) -> uint32:
    return CellReference_toIndices(Range_toBoundaries(area)[1])[1]


def Range_moveHorizontal(amount: int, area: str) -> str:
    tupled_arg_1: tuple[str, str]
    tupled_arg: tuple[str, str] = Range_toBoundaries(area)
    tupled_arg_1 = (CellReference_moveHorizontal(amount, tupled_arg[0]), CellReference_moveHorizontal(amount, tupled_arg[1]))
    return Range_ofBoundaries(tupled_arg_1[0], tupled_arg_1[1])


def Range_moveVertical(amount: int, area: str) -> str:
    tupled_arg_1: tuple[str, str]
    tupled_arg: tuple[str, str] = Range_toBoundaries(area)
    tupled_arg_1 = (CellReference_moveHorizontal(amount, tupled_arg[0]), CellReference_moveHorizontal(amount, tupled_arg[1]))
    return Range_ofBoundaries(tupled_arg_1[0], tupled_arg_1[1])


def Range_extendRight(amount: int, area: str) -> str:
    tupled_arg_1: tuple[str, str]
    tupled_arg: tuple[str, str] = Range_toBoundaries(area)
    tupled_arg_1 = (tupled_arg[0], CellReference_moveHorizontal(amount, tupled_arg[1]))
    return Range_ofBoundaries(tupled_arg_1[0], tupled_arg_1[1])


def Range_extendLeft(amount: int, area: str) -> str:
    tupled_arg_1: tuple[str, str]
    tupled_arg: tuple[str, str] = Range_toBoundaries(area)
    tupled_arg_1 = (CellReference_moveHorizontal(amount, tupled_arg[0]), tupled_arg[1])
    return Range_ofBoundaries(tupled_arg_1[0], tupled_arg_1[1])


def Range_referenceExceedsAreaRight(reference: str, area: str) -> bool:
    return CellReference_toIndices(reference)[0] > Range_rightBoundary(area)


def Range_referenceExceedsAreaLeft(reference: str, area: str) -> bool:
    return CellReference_toIndices(reference)[0] < Range_leftBoundary(area)


def Range_referenceExceedsAreaAbove(reference: str, area: str) -> bool:
    return CellReference_toIndices(reference)[1] > Range_upperBoundary(area)


def Range_referenceExceedsAreaBelow(reference: str, area: str) -> bool:
    return CellReference_toIndices(reference)[1] < Range_lowerBoundary(area)


def Range_referenceExceedsArea(reference: str, area: str) -> bool:
    if True if (True if Range_referenceExceedsAreaRight(reference, area) else Range_referenceExceedsAreaLeft(reference, area)) else Range_referenceExceedsAreaAbove(reference, area):
        return True

    else: 
        return Range_referenceExceedsAreaBelow(reference, area)



def Range_isCorrect(area: str) -> bool:
    try: 
        hor: bool = Range_leftBoundary(area) <= Range_rightBoundary(area)
        ver: bool = Range_upperBoundary(area) <= Range_lowerBoundary(area)
        if not hor:
            to_console(printf("Right area boundary must be higher or equal to left area boundary."))

        if not ver:
            to_console(printf("Lower area boundary must be higher or equal to upper area boundary."))

        return ver if hor else False

    except Exception as err:
        arg_1: str = str(err)
        to_console(printf("Area \"%s\" could not be parsed: %s"))(area)(arg_1)
        return False



def FsRangeAddress__ctor_Z721C83C5(range_address: str) -> FsRangeAddress:
    pattern_input: tuple[str, str] = Range_toBoundaries(range_address)
    return FsRangeAddress__ctor_7E77A4A0(FsAddress__ctor_Z721C83C5(pattern_input[0]), FsAddress__ctor_Z721C83C5(pattern_input[1]))


def FsRangeAddress__Copy(self_1: FsRangeAddress) -> FsRangeAddress:
    return FsRangeAddress__ctor_Z721C83C5(FsRangeAddress__get_Range(self_1))


def FsRangeAddress_copy_6A2513BC(range_address: FsRangeAddress) -> FsRangeAddress:
    return FsRangeAddress__Copy(range_address)


def FsRangeAddress__Extend_6D30B323(self_1: FsRangeAddress, address: FsAddress) -> None:
    if FsAddress__get_RowNumber(address) < FsAddress__get_RowNumber(self_1._firstAddress):
        FsAddress__set_RowNumber_Z524259A4(self_1._firstAddress, FsAddress__get_RowNumber(address))

    if FsAddress__get_RowNumber(address) > FsAddress__get_RowNumber(self_1._lastAddress):
        FsAddress__set_RowNumber_Z524259A4(self_1._lastAddress, FsAddress__get_RowNumber(address))

    if FsAddress__get_ColumnNumber(address) < FsAddress__get_ColumnNumber(self_1._firstAddress):
        FsAddress__set_ColumnNumber_Z524259A4(self_1._firstAddress, FsAddress__get_ColumnNumber(address))

    if FsAddress__get_ColumnNumber(address) > FsAddress__get_ColumnNumber(self_1._lastAddress):
        FsAddress__set_ColumnNumber_Z524259A4(self_1._lastAddress, FsAddress__get_ColumnNumber(address))



def FsRangeAddress__Normalize(self_1: FsRangeAddress) -> None:
    pattern_input: tuple[int, int] = ((FsAddress__get_RowNumber(self_1.first_address), FsAddress__get_RowNumber(self_1.last_address))) if (FsAddress__get_RowNumber(self_1.first_address) < FsAddress__get_RowNumber(self_1.last_address)) else ((FsAddress__get_RowNumber(self_1.last_address), FsAddress__get_RowNumber(self_1.first_address)))
    pattern_input_1: tuple[int, int] = ((FsAddress__get_RowNumber(self_1.first_address), FsAddress__get_RowNumber(self_1.last_address))) if (FsAddress__get_RowNumber(self_1.first_address) < FsAddress__get_RowNumber(self_1.last_address)) else ((FsAddress__get_RowNumber(self_1.last_address), FsAddress__get_RowNumber(self_1.first_address)))
    self_1._firstAddress = FsAddress__ctor_Z37302880(pattern_input[0], pattern_input_1[0])
    self_1._lastAddress = FsAddress__ctor_Z37302880(pattern_input[1], pattern_input_1[1])


def FsRangeAddress__get_Range(self_1: FsRangeAddress) -> str:
    return Range_ofBoundaries(FsAddress__get_Address(self_1._firstAddress), FsAddress__get_Address(self_1._lastAddress))


def FsRangeAddress__set_Range_Z721C83C5(self_1: FsRangeAddress, address: str) -> None:
    pattern_input: tuple[str, str] = Range_toBoundaries(address)
    self_1._firstAddress = FsAddress__ctor_Z721C83C5(pattern_input[0])
    self_1._lastAddress = FsAddress__ctor_Z721C83C5(pattern_input[1])


def FsRangeAddress__get_FirstAddress(self_1: FsRangeAddress) -> FsAddress:
    return self_1._firstAddress


def FsRangeAddress__get_LastAddress(self_1: FsRangeAddress) -> FsAddress:
    return self_1._lastAddress


def FsRangeAddress__Union_6A2513BC(self_1: FsRangeAddress, range_address: FsRangeAddress) -> FsRangeAddress:
    FsRangeAddress__Extend_6D30B323(self_1, FsRangeAddress__get_FirstAddress(range_address))
    FsRangeAddress__Extend_6D30B323(self_1, FsRangeAddress__get_LastAddress(range_address))
    return self_1


__all__ = ["FsRangeAddress_reflection", "Range_ofBoundaries", "Range_toBoundaries", "Range_rightBoundary", "Range_leftBoundary", "Range_upperBoundary", "Range_lowerBoundary", "Range_moveHorizontal", "Range_moveVertical", "Range_extendRight", "Range_extendLeft", "Range_referenceExceedsAreaRight", "Range_referenceExceedsAreaLeft", "Range_referenceExceedsAreaAbove", "Range_referenceExceedsAreaBelow", "Range_referenceExceedsArea", "Range_isCorrect", "FsRangeAddress__ctor_Z721C83C5", "FsRangeAddress__Copy", "FsRangeAddress_copy_6A2513BC", "FsRangeAddress__Extend_6D30B323", "FsRangeAddress__Normalize", "FsRangeAddress__get_Range", "FsRangeAddress__set_Range_Z721C83C5", "FsRangeAddress__get_FirstAddress", "FsRangeAddress__get_LastAddress", "FsRangeAddress__Union_6A2513BC"]

