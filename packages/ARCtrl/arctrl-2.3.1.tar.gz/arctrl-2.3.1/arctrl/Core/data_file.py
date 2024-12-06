from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.reflection import (TypeInfo, union_type)
from ..fable_modules.fable_library.types import (Array, Union)

def _expr607() -> TypeInfo:
    return union_type("ARCtrl.DataFile", [], DataFile, lambda: [[], [], []])


class DataFile(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["RawDataFile", "DerivedDataFile", "ImageFile"]


DataFile_reflection = _expr607

def DataFile_get_RawDataFileJson(__unit: None=None) -> str:
    return "Raw Data File"


def DataFile_get_DerivedDataFileJson(__unit: None=None) -> str:
    return "Derived Data File"


def DataFile_get_ImageFileJson(__unit: None=None) -> str:
    return "Image File"


def DataFile__get_AsString(this: DataFile) -> str:
    if this.tag == 1:
        return "DerivedDataFileJson"

    elif this.tag == 2:
        return "ImageFileJson"

    else: 
        return "RawDataFileJson"



def DataFile__get_IsDerivedData(this: DataFile) -> bool:
    if this.tag == 1:
        return True

    else: 
        return False



def DataFile__get_IsRawData(this: DataFile) -> bool:
    if this.tag == 0:
        return True

    else: 
        return False



def DataFile__get_IsImage(this: DataFile) -> bool:
    if this.tag == 2:
        return True

    else: 
        return False



__all__ = ["DataFile_reflection", "DataFile_get_RawDataFileJson", "DataFile_get_DerivedDataFileJson", "DataFile_get_ImageFileJson", "DataFile__get_AsString", "DataFile__get_IsDerivedData", "DataFile__get_IsRawData", "DataFile__get_IsImage"]

