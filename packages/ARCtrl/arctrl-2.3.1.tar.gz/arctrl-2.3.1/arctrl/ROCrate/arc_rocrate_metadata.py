from __future__ import annotations
from ..fable_modules.dynamic_obj.dynamic_obj import DynamicObj
from ..fable_modules.dynamic_obj.dyn_obj import set_optional_property
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.types import FSharpRef
from .ldobject import (LDContext__ctor, LDContext, LDObject, LDObject_reflection)

def _expr1405() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.ArcROCrateMetadata", None, ArcROCrateMetadata, LDObject_reflection())


class ArcROCrateMetadata(LDObject):
    def __init__(self, about: LDObject | None=None) -> None:
        super().__init__("ro-crate-metadata", "CreativeWork")
        this: FSharpRef[ArcROCrateMetadata] = FSharpRef(None)
        this.contents = self
        self.init_00405: int = 1
        set_optional_property("about", about, this.contents)
        conforms_to: DynamicObj = DynamicObj()
        conforms_to.SetProperty("@id", "https://w3id.org/ro/crate/1.1")
        this.contents.SetProperty("conformsTo", conforms_to)
        context: LDContext = LDContext__ctor()
        context.SetProperty("sdo", "http://schema.org/")
        context.SetProperty("arc", "http://purl.org/nfdi4plants/ontology/")
        context.SetProperty("CreativeWork", "sdo:CreativeWork")
        context.SetProperty("about", "sdo:about")
        context.SetProperty("conformsTo", "sdo:conformsTo")
        this.contents.SetProperty("@context", context)


ArcROCrateMetadata_reflection = _expr1405

def ArcROCrateMetadata__ctor_Z475E1643(about: LDObject | None=None) -> ArcROCrateMetadata:
    return ArcROCrateMetadata(about)


__all__ = ["ArcROCrateMetadata_reflection"]

