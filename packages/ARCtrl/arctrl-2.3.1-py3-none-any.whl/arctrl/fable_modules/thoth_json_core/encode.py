from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_library.array_ import map as map_3
from ..fable_library.list import (map as map_1, FSharpList)
from ..fable_library.map import (to_seq, to_list)
from ..fable_library.option import (default_arg_with, map as map_4)
from ..fable_library.seq import map as map_2
from ..fable_library.types import (float32 as float32_1, Array)
from ..fable_library.util import (IEnumerable_1, get_enumerator, dispose)
from .types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

_T1 = TypeVar("_T1")

_T2 = TypeVar("_T2")

_T3 = TypeVar("_T3")

_T4 = TypeVar("_T4")

_T5 = TypeVar("_T5")

_T6 = TypeVar("_T6")

_T7 = TypeVar("_T7")

_T8 = TypeVar("_T8")

_KEY = TypeVar("_KEY")

_VALUE = TypeVar("_VALUE")

_A = TypeVar("_A")

def float32(value: float32_1) -> IEncodable:
    class ObjectExpr32(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
            return helpers.encode_decimal_number(value)

    return ObjectExpr32()


def list_1(values: FSharpList[IEncodable]) -> IEncodable:
    class ObjectExpr33(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], values: Any=values) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: FSharpList[__A_] = map_1(mapping, values)
            return helpers.encode_list(arg)

    return ObjectExpr33()


def seq(values: IEnumerable_1[IEncodable]) -> IEncodable:
    class ObjectExpr34(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], values: Any=values) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: IEnumerable_1[__A_] = map_2(mapping, values)
            return helpers.encode_seq(arg)

    return ObjectExpr34()


def resize_array(values: Array[IEncodable]) -> IEncodable:
    class ObjectExpr35(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], values: Any=values) -> Any:
            result: Array[__A_] = []
            enumerator: Any = get_enumerator(values)
            try: 
                while enumerator.System_Collections_IEnumerator_MoveNext():
                    v: IEncodable = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                    (result.append(v.Encode(helpers)))

            finally: 
                dispose(enumerator)

            return helpers.encode_resize_array(result)

    return ObjectExpr35()


def dict_1(values: Any) -> IEncodable:
    values_1: IEnumerable_1[tuple[str, IEncodable]] = to_seq(values)
    class ObjectExpr36(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], values: Any=values) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers))

            arg: IEnumerable_1[tuple[str, __A_]] = map_2(mapping, values_1)
            return helpers.encode_object(arg)

    return ObjectExpr36()


