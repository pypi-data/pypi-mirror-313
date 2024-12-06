from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.option import (map, value as value_6)
from ..fable_modules.fable_library.seq import map as map_1
from ..fable_modules.fable_library.string_ import replace
from ..fable_modules.fable_library.types import to_string
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, IGetters, map as map_2)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.comment import Comment
from .context.rocrate.isa_comment_context import context_jsonvalue
from .encode import try_include
from .idtable import encode

__A_ = TypeVar("__A_")

def encoder(comment: Comment) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], comment: Any=comment) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow1706(value: str, comment: Any=comment) -> IEncodable:
        class ObjectExpr1705(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr1705()

    def _arrow1708(value_2: str, comment: Any=comment) -> IEncodable:
        class ObjectExpr1707(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr1707()

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("name", _arrow1706, comment.Name), try_include("value", _arrow1708, comment.Value)]))
    class ObjectExpr1709(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], comment: Any=comment) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_2))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_2.encode_object(arg)

    return ObjectExpr1709()


def _arrow1712(get: IGetters) -> Comment:
    def _arrow1710(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("name", string)

    def _arrow1711(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("value", string)

    return Comment(_arrow1710(), _arrow1711())


decoder: Decoder_1[Comment] = object(_arrow1712)

def ROCrate_genID(c: Comment) -> str:
    match_value: str | None = c.Name
    if match_value is None:
        return "#EmptyComment"

    else: 
        n: str = match_value
        v: str = ("_" + replace(value_6(c.Value), " ", "_")) if (c.Value is not None) else ""
        return ("#Comment_" + replace(n, " ", "_")) + v



def ROCrate_encoder(comment: Comment) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], comment: Any=comment) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow1716(__unit: None=None, comment: Any=comment) -> IEncodable:
        value: str = ROCrate_genID(comment)
        class ObjectExpr1715(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr1715()

    class ObjectExpr1717(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], comment: Any=comment) -> Any:
            return helpers_1.encode_string("Comment")

    def _arrow1719(value_2: str, comment: Any=comment) -> IEncodable:
        class ObjectExpr1718(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr1718()

    def _arrow1721(value_4: str, comment: Any=comment) -> IEncodable:
        class ObjectExpr1720(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_4)

        return ObjectExpr1720()

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow1716()), ("@type", ObjectExpr1717()), try_include("name", _arrow1719, comment.Name), try_include("value", _arrow1721, comment.Value), ("@context", context_jsonvalue)]))
    class ObjectExpr1722(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], comment: Any=comment) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr1722()


def _arrow1725(get: IGetters) -> Comment:
    def _arrow1723(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("name", string)

    def _arrow1724(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("value", string)

    return Comment(_arrow1723(), _arrow1724())


ROCrate_decoder: Decoder_1[Comment] = object(_arrow1725)

def ROCrate_encoderDisambiguatingDescription(comment: Comment) -> IEncodable:
    value: str = to_string(comment)
    class ObjectExpr1726(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], comment: Any=comment) -> Any:
            return helpers.encode_string(value)

    return ObjectExpr1726()


def ctor(s: str) -> Comment:
    return Comment.from_string(s)


ROCrate_decoderDisambiguatingDescription: Decoder_1[Comment] = map_2(ctor, string)

def ISAJson_encoder(id_map: Any | None, comment: Comment) -> IEncodable:
    def f(comment_1: Comment, id_map: Any=id_map, comment: Any=comment) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], comment_1: Any=comment_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow1730(value: str, comment_1: Any=comment_1) -> IEncodable:
            class ObjectExpr1729(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr1729()

        def _arrow1732(value_2: str, comment_1: Any=comment_1) -> IEncodable:
            class ObjectExpr1731(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_2)

            return ObjectExpr1731()

        def _arrow1734(value_4: str, comment_1: Any=comment_1) -> IEncodable:
            class ObjectExpr1733(IEncodable):
                def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_2.encode_string(value_4)

            return ObjectExpr1733()

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow1730, ROCrate_genID(comment_1)), try_include("name", _arrow1732, comment_1.Name), try_include("value", _arrow1734, comment_1.Value)]))
        class ObjectExpr1735(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any], comment_1: Any=comment_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_3))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_3.encode_object(arg)

        return ObjectExpr1735()

    if id_map is None:
        return f(comment)

    else: 
        def _arrow1736(c: Comment, id_map: Any=id_map, comment: Any=comment) -> str:
            return ROCrate_genID(c)

        return encode(_arrow1736, f, comment, id_map)



ISAJson_decoder: Decoder_1[Comment] = decoder

__all__ = ["encoder", "decoder", "ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ROCrate_encoderDisambiguatingDescription", "ROCrate_decoderDisambiguatingDescription", "ISAJson_encoder", "ISAJson_decoder"]

