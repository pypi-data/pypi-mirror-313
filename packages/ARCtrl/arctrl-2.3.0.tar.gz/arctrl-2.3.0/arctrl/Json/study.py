from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.list import (try_find, FSharpList, choose, of_array, singleton, map as map_2, empty)
from ..fable_modules.fable_library.option import (default_arg, value as value_17, map, bind, default_arg_with)
from ..fable_modules.fable_library.seq import (map as map_1, is_empty)
from ..fable_modules.fable_library.string_ import replace
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (IEnumerable_1, get_enumerator, dispose)
from ..fable_modules.thoth_json_core.decode import (object, IRequiredGetter, string, IOptionalGetter, resize_array, IGetters, list_1 as list_1_2)
from ..fable_modules.thoth_json_core.encode import list_1 as list_1_1
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.arc_types import (ArcAssay, ArcStudy)
from ..Core.comment import Comment
from ..Core.conversion import (ARCtrl_ArcTables__ArcTables_GetProcesses, ARCtrl_ArcTables__ArcTables_fromProcesses_Static_62A3309D, Person_setSourceAssayComment, Person_getSourceAssayIdentifiersFromComments, Person_removeSourceAssayComments)
from ..Core.data_map import DataMap
from ..Core.Helper.collections_ import (ResizeArray_map, Option_fromValueWithDefault)
from ..Core.Helper.identifier import (Study_tryFileNameFromIdentifier, Study_tryIdentifierFromFileName, create_missing_identifier, Study_fileNameFromIdentifier)
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.person import Person
from ..Core.Process.factor import Factor
from ..Core.Process.material_attribute import MaterialAttribute
from ..Core.Process.process import Process
from ..Core.Process.process_sequence import (get_units, get_factors, get_characteristics, get_protocols)
from ..Core.Process.protocol import Protocol
from ..Core.publication import Publication
from ..Core.Table.arc_table import ArcTable
from ..Core.Table.arc_tables import ArcTables
from ..Core.Table.composite_cell import CompositeCell
from .assay import (ROCrate_encoder as ROCrate_encoder_4, ROCrate_decoder as ROCrate_decoder_1, ISAJson_encoder as ISAJson_encoder_5, ISAJson_decoder as ISAJson_decoder_2)
from .comment import (encoder as encoder_9, decoder as decoder_6, ROCrate_encoder as ROCrate_encoder_5, ROCrate_decoder as ROCrate_decoder_5, ISAJson_encoder as ISAJson_encoder_6, ISAJson_decoder as ISAJson_decoder_5)
from .context.rocrate.isa_study_context import context_jsonvalue
from .DataMap.data_map import (encoder as encoder_8, decoder as decoder_5, encoder_compressed as encoder_compressed_2, decoder_compressed as decoder_compressed_2)
from .decode import Decode_objectNoAdditionalProperties
from .encode import (try_include, try_include_seq, try_include_list)
from .idtable import encode
from .ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder, OntologyAnnotation_ROCrate_encoderDefinedTerm, OntologyAnnotation_ROCrate_decoderDefinedTerm, OntologyAnnotation_ISAJson_encoder, OntologyAnnotation_ISAJson_decoder)
from .person import (encoder as encoder_6, decoder as decoder_3, ROCrate_encoder as ROCrate_encoder_2, ROCrate_decoder as ROCrate_decoder_4, ISAJson_encoder as ISAJson_encoder_3, ISAJson_decoder as ISAJson_decoder_3)
from .Process.factor import encoder as encoder_10
from .Process.material_attribute import encoder as encoder_11
from .Process.process import (ROCrate_encoder as ROCrate_encoder_3, ROCrate_decoder as ROCrate_decoder_2, ISAJson_encoder as ISAJson_encoder_4, ISAJson_decoder as ISAJson_decoder_1)
from .Process.protocol import ISAJson_encoder as ISAJson_encoder_1
from .Process.study_materials import encoder as encoder_12
from .publication import (encoder as encoder_5, decoder as decoder_2, ROCrate_encoder as ROCrate_encoder_1, ROCrate_decoder as ROCrate_decoder_3, ISAJson_encoder as ISAJson_encoder_2, ISAJson_decoder as ISAJson_decoder_4)
from .Table.arc_table import (encoder as encoder_7, decoder as decoder_4, encoder_compressed as encoder_compressed_1, decoder_compressed as decoder_compressed_1)