def tuple2(enc1: Callable[[_T1], IEncodable], enc2: Callable[[_T2], IEncodable], v1: Any, v2: Any) -> IEncodable:
    values: Array[IEncodable] = [enc1(v1), enc2(v2)]
    class ObjectExpr37(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], enc1: Any=enc1, enc2: Any=enc2, v1: Any=v1, v2: Any=v2) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_3(mapping, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr37()


def tuple3(enc1: Callable[[_T1], IEncodable], enc2: Callable[[_T2], IEncodable], enc3: Callable[[_T3], IEncodable], v1: Any, v2: Any, v3: Any) -> IEncodable:
    values: Array[IEncodable] = [enc1(v1), enc2(v2), enc3(v3)]
    class ObjectExpr38(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], enc1: Any=enc1, enc2: Any=enc2, enc3: Any=enc3, v1: Any=v1, v2: Any=v2, v3: Any=v3) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_3(mapping, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr38()


def tuple4(enc1: Callable[[_T1], IEncodable], enc2: Callable[[_T2], IEncodable], enc3: Callable[[_T3], IEncodable], enc4: Callable[[_T4], IEncodable], v1: Any, v2: Any, v3: Any, v4: Any) -> IEncodable:
    values: Array[IEncodable] = [enc1(v1), enc2(v2), enc3(v3), enc4(v4)]
    class ObjectExpr39(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], enc1: Any=enc1, enc2: Any=enc2, enc3: Any=enc3, enc4: Any=enc4, v1: Any=v1, v2: Any=v2, v3: Any=v3, v4: Any=v4) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_3(mapping, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr39()


def tuple5(enc1: Callable[[_T1], IEncodable], enc2: Callable[[_T2], IEncodable], enc3: Callable[[_T3], IEncodable], enc4: Callable[[_T4], IEncodable], enc5: Callable[[_T5], IEncodable], v1: Any, v2: Any, v3: Any, v4: Any, v5: Any) -> IEncodable:
    values: Array[IEncodable] = [enc1(v1), enc2(v2), enc3(v3), enc4(v4), enc5(v5)]
    class ObjectExpr40(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], enc1: Any=enc1, enc2: Any=enc2, enc3: Any=enc3, enc4: Any=enc4, enc5: Any=enc5, v1: Any=v1, v2: Any=v2, v3: Any=v3, v4: Any=v4, v5: Any=v5) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_3(mapping, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr40()


def tuple6(enc1: Callable[[_T1], IEncodable], enc2: Callable[[_T2], IEncodable], enc3: Callable[[_T3], IEncodable], enc4: Callable[[_T4], IEncodable], enc5: Callable[[_T5], IEncodable], enc6: Callable[[_T6], IEncodable], v1: Any, v2: Any, v3: Any, v4: Any, v5: Any, v6: Any) -> IEncodable:
    values: Array[IEncodable] = [enc1(v1), enc2(v2), enc3(v3), enc4(v4), enc5(v5), enc6(v6)]
    class ObjectExpr41(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], enc1: Any=enc1, enc2: Any=enc2, enc3: Any=enc3, enc4: Any=enc4, enc5: Any=enc5, enc6: Any=enc6, v1: Any=v1, v2: Any=v2, v3: Any=v3, v4: Any=v4, v5: Any=v5, v6: Any=v6) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_3(mapping, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr41()


def tuple7(enc1: Callable[[_T1], IEncodable], enc2: Callable[[_T2], IEncodable], enc3: Callable[[_T3], IEncodable], enc4: Callable[[_T4], IEncodable], enc5: Callable[[_T5], IEncodable], enc6: Callable[[_T6], IEncodable], enc7: Callable[[_T7], IEncodable], v1: Any, v2: Any, v3: Any, v4: Any, v5: Any, v6: Any, v7: Any) -> IEncodable:
    values: Array[IEncodable] = [enc1(v1), enc2(v2), enc3(v3), enc4(v4), enc5(v5), enc6(v6), enc7(v7)]
    class ObjectExpr42(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], enc1: Any=enc1, enc2: Any=enc2, enc3: Any=enc3, enc4: Any=enc4, enc5: Any=enc5, enc6: Any=enc6, enc7: Any=enc7, v1: Any=v1, v2: Any=v2, v3: Any=v3, v4: Any=v4, v5: Any=v5, v6: Any=v6, v7: Any=v7) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_3(mapping, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr42()


def tuple8(enc1: Callable[[_T1], IEncodable], enc2: Callable[[_T2], IEncodable], enc3: Callable[[_T3], IEncodable], enc4: Callable[[_T4], IEncodable], enc5: Callable[[_T5], IEncodable], enc6: Callable[[_T6], IEncodable], enc7: Callable[[_T7], IEncodable], enc8: Callable[[_T8], IEncodable], v1: Any, v2: Any, v3: Any, v4: Any, v5: Any, v6: Any, v7: Any, v8: Any) -> IEncodable:
    values: Array[IEncodable] = [enc1(v1), enc2(v2), enc3(v3), enc4(v4), enc5(v5), enc6(v6), enc7(v7), enc8(v8)]
    class ObjectExpr43(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], enc1: Any=enc1, enc2: Any=enc2, enc3: Any=enc3, enc4: Any=enc4, enc5: Any=enc5, enc6: Any=enc6, enc7: Any=enc7, enc8: Any=enc8, v1: Any=v1, v2: Any=v2, v3: Any=v3, v4: Any=v4, v5: Any=v5, v6: Any=v6, v7: Any=v7, v8: Any=v8) -> Any:
            def mapping(v: IEncodable) -> __A_:
                return v.Encode(helpers)

            arg: Array[__A_] = map_3(mapping, values, None)
            return helpers.encode_array(arg)

    return ObjectExpr43()


def map(key_encoder: Callable[[_KEY], IEncodable], value_encoder: Callable[[_VALUE], IEncodable], values: Any) -> IEncodable:
    def mapping(tupled_arg: tuple[_KEY, _VALUE], key_encoder: Any=key_encoder, value_encoder: Any=value_encoder, values: Any=values) -> IEncodable:
        return tuple2(key_encoder, value_encoder, tupled_arg[0], tupled_arg[1])

    return list_1(map_1(mapping, to_list(values)))


def Enum_byte(value: Any | None=None) -> IEncodable:
    class ObjectExpr44(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
            return helpers.encode_unsigned_integral_number(value)

    return ObjectExpr44()


def Enum_sbyte(value: Any | None=None) -> IEncodable:
    class ObjectExpr45(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
            return helpers.encode_signed_integral_number(value)

    return ObjectExpr45()


def Enum_int16(value: Any | None=None) -> IEncodable:
    class ObjectExpr46(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
            return helpers.encode_signed_integral_number(value)

    return ObjectExpr46()


def Enum_uint16(value: Any | None=None) -> IEncodable:
    class ObjectExpr47(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
            return helpers.encode_unsigned_integral_number(value)

    return ObjectExpr47()


def Enum_int(value: Any | None=None) -> IEncodable:
    class ObjectExpr48(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
            return helpers.encode_signed_integral_number(value)

    return ObjectExpr48()


def Enum_uint32(value: Any | None=None) -> IEncodable:
    class ObjectExpr49(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], value: Any=value) -> Any:
            return helpers.encode_unsigned_integral_number(value)

    return ObjectExpr49()


def option(encoder: Callable[[_A], IEncodable]) -> Callable[[_A | None], IEncodable]:
    def _arrow51(arg: _A | None=None, encoder: Any=encoder) -> IEncodable:
        def def_thunk(__unit: None=None) -> IEncodable:
            class ObjectExpr50(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_null()

            return ObjectExpr50()

        return default_arg_with(map_4(encoder, arg), def_thunk)

    return _arrow51


__all__ = ["float32", "list_1", "seq", "resize_array", "dict_1", "tuple2", "tuple3", "tuple4", "tuple5", "tuple6", "tuple7", "tuple8", "map", "Enum_byte", "Enum_sbyte", "Enum_int16", "Enum_uint16", "Enum_int", "Enum_uint32", "option"]

