from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.array_ import map as map_2
from ..fable_modules.fable_library.date import to_string
from ..fable_modules.fable_library.list import (is_empty as is_empty_1, map as map_3, FSharpList)
from ..fable_modules.fable_library.option import (map, default_arg)
from ..fable_modules.fable_library.seq import (is_empty, map as map_1, append)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import to_enumerable
from ..fable_modules.thoth_json_core.encode import (seq, list_1 as list_1_1)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Json)

_VALUE = TypeVar("_VALUE")

__A = TypeVar("__A")

__A_ = TypeVar("__A_")

def try_include(name: str, encoder: Callable[[_VALUE], IEncodable], value: Any | None=None) -> tuple[str, IEncodable | None]:
    return (name, map(encoder, value))


def try_include_seq(name: Any, encoder: Callable[[_VALUE], IEncodable], value: Any) -> tuple[__A, IEncodable | None]:
    return (name, None if is_empty(value) else seq(map_1(encoder, value)))


def try_include_array(name: Any, encoder: Callable[[_VALUE], IEncodable], value: Array[Any]) -> tuple[__A, IEncodable | None]:
    def _arrow1685(__unit: None=None, name: Any=name, encoder: Any=encoder, value: Any=value) -> IEncodable:
        values: Array[IEncodable] = map_2(encoder, value, None)
        class ObjectExpr1684(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[__A_]) -> __A_:
                def mapping(v: IEncodable) -> __A_:
                    return v.Encode(helpers)

                arg: Array[__A_] = map_2(mapping, values, None)
                return helpers.encode_array(arg)

        return ObjectExpr1684()

    return (name, None if (len(value) == 0) else _arrow1685())


def try_include_list(name: Any, encoder: Callable[[_VALUE], IEncodable], value: FSharpList[Any]) -> tuple[__A, IEncodable | None]:
    return (name, None if is_empty_1(value) else list_1_1(map_3(encoder, value)))


def try_include_list_opt(name: Any, encoder: Callable[[_VALUE], IEncodable], value: FSharpList[Any] | None=None) -> tuple[__A, IEncodable | None]:
    def _arrow1688(__unit: None=None, name: Any=name, encoder: Any=encoder, value: Any=value) -> IEncodable | None:
        o: FSharpList[_VALUE] = value
        return None if is_empty_1(o) else list_1_1(map_3(encoder, o))

    return (name, _arrow1688() if (value is not None) else None)


DefaultSpaces: int = 0

def default_spaces(spaces: int | None=None) -> int:
    return default_arg(spaces, DefaultSpaces)


def date_time(d: Any) -> IEncodable:
    value: str = to_string(d, "O", {}).split("+")[0]
    class ObjectExpr1689(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], d: Any=d) -> Any:
            return helpers.encode_string(value)

    return ObjectExpr1689()


def add_property_to_object(name: str, value: Json, obj: Json) -> Json:
    if obj.tag == 5:
        return Json(5, append(obj.fields[0], to_enumerable([(name, value)])))

    else: 
        raise Exception("Expected object")



__all__ = ["try_include", "try_include_seq", "try_include_array", "try_include_list", "try_include_list_opt", "DefaultSpaces", "default_spaces", "date_time", "add_property_to_object"]

