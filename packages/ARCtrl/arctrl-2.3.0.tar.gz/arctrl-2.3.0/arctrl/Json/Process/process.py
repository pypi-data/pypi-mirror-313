from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (choose, singleton, of_array, FSharpList)
from ...fable_modules.fable_library.option import map
from ...fable_modules.fable_library.seq import map as map_1
from ...fable_modules.fable_library.string_ import replace
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, list_1 as list_1_2, IGetters)
from ...fable_modules.thoth_json_core.encode import list_1 as list_1_1
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ...Core.comment import Comment
from ...Core.Process.process import Process
from ...Core.Process.process_input import ProcessInput
from ...Core.Process.process_output import ProcessOutput
from ...Core.Process.process_parameter_value import ProcessParameterValue
from ...Core.Process.protocol import Protocol
from ...Core.uri import URIModule_toString
from ..comment import (ROCrate_encoder as ROCrate_encoder_5, ROCrate_decoder as ROCrate_decoder_5, ISAJson_encoder as ISAJson_encoder_5, ISAJson_decoder as ISAJson_decoder_5)
from ..context.rocrate.isa_process_context import context_jsonvalue
from ..decode import Decode_uri
from ..encode import (try_include, try_include_list_opt)
from ..idtable import encode
from ..person import (ROCrate_encodeAuthorListString, ROCrate_decodeAuthorListString)
from .process_input import (ROCrate_encoder as ROCrate_encoder_3, ROCrate_decoder as ROCrate_decoder_3, ISAJson_encoder as ISAJson_encoder_3, ISAJson_decoder as ISAJson_decoder_3)
from .process_output import (ROCrate_encoder as ROCrate_encoder_4, ROCrate_decoder as ROCrate_decoder_4, ISAJson_encoder as ISAJson_encoder_4, ISAJson_decoder as ISAJson_decoder_4)
from .process_parameter_value import (ROCrate_encoder as ROCrate_encoder_2, ROCrate_decoder as ROCrate_decoder_2, ISAJson_encoder as ISAJson_encoder_2, ISAJson_decoder as ISAJson_decoder_2)
from .protocol import (ROCrate_encoder as ROCrate_encoder_1, ROCrate_decoder as ROCrate_decoder_1, ISAJson_encoder as ISAJson_encoder_1, ISAJson_decoder as ISAJson_decoder_1)

__A_ = TypeVar("__A_")

def ROCrate_genID(p: Process) -> str:
    match_value: str | None = p.ID
    if match_value is None:
        match_value_1: str | None = p.Name
        if match_value_1 is None:
            return "#EmptyProcess"

        else: 
            return "#Process_" + replace(match_value_1, " ", "_")


    else: 
        return URIModule_toString(match_value)



