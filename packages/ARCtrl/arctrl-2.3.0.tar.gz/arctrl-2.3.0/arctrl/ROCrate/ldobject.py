from __future__ import annotations
from abc import abstractmethod
from collections.abc import Callable
from typing import (Protocol, Any, TypeVar)
from ..fable_modules.dynamic_obj.dynamic_obj import (DynamicObj, DynamicObj_reflection)
from ..fable_modules.fable_library.option import value as value_1
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)

__C = TypeVar("__C")

__B = TypeVar("__B")

__A = TypeVar("__A")

def _expr1360() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDContext", None, LDContext, DynamicObj_reflection())


class LDContext(DynamicObj):
    def __init__(self, __unit: None=None) -> None:
        super().__init__()
        pass


LDContext_reflection = _expr1360

def LDContext__ctor(__unit: None=None) -> LDContext:
    return LDContext(__unit)


class ILDObject(Protocol):
    @property
    @abstractmethod
    def AdditionalType(self) -> str | None:
        ...

    @AdditionalType.setter
    @abstractmethod
    def AdditionalType(self, __arg0: str | None) -> None:
        ...

    @property
    @abstractmethod
    def Id(self) -> str:
        ...

    @property
    @abstractmethod
    def SchemaType(self) -> str:
        ...

    @SchemaType.setter
    @abstractmethod
    def SchemaType(self, __arg0: str) -> None:
        ...


def _expr1365() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.LDObject", None, LDObject, DynamicObj_reflection())


class LDObject(DynamicObj):
    def __init__(self, id: str, schema_type: str, additional_type: str | None=None) -> None:
        super().__init__()
        self.id: str = id
        self.schema_type_004022: str = schema_type
        self.additional_type_004023: str | None = additional_type

    @property
    def Id(self, __unit: None=None) -> str:
        this: LDObject = self
        return this.id

    @property
    def SchemaType(self, __unit: None=None) -> str:
        this: LDObject = self
        return this.schema_type_004022

    @SchemaType.setter
    def SchemaType(self, value: str) -> None:
        this: LDObject = self
        this.schema_type_004022 = value

    @property
    def AdditionalType(self, __unit: None=None) -> str | None:
        this: LDObject = self
        return this.additional_type_004023

    @AdditionalType.setter
    def AdditionalType(self, value: str | None=None) -> None:
        this: LDObject = self
        this.additional_type_004023 = value

    def SetContext(self, context: LDContext) -> None:
        this: LDObject = self
        this.SetProperty("@context", context)

    @staticmethod
    def set_context(context: LDContext) -> Callable[[__C], None]:
        def _arrow1362(roc: __C | None=None) -> None:
            roc.SetContext(context)

        return _arrow1362

    def TryGetContext(self, __unit: None=None) -> DynamicObj | None:
        this: LDObject = self
        match_value: Any | None = this.TryGetPropertyValue("@context")
        if match_value is not None:
            o: Any = value_1(match_value)
            return o if isinstance(o, DynamicObj) else None

        else: 
            return None


    @staticmethod
    def try_get_context(__unit: None=None) -> Callable[[__B], DynamicObj | None]:
        def _arrow1363(roc: __B | None=None) -> DynamicObj | None:
            return roc.TryGetContext()

        return _arrow1363

    def RemoveContext(self, __unit: None=None) -> bool:
        this: LDObject = self
        return this.RemoveProperty("@context")

    @staticmethod
    def remove_context(__unit: None=None) -> Callable[[__A], bool]:
        def _arrow1364(roc: __A | None=None) -> bool:
            return roc.RemoveContext()

        return _arrow1364

    @property
    def SchemaType(self, __unit: None=None) -> str:
        this: LDObject = self
        return this.schema_type_004022

    @SchemaType.setter
    def SchemaType(self, value: str) -> None:
        this: LDObject = self
        this.schema_type_004022 = value

    @property
    def Id(self, __unit: None=None) -> str:
        this: LDObject = self
        return this.id

    @property
    def AdditionalType(self, __unit: None=None) -> str | None:
        this: LDObject = self
        return this.additional_type_004023

    @AdditionalType.setter
    def AdditionalType(self, value: str | None=None) -> None:
        this: LDObject = self
        this.additional_type_004023 = value


LDObject_reflection = _expr1365

def LDObject__ctor_Z2FC25A28(id: str, schema_type: str, additional_type: str | None=None) -> LDObject:
    return LDObject(id, schema_type, additional_type)


__all__ = ["LDContext_reflection", "LDObject_reflection"]

