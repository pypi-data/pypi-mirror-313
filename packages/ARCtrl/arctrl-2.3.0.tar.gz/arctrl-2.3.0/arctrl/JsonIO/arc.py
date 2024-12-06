from __future__ import annotations
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.option import map
from ..fable_modules.fable_library.seq import map as map_1
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, IGetters)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.arc_types import ArcInvestigation
from ..Json.context.rocrate.rocrate_context import (conforms_to_jsonvalue, context_jsonvalue)
from ..Json.encode import try_include
from ..Json.investigation import (ROCrate_encoder, ROCrate_decoder)

__A_ = TypeVar("__A_")

def encoder(isa: ArcInvestigation) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], isa: Any=isa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow3207(value: str, isa: Any=isa) -> IEncodable:
        class ObjectExpr3206(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr3206()

    def _arrow3209(value_2: str, isa: Any=isa) -> IEncodable:
        class ObjectExpr3208(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr3208()

    def _arrow3210(oa: ArcInvestigation, isa: Any=isa) -> IEncodable:
        return ROCrate_encoder(oa)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@type", _arrow3207, "CreativeWork"), try_include("@id", _arrow3209, "ro-crate-metadata.json"), try_include("about", _arrow3210, isa), ("conformsTo", conforms_to_jsonvalue), ("@context", context_jsonvalue)]))
    class ObjectExpr3211(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], isa: Any=isa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_2))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_2.encode_object(arg)

    return ObjectExpr3211()


def _arrow3212(get: IGetters) -> ArcInvestigation | None:
    object_arg: IOptionalGetter = get.Optional
    return object_arg.Field("about", ROCrate_decoder)


decoder: Decoder_1[ArcInvestigation | None] = object(_arrow3212)

__all__ = ["encoder", "decoder"]

