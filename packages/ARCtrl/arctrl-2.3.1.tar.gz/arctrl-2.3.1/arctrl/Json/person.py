from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.array_ import map as map_2
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.option import (map, default_arg)
from ..fable_modules.fable_library.seq import (map as map_1, try_pick)
from ..fable_modules.fable_library.string_ import (replace, split, join)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, resize_array, IGetters, IRequiredGetter, map as map_3, array as array_3)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.comment import Comment
from ..Core.conversion import (Person_setCommentFromORCID, Person_setOrcidFromComments)
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.person import Person
from .comment import (encoder as encoder_1, decoder as decoder_1, ROCrate_encoderDisambiguatingDescription, ROCrate_decoderDisambiguatingDescription)
from .context.rocrate.isa_organization_context import context_jsonvalue
from .context.rocrate.isa_person_context import (context_jsonvalue as context_jsonvalue_1, context_minimal_json_value)
from .decode import Decode_objectNoAdditionalProperties
from .encode import (try_include, try_include_seq)
from .idtable import encode
from .ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder, OntologyAnnotation_ROCrate_encoderDefinedTerm, OntologyAnnotation_ROCrate_decoderDefinedTerm)

__A_ = TypeVar("__A_")

def encoder(person: Person) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], person: Any=person) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2015(value: str, person: Any=person) -> IEncodable:
        class ObjectExpr2014(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2014()

    def _arrow2017(value_2: str, person: Any=person) -> IEncodable:
        class ObjectExpr2016(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr2016()

    def _arrow2020(value_4: str, person: Any=person) -> IEncodable:
        class ObjectExpr2019(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr2019()

    def _arrow2022(value_6: str, person: Any=person) -> IEncodable:
        class ObjectExpr2021(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_6)

        return ObjectExpr2021()

    def _arrow2027(value_8: str, person: Any=person) -> IEncodable:
        class ObjectExpr2026(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_8)

        return ObjectExpr2026()

    def _arrow2031(value_10: str, person: Any=person) -> IEncodable:
        class ObjectExpr2030(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_10)

        return ObjectExpr2030()

    def _arrow2035(value_12: str, person: Any=person) -> IEncodable:
        class ObjectExpr2034(IEncodable):
            def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                return helpers_6.encode_string(value_12)

        return ObjectExpr2034()

    def _arrow2037(value_14: str, person: Any=person) -> IEncodable:
        class ObjectExpr2036(IEncodable):
            def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                return helpers_7.encode_string(value_14)

        return ObjectExpr2036()

    def _arrow2041(value_16: str, person: Any=person) -> IEncodable:
        class ObjectExpr2040(IEncodable):
            def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                return helpers_8.encode_string(value_16)

        return ObjectExpr2040()

    def _arrow2042(oa: OntologyAnnotation, person: Any=person) -> IEncodable:
        return OntologyAnnotation_encoder(oa)

    def _arrow2045(comment: Comment, person: Any=person) -> IEncodable:
        return encoder_1(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("firstName", _arrow2015, person.FirstName), try_include("lastName", _arrow2017, person.LastName), try_include("midInitials", _arrow2020, person.MidInitials), try_include("orcid", _arrow2022, person.ORCID), try_include("email", _arrow2027, person.EMail), try_include("phone", _arrow2031, person.Phone), try_include("fax", _arrow2035, person.Fax), try_include("address", _arrow2037, person.Address), try_include("affiliation", _arrow2041, person.Affiliation), try_include_seq("roles", _arrow2042, person.Roles), try_include_seq("comments", _arrow2045, person.Comments)]))
    class ObjectExpr2049(IEncodable):
        def Encode(self, helpers_9: IEncoderHelpers_1[Any], person: Any=person) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_9))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_9.encode_object(arg)

    return ObjectExpr2049()