__A_ = TypeVar("__A_")

def Helper_getAssayInformation(assays: FSharpList[ArcAssay] | None, study: ArcStudy) -> Array[ArcAssay]:
    if assays is not None:
        def f(assay_id: str, assays: Any=assays, study: Any=study) -> ArcAssay:
            def predicate(a: ArcAssay, assay_id: Any=assay_id) -> bool:
                return a.Identifier == assay_id

            return default_arg(try_find(predicate, value_17(assays)), ArcAssay.init(assay_id))

        return ResizeArray_map(f, study.RegisteredAssayIdentifiers)

    else: 
        return study.GetRegisteredAssaysOrIdentifier()



def encoder(study: ArcStudy) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], study: Any=study) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2714(__unit: None=None, study: Any=study) -> IEncodable:
        value: str = study.Identifier
        class ObjectExpr2713(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2713()

    def _arrow2716(value_1: str, study: Any=study) -> IEncodable:
        class ObjectExpr2715(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr2715()

    def _arrow2718(value_3: str, study: Any=study) -> IEncodable:
        class ObjectExpr2717(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_3)

        return ObjectExpr2717()

    def _arrow2720(value_5: str, study: Any=study) -> IEncodable:
        class ObjectExpr2719(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_5)

        return ObjectExpr2719()

    def _arrow2722(value_7: str, study: Any=study) -> IEncodable:
        class ObjectExpr2721(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_7)

        return ObjectExpr2721()

    def _arrow2723(oa: Publication, study: Any=study) -> IEncodable:
        return encoder_5(oa)

    def _arrow2724(person: Person, study: Any=study) -> IEncodable:
        return encoder_6(person)

    def _arrow2725(oa_1: OntologyAnnotation, study: Any=study) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow2726(table: ArcTable, study: Any=study) -> IEncodable:
        return encoder_7(table)

    def _arrow2727(dm: DataMap, study: Any=study) -> IEncodable:
        return encoder_8(dm)

    def _arrow2729(value_9: str, study: Any=study) -> IEncodable:
        class ObjectExpr2728(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_9)

        return ObjectExpr2728()

    def _arrow2730(comment: Comment, study: Any=study) -> IEncodable:
        return encoder_9(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("Identifier", _arrow2714()), try_include("Title", _arrow2716, study.Title), try_include("Description", _arrow2718, study.Description), try_include("SubmissionDate", _arrow2720, study.SubmissionDate), try_include("PublicReleaseDate", _arrow2722, study.PublicReleaseDate), try_include_seq("Publications", _arrow2723, study.Publications), try_include_seq("Contacts", _arrow2724, study.Contacts), try_include_seq("StudyDesignDescriptors", _arrow2725, study.StudyDesignDescriptors), try_include_seq("Tables", _arrow2726, study.Tables), try_include("DataMap", _arrow2727, study.DataMap), try_include_seq("RegisteredAssayIdentifiers", _arrow2729, study.RegisteredAssayIdentifiers), try_include_seq("Comments", _arrow2730, study.Comments)]))
    class ObjectExpr2731(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any], study: Any=study) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_6))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_6.encode_object(arg)

    return ObjectExpr2731()


