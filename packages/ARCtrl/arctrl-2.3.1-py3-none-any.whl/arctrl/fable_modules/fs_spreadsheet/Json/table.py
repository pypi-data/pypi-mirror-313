from __future__ import annotations
from typing import (Any, TypeVar)
from ...fable_library.seq import map
from ...fable_library.util import (to_enumerable, IEnumerable_1)
from ...thoth_json_core.decode import (object, IRequiredGetter, string, IGetters)
from ...thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Ranges.fs_range_address import (FsRangeAddress__get_Range, FsRangeAddress__ctor_Z721C83C5)
from ..Ranges.fs_range_base import FsRangeBase__get_RangeAddress
from ..Tables.fs_table import FsTable

__A_ = TypeVar("__A_")

def encode(sheet: FsTable) -> IEncodable:
    def _arrow291(__unit: None=None, sheet: Any=sheet) -> IEncodable:
        value: str = sheet.Name
        class ObjectExpr290(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr290()

    def _arrow293(__unit: None=None, sheet: Any=sheet) -> IEncodable:
        value_1: str = FsRangeAddress__get_Range(FsRangeBase__get_RangeAddress(sheet))
        class ObjectExpr292(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr292()

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("name", _arrow291()), ("range", _arrow293())])
    class ObjectExpr296(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], sheet: Any=sheet) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_2))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_2.encode_object(arg)

    return ObjectExpr296()


def _arrow300(builder: IGetters) -> FsTable:
    def _arrow297(__unit: None=None) -> str:
        object_arg: IRequiredGetter = builder.Required
        return object_arg.Field("name", string)

    def _arrow299(__unit: None=None) -> str:
        object_arg_1: IRequiredGetter = builder.Required
        return object_arg_1.Field("range", string)

    return FsTable(_arrow297(), FsRangeAddress__ctor_Z721C83C5(_arrow299()))


decode: Decoder_1[FsTable] = object(_arrow300)

__all__ = ["encode", "decode"]

