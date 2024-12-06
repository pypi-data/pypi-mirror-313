from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ...fable_modules.fable_library.option import map
from ...fable_modules.fable_library.seq import map as map_1
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.thoth_json_core.decode import (object, IOptionalGetter, IGetters)
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Process.protocol_parameter import ProtocolParameter
from ..encode import try_include
from ..idtable import encode
from ..ontology_annotation import (OntologyAnnotation_ROCrate_genID, OntologyAnnotation_ISAJson_encoder, OntologyAnnotation_ISAJson_decoder)

__A_ = TypeVar("__A_")

def gen_id(p: ProtocolParameter) -> str:
    match_value: OntologyAnnotation | None = p.ParameterName
    if match_value is None:
        return "#EmptyProtocolParameter"

    else: 
        return ("#ProtocolParameter/" + OntologyAnnotation_ROCrate_genID(match_value)) + ""



def encoder(id_map: Any | None, value: ProtocolParameter) -> IEncodable:
    def f(value_1: ProtocolParameter, id_map: Any=id_map, value: Any=value) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], value_1: Any=value_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow2059(value_2: str, value_1: Any=value_1) -> IEncodable:
            class ObjectExpr2058(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value_2)

            return ObjectExpr2058()

        def _arrow2062(oa: OntologyAnnotation, value_1: Any=value_1) -> IEncodable:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2059, gen_id(value_1)), try_include("parameterName", _arrow2062, value_1.ParameterName)]))
        class ObjectExpr2065(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any], value_1: Any=value_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_1))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_1.encode_object(arg)

        return ObjectExpr2065()

    if id_map is not None:
        def _arrow2066(p_1: ProtocolParameter, id_map: Any=id_map, value: Any=value) -> str:
            return gen_id(p_1)

        return encode(_arrow2066, f, value, id_map)

    else: 
        return f(value)



def _arrow2071(get: IGetters) -> ProtocolParameter:
    def _arrow2069(__unit: None=None) -> OntologyAnnotation | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("parameterName", OntologyAnnotation_ISAJson_decoder)

    return ProtocolParameter(None, _arrow2069())


decoder: Decoder_1[ProtocolParameter] = object(_arrow2071)

__all__ = ["gen_id", "encoder", "decoder"]