def _arrow2070(get: IGetters) -> Person:
    def _arrow2055(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("orcid", string)

    def _arrow2057(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("lastName", string)

    def _arrow2059(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("firstName", string)

    def _arrow2060(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("midInitials", string)

    def _arrow2061(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("email", string)

    def _arrow2062(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("phone", string)

    def _arrow2063(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("fax", string)

    def _arrow2064(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("address", string)

    def _arrow2066(__unit: None=None) -> str | None:
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("affiliation", string)

    def _arrow2067(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_19: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_decoder)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("roles", arg_19)

    def _arrow2069(__unit: None=None) -> Array[Comment] | None:
        arg_21: Decoder_1[Array[Comment]] = resize_array(decoder_1)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("comments", arg_21)

    return Person(_arrow2055(), _arrow2057(), _arrow2059(), _arrow2060(), _arrow2061(), _arrow2062(), _arrow2063(), _arrow2064(), _arrow2066(), _arrow2067(), _arrow2069())


decoder: Decoder_1[Person] = object(_arrow2070)

def ROCrate_genID(p: Person) -> str:
    def chooser(c: Comment, p: Any=p) -> str | None:
        match_value: str | None = c.Name
        match_value_1: str | None = c.Value
        (pattern_matching_result, n, v) = (None, None, None)
        if match_value is not None:
            if match_value_1 is not None:
                pattern_matching_result = 0
                n = match_value
                v = match_value_1

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            if True if (True if (n == "orcid") else (n == "Orcid")) else (n == "ORCID"):
                return v

            else: 
                return None


        elif pattern_matching_result == 1:
            return None


    orcid: str | None = try_pick(chooser, p.Comments)
    if orcid is None:
        match_value_1: str | None = p.EMail
        if match_value_1 is None:
            match_value_2: str | None = p.FirstName
            match_value_3: str | None = p.MidInitials
            match_value_4: str | None = p.LastName
            (pattern_matching_result_1, fn, ln, mn, fn_1, ln_1, ln_2, fn_2) = (None, None, None, None, None, None, None, None)
            if match_value_2 is None:
                if match_value_3 is None:
                    if match_value_4 is not None:
                        pattern_matching_result_1 = 2
                        ln_2 = match_value_4

                    else: 
                        pattern_matching_result_1 = 4


                else: 
                    pattern_matching_result_1 = 4


            elif match_value_3 is None:
                if match_value_4 is None:
                    pattern_matching_result_1 = 3
                    fn_2 = match_value_2

                else: 
                    pattern_matching_result_1 = 1
                    fn_1 = match_value_2
                    ln_1 = match_value_4


            elif match_value_4 is not None:
                pattern_matching_result_1 = 0
                fn = match_value_2
                ln = match_value_4
                mn = match_value_3

            else: 
                pattern_matching_result_1 = 4

            if pattern_matching_result_1 == 0:
                return (((("#" + replace(fn, " ", "_")) + "_") + replace(mn, " ", "_")) + "_") + replace(ln, " ", "_")

            elif pattern_matching_result_1 == 1:
                return (("#" + replace(fn_1, " ", "_")) + "_") + replace(ln_1, " ", "_")

            elif pattern_matching_result_1 == 2:
                return "#" + replace(ln_2, " ", "_")

            elif pattern_matching_result_1 == 3:
                return "#" + replace(fn_2, " ", "_")

            elif pattern_matching_result_1 == 4:
                return "#EmptyPerson"


        else: 
            return match_value_1


    else: 
        return orcid



def ROCrate_Affiliation_encoder(affiliation: str) -> IEncodable:
    class ObjectExpr2080(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], affiliation: Any=affiliation) -> Any:
            return helpers.encode_string("Organization")

    def _arrow2084(__unit: None=None, affiliation: Any=affiliation) -> IEncodable:
        value_1: str = replace(("#Organization_" + affiliation) + "", " ", "_")
        class ObjectExpr2083(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr2083()

    class ObjectExpr2087(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], affiliation: Any=affiliation) -> Any:
            return helpers_2.encode_string(affiliation)

    values: FSharpList[tuple[str, IEncodable]] = of_array([("@type", ObjectExpr2080()), ("@id", _arrow2084()), ("name", ObjectExpr2087()), ("@context", context_jsonvalue)])
    class ObjectExpr2092(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any], affiliation: Any=affiliation) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_3))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping, values)
            return helpers_3.encode_object(arg)

    return ObjectExpr2092()


def _arrow2094(get: IGetters) -> str:
    object_arg: IRequiredGetter = get.Required
    return object_arg.Field("name", string)


ROCrate_Affiliation_decoder: Decoder_1[str] = object(_arrow2094)

def ROCrate_encoder(oa: Person) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2100(__unit: None=None, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(oa)
        class ObjectExpr2099(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2099()

    class ObjectExpr2101(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_1.encode_string("Person")

    def _arrow2103(value_2: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2102(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr2102()

    def _arrow2105(value_4: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2104(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_4)

        return ObjectExpr2104()

    def _arrow2107(value_6: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2106(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_6)

        return ObjectExpr2106()

    def _arrow2109(value_8: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2108(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_8)

        return ObjectExpr2108()

    def _arrow2111(value_10: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2110(IEncodable):
            def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                return helpers_6.encode_string(value_10)

        return ObjectExpr2110()

    def _arrow2113(value_12: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2112(IEncodable):
            def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                return helpers_7.encode_string(value_12)

        return ObjectExpr2112()

    def _arrow2115(value_14: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2114(IEncodable):
            def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                return helpers_8.encode_string(value_14)

        return ObjectExpr2114()

    def _arrow2117(value_16: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2116(IEncodable):
            def Encode(self, helpers_9: IEncoderHelpers_1[Any]) -> Any:
                return helpers_9.encode_string(value_16)

        return ObjectExpr2116()

    def _arrow2118(affiliation: str, oa: Any=oa) -> IEncodable:
        return ROCrate_Affiliation_encoder(affiliation)

    def _arrow2119(oa_1: OntologyAnnotation, oa: Any=oa) -> IEncodable:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa_1)

    def _arrow2120(comment: Comment, oa: Any=oa) -> IEncodable:
        return ROCrate_encoderDisambiguatingDescription(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2100()), ("@type", ObjectExpr2101()), try_include("orcid", _arrow2103, oa.ORCID), try_include("firstName", _arrow2105, oa.FirstName), try_include("lastName", _arrow2107, oa.LastName), try_include("midInitials", _arrow2109, oa.MidInitials), try_include("email", _arrow2111, oa.EMail), try_include("phone", _arrow2113, oa.Phone), try_include("fax", _arrow2115, oa.Fax), try_include("address", _arrow2117, oa.Address), try_include("affiliation", _arrow2118, oa.Affiliation), try_include_seq("roles", _arrow2119, oa.Roles), try_include_seq("comments", _arrow2120, oa.Comments), ("@context", context_jsonvalue_1)]))
    class ObjectExpr2121(IEncodable):
        def Encode(self, helpers_10: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_10))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_10.encode_object(arg)

    return ObjectExpr2121()


def _arrow2133(get: IGetters) -> Person:
    def _arrow2122(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("orcid", string)

    def _arrow2123(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("lastName", string)

    def _arrow2124(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("firstName", string)

    def _arrow2125(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("midInitials", string)

    def _arrow2126(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("email", string)

    def _arrow2127(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("phone", string)

    def _arrow2128(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("fax", string)

    def _arrow2129(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("address", string)

    def _arrow2130(__unit: None=None) -> str | None:
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("affiliation", ROCrate_Affiliation_decoder)

    def _arrow2131(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_19: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_ROCrate_decoderDefinedTerm)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("roles", arg_19)

    def _arrow2132(__unit: None=None) -> Array[Comment] | None:
        arg_21: Decoder_1[Array[Comment]] = resize_array(ROCrate_decoderDisambiguatingDescription)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("comments", arg_21)

    return Person(_arrow2122(), _arrow2123(), _arrow2124(), _arrow2125(), _arrow2126(), _arrow2127(), _arrow2128(), _arrow2129(), _arrow2130(), _arrow2131(), _arrow2132())


ROCrate_decoder: Decoder_1[Person] = object(_arrow2133)

def ROCrate_encodeAuthorListString(author_list: str) -> IEncodable:
    def encode_single(name: str, author_list: Any=author_list) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], name: Any=name) -> tuple[str, IEncodable] | None:
            def mapping_1(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping_1, tupled_arg[1])

        class ObjectExpr2135(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], name: Any=name) -> Any:
                return helpers.encode_string("Person")

        def _arrow2137(value_1: str, name: Any=name) -> IEncodable:
            class ObjectExpr2136(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_1)

            return ObjectExpr2136()

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@type", ObjectExpr2135()), try_include("name", _arrow2137, name), ("@context", context_minimal_json_value)]))
        class ObjectExpr2138(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], name: Any=name) -> Any:
                def mapping_2(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_2))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_2, values)
                return helpers_2.encode_object(arg)

        return ObjectExpr2138()

    def mapping(s: str, author_list: Any=author_list) -> str:
        return s.strip()

    values_2: Array[IEncodable] = map_2(encode_single, map_2(mapping, split(author_list, ["\t" if (author_list.find("\t") >= 0) else (";" if (author_list.find(";") >= 0) else ",")], None, 0), None), None)
    class ObjectExpr2139(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any], author_list: Any=author_list) -> Any:
            def mapping_3(v_3: IEncodable) -> __A_:
                return v_3.Encode(helpers_3)

            arg_1: Array[__A_] = map_2(mapping_3, values_2, None)
            return helpers_3.encode_array(arg_1)

    return ObjectExpr2139()


def ctor(v: Array[str]) -> str:
    return join(", ", v)


def _arrow2141(get: IGetters) -> str:
    def _arrow2140(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("name", string)

    return default_arg(_arrow2140(), "")


ROCrate_decodeAuthorListString: Decoder_1[str] = map_3(ctor, array_3(object(_arrow2141)))

ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "firstName", "lastName", "midInitials", "email", "phone", "fax", "address", "affiliation", "roles", "comments", "@type", "@context"])

def ISAJson_encoder(id_map: Any | None, person: Person) -> IEncodable:
    def f(person_1: Person, id_map: Any=id_map, person: Any=person) -> IEncodable:
        person_2: Person = Person_setCommentFromORCID(person_1)
        def chooser(tupled_arg: tuple[str, IEncodable | None], person_1: Any=person_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow2145(value: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2144(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr2144()

        def _arrow2147(value_2: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2146(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_2)

            return ObjectExpr2146()

        def _arrow2149(value_4: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2148(IEncodable):
                def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_2.encode_string(value_4)

            return ObjectExpr2148()

        def _arrow2151(value_6: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2150(IEncodable):
                def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_3.encode_string(value_6)

            return ObjectExpr2150()

        def _arrow2153(value_8: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2152(IEncodable):
                def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_4.encode_string(value_8)

            return ObjectExpr2152()

        def _arrow2155(value_10: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2154(IEncodable):
                def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_5.encode_string(value_10)

            return ObjectExpr2154()

        def _arrow2159(value_12: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2158(IEncodable):
                def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_6.encode_string(value_12)

            return ObjectExpr2158()

        def _arrow2163(value_14: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2162(IEncodable):
                def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_7.encode_string(value_14)

            return ObjectExpr2162()

        def _arrow2166(value_16: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2165(IEncodable):
                def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_8.encode_string(value_16)

            return ObjectExpr2165()

        def _arrow2168(oa: OntologyAnnotation, person_1: Any=person_1) -> IEncodable:
            return OntologyAnnotation_encoder(oa)

        def _arrow2169(comment: Comment, person_1: Any=person_1) -> IEncodable:
            return encoder_1(comment)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2145, ROCrate_genID(person_2)), try_include("firstName", _arrow2147, person_2.FirstName), try_include("lastName", _arrow2149, person_2.LastName), try_include("midInitials", _arrow2151, person_2.MidInitials), try_include("email", _arrow2153, person_2.EMail), try_include("phone", _arrow2155, person_2.Phone), try_include("fax", _arrow2159, person_2.Fax), try_include("address", _arrow2163, person_2.Address), try_include("affiliation", _arrow2166, person_2.Affiliation), try_include_seq("roles", _arrow2168, person_2.Roles), try_include_seq("comments", _arrow2169, person_2.Comments)]))
        class ObjectExpr2174(IEncodable):
            def Encode(self, helpers_9: IEncoderHelpers_1[Any], person_1: Any=person_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_9))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_9.encode_object(arg)

        return ObjectExpr2174()

    if id_map is not None:
        def _arrow2177(p_1: Person, id_map: Any=id_map, person: Any=person) -> str:
            return ROCrate_genID(p_1)

        return encode(_arrow2177, f, person, id_map)

    else: 
        return f(person)



def _arrow2188(get: IGetters) -> Person:
    def _arrow2178(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("lastName", string)

    def _arrow2179(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("firstName", string)

    def _arrow2180(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("midInitials", string)

    def _arrow2181(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("email", string)

    def _arrow2182(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("phone", string)

    def _arrow2183(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("fax", string)

    def _arrow2184(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("address", string)

    def _arrow2185(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("affiliation", string)

    def _arrow2186(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_17: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_decoder)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("roles", arg_17)

    def _arrow2187(__unit: None=None) -> Array[Comment] | None:
        arg_19: Decoder_1[Array[Comment]] = resize_array(decoder_1)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("comments", arg_19)

    return Person_setOrcidFromComments(Person(None, _arrow2178(), _arrow2179(), _arrow2180(), _arrow2181(), _arrow2182(), _arrow2183(), _arrow2184(), _arrow2185(), _arrow2186(), _arrow2187()))


ISAJson_decoder: Decoder_1[Person] = Decode_objectNoAdditionalProperties(ISAJson_allowedFields, _arrow2188)

__all__ = ["encoder", "decoder", "ROCrate_genID", "ROCrate_Affiliation_encoder", "ROCrate_Affiliation_decoder", "ROCrate_encoder", "ROCrate_decoder", "ROCrate_encodeAuthorListString", "ROCrate_decodeAuthorListString", "ISAJson_allowedFields", "ISAJson_encoder", "ISAJson_decoder"]

