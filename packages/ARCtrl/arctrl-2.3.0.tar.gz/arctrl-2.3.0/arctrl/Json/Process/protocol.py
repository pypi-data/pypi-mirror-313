from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (choose, singleton, of_array, FSharpList, empty, append)
from ...fable_modules.fable_library.option import (map, default_arg)
from ...fable_modules.fable_library.seq import map as map_1
from ...fable_modules.fable_library.string_ import replace
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.thoth_json_core.decode import (object, list_1 as list_1_2, IOptionalGetter, string, IGetters)
from ...fable_modules.thoth_json_core.encode import list_1 as list_1_1
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ...Core.comment import Comment
from ...Core.Helper.collections_ import Option_fromValueWithDefault
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Process.component import Component
from ...Core.Process.protocol import Protocol
from ...Core.Process.protocol_parameter import ProtocolParameter
from ..comment import (ROCrate_encoder as ROCrate_encoder_2, ROCrate_decoder as ROCrate_decoder_2, ISAJson_encoder as ISAJson_encoder_2, ISAJson_decoder as ISAJson_decoder_2)
from ..context.rocrate.isa_protocol_context import context_jsonvalue
from ..decode import Decode_uri
from ..encode import (try_include, try_include_list_opt)
from ..idtable import encode
from ..ontology_annotation import (OntologyAnnotation_ROCrate_encoderDefinedTerm, OntologyAnnotation_ROCrate_decoderDefinedTerm, OntologyAnnotation_ISAJson_encoder, OntologyAnnotation_ISAJson_decoder)
from .component import (ROCrate_encoder as ROCrate_encoder_1, ROCrate_decoder as ROCrate_decoder_1, ISAJson_encoder as ISAJson_encoder_1, ISAJson_decoder as ISAJson_decoder_1)
from .protocol_parameter import (encoder, decoder)

__A_ = TypeVar("__A_")

def ROCrate_genID(study_name: str | None, assay_name: str | None, process_name: str | None, p: Protocol) -> str:
    match_value: str | None = p.ID
    (pattern_matching_result, id_1) = (None, None)
    if match_value is not None:
        if match_value != "":
            pattern_matching_result = 0
            id_1 = match_value

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        return id_1

    elif pattern_matching_result == 1:
        match_value_1: str | None = p.Uri
        if match_value_1 is None:
            match_value_2: str | None = p.Name
            if match_value_2 is None:
                (pattern_matching_result_1, an, pn, sn, pn_1, sn_1, pn_2) = (None, None, None, None, None, None, None)
                if study_name is None:
                    if assay_name is None:
                        if process_name is not None:
                            pattern_matching_result_1 = 2
                            pn_2 = process_name

                        else: 
                            pattern_matching_result_1 = 3


                    else: 
                        pattern_matching_result_1 = 3


                elif assay_name is None:
                    if process_name is not None:
                        pattern_matching_result_1 = 1
                        pn_1 = process_name
                        sn_1 = study_name

                    else: 
                        pattern_matching_result_1 = 3


                elif process_name is not None:
                    pattern_matching_result_1 = 0
                    an = assay_name
                    pn = process_name
                    sn = study_name

                else: 
                    pattern_matching_result_1 = 3

                if pattern_matching_result_1 == 0:
                    return (((("#Protocol_" + replace(sn, " ", "_")) + "_") + replace(an, " ", "_")) + "_") + replace(pn, " ", "_")

                elif pattern_matching_result_1 == 1:
                    return (("#Protocol_" + replace(sn_1, " ", "_")) + "_") + replace(pn_1, " ", "_")

                elif pattern_matching_result_1 == 2:
                    return "#Protocol_" + replace(pn_2, " ", "_")

                elif pattern_matching_result_1 == 3:
                    return "#EmptyProtocol"


            else: 
                return "#Protocol_" + replace(match_value_2, " ", "_")


        else: 
            return match_value_1




