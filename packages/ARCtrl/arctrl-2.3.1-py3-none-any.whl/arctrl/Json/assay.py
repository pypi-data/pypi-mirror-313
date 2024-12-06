from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList, singleton, empty)
from ..fable_modules.fable_library.option import (map, default_arg, bind)
from ..fable_modules.fable_library.seq import map as map_1
from ..fable_modules.fable_library.string_ import replace
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.decode import (object, IRequiredGetter, string, IOptionalGetter, resize_array, IGetters, list_1 as list_1_2, map as map_2)
from ..fable_modules.thoth_json_core.encode import list_1 as list_1_1
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.arc_types import ArcAssay
from ..Core.comment import Comment
from ..Core.conversion import (ARCtrl_ArcTables__ArcTables_GetProcesses, ARCtrl_ArcTables__ArcTables_fromProcesses_Static_62A3309D, JsonTypes_composeTechnologyPlatform, JsonTypes_decomposeTechnologyPlatform)
from ..Core.data import Data
from ..Core.data_map import DataMap
from ..Core.Helper.collections_ import Option_fromValueWithDefault
from ..Core.Helper.identifier import (Assay_fileNameFromIdentifier, create_missing_identifier, Assay_tryIdentifierFromFileName)
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.person import Person
from ..Core.Process.material_attribute import MaterialAttribute
from ..Core.Process.process import Process
from ..Core.Process.process_sequence import (get_data, get_units, get_characteristics)
from ..Core.Table.arc_table import ArcTable
from ..Core.Table.arc_tables import ArcTables
from ..Core.Table.composite_cell import CompositeCell
from .comment import (encoder as encoder_7, decoder as decoder_4, ROCrate_encoder as ROCrate_encoder_4, ROCrate_decoder as ROCrate_decoder_3, ISAJson_encoder as ISAJson_encoder_3, ISAJson_decoder as ISAJson_decoder_2)
from .context.rocrate.isa_assay_context import context_jsonvalue
from .data import (ROCrate_encoder as ROCrate_encoder_2, ISAJson_encoder as ISAJson_encoder_1)
from .DataMap.data_map import (encoder as encoder_4, decoder as decoder_2, encoder_compressed as encoder_compressed_2, decoder_compressed as decoder_compressed_2)
from .decode import Decode_objectNoAdditionalProperties
from .encode import (try_include, try_include_seq, try_include_list)
from .idtable import encode
from .ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder, OntologyAnnotation_ROCrate_encoderPropertyValue, OntologyAnnotation_ROCrate_encoderDefinedTerm, OntologyAnnotation_ROCrate_decoderPropertyValue, OntologyAnnotation_ROCrate_decoderDefinedTerm, OntologyAnnotation_ISAJson_encoder, OntologyAnnotation_ISAJson_decoder)
from .person import (encoder as encoder_6, decoder as decoder_3, ROCrate_encoder as ROCrate_encoder_1, ROCrate_decoder as ROCrate_decoder_2)
from .Process.assay_materials import encoder as encoder_9
from .Process.material_attribute import encoder as encoder_8
from .Process.process import (ROCrate_encoder as ROCrate_encoder_3, ROCrate_decoder as ROCrate_decoder_1, ISAJson_encoder as ISAJson_encoder_2, ISAJson_decoder as ISAJson_decoder_1)
from .Table.arc_table import (encoder as encoder_5, decoder as decoder_1, encoder_compressed as encoder_compressed_1, decoder_compressed as decoder_compressed_1)

__A_ = TypeVar("__A_")

def encoder(assay: ArcAssay) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], assay: Any=assay) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2624(__unit: None=None, assay: Any=assay) -> IEncodable:
        value: str = assay.Identifier
        class ObjectExpr2623(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2623()

    def _arrow2625(oa: OntologyAnnotation, assay: Any=assay) -> IEncodable:
        return OntologyAnnotation_encoder(oa)

    def _arrow2626(oa_1: OntologyAnnotation, assay: Any=assay) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow2627(oa_2: OntologyAnnotation, assay: Any=assay) -> IEncodable:
        return OntologyAnnotation_encoder(oa_2)

    def _arrow2628(dm: DataMap, assay: Any=assay) -> IEncodable:
        return encoder_4(dm)

    def _arrow2629(table: ArcTable, assay: Any=assay) -> IEncodable:
        return encoder_5(table)

    def _arrow2630(person: Person, assay: Any=assay) -> IEncodable:
        return encoder_6(person)

    def _arrow2631(comment: Comment, assay: Any=assay) -> IEncodable:
        return encoder_7(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("Identifier", _arrow2624()), try_include("MeasurementType", _arrow2625, assay.MeasurementType), try_include("TechnologyType", _arrow2626, assay.TechnologyType), try_include("TechnologyPlatform", _arrow2627, assay.TechnologyPlatform), try_include("DataMap", _arrow2628, assay.DataMap), try_include_seq("Tables", _arrow2629, assay.Tables), try_include_seq("Performers", _arrow2630, assay.Performers), try_include_seq("Comments", _arrow2631, assay.Comments)]))
    class ObjectExpr2632(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], assay: Any=assay) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_1))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_1.encode_object(arg)

    return ObjectExpr2632()


