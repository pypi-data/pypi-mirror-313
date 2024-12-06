from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.array_ import contains
from ...fable_modules.fable_library.list import (is_empty, tail, FSharpList, head, append, singleton, empty)
from ...fable_modules.fable_library.map_util import (add_to_dict, try_get_value, remove_from_dict)
from ...fable_modules.fable_library.mutable_map import Dictionary
from ...fable_modules.fable_library.option import (some, value as value_1)
from ...fable_modules.fable_library.seq import iterate
from ...fable_modules.fable_library.types import (FSharpRef, Array)
from ...fable_modules.fable_library.util import (equals, structural_hash, IEnumerable_1, ignore, get_enumerator, dispose)

_T = TypeVar("_T")

_U = TypeVar("_U")

_KEY_ = TypeVar("_KEY_")

_KEY = TypeVar("_KEY")

__B = TypeVar("__B")

__A = TypeVar("__A")

__C = TypeVar("__C")

__A_ = TypeVar("__A_")

def Option_fromValueWithDefault(d: Any, v: Any) -> Any | None:
    if equals(d, v):
        return None

    else: 
        return some(v)



def Option_mapDefault(d: Any, f: Callable[[_T], _T], o: Any | None=None) -> Any | None:
    return Option_fromValueWithDefault(d, f(d) if (o is None) else f(value_1(o)))


def Option_mapOrDefault(d: Any | None, f: Callable[[_U], _T], o: Any | None=None) -> Any | None:
    if o is None:
        return d

    else: 
        return some(f(value_1(o)))



def List_tryPickAndRemove(f: Callable[[_T], _U | None], lst: FSharpList[Any]) -> tuple[_U | None, FSharpList[_T]]:
    def loop(new_list_mut: FSharpList[_T], remaining_list_mut: FSharpList[_T], f: Any=f, lst: Any=lst) -> tuple[_U | None, FSharpList[_T]]:
        while True:
            (new_list, remaining_list) = (new_list_mut, remaining_list_mut)
            if not is_empty(remaining_list):
                t: FSharpList[_T] = tail(remaining_list)
                h: _T = head(remaining_list)
                match_value: _U | None = f(h)
                if match_value is None:
                    new_list_mut = append(new_list, singleton(h))
                    remaining_list_mut = t
                    continue

                else: 
                    return (some(value_1(match_value)), append(new_list, t))


            else: 
                return (None, new_list)

            break

    return loop(empty(), lst)


def Dictionary_ofSeq(s: IEnumerable_1[tuple[_KEY, _T]]) -> Any:
    class ObjectExpr513:
        @property
        def Equals(self) -> Callable[[_KEY_, _KEY_], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[_KEY_], int]:
            return structural_hash

    dict_1: Any = Dictionary([], ObjectExpr513())
    def action(tupled_arg: tuple[_KEY, _T], s: Any=s) -> None:
        add_to_dict(dict_1, tupled_arg[0], tupled_arg[1])

    iterate(action, s)
    return dict_1


def Dictionary_tryFind(key: Any, dict_1: Any) -> Any | None:
    pattern_input: tuple[bool, _T]
    out_arg: _T = None
    def _arrow514(__unit: None=None, key: Any=key, dict_1: Any=dict_1) -> _T:
        return out_arg

    def _arrow515(v: _T | None=None, key: Any=key, dict_1: Any=dict_1) -> None:
        nonlocal out_arg
        out_arg = v

    pattern_input = (try_get_value(dict_1, key, FSharpRef(_arrow514, _arrow515)), out_arg)
    if pattern_input[0]:
        return some(pattern_input[1])

    else: 
        return None



def Dictionary_ofSeqWithMerge(merge: Callable[[_T, _T], _T], s: IEnumerable_1[tuple[_KEY, _T]]) -> Any:
    class ObjectExpr516:
        @property
        def Equals(self) -> Callable[[_KEY_, _KEY_], bool]:
            return equals

        @property
        def GetHashCode(self) -> Callable[[_KEY_], int]:
            return structural_hash

    dict_1: Any = Dictionary([], ObjectExpr516())
    def action(tupled_arg: tuple[_KEY, _T], merge: Any=merge, s: Any=s) -> None:
        k: _KEY = tupled_arg[0]
        v: _T = tupled_arg[1]
        match_value: _T | None = Dictionary_tryFind(k, dict_1)
        if match_value is None:
            add_to_dict(dict_1, k, v)

        else: 
            v_0027: _T = value_1(match_value)
            ignore(remove_from_dict(dict_1, k))
            add_to_dict(dict_1, k, merge(v_0027, v))


    iterate(action, s)
    return dict_1


