from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.array_ import (map as map_2, iterate_indexed, fold, fill)
from ...fable_modules.fable_library.list import (FSharpList, empty as empty_1)
from ...fable_modules.fable_library.map import (of_seq, empty as empty_2)
from ...fable_modules.fable_library.map_util import (get_item_from_dict, add_to_dict)
from ...fable_modules.fable_library.mutable_map import Dictionary
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.range import range_big_int
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.seq import (to_list, delay, append, singleton, map, empty, collect, to_array)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import (IEnumerable_1, compare_arrays, equal_arrays, array_hash, equals, to_enumerable, int32_to_string, ignore)
from ...fable_modules.thoth_json_core.decode import (object, list_1 as list_1_1, IOptionalGetter, map_0027, tuple2 as tuple2_1, int_1, IRequiredGetter, string, IGetters, array as array_2, Helpers_prependPath)
from ...fable_modules.thoth_json_core.encode import (list_1, map as map_1, tuple2)
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1, ErrorReason_1, IDecoderHelpers_1)
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Table.arc_table import ArcTable
from ...Core.Table.composite_cell import CompositeCell
from ...Core.Table.composite_header import CompositeHeader
from ..string_table import (encode_string, decode_string)
from .cell_table import (encode_cell, decode_cell)
from .composite_cell import (encoder as encoder_2, decoder as decoder_2)
from .composite_header import (encoder as encoder_1, decoder as decoder_1)

__A_ = TypeVar("__A_")

_VALUE_ = TypeVar("_VALUE_")

_VALUE = TypeVar("_VALUE")

def encoder(table: ArcTable) -> IEncodable:
    def _arrow2556(__unit: None=None, table: Any=table) -> IEnumerable_1[tuple[str, IEncodable]]:
        def _arrow2537(__unit: None=None) -> IEncodable:
            value_4: str = table.Name
            class ObjectExpr2536(IEncodable):
                def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_2.encode_string(value_4)

            return ObjectExpr2536()

        def _arrow2554(__unit: None=None) -> IEnumerable_1[tuple[str, IEncodable]]:
            def _arrow2539(__unit: None=None) -> IEnumerable_1[IEncodable]:
                return map(encoder_1, table.Headers)

            def _arrow2553(__unit: None=None) -> IEnumerable_1[tuple[str, IEncodable]]:
                def key_encoder(tupled_arg: tuple[int, int]) -> IEncodable:
                    def _arrow2545(value: int, tupled_arg: Any=tupled_arg) -> IEncodable:
                        class ObjectExpr2543(IEncodable):
                            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                                return helpers.encode_signed_integral_number(value)

                        return ObjectExpr2543()

                    def _arrow2547(value_2: int, tupled_arg: Any=tupled_arg) -> IEncodable:
                        class ObjectExpr2546(IEncodable):
                            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                                return helpers_1.encode_signed_integral_number(value_2)

                        return ObjectExpr2546()

                    return tuple2(_arrow2545, _arrow2547, tupled_arg[0], tupled_arg[1])

                def _arrow2551(__unit: None=None) -> IEnumerable_1[tuple[tuple[int, int], CompositeCell]]:
                    def _arrow2550(match_value: Any) -> IEnumerable_1[tuple[tuple[int, int], CompositeCell]]:
                        active_pattern_result: tuple[tuple[int, int], CompositeCell] = match_value
                        return singleton((active_pattern_result[0], active_pattern_result[1]))

                    return collect(_arrow2550, table.Values)

                class ObjectExpr2552:
                    @property
                    def Compare(self) -> Callable[[tuple[int, int], tuple[int, int]], int]:
                        return compare_arrays

                return singleton(("values", map_1(key_encoder, encoder_2, of_seq(to_list(delay(_arrow2551)), ObjectExpr2552())))) if (len(table.Values) != 0) else empty()

            return append(singleton(("header", list_1(to_list(delay(_arrow2539))))) if (len(table.Headers) != 0) else empty(), delay(_arrow2553))

        return append(singleton(("name", _arrow2537())), delay(_arrow2554))

    values: IEnumerable_1[tuple[str, IEncodable]] = to_list(delay(_arrow2556))
    class ObjectExpr2560(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any], table: Any=table) -> Any:
            def mapping(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_3))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_3.encode_object(arg)

    return ObjectExpr2560()


