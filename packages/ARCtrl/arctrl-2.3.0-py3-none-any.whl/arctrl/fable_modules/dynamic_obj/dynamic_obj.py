from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_library.option import (map, value as value_1, default_arg)
from ..fable_library.reflection import (TypeInfo, class_type)
from ..fable_library.seq import (filter, choose, map as map_1, iterate, sort_by)
from ..fable_library.util import (IEnumerable_1, compare_primitives, safe_hash)
from .fable_py import (try_get_dynamic_property_helper, get_property_helpers)
from .hash_codes import box_hash_key_val_seq
from .property_helper import PropertyHelper
from .reflection_utils import try_get_static_property_info

def _expr25() -> TypeInfo:
    return class_type("DynamicObj.DynamicObj", None, DynamicObj)


class DynamicObj:
    def __init__(self, __unit: None=None) -> None:
        self.properties: Any = dict([])

    @property
    def Properties(self, __unit: None=None) -> Any:
        this: DynamicObj = self
        return this.properties

    @Properties.setter
    def Properties(self, value: Any) -> None:
        this: DynamicObj = self
        this.properties = value

    @staticmethod
    def of_dict(dynamic_properties: Any) -> DynamicObj:
        obj: DynamicObj = DynamicObj()
        obj.Properties = dynamic_properties
        return obj

    def TryGetStaticPropertyHelper(self, property_name: str) -> PropertyHelper | None:
        this: DynamicObj = self
        return try_get_static_property_info(this, property_name)

    def TryGetDynamicPropertyHelper(self, property_name: str) -> PropertyHelper | None:
        this: DynamicObj = self
        return try_get_dynamic_property_helper(this, property_name)

    def TryGetPropertyHelper(self, property_name: str) -> PropertyHelper | None:
        this: DynamicObj = self
        match_value: PropertyHelper | None = this.TryGetStaticPropertyHelper(property_name)
        return this.TryGetDynamicPropertyHelper(property_name) if (match_value is None) else match_value

    def TryGetPropertyValue(self, property_name: str) -> Any | None:
        this: DynamicObj = self
        def mapping(pi: PropertyHelper) -> Any:
            return pi.GetValue(this)

        return map(mapping, this.TryGetPropertyHelper(property_name))

    def GetPropertyValue(self, property_name: str) -> Any:
        this: DynamicObj = self
        match_value: Any | None = this.TryGetPropertyValue(property_name)
        if match_value is None:
            raise Exception(("No dynamic or static property \"" + property_name) + "\" does exist on object.")

        else: 
            return value_1(match_value)


    def SetProperty(self, property_name: str, property_value: Any=None) -> None:
        this: DynamicObj = self
        match_value: PropertyHelper | None = this.TryGetStaticPropertyHelper(property_name)
        if match_value is None:
            setattr(this,property_name,property_value)

        else: 
            pi: PropertyHelper = match_value
            if pi.IsMutable:
                pi.SetValue(this, property_value)

            else: 
                raise Exception(("Cannot set value for static, immutable property \"" + property_name) + "\"")



    def RemoveProperty(self, property_name: str) -> bool:
        this: DynamicObj = self
        match_value: PropertyHelper | None = this.TryGetPropertyHelper(property_name)
        if match_value is None:
            return False

        elif match_value.IsMutable:
            pi_1: PropertyHelper = match_value
            pi_1.RemoveValue(this)
            return True

        else: 
            raise Exception(("Cannot remove value for static, immutable property \"" + property_name) + "\"")


    def GetPropertyHelpers(self, include_instance_properties: bool) -> IEnumerable_1[PropertyHelper]:
        this: DynamicObj = self
        def predicate_1(p: PropertyHelper) -> bool:
            return p.Name.lower() != "properties"

        def predicate(pd: PropertyHelper) -> bool:
            if include_instance_properties:
                return True

            else: 
                return pd.IsDynamic


        return filter(predicate_1, filter(predicate, get_property_helpers(this)))

    def GetProperties(self, include_instance_properties: bool) -> IEnumerable_1[Any]:
        this: DynamicObj = self
        def chooser(kv: PropertyHelper) -> Any | None:
            if kv.Name != "properties":
                return (kv.Name, kv.GetValue(this))

            else: 
                return None


        return choose(chooser, this.GetPropertyHelpers(include_instance_properties))

    def GetPropertyNames(self, include_instance_properties: bool) -> IEnumerable_1[str]:
        this: DynamicObj = self
        def mapping(kv: Any) -> str:
            return kv[0]

        return map_1(mapping, this.GetProperties(include_instance_properties))

    def CopyDynamicPropertiesTo(self, target: Any, over_write: bool | None=None) -> None:
        this: DynamicObj = self
        over_write_1: bool = default_arg(over_write, False)
        def action(kv: Any) -> None:
            match_value: PropertyHelper | None = target.TryGetPropertyHelper(kv[0])
            if match_value is None:
                target.SetProperty(kv[0], kv[1])

            else: 
                def _arrow23(__unit: None=None, kv: Any=kv) -> bool:
                    pi: PropertyHelper = match_value
                    return over_write_1

                if _arrow23():
                    pi_1: PropertyHelper = match_value
                    pi_1.SetValue(target, kv[1])

                else: 
                    raise Exception(("Property \"" + kv[0]) + "\" already exists on target object and overWrite was not set to true.")



        iterate(action, this.GetProperties(False))

    def CopyDynamicProperties(self, __unit: None=None) -> DynamicObj:
        this: DynamicObj = self
        target: DynamicObj = DynamicObj()
        this.CopyDynamicPropertiesTo(target)
        return target

    @staticmethod
    def op_dynamic(lookup: Any, name: str) -> Any:
        match_value: Any | None = lookup.TryGetPropertyValue(name)
        if match_value is None:
            raise Exception()

        else: 
            return value_1(match_value)


    @staticmethod
    def op_dynamic_assignment(lookup: Any, name: str, value: Any) -> None:
        lookup.SetProperty(name, value)

    def __hash__(self, __unit: None=None) -> Any:
        this: DynamicObj = self
        def projection(pair: Any) -> str:
            return pair[0]

        class ObjectExpr24:
            @property
            def Compare(self) -> Callable[[str, str], int]:
                return compare_primitives

        return box_hash_key_val_seq(sort_by(projection, this.GetProperties(True), ObjectExpr24()))

    def __eq__(self, o: Any=None) -> bool:
        this: DynamicObj = self
        return (safe_hash(this) == safe_hash(o)) if isinstance(o, DynamicObj) else False


DynamicObj_reflection = _expr25

def DynamicObj__ctor(__unit: None=None) -> DynamicObj:
    return DynamicObj(__unit)


__all__ = ["DynamicObj_reflection"]

