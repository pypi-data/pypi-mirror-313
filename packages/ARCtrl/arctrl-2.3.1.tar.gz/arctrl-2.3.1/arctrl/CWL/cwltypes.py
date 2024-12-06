from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from ..fable_modules.dynamic_obj.dynamic_obj import (DynamicObj, DynamicObj_reflection)
from ..fable_modules.dynamic_obj.dyn_obj import set_property
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type, string_type, option_type, bool_type, record_type, union_type, array_type)
from ..fable_modules.fable_library.types import (Record, Array, Union, FSharpRef)

def _expr431() -> TypeInfo:
    return class_type("ARCtrl.CWL.FileInstance", None, FileInstance, DynamicObj_reflection())


class FileInstance(DynamicObj):
    def __init__(self, __unit: None=None) -> None:
        super().__init__()
        pass


FileInstance_reflection = _expr431

def FileInstance__ctor(__unit: None=None) -> FileInstance:
    return FileInstance(__unit)


def _expr432() -> TypeInfo:
    return class_type("ARCtrl.CWL.DirectoryInstance", None, DirectoryInstance, DynamicObj_reflection())


class DirectoryInstance(DynamicObj):
    def __init__(self, __unit: None=None) -> None:
        super().__init__()
        pass


DirectoryInstance_reflection = _expr432

def DirectoryInstance__ctor(__unit: None=None) -> DirectoryInstance:
    return DirectoryInstance(__unit)


def _expr434() -> TypeInfo:
    return record_type("ARCtrl.CWL.DirentInstance", [], DirentInstance, lambda: [("Entry", string_type), ("Entryname", option_type(string_type)), ("Writable", option_type(bool_type))])


@dataclass(eq = False, repr = False, slots = True)
class DirentInstance(Record):
    Entry: str
    Entryname: str | None
    Writable: bool | None

DirentInstance_reflection = _expr434

def _expr435() -> TypeInfo:
    return union_type("ARCtrl.CWL.CWLType", [], CWLType, lambda: [[("Item", FileInstance_reflection())], [("Item", DirectoryInstance_reflection())], [("Item", DirentInstance_reflection())], [], [], [], [], [], [], [], [], [("Item", CWLType_reflection())]])


class CWLType(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["File", "Directory", "Dirent", "String", "Int", "Long", "Float", "Double", "Boolean", "Stdout", "Null", "Array"]


CWLType_reflection = _expr435

def _expr437() -> TypeInfo:
    return class_type("ARCtrl.CWL.InputRecordSchema", None, InputRecordSchema, DynamicObj_reflection())


class InputRecordSchema(DynamicObj):
    def __init__(self, __unit: None=None) -> None:
        super().__init__()
        pass


InputRecordSchema_reflection = _expr437

def InputRecordSchema__ctor(__unit: None=None) -> InputRecordSchema:
    return InputRecordSchema(__unit)


def _expr438() -> TypeInfo:
    return class_type("ARCtrl.CWL.InputEnumSchema", None, InputEnumSchema, DynamicObj_reflection())


class InputEnumSchema(DynamicObj):
    def __init__(self, __unit: None=None) -> None:
        super().__init__()
        pass


InputEnumSchema_reflection = _expr438

def InputEnumSchema__ctor(__unit: None=None) -> InputEnumSchema:
    return InputEnumSchema(__unit)


def _expr439() -> TypeInfo:
    return class_type("ARCtrl.CWL.InputArraySchema", None, InputArraySchema, DynamicObj_reflection())


class InputArraySchema(DynamicObj):
    def __init__(self, __unit: None=None) -> None:
        super().__init__()
        pass


InputArraySchema_reflection = _expr439

def InputArraySchema__ctor(__unit: None=None) -> InputArraySchema:
    return InputArraySchema(__unit)


def _expr441() -> TypeInfo:
    return class_type("ARCtrl.CWL.SchemaDefRequirementType", None, SchemaDefRequirementType, DynamicObj_reflection())


class SchemaDefRequirementType(DynamicObj):
    def __init__(self, types: Any=None, definitions: Any=None) -> None:
        super().__init__()
        this: FSharpRef[SchemaDefRequirementType] = FSharpRef(None)
        this.contents = self
        self.init_004047: int = 1
        set_property("types", definitions, this.contents)


SchemaDefRequirementType_reflection = _expr441

def SchemaDefRequirementType__ctor_541DA560(types: Any=None, definitions: Any=None) -> SchemaDefRequirementType:
    return SchemaDefRequirementType(types, definitions)


def _expr445() -> TypeInfo:
    return record_type("ARCtrl.CWL.SoftwarePackage", [], SoftwarePackage, lambda: [("Package", string_type), ("Version", option_type(array_type(string_type))), ("Specs", option_type(array_type(string_type)))])


@dataclass(eq = False, repr = False, slots = True)
class SoftwarePackage(Record):
    Package: str
    Version: Array[str] | None
    Specs: Array[str] | None

SoftwarePackage_reflection = _expr445

__all__ = ["FileInstance_reflection", "DirectoryInstance_reflection", "DirentInstance_reflection", "CWLType_reflection", "InputRecordSchema_reflection", "InputEnumSchema_reflection", "InputArraySchema_reflection", "SchemaDefRequirementType_reflection", "SoftwarePackage_reflection"]