def ROCrate_encoder(study_name: str | None, assay_name: str | None, process_name: str | None, oa: Protocol) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], study_name: Any=study_name, assay_name: Any=assay_name, process_name: Any=process_name, oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2224(__unit: None=None, study_name: Any=study_name, assay_name: Any=assay_name, process_name: Any=process_name, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(study_name, assay_name, process_name, oa)
        class ObjectExpr2223(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2223()

    class ObjectExpr2225(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], study_name: Any=study_name, assay_name: Any=assay_name, process_name: Any=process_name, oa: Any=oa) -> Any:
            return helpers_1.encode_string("Protocol")

    def _arrow2227(value_2: str, study_name: Any=study_name, assay_name: Any=assay_name, process_name: Any=process_name, oa: Any=oa) -> IEncodable:
        class ObjectExpr2226(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr2226()

    def _arrow2228(oa_1: OntologyAnnotation, study_name: Any=study_name, assay_name: Any=assay_name, process_name: Any=process_name, oa: Any=oa) -> IEncodable:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa_1)

    def _arrow2230(value_4: str, study_name: Any=study_name, assay_name: Any=assay_name, process_name: Any=process_name, oa: Any=oa) -> IEncodable:
        class ObjectExpr2229(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_4)

        return ObjectExpr2229()

    def _arrow2232(value_6: str, study_name: Any=study_name, assay_name: Any=assay_name, process_name: Any=process_name, oa: Any=oa) -> IEncodable:
        class ObjectExpr2231(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_6)

        return ObjectExpr2231()

    def _arrow2234(value_8: str, study_name: Any=study_name, assay_name: Any=assay_name, process_name: Any=process_name, oa: Any=oa) -> IEncodable:
        class ObjectExpr2233(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_8)

        return ObjectExpr2233()

    def _arrow2235(comment: Comment, study_name: Any=study_name, assay_name: Any=assay_name, process_name: Any=process_name, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_2(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2224()), ("@type", list_1_1(singleton(ObjectExpr2225()))), try_include("name", _arrow2227, oa.Name), try_include("protocolType", _arrow2228, oa.ProtocolType), try_include("description", _arrow2230, oa.Description), try_include("uri", _arrow2232, oa.Uri), try_include("version", _arrow2234, oa.Version), try_include_list_opt("components", ROCrate_encoder_1, oa.Components), try_include_list_opt("comments", _arrow2235, oa.Comments), ("@context", context_jsonvalue)]))
    class ObjectExpr2236(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any], study_name: Any=study_name, assay_name: Any=assay_name, process_name: Any=process_name, oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_6))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_6.encode_object(arg)

    return ObjectExpr2236()