def _arrow2744(get: IGetters) -> ArcStudy:
    def _arrow2732(__unit: None=None) -> str:
        object_arg: IRequiredGetter = get.Required
        return object_arg.Field("Identifier", string)

    def _arrow2733(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("Title", string)

    def _arrow2734(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("Description", string)

    def _arrow2735(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("SubmissionDate", string)

    def _arrow2736(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("PublicReleaseDate", string)

    def _arrow2737(__unit: None=None) -> Array[Publication] | None:
        arg_11: Decoder_1[Array[Publication]] = resize_array(decoder_2)
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("Publications", arg_11)

    def _arrow2738(__unit: None=None) -> Array[Person] | None:
        arg_13: Decoder_1[Array[Person]] = resize_array(decoder_3)
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("Contacts", arg_13)

    def _arrow2739(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_15: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_decoder)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("StudyDesignDescriptors", arg_15)

    def _arrow2740(__unit: None=None) -> Array[ArcTable] | None:
        arg_17: Decoder_1[Array[ArcTable]] = resize_array(decoder_4)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("Tables", arg_17)

    def _arrow2741(__unit: None=None) -> DataMap | None:
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("DataMap", decoder_5)

    def _arrow2742(__unit: None=None) -> Array[str] | None:
        arg_21: Decoder_1[Array[str]] = resize_array(string)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("RegisteredAssayIdentifiers", arg_21)

    def _arrow2743(__unit: None=None) -> Array[Comment] | None:
        arg_23: Decoder_1[Array[Comment]] = resize_array(decoder_6)
        object_arg_11: IOptionalGetter = get.Optional
        return object_arg_11.Field("Comments", arg_23)

    return ArcStudy(_arrow2732(), _arrow2733(), _arrow2734(), _arrow2735(), _arrow2736(), _arrow2737(), _arrow2738(), _arrow2739(), _arrow2740(), _arrow2741(), _arrow2742(), _arrow2743())


decoder: Decoder_1[ArcStudy] = object(_arrow2744)

def encoder_compressed(string_table: Any, oa_table: Any, cell_table: Any, study: ArcStudy) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2748(__unit: None=None, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> IEncodable:
        value: str = study.Identifier
        class ObjectExpr2747(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2747()

    def _arrow2750(value_1: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> IEncodable:
        class ObjectExpr2749(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr2749()

    def _arrow2752(value_3: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> IEncodable:
        class ObjectExpr2751(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_3)

        return ObjectExpr2751()

    def _arrow2754(value_5: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> IEncodable:
        class ObjectExpr2753(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_5)

        return ObjectExpr2753()

    def _arrow2756(value_7: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> IEncodable:
        class ObjectExpr2755(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_7)

        return ObjectExpr2755()

    def _arrow2757(oa: Publication, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> IEncodable:
        return encoder_5(oa)

    def _arrow2758(person: Person, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> IEncodable:
        return encoder_6(person)

    def _arrow2759(oa_1: OntologyAnnotation, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> IEncodable:
        return OntologyAnnotation_encoder(oa_1)

    def _arrow2760(table: ArcTable, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> IEncodable:
        return encoder_compressed_1(string_table, oa_table, cell_table, table)

    def _arrow2761(dm: DataMap, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> IEncodable:
        return encoder_compressed_2(string_table, oa_table, cell_table, dm)

    def _arrow2763(value_9: str, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> IEncodable:
        class ObjectExpr2762(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_9)

        return ObjectExpr2762()

    def _arrow2764(comment: Comment, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> IEncodable:
        return encoder_9(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("Identifier", _arrow2748()), try_include("Title", _arrow2750, study.Title), try_include("Description", _arrow2752, study.Description), try_include("SubmissionDate", _arrow2754, study.SubmissionDate), try_include("PublicReleaseDate", _arrow2756, study.PublicReleaseDate), try_include_seq("Publications", _arrow2757, study.Publications), try_include_seq("Contacts", _arrow2758, study.Contacts), try_include_seq("StudyDesignDescriptors", _arrow2759, study.StudyDesignDescriptors), try_include_seq("Tables", _arrow2760, study.Tables), try_include("DataMap", _arrow2761, study.DataMap), try_include_seq("RegisteredAssayIdentifiers", _arrow2763, study.RegisteredAssayIdentifiers), try_include_seq("Comments", _arrow2764, study.Comments)]))
    class ObjectExpr2765(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, study: Any=study) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_6))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_6.encode_object(arg)

    return ObjectExpr2765()


def decoder_compressed(string_table: Array[str], oa_table: Array[OntologyAnnotation], cell_table: Array[CompositeCell]) -> Decoder_1[ArcStudy]:
    def _arrow2778(get: IGetters, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table) -> ArcStudy:
        def _arrow2766(__unit: None=None) -> str:
            object_arg: IRequiredGetter = get.Required
            return object_arg.Field("Identifier", string)

        def _arrow2767(__unit: None=None) -> str | None:
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("Title", string)

        def _arrow2768(__unit: None=None) -> str | None:
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("Description", string)

        def _arrow2769(__unit: None=None) -> str | None:
            object_arg_3: IOptionalGetter = get.Optional
            return object_arg_3.Field("SubmissionDate", string)

        def _arrow2770(__unit: None=None) -> str | None:
            object_arg_4: IOptionalGetter = get.Optional
            return object_arg_4.Field("PublicReleaseDate", string)

        def _arrow2771(__unit: None=None) -> Array[Publication] | None:
            arg_11: Decoder_1[Array[Publication]] = resize_array(decoder_2)
            object_arg_5: IOptionalGetter = get.Optional
            return object_arg_5.Field("Publications", arg_11)

        def _arrow2772(__unit: None=None) -> Array[Person] | None:
            arg_13: Decoder_1[Array[Person]] = resize_array(decoder_3)
            object_arg_6: IOptionalGetter = get.Optional
            return object_arg_6.Field("Contacts", arg_13)

        def _arrow2773(__unit: None=None) -> Array[OntologyAnnotation] | None:
            arg_15: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_decoder)
            object_arg_7: IOptionalGetter = get.Optional
            return object_arg_7.Field("StudyDesignDescriptors", arg_15)

        def _arrow2774(__unit: None=None) -> Array[ArcTable] | None:
            arg_17: Decoder_1[Array[ArcTable]] = resize_array(decoder_compressed_1(string_table, oa_table, cell_table))
            object_arg_8: IOptionalGetter = get.Optional
            return object_arg_8.Field("Tables", arg_17)

        def _arrow2775(__unit: None=None) -> DataMap | None:
            arg_19: Decoder_1[DataMap] = decoder_compressed_2(string_table, oa_table, cell_table)
            object_arg_9: IOptionalGetter = get.Optional
            return object_arg_9.Field("DataMap", arg_19)

        def _arrow2776(__unit: None=None) -> Array[str] | None:
            arg_21: Decoder_1[Array[str]] = resize_array(string)
            object_arg_10: IOptionalGetter = get.Optional
            return object_arg_10.Field("RegisteredAssayIdentifiers", arg_21)

        def _arrow2777(__unit: None=None) -> Array[Comment] | None:
            arg_23: Decoder_1[Array[Comment]] = resize_array(decoder_6)
            object_arg_11: IOptionalGetter = get.Optional
            return object_arg_11.Field("Comments", arg_23)

        return ArcStudy(_arrow2766(), _arrow2767(), _arrow2768(), _arrow2769(), _arrow2770(), _arrow2771(), _arrow2772(), _arrow2773(), _arrow2774(), _arrow2775(), _arrow2776(), _arrow2777())

    return object(_arrow2778)


def ROCrate_genID(a: ArcStudy) -> str:
    match_value: str = a.Identifier
    if match_value == "":
        return "#EmptyStudy"

    else: 
        return ("#study/" + replace(match_value, " ", "_")) + ""



def ROCrate_encoder(assays: FSharpList[ArcAssay] | None, s: ArcStudy) -> IEncodable:
    file_name: str | None = Study_tryFileNameFromIdentifier(s.Identifier)
    processes: FSharpList[Process] = ARCtrl_ArcTables__ArcTables_GetProcesses(s)
    assays_1: Array[ArcAssay] = Helper_getAssayInformation(assays, s)
    def chooser(tupled_arg: tuple[str, IEncodable | None], assays: Any=assays, s: Any=s) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2782(__unit: None=None, assays: Any=assays, s: Any=s) -> IEncodable:
        value: str = ROCrate_genID(s)
        class ObjectExpr2781(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2781()

    class ObjectExpr2783(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], assays: Any=assays, s: Any=s) -> Any:
            return helpers_1.encode_string("Study")

    class ObjectExpr2784(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], assays: Any=assays, s: Any=s) -> Any:
            return helpers_2.encode_string("Study")

    def _arrow2786(__unit: None=None, assays: Any=assays, s: Any=s) -> IEncodable:
        value_3: str = s.Identifier
        class ObjectExpr2785(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_3)

        return ObjectExpr2785()

    def _arrow2788(value_4: str, assays: Any=assays, s: Any=s) -> IEncodable:
        class ObjectExpr2787(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_4)

        return ObjectExpr2787()

    def _arrow2790(value_6: str, assays: Any=assays, s: Any=s) -> IEncodable:
        class ObjectExpr2789(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_6)

        return ObjectExpr2789()

    def _arrow2792(value_8: str, assays: Any=assays, s: Any=s) -> IEncodable:
        class ObjectExpr2791(IEncodable):
            def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                return helpers_6.encode_string(value_8)

        return ObjectExpr2791()

    def _arrow2793(oa: OntologyAnnotation, assays: Any=assays, s: Any=s) -> IEncodable:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa)

    def _arrow2795(value_10: str, assays: Any=assays, s: Any=s) -> IEncodable:
        class ObjectExpr2794(IEncodable):
            def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                return helpers_7.encode_string(value_10)

        return ObjectExpr2794()

    def _arrow2797(value_12: str, assays: Any=assays, s: Any=s) -> IEncodable:
        class ObjectExpr2796(IEncodable):
            def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                return helpers_8.encode_string(value_12)

        return ObjectExpr2796()

    def _arrow2798(oa_1: Publication, assays: Any=assays, s: Any=s) -> IEncodable:
        return ROCrate_encoder_1(oa_1)

    def _arrow2799(oa_2: Person, assays: Any=assays, s: Any=s) -> IEncodable:
        return ROCrate_encoder_2(oa_2)

    def _arrow2801(__unit: None=None, assays: Any=assays, s: Any=s) -> Callable[[Process], IEncodable]:
        study_name: str | None = s.Identifier
        def _arrow2800(oa_3: Process) -> IEncodable:
            return ROCrate_encoder_3(study_name, None, oa_3)

        return _arrow2800

    def _arrow2803(__unit: None=None, assays: Any=assays, s: Any=s) -> Callable[[ArcAssay], IEncodable]:
        study_name_1: str | None = s.Identifier
        def _arrow2802(a_1: ArcAssay) -> IEncodable:
            return ROCrate_encoder_4(study_name_1, a_1)

        return _arrow2802

    def _arrow2804(comment: Comment, assays: Any=assays, s: Any=s) -> IEncodable:
        return ROCrate_encoder_5(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2782()), ("@type", list_1_1(singleton(ObjectExpr2783()))), ("additionalType", ObjectExpr2784()), ("identifier", _arrow2786()), try_include("filename", _arrow2788, file_name), try_include("title", _arrow2790, s.Title), try_include("description", _arrow2792, s.Description), try_include_seq("studyDesignDescriptors", _arrow2793, s.StudyDesignDescriptors), try_include("submissionDate", _arrow2795, s.SubmissionDate), try_include("publicReleaseDate", _arrow2797, s.PublicReleaseDate), try_include_seq("publications", _arrow2798, s.Publications), try_include_seq("people", _arrow2799, s.Contacts), try_include_list("processSequence", _arrow2801(), processes), try_include_seq("assays", _arrow2803(), assays_1), try_include_seq("comments", _arrow2804, s.Comments), ("@context", context_jsonvalue)]))
    class ObjectExpr2805(IEncodable):
        def Encode(self, helpers_9: IEncoderHelpers_1[Any], assays: Any=assays, s: Any=s) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_9))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_9.encode_object(arg)

    return ObjectExpr2805()


def _arrow2825(get: IGetters) -> tuple[ArcStudy, FSharpList[ArcAssay]]:
    def _arrow2806(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("filename", string)

    identifier: str = default_arg(bind(Study_tryIdentifierFromFileName, _arrow2806()), create_missing_identifier())
    assays: FSharpList[ArcAssay] | None
    arg_3: Decoder_1[FSharpList[ArcAssay]] = list_1_2(ROCrate_decoder_1)
    object_arg_1: IOptionalGetter = get.Optional
    assays = object_arg_1.Field("assays", arg_3)
    def mapping_1(arg_4: FSharpList[ArcAssay]) -> Array[str]:
        def mapping(a: ArcAssay, arg_4: Any=arg_4) -> str:
            return a.Identifier

        return list(map_2(mapping, arg_4))

    assay_identifiers: Array[str] | None = map(mapping_1, assays)
    def mapping_2(ps: FSharpList[Process]) -> Array[ArcTable]:
        return ARCtrl_ArcTables__ArcTables_fromProcesses_Static_62A3309D(ps).Tables

    def _arrow2809(__unit: None=None) -> FSharpList[Process] | None:
        arg_6: Decoder_1[FSharpList[Process]] = list_1_2(ROCrate_decoder_2)
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("processSequence", arg_6)

    tables: Array[ArcTable] | None = map(mapping_2, _arrow2809())
    def _arrow2815(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("title", string)

    def _arrow2816(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("description", string)

    def _arrow2817(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("submissionDate", string)

    def _arrow2818(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("publicReleaseDate", string)

    def _arrow2820(__unit: None=None) -> Array[Publication] | None:
        arg_16: Decoder_1[Array[Publication]] = resize_array(ROCrate_decoder_3)
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("publications", arg_16)

    def _arrow2822(__unit: None=None) -> Array[Person] | None:
        arg_18: Decoder_1[Array[Person]] = resize_array(ROCrate_decoder_4)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("people", arg_18)

    def _arrow2823(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_20: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_ROCrate_decoderDefinedTerm)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("studyDesignDescriptors", arg_20)

    def _arrow2824(__unit: None=None) -> Array[Comment] | None:
        arg_22: Decoder_1[Array[Comment]] = resize_array(ROCrate_decoder_5)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("comments", arg_22)

    return (ArcStudy(identifier, _arrow2815(), _arrow2816(), _arrow2817(), _arrow2818(), _arrow2820(), _arrow2822(), _arrow2823(), tables, None, assay_identifiers, _arrow2824()), default_arg(assays, empty()))


ROCrate_decoder: Decoder_1[tuple[ArcStudy, FSharpList[ArcAssay]]] = object(_arrow2825)

def ISAJson_encoder(id_map: Any | None, assays: FSharpList[ArcAssay] | None, s: ArcStudy) -> IEncodable:
    def f(s_1: ArcStudy, id_map: Any=id_map, assays: Any=assays, s: Any=s) -> IEncodable:
        study: ArcStudy = s_1.Copy(True)
        file_name: str = Study_fileNameFromIdentifier(study.Identifier)
        assays_1: Array[ArcAssay]
        n: Array[ArcAssay] = []
        enumerator: Any = get_enumerator(Helper_getAssayInformation(assays, study))
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                a: ArcAssay = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                assay: ArcAssay = a.Copy()
                enumerator_1: Any = get_enumerator(assay.Performers)
                try: 
                    while enumerator_1.System_Collections_IEnumerator_MoveNext():
                        person_1: Person = Person_setSourceAssayComment(enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current(), assay.Identifier)
                        (study.Contacts.append(person_1))

                finally: 
                    dispose(enumerator_1)

                assay.Performers = []
                (n.append(assay))

        finally: 
            dispose(enumerator)

        assays_1 = n
        processes: FSharpList[Process] = ARCtrl_ArcTables__ArcTables_GetProcesses(study)
        def encoder_1(oa: OntologyAnnotation, s_1: Any=s_1) -> IEncodable:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa)

        encoded_units: tuple[str, IEncodable | None] = try_include_list("unitCategories", encoder_1, get_units(processes))
        def encoder_2(value_1: Factor, s_1: Any=s_1) -> IEncodable:
            return encoder_10(id_map, value_1)

        encoded_factors: tuple[str, IEncodable | None] = try_include_list("factors", encoder_2, get_factors(processes))
        def encoder_3(value_3: MaterialAttribute, s_1: Any=s_1) -> IEncodable:
            return encoder_11(id_map, value_3)

        encoded_characteristics: tuple[str, IEncodable | None] = try_include_list("characteristicCategories", encoder_3, get_characteristics(processes))
        def _arrow2826(ps: FSharpList[Process], s_1: Any=s_1) -> IEncodable:
            return encoder_12(id_map, ps)

        encoded_materials: tuple[str, IEncodable | None] = try_include("materials", _arrow2826, Option_fromValueWithDefault(empty(), processes))
        encoded_protocols: tuple[str, IEncodable | None]
        value_5: FSharpList[Protocol] = get_protocols(processes)
        def _arrow2828(__unit: None=None, s_1: Any=s_1) -> Callable[[Protocol], IEncodable]:
            study_name: str | None = s_1.Identifier
            def _arrow2827(oa_1: Protocol) -> IEncodable:
                return ISAJson_encoder_1(study_name, None, None, id_map, oa_1)

            return _arrow2827

        encoded_protocols = try_include_list("protocols", _arrow2828(), value_5)
        def chooser(tupled_arg: tuple[str, IEncodable | None], s_1: Any=s_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow2832(__unit: None=None, s_1: Any=s_1) -> IEncodable:
            value_6: str = ROCrate_genID(study)
            class ObjectExpr2831(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value_6)

            return ObjectExpr2831()

        class ObjectExpr2833(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any], s_1: Any=s_1) -> Any:
                return helpers_1.encode_string(file_name)

        def _arrow2835(__unit: None=None, s_1: Any=s_1) -> IEncodable:
            value_8: str = study.Identifier
            class ObjectExpr2834(IEncodable):
                def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_2.encode_string(value_8)

            return ObjectExpr2834()

        def _arrow2837(value_9: str, s_1: Any=s_1) -> IEncodable:
            class ObjectExpr2836(IEncodable):
                def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_3.encode_string(value_9)

            return ObjectExpr2836()

        def _arrow2839(value_11: str, s_1: Any=s_1) -> IEncodable:
            class ObjectExpr2838(IEncodable):
                def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_4.encode_string(value_11)

            return ObjectExpr2838()

        def _arrow2841(value_13: str, s_1: Any=s_1) -> IEncodable:
            class ObjectExpr2840(IEncodable):
                def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_5.encode_string(value_13)

            return ObjectExpr2840()

        def _arrow2843(value_15: str, s_1: Any=s_1) -> IEncodable:
            class ObjectExpr2842(IEncodable):
                def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_6.encode_string(value_15)

            return ObjectExpr2842()

        def _arrow2844(oa_2: Publication, s_1: Any=s_1) -> IEncodable:
            return ISAJson_encoder_2(id_map, oa_2)

        def _arrow2845(person_2: Person, s_1: Any=s_1) -> IEncodable:
            return ISAJson_encoder_3(id_map, person_2)

        def _arrow2846(oa_3: OntologyAnnotation, s_1: Any=s_1) -> IEncodable:
            return OntologyAnnotation_ISAJson_encoder(id_map, oa_3)

        def _arrow2848(__unit: None=None, s_1: Any=s_1) -> Callable[[Process], IEncodable]:
            study_name_1: str | None = s_1.Identifier
            def _arrow2847(oa_4: Process) -> IEncodable:
                return ISAJson_encoder_4(study_name_1, None, id_map, oa_4)

            return _arrow2847

        def _arrow2850(__unit: None=None, s_1: Any=s_1) -> Callable[[ArcAssay], IEncodable]:
            study_name_2: str | None = s_1.Identifier
            def _arrow2849(a_2: ArcAssay) -> IEncodable:
                return ISAJson_encoder_5(study_name_2, id_map, a_2)

            return _arrow2849

        def _arrow2851(comment: Comment, s_1: Any=s_1) -> IEncodable:
            return ISAJson_encoder_6(id_map, comment)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2832()), ("filename", ObjectExpr2833()), ("identifier", _arrow2835()), try_include("title", _arrow2837, study.Title), try_include("description", _arrow2839, study.Description), try_include("submissionDate", _arrow2841, study.SubmissionDate), try_include("publicReleaseDate", _arrow2843, study.PublicReleaseDate), try_include_seq("publications", _arrow2844, study.Publications), try_include_seq("people", _arrow2845, study.Contacts), try_include_seq("studyDesignDescriptors", _arrow2846, study.StudyDesignDescriptors), encoded_protocols, encoded_materials, try_include_list("processSequence", _arrow2848(), processes), try_include_seq("assays", _arrow2850(), assays_1), encoded_factors, encoded_characteristics, encoded_units, try_include_seq("comments", _arrow2851, study.Comments)]))
        class ObjectExpr2852(IEncodable):
            def Encode(self, helpers_7: IEncoderHelpers_1[Any], s_1: Any=s_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_7))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_7.encode_object(arg)

        return ObjectExpr2852()

    if id_map is not None:
        def _arrow2853(s_2: ArcStudy, id_map: Any=id_map, assays: Any=assays, s: Any=s) -> str:
            return ROCrate_genID(s_2)

        return encode(_arrow2853, f, s, id_map)

    else: 
        return f(s)



ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "filename", "identifier", "title", "description", "submissionDate", "publicReleaseDate", "publications", "people", "studyDesignDescriptors", "protocols", "materials", "assays", "factors", "characteristicCategories", "unitCategories", "processSequence", "comments", "@type", "@context"])

def _arrow2864(get: IGetters) -> tuple[ArcStudy, FSharpList[ArcAssay]]:
    def _arrow2854(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("identifier", string)

    def def_thunk(__unit: None=None) -> str:
        def _arrow2855(__unit: None=None) -> str | None:
            object_arg_1: IOptionalGetter = get.Optional
            return object_arg_1.Field("filename", string)

        return default_arg(bind(Study_tryIdentifierFromFileName, _arrow2855()), create_missing_identifier())

    identifier: str = default_arg_with(_arrow2854(), def_thunk)
    def mapping(arg_6: FSharpList[Process]) -> Array[ArcTable]:
        a: ArcTables = ARCtrl_ArcTables__ArcTables_fromProcesses_Static_62A3309D(arg_6)
        return a.Tables

    def _arrow2856(__unit: None=None) -> FSharpList[Process] | None:
        arg_5: Decoder_1[FSharpList[Process]] = list_1_2(ISAJson_decoder_1)
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("processSequence", arg_5)

    tables: Array[ArcTable] | None = map(mapping, _arrow2856())
    assays: FSharpList[ArcAssay] | None
    arg_8: Decoder_1[FSharpList[ArcAssay]] = list_1_2(ISAJson_decoder_2)
    object_arg_3: IOptionalGetter = get.Optional
    assays = object_arg_3.Field("assays", arg_8)
    persons_raw: Array[Person] | None
    arg_10: Decoder_1[Array[Person]] = resize_array(ISAJson_decoder_3)
    object_arg_4: IOptionalGetter = get.Optional
    persons_raw = object_arg_4.Field("people", arg_10)
    persons: Array[Person] = []
    if persons_raw is not None:
        enumerator: Any = get_enumerator(value_17(persons_raw))
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                person: Person = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                source_assays: IEnumerable_1[str] = Person_getSourceAssayIdentifiersFromComments(person)
                with get_enumerator(source_assays) as enumerator_1:
                    while enumerator_1.System_Collections_IEnumerator_MoveNext():
                        assay_identifier: str = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                        with get_enumerator(value_17(assays)) as enumerator_2:
                            while enumerator_2.System_Collections_IEnumerator_MoveNext():
                                assay: ArcAssay = enumerator_2.System_Collections_Generic_IEnumerator_1_get_Current()
                                if assay.Identifier == assay_identifier:
                                    (assay.Performers.append(person))

                person.Comments = Person_removeSourceAssayComments(person)
                if is_empty(source_assays):
                    (persons.append(person))


        finally: 
            dispose(enumerator)


    def mapping_2(arg_11: FSharpList[ArcAssay]) -> Array[str]:
        def mapping_1(a_1: ArcAssay, arg_11: Any=arg_11) -> str:
            return a_1.Identifier

        return list(map_2(mapping_1, arg_11))

    assay_identifiers: Array[str] | None = map(mapping_2, assays)
    def _arrow2857(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("title", string)

    def _arrow2858(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("description", string)

    def _arrow2859(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("submissionDate", string)

    def _arrow2860(__unit: None=None) -> str | None:
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("publicReleaseDate", string)

    def _arrow2861(__unit: None=None) -> Array[Publication] | None:
        arg_21: Decoder_1[Array[Publication]] = resize_array(ISAJson_decoder_4)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("publications", arg_21)

    def _arrow2862(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_23: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_ISAJson_decoder)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("studyDesignDescriptors", arg_23)

    def _arrow2863(__unit: None=None) -> Array[Comment] | None:
        arg_25: Decoder_1[Array[Comment]] = resize_array(ISAJson_decoder_5)
        object_arg_11: IOptionalGetter = get.Optional
        return object_arg_11.Field("comments", arg_25)

    return (ArcStudy(identifier, _arrow2857(), _arrow2858(), _arrow2859(), _arrow2860(), _arrow2861(), None if (len(persons) == 0) else persons, _arrow2862(), tables, None, assay_identifiers, _arrow2863()), default_arg(assays, empty()))


ISAJson_decoder: Decoder_1[tuple[ArcStudy, FSharpList[ArcAssay]]] = Decode_objectNoAdditionalProperties(ISAJson_allowedFields, _arrow2864)

__all__ = ["Helper_getAssayInformation", "encoder", "decoder", "encoder_compressed", "decoder_compressed", "ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_allowedFields", "ISAJson_decoder"]