def _arrow2570(get: IGetters) -> ArcTable:
    def _arrow2563(__unit: None=None) -> FSharpList[CompositeHeader] | None:
        arg_1: Decoder_1[FSharpList[CompositeHeader]] = list_1_1(decoder_1)
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("header", arg_1)

    decoded_header: Array[CompositeHeader] = list(default_arg(_arrow2563(), empty_1()))
    def _arrow2564(__unit: None=None) -> Any | None:
        arg_3: Decoder_1[Any] = map_0027(tuple2_1(int_1, int_1), decoder_2)
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("values", arg_3)

    class ObjectExpr2565:
        @property
        def Compare(self) -> Callable[[tuple[int, int], tuple[int, int]], int]:
            return compare_arrays

    class ObjectExpr2566:
        @property
        def Equals(self) -> Callable[[tuple[int, int], tuple[int, int]], bool]:
            return equal_arrays

        @property
        def GetHashCode(self) -> Callable[[tuple[int, int]], int]:
            return array_hash

    decoded_values: Any = Dictionary(default_arg(_arrow2564(), empty_2(ObjectExpr2565())), ObjectExpr2566())
    def _arrow2569(__unit: None=None) -> str:
        object_arg_2: IRequiredGetter = get.Required
        return object_arg_2.Field("name", string)

    return ArcTable.create(_arrow2569(), decoded_header, decoded_values)


decoder: Decoder_1[ArcTable] = object(_arrow2570)

def encoder_compressed_column(column_index: int, row_count: int, cell_table: Any, table: ArcTable) -> IEncodable:
    if True if table.Headers[column_index].IsIOType else (row_count < 100):
        def _arrow2573(__unit: None=None, column_index: Any=column_index, row_count: Any=row_count, cell_table: Any=cell_table, table: Any=table) -> IEnumerable_1[IEncodable]:
            def _arrow2572(r: int) -> IEncodable:
                return encode_cell(cell_table, get_item_from_dict(table.Values, (column_index, r)))

            return map(_arrow2572, range_big_int(0, 1, row_count - 1))

        values: Array[IEncodable] = to_array(delay(_arrow2573))
        class ObjectExpr2575(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], column_index: Any=column_index, row_count: Any=row_count, cell_table: Any=cell_table, table: Any=table) -> Any:
                def mapping(v: IEncodable) -> __A_:
                    return v.Encode(helpers)

                arg: Array[__A_] = map_2(mapping, values, None)
                return helpers.encode_array(arg)

        return ObjectExpr2575()

    else: 
        current: CompositeCell = get_item_from_dict(table.Values, (column_index, 0))
        from_: int = 0
        def _arrow2602(__unit: None=None, column_index: Any=column_index, row_count: Any=row_count, cell_table: Any=cell_table, table: Any=table) -> IEnumerable_1[IEncodable]:
            def _arrow2593(i: int) -> IEnumerable_1[IEncodable]:
                next_1: CompositeCell = get_item_from_dict(table.Values, (column_index, i))
                def _arrow2591(__unit: None=None) -> IEncodable:
                    def _arrow2582(__unit: None=None) -> IEncodable:
                        value: int = from_ or 0
                        class ObjectExpr2581(IEncodable):
                            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                                return helpers_1.encode_signed_integral_number(value)

                        return ObjectExpr2581()

                    def _arrow2585(__unit: None=None) -> IEncodable:
                        value_1: int = (i - 1) or 0
                        class ObjectExpr2584(IEncodable):
                            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                                return helpers_2.encode_signed_integral_number(value_1)

                        return ObjectExpr2584()

                    values_1: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("f", _arrow2582()), ("t", _arrow2585()), ("v", encode_cell(cell_table, current))])
                    class ObjectExpr2590(IEncodable):
                        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                            def mapping_1(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                                return (tupled_arg[0], tupled_arg[1].Encode(helpers_3))

                            arg_1: IEnumerable_1[tuple[str, __A_]] = map(mapping_1, values_1)
                            return helpers_3.encode_object(arg_1)

                    return ObjectExpr2590()

                def _arrow2592(__unit: None=None) -> IEnumerable_1[IEncodable]:
                    nonlocal current, from_
                    current = next_1
                    from_ = i or 0
                    return empty()

                return append(singleton(_arrow2591()), delay(_arrow2592)) if (not equals(next_1, current)) else empty()

            def _arrow2601(__unit: None=None) -> IEnumerable_1[IEncodable]:
                def _arrow2600(__unit: None=None) -> IEncodable:
                    def _arrow2596(__unit: None=None) -> IEncodable:
                        value_2: int = from_ or 0
                        class ObjectExpr2595(IEncodable):
                            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                                return helpers_4.encode_signed_integral_number(value_2)

                        return ObjectExpr2595()

                    def _arrow2598(__unit: None=None) -> IEncodable:
                        value_3: int = (row_count - 1) or 0
                        class ObjectExpr2597(IEncodable):
                            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                                return helpers_5.encode_signed_integral_number(value_3)

                        return ObjectExpr2597()

                    values_2: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("f", _arrow2596()), ("t", _arrow2598()), ("v", encode_cell(cell_table, current))])
                    class ObjectExpr2599(IEncodable):
                        def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                            def mapping_2(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_6))

                            arg_2: IEnumerable_1[tuple[str, __A_]] = map(mapping_2, values_2)
                            return helpers_6.encode_object(arg_2)

                    return ObjectExpr2599()

                return singleton(_arrow2600())

            return append(collect(_arrow2593, range_big_int(1, 1, row_count - 1)), delay(_arrow2601))

        values_3: Array[IEncodable] = to_array(delay(_arrow2602))
        class ObjectExpr2603(IEncodable):
            def Encode(self, helpers_7: IEncoderHelpers_1[Any], column_index: Any=column_index, row_count: Any=row_count, cell_table: Any=cell_table, table: Any=table) -> Any:
                def mapping_3(v_3: IEncodable) -> __A_:
                    return v_3.Encode(helpers_7)

                arg_3: Array[__A_] = map_2(mapping_3, values_3, None)
                return helpers_7.encode_array(arg_3)

        return ObjectExpr2603()



