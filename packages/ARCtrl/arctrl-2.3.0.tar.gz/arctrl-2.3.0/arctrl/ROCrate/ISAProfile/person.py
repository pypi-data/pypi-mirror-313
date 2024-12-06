from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ...fable_modules.dynamic_obj.dynamic_obj import DynamicObj
from ...fable_modules.dynamic_obj.dyn_obj import (try_get_property_value, set_property, set_optional_property)
from ...fable_modules.fable_library.option import value as value_1
from ...fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ...fable_modules.fable_library.types import FSharpRef
from ..ldobject import (LDObject, LDObject_reflection)

def _expr1401() -> TypeInfo:
    return class_type("ARCtrl.ROCrate.Person", None, Person, LDObject_reflection())


class Person(LDObject):
    def __init__(self, id: str, given_name: Any=None, additional_type: str | None=None, family_name: Any | None=None, email: Any | None=None, identifier: Any | None=None, affiliation: Any | None=None, job_title: Any | None=None, additional_name: Any | None=None, address: Any | None=None, telephone: Any | None=None, fax_number: Any | None=None, disambiguating_description: Any | None=None) -> None:
        super().__init__(id, "schema.org/Person", additional_type)
        this: FSharpRef[Person] = FSharpRef(None)
        this.contents = self
        self.init_00408: int = 1
        set_property("givenName", given_name, this.contents)
        set_optional_property("familyName", family_name, this.contents)
        set_optional_property("email", email, this.contents)
        set_optional_property("identifier", identifier, this.contents)
        set_optional_property("affiliation", affiliation, this.contents)
        set_optional_property("jobTitle", job_title, this.contents)
        set_optional_property("additionalName", additional_name, this.contents)
        set_optional_property("address", address, this.contents)
        set_optional_property("telephone", telephone, this.contents)
        set_optional_property("faxNumber", fax_number, this.contents)
        set_optional_property("disambiguatingDescription", disambiguating_description, this.contents)

    def GetGivenName(self, __unit: None=None) -> str:
        this: Person = self
        obj: DynamicObj = this
        if try_get_property_value("givenName", obj) is not None:
            match_value: str | None
            match_value_1: Any | None = obj.TryGetPropertyValue("givenName")
            if match_value_1 is not None:
                o: Any = value_1(match_value_1)
                match_value = o if (str(type(o)) == "<class \'str\'>") else None

            else: 
                match_value = None

            if match_value is None:
                raise Exception(((((("Property \'" + "givenName") + "\' is set on this \'") + "Person") + "\' object but cannot be cast to \'") + "String") + "\'")

            else: 
                return match_value


        else: 
            raise Exception(((("No property \'" + "givenName") + "\' set on this \'") + "Person") + "\' object although it is mandatory. Was it created correctly?")


    @staticmethod
    def get_given_name() -> Callable[[Person], str]:
        def _arrow1400(p: Person) -> str:
            return p.GetGivenName()

        return _arrow1400


Person_reflection = _expr1401

def Person__ctor_Z45412208(id: str, given_name: Any=None, additional_type: str | None=None, family_name: Any | None=None, email: Any | None=None, identifier: Any | None=None, affiliation: Any | None=None, job_title: Any | None=None, additional_name: Any | None=None, address: Any | None=None, telephone: Any | None=None, fax_number: Any | None=None, disambiguating_description: Any | None=None) -> Person:
    return Person(id, given_name, additional_type, family_name, email, identifier, affiliation, job_title, additional_name, address, telephone, fax_number, disambiguating_description)


__all__ = ["Person_reflection"]

