from __future__ import annotations
from dataclasses import dataclass
from typing import (Any, TypeVar)
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.seq import map
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ....fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

def _expr1604() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.Protocol.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("Protocol", string_type), ("ArcProtocol", string_type), ("name", string_type), ("protocol_type", string_type), ("description", string_type), ("version", string_type), ("components", string_type), ("parameters", string_type), ("uri", string_type), ("comments", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    Protocol: str
    ArcProtocol: str
    name: str
    protocol_type: str
    description: str
    version: str
    components: str
    parameters: str
    uri: str
    comments: str

IContext_reflection = _expr1604

def _arrow1618(__unit: None=None) -> IEncodable:
    class ObjectExpr1605(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("http://schema.org/")

    class ObjectExpr1606(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            return helpers_1.encode_string("https://bioschemas.org/")

    class ObjectExpr1607(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
            return helpers_2.encode_string("bio:LabProtocol")

    class ObjectExpr1608(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
            return helpers_3.encode_string("sdo:name")

    class ObjectExpr1609(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
            return helpers_4.encode_string("bio:intendedUse")

    class ObjectExpr1610(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
            return helpers_5.encode_string("sdo:description")

    class ObjectExpr1611(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
            return helpers_6.encode_string("sdo:version")

    class ObjectExpr1612(IEncodable):
        def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
            return helpers_7.encode_string("bio:labEquipment")

    class ObjectExpr1613(IEncodable):
        def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
            return helpers_8.encode_string("bio:reagent")

    class ObjectExpr1614(IEncodable):
        def Encode(self, helpers_9: IEncoderHelpers_1[Any]) -> Any:
            return helpers_9.encode_string("bio:computationalTool")

    class ObjectExpr1615(IEncodable):
        def Encode(self, helpers_10: IEncoderHelpers_1[Any]) -> Any:
            return helpers_10.encode_string("sdo:url")

    class ObjectExpr1616(IEncodable):
        def Encode(self, helpers_11: IEncoderHelpers_1[Any]) -> Any:
            return helpers_11.encode_string("sdo:comment")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("sdo", ObjectExpr1605()), ("bio", ObjectExpr1606()), ("Protocol", ObjectExpr1607()), ("name", ObjectExpr1608()), ("protocolType", ObjectExpr1609()), ("description", ObjectExpr1610()), ("version", ObjectExpr1611()), ("components", ObjectExpr1612()), ("reagents", ObjectExpr1613()), ("computationalTools", ObjectExpr1614()), ("uri", ObjectExpr1615()), ("comments", ObjectExpr1616())])
    class ObjectExpr1617(IEncodable):
        def Encode(self, helpers_12: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_12))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_12.encode_object(arg)

    return ObjectExpr1617()


context_jsonvalue: IEncodable = _arrow1618()

__all__ = ["IContext_reflection", "context_jsonvalue"]