def _arrow2641(get: IGetters) -> ArcAssay:
    def _arrow2633(__unit: None=None) -> str:
        object_arg: IRequiredGetter = get.Required
        return object_arg.Field("Identifier", string)

    def _arrow2634(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("MeasurementType", OntologyAnnotation_decoder)

    def _arrow2635(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("TechnologyType", OntologyAnnotation_decoder)

    def _arrow2636(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("TechnologyPlatform", OntologyAnnotation_decoder)

    def _arrow2637(__unit: None=None) -> Array[ArcTable] | None:
        arg_9: Decoder_1[Array[ArcTable]] = resize_array(decoder_1)
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("Tables", arg_9)

    def _arrow2638(__unit: None=None) -> DataMap | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("DataMap", decoder_2)

    def _arrow2639(__unit: None=None) -> Array[Person] | None:
        arg_13: Decoder_1[Array[Person]] = resize_array(decoder_3)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("Performers", arg_13)

    def _arrow2640(__unit: None=None) -> Array[Comment] | None:
        arg_15: Decoder_1[Array[Comment]] = resize_array(decoder_4)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("Comments", arg_15)

    return ArcAssay.create(_arrow2633(), _arrow2634(), _arrow2635(), _arrow2636(), _arrow2637(), _arrow2638(), _arrow2639(), _arrow2640())


decoder: Decoder_1[ArcAssay] = object(_arrow2641)

def encoder_compressed(string_table: Any, oa_table: Any, cell_table: Any, assay: ArcAssay) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2645(__unit: None=None, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> IEncodable:
        value: str = assay.Identifier
        class ObjectExpr2644(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2644()

    def _arrow2646(oa: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> IEncodable:
        return OntologyAnnotation_encoder(oa)

    def _arrow2647(oa_1: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow2648(oa_2: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> IEncodable:
        return OntologyAnnotation_encoder(oa_2)

    def _arrow2649(table: ArcTable, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> IEncodable:
        return encoder_compressed_1(string_table, oa_table, cell_table, table)

    def _arrow2650(dm: DataMap, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> IEncodable:
        return encoder_compressed_2(string_table, oa_table, cell_table, dm)

    def _arrow2651(person: Person, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> IEncodable:
        return encoder_6(person)

    def _arrow2652(comment: Comment, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> IEncodable:
        return encoder_7(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("Identifier", _arrow2645()), try_include("MeasurementType", _arrow2646, assay.MeasurementType), try_include("TechnologyType", _arrow2647, assay.TechnologyType), try_include("TechnologyPlatform", _arrow2648, assay.TechnologyPlatform), try_include_seq("Tables", _arrow2649, assay.Tables), try_include("DataMap", _arrow2650, assay.DataMap), try_include_seq("Performers", _arrow2651, assay.Performers), try_include_seq("Comments", _arrow2652, assay.Comments)]))
    class ObjectExpr2653(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, assay: Any=assay) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_1))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_1.encode_object(arg)

    return ObjectExpr2653()


def decoder_compressed(string_table: Array[str], oa_table: Array[OntologyAnnotation], cell_table: Array[CompositeCell]) -> Decoder_1[ArcAssay]:
    def _arrow2662(get: IGetters, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table) -> ArcAssay:
        def _arrow2654(__unit: None=None) -> str:
            object_arg: IRequiredGetter = get.Required
            return object_arg.Field("Identifier", string)

        def _arrow2655(__unit: None=None) -> OntologyAnnotation | None:
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("MeasurementType", OntologyAnnotation_decoder)

        def _arrow2656(__unit: None=None) -> OntologyAnnotation | None:
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("TechnologyType", OntologyAnnotation_decoder)

        def _arrow2657(__unit: None=None) -> OntologyAnnotation | None:
            object_arg_3: IOptionalGetter = get.Optional
            return object_arg_3.Field("TechnologyPlatform", OntologyAnnotation_decoder)

        def _arrow2658(__unit: None=None) -> Array[ArcTable] | None:
            arg_9: Decoder_1[Array[ArcTable]] = resize_array(decoder_compressed_1(string_table, oa_table, cell_table))
            object_arg_4: IOptionalGetter = get.Optional
            return object_arg_4.Field("Tables", arg_9)

        def _arrow2659(__unit: None=None) -> DataMap | None:
            arg_11: Decoder_1[DataMap] = decoder_compressed_2(string_table, oa_table, cell_table)
            object_arg_5: IOptionalGetter = get.Optional
            return object_arg_5.Field("DataMap", arg_11)

        def _arrow2660(__unit: None=None) -> Array[Person] | None:
            arg_13: Decoder_1[Array[Person]] = resize_array(decoder_3)
            object_arg_6: IOptionalGetter = get.Optional
            return object_arg_6.Field("Performers", arg_13)

        def _arrow2661(__unit: None=None) -> Array[Comment] | None:
            arg_15: Decoder_1[Array[Comment]] = resize_array(decoder_4)
            object_arg_7: IOptionalGetter = get.Optional
            return object_arg_7.Field("Comments", arg_15)

        return ArcAssay.create(_arrow2654(), _arrow2655(), _arrow2656(), _arrow2657(), _arrow2658(), _arrow2659(), _arrow2660(), _arrow2661())

    return object(_arrow2662)


def ROCrate_genID(a: ArcAssay) -> str:
    match_value: str = a.Identifier
    if match_value == "":
        return "#EmptyAssay"

    else: 
        return ("#assay/" + replace(match_value, " ", "_")) + ""



def ROCrate_encoder(study_name: str | None, a: ArcAssay) -> IEncodable:
    file_name: str = Assay_fileNameFromIdentifier(a.Identifier)
    processes: FSharpList[Process] = ARCtrl_ArcTables__ArcTables_GetProcesses(a)
    data_files: FSharpList[Data] = get_data(processes)
    def chooser(tupled_arg: tuple[str, IEncodable | None], study_name: Any=study_name, a: Any=a) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2666(__unit: None=None, study_name: Any=study_name, a: Any=a) -> IEncodable:
        value: str = ROCrate_genID(a)
        class ObjectExpr2665(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2665()

    class ObjectExpr2667(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], study_name: Any=study_name, a: Any=a) -> Any:
            return helpers_1.encode_string("Assay")

    class ObjectExpr2668(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], study_name: Any=study_name, a: Any=a) -> Any:
            return helpers_2.encode_string("Assay")

    def _arrow2670(__unit: None=None, study_name: Any=study_name, a: Any=a) -> IEncodable:
        value_3: str = a.Identifier
        class ObjectExpr2669(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_3)

        return ObjectExpr2669()

    class ObjectExpr2671(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], study_name: Any=study_name, a: Any=a) -> Any:
            return helpers_4.encode_string(file_name)

    def _arrow2672(oa: OntologyAnnotation, study_name: Any=study_name, a: Any=a) -> IEncodable:
        return OntologyAnnotation_ROCrate_encoderPropertyValue(oa)

    def _arrow2673(oa_1: OntologyAnnotation, study_name: Any=study_name, a: Any=a) -> IEncodable:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa_1)

    def _arrow2674(oa_2: OntologyAnnotation, study_name: Any=study_name, a: Any=a) -> IEncodable:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa_2)

    def _arrow2675(oa_3: Person, study_name: Any=study_name, a: Any=a) -> IEncodable:
        return ROCrate_encoder_1(oa_3)

    def _arrow2676(oa_4: Data, study_name: Any=study_name, a: Any=a) -> IEncodable:
        return ROCrate_encoder_2(oa_4)

    def _arrow2678(__unit: None=None, study_name: Any=study_name, a: Any=a) -> Callable[[Process], IEncodable]:
        assay_name: str | None = a.Identifier
        def _arrow2677(oa_5: Process) -> IEncodable:
            return ROCrate_encoder_3(study_name, assay_name, oa_5)

        return _arrow2677

    def _arrow2679(comment: Comment, study_name: Any=study_name, a: Any=a) -> IEncodable:
        return ROCrate_encoder_4(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2666()), ("@type", list_1_1(singleton(ObjectExpr2667()))), ("additionalType", ObjectExpr2668()), ("identifier", _arrow2670()), ("filename", ObjectExpr2671()), try_include("measurementType", _arrow2672, a.MeasurementType), try_include("technologyType", _arrow2673, a.TechnologyType), try_include("technologyPlatform", _arrow2674, a.TechnologyPlatform), try_include_seq("performers", _arrow2675, a.Performers), try_include_list("dataFiles", _arrow2676, data_files), try_include_list("processSequence", _arrow2678(), processes), try_include_seq("comments", _arrow2679, a.Comments), ("@context", context_jsonvalue)]))
    class ObjectExpr2680(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any], study_name: Any=study_name, a: Any=a) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_5))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_5.encode_object(arg)

    return ObjectExpr2680()