def ResizeArray_map(f: Callable[[__A], __B], a: Array[Any]) -> Array[Any]:
    b: Array[__B] = []
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            i: __A = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            (b.append(f(i)))

    finally: 
        dispose(enumerator)

    return b


def ResizeArray_choose(f: Callable[[__A], __B | None], a: Array[Any]) -> Array[Any]:
    b: Array[__B] = []
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            match_value: __B | None = f(enumerator.System_Collections_Generic_IEnumerator_1_get_Current())
            if match_value is None:
                pass

            else: 
                x: __B = value_1(match_value)
                (b.append(x))


    finally: 
        dispose(enumerator)

    return b


def ResizeArray_filter(f: Callable[[__A], bool], a: Array[Any]) -> Array[Any]:
    b: Array[__A] = []
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            i: __A = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            if f(i):
                (b.append(i))


    finally: 
        dispose(enumerator)

    return b


def ResizeArray_fold(f: Callable[[__A, __B], __A], s: Any, a: Array[Any]) -> Any:
    state: __A = s
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            i: __B = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            state = f(state, i)

    finally: 
        dispose(enumerator)

    return state


def ResizeArray_foldBack(f: Callable[[__A, __B], __B], a: Array[Any], s: Any) -> Any:
    state: __B = s
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            i: __A = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            state = f(i, state)

    finally: 
        dispose(enumerator)

    return state


def ResizeArray_iter(f: Callable[[__A], None], a: Array[Any]) -> None:
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            f(enumerator.System_Collections_Generic_IEnumerator_1_get_Current())

    finally: 
        dispose(enumerator)



def ResizeArray_reduce(f: Callable[[__A, __A], __A], a: Array[Any]) -> Any:
    if len(a) == 0:
        raise Exception("ResizeArray.reduce: empty array")

    elif len(a) == 1:
        return a[0]

    else: 
        a_5: Array[__A] = a
        state: __A = a_5[0]
        for i in range(1, (len(a_5) - 1) + 1, 1):
            state = f(state, a_5[i])
        return state



def ResizeArray_collect(f: Callable[[__A], __B], a: Array[Any]) -> Array[Any]:
    b: Array[__C] = []
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            with get_enumerator(f(enumerator.System_Collections_Generic_IEnumerator_1_get_Current())) as enumerator_1:
                while enumerator_1.System_Collections_IEnumerator_MoveNext():
                    j: __C = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                    (b.append(j))

    finally: 
        dispose(enumerator)

    return b


def ResizeArray_distinct(a: Array[Any]) -> Array[Any]:
    b: Array[__A] = []
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            i: __A = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            class ObjectExpr517:
                @property
                def Equals(self) -> Callable[[__A_, __A_], bool]:
                    return equals

                @property
                def GetHashCode(self) -> Callable[[__A_], int]:
                    return structural_hash

            if not contains(i, b, ObjectExpr517()):
                (b.append(i))


    finally: 
        dispose(enumerator)

    return b


def ResizeArray_isEmpty(a: Array[Any]) -> bool:
    return len(a) == 0


def ResizeArray_append(a: Array[Any], b: Array[Any]) -> Array[Any]:
    c: Array[__A] = []
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            i: __A = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            (c.append(i))

    finally: 
        dispose(enumerator)

    enumerator_1: Any = get_enumerator(b)
    try: 
        while enumerator_1.System_Collections_IEnumerator_MoveNext():
            i_1: __A = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
            (c.append(i_1))

    finally: 
        dispose(enumerator_1)

    return c


def ResizeArray_appendSingleton(b: Any, a: Array[Any]) -> Array[Any]:
    c: Array[_T] = []
    enumerator: Any = get_enumerator(a)
    try: 
        while enumerator.System_Collections_IEnumerator_MoveNext():
            i: _T = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
            (c.append(i))

    finally: 
        dispose(enumerator)

    (c.append(b))
    return c


__all__ = ["Option_fromValueWithDefault", "Option_mapDefault", "Option_mapOrDefault", "List_tryPickAndRemove", "Dictionary_ofSeq", "Dictionary_tryFind", "Dictionary_ofSeqWithMerge", "ResizeArray_map", "ResizeArray_choose", "ResizeArray_filter", "ResizeArray_fold", "ResizeArray_foldBack", "ResizeArray_iter", "ResizeArray_reduce", "ResizeArray_collect", "ResizeArray_distinct", "ResizeArray_isEmpty", "ResizeArray_append", "ResizeArray_appendSingleton"]

