from __future__ import annotations
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..ldobject import (LDObject, LDObject_reflection)

def _expr1361() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.Dataset", None, Dataset, LDObject_reflection())


class Dataset(LDObject):
    def __init__(self, id: str, additional_type: str | None=None) -> None:
        super().__init__(id, "schema.org/Dataset", additional_type)
        pass


Dataset_reflection = _expr1361

def Dataset__ctor_27AED5E3(id: str, additional_type: str | None=None) -> Dataset:
    return Dataset(id, additional_type)


__all__ = ["Dataset_reflection"]