def _arrow2248(get: IGetters) -> Protocol:
    def _arrow2240(__unit: None=None) -> FSharpList[Component]:
        list_4: FSharpList[Component]
        def _arrow2237(__unit: None=None) -> FSharpList[Component] | None:
            arg_1: Decoder_1[FSharpList[Component]] = list_1_2(ROCrate_decoder_1)
            object_arg: IOptionalGetter = get.Optional
            return object_arg.Field("components", arg_1)

        list_2: FSharpList[Component] = default_arg(_arrow2237(), empty())
        def _arrow2238(__unit: None=None) -> FSharpList[Component] | None:
            arg_3: Decoder_1[FSharpList[Component]] = list_1_2(ROCrate_decoder_1)
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("reagents", arg_3)

        list_4 = append(default_arg(_arrow2238(), empty()), list_2)
        def _arrow2239(__unit: None=None) -> FSharpList[Component] | None:
            arg_5: Decoder_1[FSharpList[Component]] = list_1_2(ROCrate_decoder_1)
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("computationalTools", arg_5)

        return append(default_arg(_arrow2239(), empty()), list_4)

    components: FSharpList[Component] | None = Option_fromValueWithDefault(empty(), _arrow2240())
    def _arrow2241(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("@id", Decode_uri)

    def _arrow2242(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("name", string)

    def _arrow2243(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("protocolType", OntologyAnnotation_ROCrate_decoderDefinedTerm)

    def _arrow2244(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("description", string)

    def _arrow2245(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("uri", Decode_uri)

    def _arrow2246(__unit: None=None) -> str | None:
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("version", string)

    def _arrow2247(__unit: None=None) -> FSharpList[Comment] | None:
        arg_19: Decoder_1[FSharpList[Comment]] = list_1_2(ROCrate_decoder_2)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("comments", arg_19)

    return Protocol(_arrow2241(), _arrow2242(), _arrow2243(), _arrow2244(), _arrow2245(), _arrow2246(), None, components, _arrow2247())


ROCrate_decoder: Decoder_1[Protocol] = object(_arrow2248)

def ISAJson_encoder(study_name: str | None, assay_name: str | None, process_name: str | None, id_map: Any | None, oa: Protocol) -> IEncodable:
    def f(oa_1: Protocol, study_name: Any=study_name, assay_name: Any=assay_name, process_name: Any=process_name, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], oa_1: Any=oa_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow2252(value: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2251(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr2251()

        def _arrow2254(value_2: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2253(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_2)

            return ObjectExpr2253()

        def _arrow2255(oa_2: OntologyAnnotation, oa_1: Any=oa_1) -> IEncodable:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa_2)

        def _arrow2257(value_4: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2256(IEncodable):
                def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_2.encode_string(value_4)

            return ObjectExpr2256()

        def _arrow2259(value_6: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2258(IEncodable):
                def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_3.encode_string(value_6)

            return ObjectExpr2258()

        def _arrow2261(value_8: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2260(IEncodable):
                def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_4.encode_string(value_8)

            return ObjectExpr2260()

        def _arrow2262(value_10: ProtocolParameter, oa_1: Any=oa_1) -> IEncodable:
            return encoder(id_map, value_10)

        def _arrow2263(c: Component, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_1(id_map, c)

        def _arrow2264(comment: Comment, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_2(id_map, comment)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2252, ROCrate_genID(study_name, assay_name, process_name, oa_1)), try_include("name", _arrow2254, oa_1.Name), try_include("protocolType", _arrow2255, oa_1.ProtocolType), try_include("description", _arrow2257, oa_1.Description), try_include("uri", _arrow2259, oa_1.Uri), try_include("version", _arrow2261, oa_1.Version), try_include_list_opt("parameters", _arrow2262, oa_1.Parameters), try_include_list_opt("components", _arrow2263, oa_1.Components), try_include_list_opt("comments", _arrow2264, oa_1.Comments)]))
        class ObjectExpr2265(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any], oa_1: Any=oa_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_5))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_5.encode_object(arg)

        return ObjectExpr2265()

    if id_map is not None:
        def _arrow2266(p_1: Protocol, study_name: Any=study_name, assay_name: Any=assay_name, process_name: Any=process_name, id_map: Any=id_map, oa: Any=oa) -> str:
            return ROCrate_genID(study_name, assay_name, process_name, p_1)

        return encode(_arrow2266, f, oa, id_map)

    else: 
        return f(oa)



def _arrow2276(get: IGetters) -> Protocol:
    def _arrow2267(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow2268(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow2269(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("protocolType", OntologyAnnotation_ISAJson_decoder)

    def _arrow2270(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("description", string)

    def _arrow2271(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("uri", Decode_uri)

    def _arrow2272(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("version", string)

    def _arrow2273(__unit: None=None) -> FSharpList[ProtocolParameter] | None:
        arg_13: Decoder_1[FSharpList[ProtocolParameter]] = list_1_2(decoder)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("parameters", arg_13)

    def _arrow2274(__unit: None=None) -> FSharpList[Component] | None:
        arg_15: Decoder_1[FSharpList[Component]] = list_1_2(ISAJson_decoder_1)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("components", arg_15)

    def _arrow2275(__unit: None=None) -> FSharpList[Comment] | None:
        arg_17: Decoder_1[FSharpList[Comment]] = list_1_2(ISAJson_decoder_2)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("comments", arg_17)

    return Protocol(_arrow2267(), _arrow2268(), _arrow2269(), _arrow2270(), _arrow2271(), _arrow2272(), _arrow2273(), _arrow2274(), _arrow2275())


ISAJson_decoder: Decoder_1[Protocol] = object(_arrow2276)

__all__ = ["ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_decoder"]

