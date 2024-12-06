from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.result import FSharpResult_2
from ..fable_modules.fable_library.string_ import (to_text, printf)
from ..fable_modules.thoth_json_core.types import IEncodable
from ..fable_modules.thoth_json_python.decode import Decode_fromString
from ..fable_modules.thoth_json_python.encode import to_string
from ..Json.encode import default_spaces
from ..Json.ldobject import (decoder as decoder_1, encoder)
from ..ROCrate.ldobject import LDObject

def ARCtrl_ROCrate_LDObject__LDObject_fromROCrateJsonString_Static_Z721C83C5(s: str) -> LDObject:
    match_value: FSharpResult_2[LDObject, str] = Decode_fromString(decoder_1, s)
    if match_value.tag == 1:
        raise Exception(to_text(printf("Error decoding string: %O"))(match_value.fields[0]))

    else: 
        return match_value.fields[0]



def ARCtrl_ROCrate_LDObject__LDObject_toROCrateJsonString_Static_71136F3F(spaces: int | None=None) -> Callable[[LDObject], str]:
    def _arrow3203(obj: LDObject, spaces: Any=spaces) -> str:
        value: IEncodable = encoder(obj)
        return to_string(default_spaces(spaces), value)

    return _arrow3203


def ARCtrl_ROCrate_LDObject__LDObject_ToROCrateJsonString_71136F3F(this: LDObject, spaces: int | None=None) -> str:
    return ARCtrl_ROCrate_LDObject__LDObject_toROCrateJsonString_Static_71136F3F(spaces)(this)


__all__ = ["ARCtrl_ROCrate_LDObject__LDObject_fromROCrateJsonString_Static_Z721C83C5", "ARCtrl_ROCrate_LDObject__LDObject_toROCrateJsonString_Static_71136F3F", "ARCtrl_ROCrate_LDObject__LDObject_ToROCrateJsonString_71136F3F"]