def _arrow2688(get: IGetters) -> ArcAssay:
    def _arrow2681(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("identifier", string)

    identifier: str = default_arg(_arrow2681(), create_missing_identifier())
    def mapping(arg_4: FSharpList[Process]) -> Array[ArcTable]:
        a: ArcTables = ARCtrl_ArcTables__ArcTables_fromProcesses_Static_62A3309D(arg_4)
        return a.Tables

    def _arrow2682(__unit: None=None) -> FSharpList[Process] | None:
        arg_3: Decoder_1[FSharpList[Process]] = list_1_2(ROCrate_decoder_1)
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("processSequence", arg_3)

    tables: Array[ArcTable] | None = map(mapping, _arrow2682())
    def _arrow2683(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("measurementType", OntologyAnnotation_ROCrate_decoderPropertyValue)

    def _arrow2684(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("technologyType", OntologyAnnotation_ROCrate_decoderDefinedTerm)

    def _arrow2685(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("technologyPlatform", OntologyAnnotation_ROCrate_decoderDefinedTerm)

    def _arrow2686(__unit: None=None) -> Array[Person] | None:
        arg_12: Decoder_1[Array[Person]] = resize_array(ROCrate_decoder_2)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("performers", arg_12)

    def _arrow2687(__unit: None=None) -> Array[Comment] | None:
        arg_14: Decoder_1[Array[Comment]] = resize_array(ROCrate_decoder_3)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("comments", arg_14)

    return ArcAssay(identifier, _arrow2683(), _arrow2684(), _arrow2685(), tables, None, _arrow2686(), _arrow2687())


ROCrate_decoder: Decoder_1[ArcAssay] = object(_arrow2688)

def ISAJson_encoder(study_name: str | None, id_map: Any | None, a: ArcAssay) -> IEncodable:
    def f(a_1: ArcAssay, study_name: Any=study_name, id_map: Any=id_map, a: Any=a) -> IEncodable:
        file_name: str = Assay_fileNameFromIdentifier(a_1.Identifier)
        processes: FSharpList[Process] = ARCtrl_ArcTables__ArcTables_GetProcesses(a_1)
        def encoder_1(oa: OntologyAnnotation, a_1: Any=a_1) -> IEncodable:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa)

        encoded_units: tuple[str, IEncodable | None] = try_include_list("unitCategories", encoder_1, get_units(processes))
        def encoder_2(value_1: MaterialAttribute, a_1: Any=a_1) -> IEncodable:
            return encoder_8(id_map, value_1)

        encoded_characteristics: tuple[str, IEncodable | None] = try_include_list("characteristicCategories", encoder_2, get_characteristics(processes))
        def _arrow2689(ps: FSharpList[Process], a_1: Any=a_1) -> IEncodable:
            return encoder_9(id_map, ps)

        encoded_materials: tuple[str, IEncodable | None] = try_include("materials", _arrow2689, Option_fromValueWithDefault(empty(), processes))
        def encoder_3(oa_1: Data, a_1: Any=a_1) -> IEncodable:
            return ISAJson_encoder_1(id_map, oa_1)

        encoced_data_files: tuple[str, IEncodable | None] = try_include_list("dataFiles", encoder_3, get_data(processes))
        units: FSharpList[OntologyAnnotation] = get_units(processes)
        def chooser(tupled_arg: tuple[str, IEncodable | None], a_1: Any=a_1) -> tuple[str, IEncodable] | None:
            def mapping_1(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping_1, tupled_arg[1])

        class ObjectExpr2691(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], a_1: Any=a_1) -> Any:
                return helpers.encode_string(file_name)

        def _arrow2693(value_5: str, a_1: Any=a_1) -> IEncodable:
            class ObjectExpr2692(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_5)

            return ObjectExpr2692()

        def _arrow2694(oa_2: OntologyAnnotation, a_1: Any=a_1) -> IEncodable:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa_2)

        def _arrow2695(oa_3: OntologyAnnotation, a_1: Any=a_1) -> IEncodable:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa_3)

        def _arrow2697(value_7: str, a_1: Any=a_1) -> IEncodable:
            class ObjectExpr2696(IEncodable):
                def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_2.encode_string(value_7)

            return ObjectExpr2696()

        def mapping(tp: OntologyAnnotation, a_1: Any=a_1) -> str:
            return JsonTypes_composeTechnologyPlatform(tp)

        def _arrow2699(__unit: None=None, a_1: Any=a_1) -> Callable[[Process], IEncodable]:
            assay_name: str | None = a_1.Identifier
            def _arrow2698(oa_4: Process) -> IEncodable:
                return ISAJson_encoder_2(study_name, assay_name, id_map, oa_4)

            return _arrow2698

        def _arrow2700(comment: Comment, a_1: Any=a_1) -> IEncodable:
            return ISAJson_encoder_3(id_map, comment)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("filename", ObjectExpr2691()), try_include("@id", _arrow2693, ROCrate_genID(a_1)), try_include("measurementType", _arrow2694, a_1.MeasurementType), try_include("technologyType", _arrow2695, a_1.TechnologyType), try_include("technologyPlatform", _arrow2697, map(mapping, a_1.TechnologyPlatform)), encoced_data_files, encoded_materials, encoded_characteristics, encoded_units, try_include_list("processSequence", _arrow2699(), processes), try_include_seq("comments", _arrow2700, a_1.Comments)]))
        class ObjectExpr2701(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any], a_1: Any=a_1) -> Any:
                def mapping_2(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_3))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_2, values)
                return helpers_3.encode_object(arg)

        return ObjectExpr2701()

    if id_map is not None:
        def _arrow2702(a_2: ArcAssay, study_name: Any=study_name, id_map: Any=id_map, a: Any=a) -> str:
            return ROCrate_genID(a_2)

        return encode(_arrow2702, f, a, id_map)

    else: 
        return f(a)



ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "filename", "measurementType", "technologyType", "technologyPlatform", "dataFiles", "materials", "characteristicCategories", "unitCategories", "processSequence", "comments", "@type", "@context"])

