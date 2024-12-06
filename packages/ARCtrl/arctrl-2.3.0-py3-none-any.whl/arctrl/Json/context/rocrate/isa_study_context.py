from __future__ import annotations
from dataclasses import dataclass
from typing import (Any, TypeVar)
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.seq import map
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ....fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

def _expr1654() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.Study.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("Study", string_type), ("ArcStudy", string_type), ("identifier", string_type), ("title", string_type), ("description", string_type), ("submission_date", string_type), ("public_release_date", string_type), ("publications", string_type), ("people", string_type), ("assays", string_type), ("filename", string_type), ("comments", string_type), ("protocols", string_type), ("materials", string_type), ("other_materials", string_type), ("sources", string_type), ("samples", string_type), ("process_sequence", string_type), ("factors", string_type), ("characteristic_categories", string_type), ("unit_categories", string_type), ("study_design_descriptors", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    Study: str
    ArcStudy: str
    identifier: str
    title: str
    description: str
    submission_date: str
    public_release_date: str
    publications: str
    people: str
    assays: str
    filename: str
    comments: str
    protocols: str
    materials: str
    other_materials: str
    sources: str
    samples: str
    process_sequence: str
    factors: str
    characteristic_categories: str
    unit_categories: str
    study_design_descriptors: str

IContext_reflection = _expr1654

def _arrow1671(__unit: None=None) -> IEncodable:
    class ObjectExpr1655(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("http://schema.org/")

    class ObjectExpr1656(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            return helpers_1.encode_string("sdo:Dataset")

    class ObjectExpr1657(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
            return helpers_2.encode_string("sdo:identifier")

    class ObjectExpr1658(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
            return helpers_3.encode_string("sdo:headline")

    class ObjectExpr1659(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
            return helpers_4.encode_string("sdo:additionalType")

    class ObjectExpr1660(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
            return helpers_5.encode_string("sdo:description")

    class ObjectExpr1661(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
            return helpers_6.encode_string("sdo:dateCreated")

    class ObjectExpr1662(IEncodable):
        def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
            return helpers_7.encode_string("sdo:datePublished")

    class ObjectExpr1663(IEncodable):
        def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
            return helpers_8.encode_string("sdo:citation")

    class ObjectExpr1664(IEncodable):
        def Encode(self, helpers_9: IEncoderHelpers_1[Any]) -> Any:
            return helpers_9.encode_string("sdo:creator")

    class ObjectExpr1665(IEncodable):
        def Encode(self, helpers_10: IEncoderHelpers_1[Any]) -> Any:
            return helpers_10.encode_string("sdo:hasPart")

    class ObjectExpr1666(IEncodable):
        def Encode(self, helpers_11: IEncoderHelpers_1[Any]) -> Any:
            return helpers_11.encode_string("sdo:alternateName")

    class ObjectExpr1667(IEncodable):
        def Encode(self, helpers_12: IEncoderHelpers_1[Any]) -> Any:
            return helpers_12.encode_string("sdo:comment")

    class ObjectExpr1668(IEncodable):
        def Encode(self, helpers_13: IEncoderHelpers_1[Any]) -> Any:
            return helpers_13.encode_string("sdo:about")

    class ObjectExpr1669(IEncodable):
        def Encode(self, helpers_14: IEncoderHelpers_1[Any]) -> Any:
            return helpers_14.encode_string("arc:ARC#ARC_00000037")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("sdo", ObjectExpr1655()), ("Study", ObjectExpr1656()), ("identifier", ObjectExpr1657()), ("title", ObjectExpr1658()), ("additionalType", ObjectExpr1659()), ("description", ObjectExpr1660()), ("submissionDate", ObjectExpr1661()), ("publicReleaseDate", ObjectExpr1662()), ("publications", ObjectExpr1663()), ("people", ObjectExpr1664()), ("assays", ObjectExpr1665()), ("filename", ObjectExpr1666()), ("comments", ObjectExpr1667()), ("processSequence", ObjectExpr1668()), ("studyDesignDescriptors", ObjectExpr1669())])
    class ObjectExpr1670(IEncodable):
        def Encode(self, helpers_15: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_15))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_15.encode_object(arg)

    return ObjectExpr1670()


context_jsonvalue: IEncodable = _arrow1671()

__all__ = ["IContext_reflection", "context_jsonvalue"]

