from __future__ import annotations
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.option import map
from ..fable_modules.fable_library.seq import map as map_1
from ..fable_modules.fable_library.string_ import replace
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, IGetters)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.comment import Comment
from ..Core.ontology_source_reference import OntologySourceReference
from .comment import (encoder as encoder_1, decoder as decoder_1, ISAJson_encoder as ISAJson_encoder_1)
from .context.rocrate.isa_ontology_source_reference_context import context_jsonvalue
from .decode import (Decode_uri, Decode_resizeArray)
from .encode import (try_include, try_include_seq)

__A_ = TypeVar("__A_")

def encoder(osr: OntologySourceReference) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], osr: Any=osr) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow1832(value: str, osr: Any=osr) -> IEncodable:
        class ObjectExpr1831(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr1831()

    def _arrow1835(value_2: str, osr: Any=osr) -> IEncodable:
        class ObjectExpr1834(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr1834()

    def _arrow1839(value_4: str, osr: Any=osr) -> IEncodable:
        class ObjectExpr1838(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr1838()

    def _arrow1842(value_6: str, osr: Any=osr) -> IEncodable:
        class ObjectExpr1841(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_6)

        return ObjectExpr1841()

    def _arrow1843(comment: Comment, osr: Any=osr) -> IEncodable:
        return encoder_1(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("description", _arrow1832, osr.Description), try_include("file", _arrow1835, osr.File), try_include("name", _arrow1839, osr.Name), try_include("version", _arrow1842, osr.Version), try_include_seq("comments", _arrow1843, osr.Comments)]))
    class ObjectExpr1846(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], osr: Any=osr) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr1846()


def _arrow1860(get: IGetters) -> OntologySourceReference:
    def _arrow1851(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("description", Decode_uri)

    def _arrow1852(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("file", string)

    def _arrow1853(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("name", string)

    def _arrow1854(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("version", string)

    def _arrow1858(__unit: None=None) -> Array[Comment] | None:
        arg_9: Decoder_1[Array[Comment]] = Decode_resizeArray(decoder_1)
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("comments", arg_9)

    return OntologySourceReference(_arrow1851(), _arrow1852(), _arrow1853(), _arrow1854(), _arrow1858())


decoder: Decoder_1[OntologySourceReference] = object(_arrow1860)

def ROCrate_genID(o: OntologySourceReference) -> str:
    match_value: str | None = o.File
    if match_value is None:
        match_value_1: str | None = o.Name
        if match_value_1 is None:
            return "#DummyOntologySourceRef"

        else: 
            return "#OntologySourceRef_" + replace(match_value_1, " ", "_")


    else: 
        return match_value



def ROCrate_encoder(osr: OntologySourceReference) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], osr: Any=osr) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow1867(__unit: None=None, osr: Any=osr) -> IEncodable:
        value: str = ROCrate_genID(osr)
        class ObjectExpr1866(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr1866()

    class ObjectExpr1868(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], osr: Any=osr) -> Any:
            return helpers_1.encode_string("OntologySourceReference")

    def _arrow1870(value_2: str, osr: Any=osr) -> IEncodable:
        class ObjectExpr1869(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr1869()

    def _arrow1872(value_4: str, osr: Any=osr) -> IEncodable:
        class ObjectExpr1871(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_4)

        return ObjectExpr1871()

    def _arrow1874(value_6: str, osr: Any=osr) -> IEncodable:
        class ObjectExpr1873(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_6)

        return ObjectExpr1873()

    def _arrow1876(value_8: str, osr: Any=osr) -> IEncodable:
        class ObjectExpr1875(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_8)

        return ObjectExpr1875()

    def _arrow1877(comment: Comment, osr: Any=osr) -> IEncodable:
        return encoder_1(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow1867()), ("@type", ObjectExpr1868()), try_include("description", _arrow1870, osr.Description), try_include("file", _arrow1872, osr.File), try_include("name", _arrow1874, osr.Name), try_include("version", _arrow1876, osr.Version), try_include_seq("comments", _arrow1877, osr.Comments), ("@context", context_jsonvalue)]))
    class ObjectExpr1878(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any], osr: Any=osr) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_6))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_6.encode_object(arg)

    return ObjectExpr1878()


def _arrow1884(get: IGetters) -> OntologySourceReference:
    def _arrow1879(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("description", Decode_uri)

    def _arrow1880(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("file", string)

    def _arrow1881(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("name", string)

    def _arrow1882(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("version", string)

    def _arrow1883(__unit: None=None) -> Array[Comment] | None:
        arg_9: Decoder_1[Array[Comment]] = Decode_resizeArray(decoder_1)
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("comments", arg_9)

    return OntologySourceReference(_arrow1879(), _arrow1880(), _arrow1881(), _arrow1882(), _arrow1883())


ROCrate_decoder: Decoder_1[OntologySourceReference] = object(_arrow1884)

def ISAJson_encoder(id_map: Any | None, osr: OntologySourceReference) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], id_map: Any=id_map, osr: Any=osr) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow1888(value: str, id_map: Any=id_map, osr: Any=osr) -> IEncodable:
        class ObjectExpr1887(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr1887()

    def _arrow1890(value_2: str, id_map: Any=id_map, osr: Any=osr) -> IEncodable:
        class ObjectExpr1889(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr1889()

    def _arrow1892(value_4: str, id_map: Any=id_map, osr: Any=osr) -> IEncodable:
        class ObjectExpr1891(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr1891()

    def _arrow1894(value_6: str, id_map: Any=id_map, osr: Any=osr) -> IEncodable:
        class ObjectExpr1893(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_6)

        return ObjectExpr1893()

    def _arrow1895(comment: Comment, id_map: Any=id_map, osr: Any=osr) -> IEncodable:
        return ISAJson_encoder_1(id_map, comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("description", _arrow1888, osr.Description), try_include("file", _arrow1890, osr.File), try_include("name", _arrow1892, osr.Name), try_include("version", _arrow1894, osr.Version), try_include_seq("comments", _arrow1895, osr.Comments)]))
    class ObjectExpr1896(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any], id_map: Any=id_map, osr: Any=osr) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_4))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_4.encode_object(arg)

    return ObjectExpr1896()


ISAJson_decoder: Decoder_1[OntologySourceReference] = decoder

__all__ = ["encoder", "decoder", "ROCrate_genID", "ROCrate_encoder", "ROCrate_decoder", "ISAJson_encoder", "ISAJson_decoder"]