def _arrow2709(get: IGetters) -> ArcAssay:
    def _arrow2703(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("filename", string)

    identifier: str = default_arg(bind(Assay_tryIdentifierFromFileName, _arrow2703()), create_missing_identifier())
    def mapping(arg_4: FSharpList[Process]) -> Array[ArcTable]:
        a: ArcTables = ARCtrl_ArcTables__ArcTables_fromProcesses_Static_62A3309D(arg_4)
        return a.Tables

    def _arrow2704(__unit: None=None) -> FSharpList[Process] | None:
        arg_3: Decoder_1[FSharpList[Process]] = list_1_2(ISAJson_decoder_1)
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("processSequence", arg_3)

    tables: Array[ArcTable] | None = map(mapping, _arrow2704())
    def _arrow2705(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("measurementType", OntologyAnnotation_ISAJson_decoder)

    def _arrow2706(__unit: None=None) -> OntologyAnnotation | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("technologyType", OntologyAnnotation_ISAJson_decoder)

    def _arrow2707(__unit: None=None) -> OntologyAnnotation | None:
        arg_10: Decoder_1[OntologyAnnotation] = map_2(JsonTypes_decomposeTechnologyPlatform, string)
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("technologyPlatform", arg_10)

    def _arrow2708(__unit: None=None) -> Array[Comment] | None:
        arg_12: Decoder_1[Array[Comment]] = resize_array(ISAJson_decoder_2)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("comments", arg_12)

    return ArcAssay(identifier, _arrow2705(), _arrow2706(), _arrow2707(), tables, None, None, _arrow2708())


ISAJson_decoder: Decoder_1[ArcAssay] = Decode_objectNoAdditionalProperties(ISAJson_allowedFields, _arrow2709)

__all__ = ["encoder", "decoder", "encoder_compressed", "decoder_compressed", "ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_allowedFields", "ISAJson_decoder"]