def decoder_compressed_column(cell_table: Array[CompositeCell], table: ArcTable, column_index: int) -> Decoder_1[None]:
    class ObjectExpr2605(Decoder_1[None]):
        def Decode(self, helper: IDecoderHelpers_1[Any], column: Any, cell_table: Any=cell_table, table: Any=table, column_index: Any=column_index) -> FSharpResult_2[None, tuple[str, ErrorReason_1[__A_]]]:
            match_value: FSharpResult_2[Array[CompositeCell], tuple[str, ErrorReason_1[__A_]]] = array_2(decode_cell(cell_table)).Decode(helper, column)
            if match_value.tag == 1:
                def _arrow2604(get: IGetters) -> None:
                    from_: int
                    object_arg: IRequiredGetter = get.Required
                    from_ = object_arg.Field("f", int_1)
                    to_: int
                    object_arg_1: IRequiredGetter = get.Required
                    to_ = object_arg_1.Field("t", int_1)
                    value: CompositeCell
                    arg_5: Decoder_1[CompositeCell] = decode_cell(cell_table)
                    object_arg_2: IRequiredGetter = get.Required
                    value = object_arg_2.Field("v", arg_5)
                    for i in range(from_, to_ + 1, 1):
                        add_to_dict(table.Values, (column_index, i), value)

                range_decoder: Decoder_1[None] = object(_arrow2604)
                match_value_1: FSharpResult_2[Array[None], tuple[str, ErrorReason_1[__A_]]] = array_2(range_decoder).Decode(helper, column)
                return FSharpResult_2(1, match_value_1.fields[0]) if (match_value_1.tag == 1) else FSharpResult_2(0, None)

            else: 
                def action(r: int, cell: CompositeCell) -> None:
                    add_to_dict(table.Values, (column_index, r), cell)

                iterate_indexed(action, match_value.fields[0])
                return FSharpResult_2(0, None)


    return ObjectExpr2605()


def arrayi(decoderi: Callable[[int], Decoder_1[_VALUE]]) -> Decoder_1[Array[Any]]:
    class ObjectExpr2607(Decoder_1[Array[_VALUE_]]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value: Any, decoderi: Any=decoderi) -> FSharpResult_2[Array[_VALUE_], tuple[str, ErrorReason_1[__A_]]]:
            if helpers.is_array(value):
                i: int = -1
                tokens: Array[__A_] = helpers.as_array(value)
                def folder(acc: FSharpResult_2[Array[_VALUE_], tuple[str, ErrorReason_1[__A_]]], value_1: __A_) -> FSharpResult_2[Array[_VALUE_], tuple[str, ErrorReason_1[__A_]]]:
                    nonlocal i
                    i = (i + 1) or 0
                    if acc.tag == 0:
                        acc_1: Array[_VALUE_] = acc.fields[0]
                        match_value: FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]] = decoderi(i).Decode(helpers, value_1)
                        if match_value.tag == 0:
                            acc_1[i] = match_value.fields[0]
                            return FSharpResult_2(0, acc_1)

                        else: 
                            def _arrow2606(__unit: None=None, acc: Any=acc, value_1: Any=value_1) -> tuple[str, ErrorReason_1[__A_]]:
                                tupled_arg: tuple[str, ErrorReason_1[__A_]] = match_value.fields[0]
                                return Helpers_prependPath((".[" + int32_to_string(i)) + "]", tupled_arg[0], tupled_arg[1])

                            return FSharpResult_2(1, _arrow2606())


                    else: 
                        return acc


                return fold(folder, FSharpResult_2(0, fill([0] * len(tokens), 0, len(tokens), None)), tokens)

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(0, "an array", value)))


    return ObjectExpr2607()


