from __future__ import annotations
from typing import Any
from ..fable_library.int32 import parse
from ..fable_library.reg_exp import (match, create, get_item, groups)
from .regex import (KeyPattern, ValuePattern, LineCommentPattern, InlineSequencePattern, SequenceOpenerPattern, SequenceCloserPattern, InlineJSONPattern, JSONOpenerPattern, JSONCloserPattern)
from .yamlicious_types import PreprocessorElement

def _007CKey_007C__007C(input: PreprocessorElement) -> dict[str, Any] | None:
    if input.tag == 2:
        m: Any = match(create(KeyPattern), input.fields[0])
        if m is not None:
            def _arrow343(__unit: None=None, input: Any=input) -> int | None:
                v: str = get_item(groups(m), "comment") or ""
                return None if (v == "") else parse(v, 511, False, 32)

            return {
                "Comment": _arrow343(),
                "Key": get_item(groups(m), "key") or ""
            }

        else: 
            return None


    else: 
        return None



def _007CKeyValue_007C__007C(input: PreprocessorElement) -> dict[str, Any] | None:
    if input.tag == 2:
        m: Any = match(create("^(?P<key>[^\\{{\\[]+):\\s+(?P<value>.*)$"), input.fields[0])
        if m is not None:
            v: str = get_item(groups(m), "value") or "".strip()
            return {
                "Key": get_item(groups(m), "key") or "",
                "Value": v
            }

        else: 
            return None


    else: 
        return None



def _007CYamlValue_007C__007C(input: PreprocessorElement) -> dict[str, Any] | None:
    if input.tag == 2:
        m: Any = match(create(ValuePattern), input.fields[0])
        if m is not None:
            def _arrow344(__unit: None=None, input: Any=input) -> int | None:
                v: str = get_item(groups(m), "comment") or ""
                return None if (v == "") else parse(v, 511, False, 32)

            return {
                "Comment": _arrow344(),
                "Value": get_item(groups(m), "value") or "".strip()
            }

        else: 
            return None


    else: 
        return None



def _007CYamlComment_007C__007C(input: PreprocessorElement) -> dict[str, Any] | None:
    if input.tag == 2:
        m: Any = match(create(LineCommentPattern), input.fields[0])
        if m is not None:
            return {
                "Comment": parse(get_item(groups(m), "comment") or "", 511, False, 32)
            }

        else: 
            return None


    else: 
        return None



def _007CSequenceMinusOpener_007C__007C(input: PreprocessorElement) -> dict[str, Any] | None:
    if input.tag == 2:
        m: Any = match(create("^-(\\s+(?P<value>.*))?$"), input.fields[0])
        if m is not None:
            def _arrow345(__unit: None=None, input: Any=input) -> str | None:
                v: str = get_item(groups(m), "value") or "".strip()
                return None if (v == "") else v

            return {
                "Value": _arrow345()
            }

        else: 
            return None


    else: 
        return None



def _007CInlineSequence_007C__007C(input: PreprocessorElement) -> dict[str, Any] | None:
    if input.tag == 2:
        m: Any = match(create(InlineSequencePattern), input.fields[0])
        if m is not None:
            def _arrow346(__unit: None=None, input: Any=input) -> int | None:
                v: str = get_item(groups(m), "comment") or ""
                return None if (v == "") else parse(v, 511, False, 32)

            return {
                "Comment": _arrow346(),
                "Value": get_item(groups(m), "inlineSequence") or ""
            }

        else: 
            return None


    else: 
        return None



def _007CSequenceSquareOpener_007C__007C(input: PreprocessorElement) -> dict[str, Any] | None:
    if input.tag == 2:
        m: Any = match(create(SequenceOpenerPattern), input.fields[0])
        if m is not None:
            def _arrow347(__unit: None=None, input: Any=input) -> int | None:
                v: str = get_item(groups(m), "comment") or ""
                return None if (v == "") else parse(v, 511, False, 32)

            return {
                "Comment": _arrow347()
            }

        else: 
            return None


    else: 
        return None



def _007CSequenceSquareCloser_007C__007C(input: PreprocessorElement) -> dict[str, Any] | None:
    if input.tag == 2:
        m: Any = match(create(SequenceCloserPattern), input.fields[0])
        if m is not None:
            def _arrow348(__unit: None=None, input: Any=input) -> int | None:
                v: str = get_item(groups(m), "comment") or ""
                return None if (v == "") else parse(v, 511, False, 32)

            return {
                "Comment": _arrow348()
            }

        else: 
            return None


    else: 
        return None



def _007CInlineJSON_007C__007C(input: PreprocessorElement) -> dict[str, Any] | None:
    if input.tag == 2:
        m: Any = match(create(InlineJSONPattern), input.fields[0])
        if m is not None:
            def _arrow349(__unit: None=None, input: Any=input) -> int | None:
                v: str = get_item(groups(m), "comment") or ""
                return None if (v == "") else parse(v, 511, False, 32)

            return {
                "Comment": _arrow349(),
                "Value": get_item(groups(m), "inlineSequence") or ""
            }

        else: 
            return None


    else: 
        return None



def _007CJSONKeyOpener_007C__007C(input: PreprocessorElement) -> dict[str, Any] | None:
    if input.tag == 2:
        m: Any = match(create(JSONOpenerPattern), input.fields[0])
        if m is not None:
            def _arrow350(__unit: None=None, input: Any=input) -> int | None:
                v: str = get_item(groups(m), "comment") or ""
                return None if (v == "") else parse(v, 511, False, 32)

            return {
                "Comment": _arrow350(),
                "Key": get_item(groups(m), "key") or ""
            }

        else: 
            return None


    else: 
        return None



def _007CJSONCloser_007C__007C(input: PreprocessorElement) -> dict[str, Any] | None:
    if input.tag == 2:
        m: Any = match(create(JSONCloserPattern), input.fields[0])
        if m is not None:
            def _arrow351(__unit: None=None, input: Any=input) -> int | None:
                v: str = get_item(groups(m), "comment") or ""
                return None if (v == "") else parse(v, 511, False, 32)

            return {
                "Comment": _arrow351()
            }

        else: 
            return None


    else: 
        return None



def _007CSchemaNamespace_007C__007C(input: PreprocessorElement) -> dict[str, Any] | None:
    if input.tag == 2:
        m: Any = match(create("^\\$(?P<key>[a-zA-Z0-9\\s:]+):$"), input.fields[0])
        if m is not None:
            return {
                "Key": get_item(groups(m), "key") or ""
            }

        else: 
            return None


    else: 
        return None



__all__ = ["_007CKey_007C__007C", "_007CKeyValue_007C__007C", "_007CYamlValue_007C__007C", "_007CYamlComment_007C__007C", "_007CSequenceMinusOpener_007C__007C", "_007CInlineSequence_007C__007C", "_007CSequenceSquareOpener_007C__007C", "_007CSequenceSquareCloser_007C__007C", "_007CInlineJSON_007C__007C", "_007CJSONKeyOpener_007C__007C", "_007CJSONCloser_007C__007C", "_007CSchemaNamespace_007C__007C"]

