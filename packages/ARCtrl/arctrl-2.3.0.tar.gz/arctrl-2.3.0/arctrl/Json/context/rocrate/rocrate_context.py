from __future__ import annotations
from dataclasses import dataclass
from typing import (Any, TypeVar)
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.seq import map
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ....fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

def _expr1672() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.ROCrate.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("CreativeWork", string_type), ("about", string_type), ("conforms_to", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    CreativeWork: str
    about: str
    conforms_to: str

IContext_reflection = _expr1672

def _arrow1675(__unit: None=None) -> IEncodable:
    class ObjectExpr1673(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("https://w3id.org/ro/crate/1.1")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("@id", ObjectExpr1673())])
    class ObjectExpr1674(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_1))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_1.encode_object(arg)

    return ObjectExpr1674()


conforms_to_jsonvalue: IEncodable = _arrow1675()

def _arrow1683(__unit: None=None) -> IEncodable:
    class ObjectExpr1676(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("http://schema.org/")

    class ObjectExpr1678(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            return helpers_1.encode_string("http://purl.org/nfdi4plants/ontology/")

    class ObjectExpr1679(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
            return helpers_2.encode_string("sdo:CreativeWork")

    class ObjectExpr1680(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
            return helpers_3.encode_string("sdo:about")

    class ObjectExpr1681(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
            return helpers_4.encode_string("sdo:conformsTo")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("sdo", ObjectExpr1676()), ("arc", ObjectExpr1678()), ("CreativeWork", ObjectExpr1679()), ("about", ObjectExpr1680()), ("conformsTo", ObjectExpr1681())])
    class ObjectExpr1682(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_5))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_5.encode_object(arg)

    return ObjectExpr1682()


context_jsonvalue: IEncodable = _arrow1683()

__all__ = ["IContext_reflection", "conforms_to_jsonvalue", "context_jsonvalue"]