def ROCrate_encoder(study_name: str | None, assay_name: str | None, oa: Process) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2411(__unit: None=None, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(oa)
        class ObjectExpr2410(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2410()

    class ObjectExpr2412(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> Any:
            return helpers_1.encode_string("Process")

    def _arrow2414(value_2: str, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> IEncodable:
        class ObjectExpr2413(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr2413()

    def _arrow2415(oa_1: Protocol, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_1(study_name, assay_name, oa.Name, oa_1)

    def _arrow2416(author_list: str, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> IEncodable:
        return ROCrate_encodeAuthorListString(author_list)

    def _arrow2418(value_4: str, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> IEncodable:
        class ObjectExpr2417(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_4)

        return ObjectExpr2417()

    def _arrow2419(value_6: ProcessInput, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_3(value_6)

    def _arrow2420(value_7: ProcessOutput, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_4(value_7)

    def _arrow2421(comment: Comment, study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> IEncodable:
        return ROCrate_encoder_5(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2411()), ("@type", list_1_1(singleton(ObjectExpr2412()))), try_include("name", _arrow2414, oa.Name), try_include("executesProtocol", _arrow2415, oa.ExecutesProtocol), try_include_list_opt("parameterValues", ROCrate_encoder_2, oa.ParameterValues), try_include("performer", _arrow2416, oa.Performer), try_include("date", _arrow2418, oa.Date), try_include_list_opt("inputs", _arrow2419, oa.Inputs), try_include_list_opt("outputs", _arrow2420, oa.Outputs), try_include_list_opt("comments", _arrow2421, oa.Comments), ("@context", context_jsonvalue)]))
    class ObjectExpr2422(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], study_name: Any=study_name, assay_name: Any=assay_name, oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr2422()


def _arrow2432(get: IGetters) -> Process:
    def _arrow2423(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("@id", Decode_uri)

    def _arrow2424(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("name", string)

    def _arrow2425(__unit: None=None) -> Protocol | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("executesProtocol", ROCrate_decoder_1)

    def _arrow2426(__unit: None=None) -> FSharpList[ProcessParameterValue] | None:
        arg_7: Decoder_1[FSharpList[ProcessParameterValue]] = list_1_2(ROCrate_decoder_2)
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("parameterValues", arg_7)

    def _arrow2427(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("performer", ROCrate_decodeAuthorListString)

    def _arrow2428(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("date", string)

    def _arrow2429(__unit: None=None) -> FSharpList[ProcessInput] | None:
        arg_13: Decoder_1[FSharpList[ProcessInput]] = list_1_2(ROCrate_decoder_3)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("inputs", arg_13)

    def _arrow2430(__unit: None=None) -> FSharpList[ProcessOutput] | None:
        arg_15: Decoder_1[FSharpList[ProcessOutput]] = list_1_2(ROCrate_decoder_4)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("outputs", arg_15)

    def _arrow2431(__unit: None=None) -> FSharpList[Comment] | None:
        arg_17: Decoder_1[FSharpList[Comment]] = list_1_2(ROCrate_decoder_5)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("comments", arg_17)

    return Process(_arrow2423(), _arrow2424(), _arrow2425(), _arrow2426(), _arrow2427(), _arrow2428(), None, None, _arrow2429(), _arrow2430(), _arrow2431())


ROCrate_decoder: Decoder_1[Process] = object(_arrow2432)

def ISAJson_encoder(study_name: str | None, assay_name: str | None, id_map: Any | None, oa: Process) -> IEncodable:
    def f(oa_1: Process, study_name: Any=study_name, assay_name: Any=assay_name, id_map: Any=id_map, oa: Any=oa) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], oa_1: Any=oa_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow2438(value: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2437(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr2437()

        def _arrow2440(value_2: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2439(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_2)

            return ObjectExpr2439()

        def _arrow2441(oa_2: Protocol, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_1(study_name, assay_name, oa_1.Name, id_map, oa_2)

        def _arrow2443(oa_3: ProcessParameterValue, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_2(id_map, oa_3)

        def _arrow2446(value_4: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2445(IEncodable):
                def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_2.encode_string(value_4)

            return ObjectExpr2445()

        def _arrow2449(value_6: str, oa_1: Any=oa_1) -> IEncodable:
            class ObjectExpr2448(IEncodable):
                def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_3.encode_string(value_6)

            return ObjectExpr2448()

        def _arrow2450(oa_4: Process, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder(study_name, assay_name, id_map, oa_4)

        def _arrow2451(oa_5: Process, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder(study_name, assay_name, id_map, oa_5)

        def _arrow2452(value_8: ProcessInput, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_3(id_map, value_8)

        def _arrow2453(value_9: ProcessOutput, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_4(id_map, value_9)

        def _arrow2454(comment: Comment, oa_1: Any=oa_1) -> IEncodable:
            return ISAJson_encoder_5(id_map, comment)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2438, ROCrate_genID(oa_1)), try_include("name", _arrow2440, oa_1.Name), try_include("executesProtocol", _arrow2441, oa_1.ExecutesProtocol), try_include_list_opt("parameterValues", _arrow2443, oa_1.ParameterValues), try_include("performer", _arrow2446, oa_1.Performer), try_include("date", _arrow2449, oa_1.Date), try_include("previousProcess", _arrow2450, oa_1.PreviousProcess), try_include("nextProcess", _arrow2451, oa_1.NextProcess), try_include_list_opt("inputs", _arrow2452, oa_1.Inputs), try_include_list_opt("outputs", _arrow2453, oa_1.Outputs), try_include_list_opt("comments", _arrow2454, oa_1.Comments)]))
        class ObjectExpr2455(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any], oa_1: Any=oa_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_4.encode_object(arg)

        return ObjectExpr2455()

    if id_map is not None:
        def _arrow2456(p: Process, study_name: Any=study_name, assay_name: Any=assay_name, id_map: Any=id_map, oa: Any=oa) -> str:
            return ROCrate_genID(p)

        return encode(_arrow2456, f, oa, id_map)

    else: 
        return f(oa)



def _arrow2469(__unit: None=None) -> Decoder_1[Process]:
    def decode(__unit: None=None) -> Decoder_1[Process]:
        def _arrow2468(get: IGetters) -> Process:
            def _arrow2457(__unit: None=None) -> str | None:
                object_arg: IOptionalGetter = get.Optional
                return object_arg.Field("@id", Decode_uri)

            def _arrow2458(__unit: None=None) -> str | None:
                object_arg_1: IOptionalGetter = get.Optional
                return object_arg_1.Field("name", string)

            def _arrow2459(__unit: None=None) -> Protocol | None:
                object_arg_2: IOptionalGetter = get.Optional
                return object_arg_2.Field("executesProtocol", ISAJson_decoder_1)

            def _arrow2460(__unit: None=None) -> FSharpList[ProcessParameterValue] | None:
                arg_7: Decoder_1[FSharpList[ProcessParameterValue]] = list_1_2(ISAJson_decoder_2)
                object_arg_3: IOptionalGetter = get.Optional
                return object_arg_3.Field("parameterValues", arg_7)

            def _arrow2461(__unit: None=None) -> str | None:
                object_arg_4: IOptionalGetter = get.Optional
                return object_arg_4.Field("performer", string)

            def _arrow2462(__unit: None=None) -> str | None:
                object_arg_5: IOptionalGetter = get.Optional
                return object_arg_5.Field("date", string)

            def _arrow2463(__unit: None=None) -> Process | None:
                arg_13: Decoder_1[Process] = decode(None)
                object_arg_6: IOptionalGetter = get.Optional
                return object_arg_6.Field("previousProcess", arg_13)

            def _arrow2464(__unit: None=None) -> Process | None:
                arg_15: Decoder_1[Process] = decode(None)
                object_arg_7: IOptionalGetter = get.Optional
                return object_arg_7.Field("nextProcess", arg_15)

            def _arrow2465(__unit: None=None) -> FSharpList[ProcessInput] | None:
                arg_17: Decoder_1[FSharpList[ProcessInput]] = list_1_2(ISAJson_decoder_3)
                object_arg_8: IOptionalGetter = get.Optional
                return object_arg_8.Field("inputs", arg_17)

            def _arrow2466(__unit: None=None) -> FSharpList[ProcessOutput] | None:
                arg_19: Decoder_1[FSharpList[ProcessOutput]] = list_1_2(ISAJson_decoder_4)
                object_arg_9: IOptionalGetter = get.Optional
                return object_arg_9.Field("outputs", arg_19)

            def _arrow2467(__unit: None=None) -> FSharpList[Comment] | None:
                arg_21: Decoder_1[FSharpList[Comment]] = list_1_2(ISAJson_decoder_5)
                object_arg_10: IOptionalGetter = get.Optional
                return object_arg_10.Field("comments", arg_21)

            return Process(_arrow2457(), _arrow2458(), _arrow2459(), _arrow2460(), _arrow2461(), _arrow2462(), _arrow2463(), _arrow2464(), _arrow2465(), _arrow2466(), _arrow2467())

        return object(_arrow2468)

    return decode(None)


ISAJson_decoder: Decoder_1[Process] = _arrow2469()

__all__ = ["ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_decoder"]