def encoder_compressed(string_table: Any, oa_table: Any, cell_table: Any, table: ArcTable) -> IEncodable:
    def _arrow2614(__unit: None=None, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, table: Any=table) -> IEnumerable_1[tuple[str, IEncodable]]:
        def _arrow2613(__unit: None=None) -> IEnumerable_1[tuple[str, IEncodable]]:
            def _arrow2608(__unit: None=None) -> IEnumerable_1[IEncodable]:
                return map(encoder_1, table.Headers)

            def _arrow2612(__unit: None=None) -> IEnumerable_1[tuple[str, IEncodable]]:
                if len(table.Values) != 0:
                    row_count: int = table.RowCount or 0
                    def _arrow2610(__unit: None=None) -> IEnumerable_1[IEncodable]:
                        def _arrow2609(c: int) -> IEncodable:
                            return encoder_compressed_column(c, row_count, cell_table, table)

                        return map(_arrow2609, range_big_int(0, 1, table.ColumnCount - 1))

                    columns: Array[IEncodable] = to_array(delay(_arrow2610))
                    class ObjectExpr2611(IEncodable):
                        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                            def mapping(v: IEncodable) -> __A_:
                                return v.Encode(helpers)

                            arg: Array[__A_] = map_2(mapping, columns, None)
                            return helpers.encode_array(arg)

                    return singleton(("c", ObjectExpr2611()))

                else: 
                    return empty()


            return append(singleton(("h", list_1(to_list(delay(_arrow2608))))) if (len(table.Headers) != 0) else empty(), delay(_arrow2612))

        return append(singleton(("n", encode_string(string_table, table.Name))), delay(_arrow2613))

    values_1: IEnumerable_1[tuple[str, IEncodable]] = to_list(delay(_arrow2614))
    class ObjectExpr2615(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, table: Any=table) -> Any:
            def mapping_1(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_1))

            arg_1: IEnumerable_1[tuple[str, __A_]] = map(mapping_1, values_1)
            return helpers_1.encode_object(arg_1)

    return ObjectExpr2615()


def decoder_compressed(string_table: Array[str], oa_table: Array[OntologyAnnotation], cell_table: Array[CompositeCell]) -> Decoder_1[ArcTable]:
    def _arrow2621(get: IGetters, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table) -> ArcTable:
        def _arrow2616(__unit: None=None) -> FSharpList[CompositeHeader] | None:
            arg_1: Decoder_1[FSharpList[CompositeHeader]] = list_1_1(decoder_1)
            object_arg: IOptionalGetter = get.Optional
            return object_arg.Field("h", arg_1)

        decoded_header: Array[CompositeHeader] = list(default_arg(_arrow2616(), empty_1()))
        def _arrow2617(__unit: None=None) -> str:
            arg_3: Decoder_1[str] = decode_string(string_table)
            object_arg_1: IRequiredGetter = get.Required
            return object_arg_1.Field("n", arg_3)

        class ObjectExpr2618:
            @property
            def Equals(self) -> Callable[[tuple[int, int], tuple[int, int]], bool]:
                return equal_arrays

            @property
            def GetHashCode(self) -> Callable[[tuple[int, int]], int]:
                return array_hash

        table: ArcTable = ArcTable.create(_arrow2617(), decoded_header, Dictionary([], ObjectExpr2618()))
        def _arrow2620(__unit: None=None) -> Array[None] | None:
            def _arrow2619(column_index: int) -> Decoder_1[None]:
                return decoder_compressed_column(cell_table, table, column_index)

            arg_5: Decoder_1[Array[None]] = arrayi(_arrow2619)
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("c", arg_5)

        ignore(_arrow2620())
        return table

    return object(_arrow2621)


__all__ = ["encoder", "decoder", "encoder_compressed_column", "decoder_compressed_column", "arrayi", "encoder_compressed", "decoder_compressed"]

