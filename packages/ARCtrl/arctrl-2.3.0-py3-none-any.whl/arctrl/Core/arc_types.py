from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.array_ import (contains as contains_1, remove_in_place, add_range_in_place)
from ..fable_modules.fable_library.option import (map, default_arg, value as value_4)
from ..fable_modules.fable_library.range import range_big_int
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.resize_array import find_index
from ..fable_modules.fable_library.seq import (to_array, filter, contains, for_all, length, fold, to_list, delay, map as map_1, item, choose, exists, try_find_index, iterate, remove_at, try_find, append as append_3, collect)
from ..fable_modules.fable_library.seq2 import Array_distinct
from ..fable_modules.fable_library.string_ import (to_text, printf)
from ..fable_modules.fable_library.types import (Array, FSharpRef)
from ..fable_modules.fable_library.util import (string_hash, IEnumerable_1, get_enumerator, dispose, equals, safe_hash, to_enumerable, ignore)
from .comment import (Comment, Remark)
from .data_map import (DataMap, DataMap__Copy)
from .Helper.collections_ import (ResizeArray_map, ResizeArray_filter, ResizeArray_choose)
from .Helper.hash_codes import (box_hash_array, box_hash_option, box_hash_seq)
from .Helper.identifier import check_valid_characters
from .ontology_annotation import OntologyAnnotation
from .ontology_source_reference import OntologySourceReference
from .person import Person
from .publication import Publication
from .Table.arc_table import ArcTable
from .Table.arc_tables import (ArcTables, ArcTables_reflection, ArcTablesAux_getIOMap, ArcTablesAux_applyIOMap)
from .Table.composite_cell import CompositeCell
from .Table.composite_column import CompositeColumn
from .Table.composite_header import CompositeHeader

def _expr944() -> TypeInfo:
    return class_type("ARCtrl.ArcAssay", None, ArcAssay, ArcTables_reflection())


class ArcAssay(ArcTables):
    def __init__(self, identifier: str, measurement_type: OntologyAnnotation | None=None, technology_type: OntologyAnnotation | None=None, technology_platform: OntologyAnnotation | None=None, tables: Array[ArcTable] | None=None, datamap: DataMap | None=None, performers: Array[Person] | None=None, comments: Array[Comment] | None=None) -> None:
        super().__init__(default_arg(tables, []))
        performers_1: Array[Person] = default_arg(performers, [])
        comments_1: Array[Comment] = default_arg(comments, [])
        def _arrow943(__unit: None=None) -> str:
            identifier_1: str = identifier.strip()
            check_valid_characters(identifier_1)
            return identifier_1

        self.identifier_0040109: str = _arrow943()
        self.investigation: ArcInvestigation | None = None
        self.measurement_type_0040114: OntologyAnnotation | None = measurement_type
        self.technology_type_0040115: OntologyAnnotation | None = technology_type
        self.technology_platform_0040116: OntologyAnnotation | None = technology_platform
        self.data_map: DataMap | None = datamap
        self.performers_0040118_002D1: Array[Person] = performers_1
        self.comments_0040119_002D1: Array[Comment] = comments_1
        self.static_hash: int = 0

    @property
    def Identifier(self, __unit: None=None) -> str:
        this: ArcAssay = self
        return this.identifier_0040109

    @Identifier.setter
    def Identifier(self, i: str) -> None:
        this: ArcAssay = self
        this.identifier_0040109 = i

    @property
    def Investigation(self, __unit: None=None) -> ArcInvestigation | None:
        this: ArcAssay = self
        return this.investigation

    @Investigation.setter
    def Investigation(self, i: ArcInvestigation | None=None) -> None:
        this: ArcAssay = self
        this.investigation = i

    @property
    def MeasurementType(self, __unit: None=None) -> OntologyAnnotation | None:
        this: ArcAssay = self
        return this.measurement_type_0040114

    @MeasurementType.setter
    def MeasurementType(self, n: OntologyAnnotation | None=None) -> None:
        this: ArcAssay = self
        this.measurement_type_0040114 = n

    @property
    def TechnologyType(self, __unit: None=None) -> OntologyAnnotation | None:
        this: ArcAssay = self
        return this.technology_type_0040115

    @TechnologyType.setter
    def TechnologyType(self, n: OntologyAnnotation | None=None) -> None:
        this: ArcAssay = self
        this.technology_type_0040115 = n

    @property
    def TechnologyPlatform(self, __unit: None=None) -> OntologyAnnotation | None:
        this: ArcAssay = self
        return this.technology_platform_0040116

    @TechnologyPlatform.setter
    def TechnologyPlatform(self, n: OntologyAnnotation | None=None) -> None:
        this: ArcAssay = self
        this.technology_platform_0040116 = n

    @property
    def DataMap(self, __unit: None=None) -> DataMap | None:
        this: ArcAssay = self
        return this.data_map

    @DataMap.setter
    def DataMap(self, n: DataMap | None=None) -> None:
        this: ArcAssay = self
        this.data_map = n

    @property
    def Performers(self, __unit: None=None) -> Array[Person]:
        this: ArcAssay = self
        return this.performers_0040118_002D1

    @Performers.setter
    def Performers(self, n: Array[Person]) -> None:
        this: ArcAssay = self
        this.performers_0040118_002D1 = n

    @property
    def Comments(self, __unit: None=None) -> Array[Comment]:
        this: ArcAssay = self
        return this.comments_0040119_002D1

    @Comments.setter
    def Comments(self, n: Array[Comment]) -> None:
        this: ArcAssay = self
        this.comments_0040119_002D1 = n

    @property
    def StaticHash(self, __unit: None=None) -> int:
        this: ArcAssay = self
        return this.static_hash

    @StaticHash.setter
    def StaticHash(self, h: int) -> None:
        this: ArcAssay = self
        this.static_hash = h or 0

    @staticmethod
    def init(identifier: str) -> ArcAssay:
        return ArcAssay(identifier)

    @staticmethod
    def create(identifier: str, measurement_type: OntologyAnnotation | None=None, technology_type: OntologyAnnotation | None=None, technology_platform: OntologyAnnotation | None=None, tables: Array[ArcTable] | None=None, datamap: DataMap | None=None, performers: Array[Person] | None=None, comments: Array[Comment] | None=None) -> ArcAssay:
        return ArcAssay(identifier, measurement_type, technology_type, technology_platform, tables, datamap, performers, comments)

    @staticmethod
    def make(identifier: str, measurement_type: OntologyAnnotation | None, technology_type: OntologyAnnotation | None, technology_platform: OntologyAnnotation | None, tables: Array[ArcTable], datamap: DataMap | None, performers: Array[Person], comments: Array[Comment]) -> ArcAssay:
        return ArcAssay(identifier, measurement_type, technology_type, technology_platform, tables, datamap, performers, comments)

    @staticmethod
    def FileName() -> str:
        return "isa.assay.xlsx"

    @property
    def StudiesRegisteredIn(self, __unit: None=None) -> Array[ArcStudy]:
        this: ArcAssay = self
        match_value: ArcInvestigation | None = this.Investigation
        if match_value is None:
            return []

        else: 
            i: ArcInvestigation = match_value
            def predicate(s: ArcStudy) -> bool:
                source: Array[str] = s.RegisteredAssayIdentifiers
                class ObjectExpr895:
                    @property
                    def Equals(self) -> Callable[[str, str], bool]:
                        def _arrow894(x: str, y: str) -> bool:
                            return x == y

                        return _arrow894

                    @property
                    def GetHashCode(self) -> Callable[[str], int]:
                        return string_hash

                return contains(this.Identifier, source, ObjectExpr895())

            return to_array(filter(predicate, i.Studies))


    @staticmethod
    def add_table(table: ArcTable, index: int | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow896(assay: ArcAssay) -> ArcAssay:
            c: ArcAssay = assay.Copy()
            c.AddTable(table, index)
            return c

        return _arrow896

    @staticmethod
    def add_tables(tables: IEnumerable_1[ArcTable], index: int | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow897(assay: ArcAssay) -> ArcAssay:
            c: ArcAssay = assay.Copy()
            c.AddTables(tables, index)
            return c

        return _arrow897

    @staticmethod
    def init_table(table_name: str, index: int | None=None) -> Callable[[ArcAssay], tuple[ArcAssay, ArcTable]]:
        def _arrow898(assay: ArcAssay) -> tuple[ArcAssay, ArcTable]:
            c: ArcAssay = assay.Copy()
            return (c, c.InitTable(table_name, index))

        return _arrow898

    @staticmethod
    def init_tables(table_names: IEnumerable_1[str], index: int | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow899(assay: ArcAssay) -> ArcAssay:
            c: ArcAssay = assay.Copy()
            c.InitTables(table_names, index)
            return c

        return _arrow899

    @staticmethod
    def get_table_at(index: int) -> Callable[[ArcAssay], ArcTable]:
        def _arrow900(assay: ArcAssay) -> ArcTable:
            new_assay: ArcAssay = assay.Copy()
            return new_assay.GetTableAt(index)

        return _arrow900

    @staticmethod
    def get_table(name: str) -> Callable[[ArcAssay], ArcTable]:
        def _arrow901(assay: ArcAssay) -> ArcTable:
            new_assay: ArcAssay = assay.Copy()
            return new_assay.GetTable(name)

        return _arrow901

    @staticmethod
    def update_table_at(index: int, table: ArcTable) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow902(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.UpdateTableAt(index, table)
            return new_assay

        return _arrow902

    @staticmethod
    def update_table(name: str, table: ArcTable) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow903(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.UpdateTable(name, table)
            return new_assay

        return _arrow903

    @staticmethod
    def set_table_at(index: int, table: ArcTable) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow904(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.SetTableAt(index, table)
            return new_assay

        return _arrow904

    @staticmethod
    def set_table(name: str, table: ArcTable) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow905(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.SetTable(name, table)
            return new_assay

        return _arrow905

    @staticmethod
    def remove_table_at(index: int) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow906(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.RemoveTableAt(index)
            return new_assay

        return _arrow906

    @staticmethod
    def remove_table(name: str) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow907(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.RemoveTable(name)
            return new_assay

        return _arrow907

    @staticmethod
    def map_table_at(index: int, update_fun: Callable[[ArcTable], None]) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow908(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.MapTableAt(index, update_fun)
            return new_assay

        return _arrow908

    @staticmethod
    def update_table(name: str, update_fun: Callable[[ArcTable], None]) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow909(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.MapTable(name, update_fun)
            return new_assay

        return _arrow909

    @staticmethod
    def rename_table_at(index: int, new_name: str) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow910(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.RenameTableAt(index, new_name)
            return new_assay

        return _arrow910

    @staticmethod
    def rename_table(name: str, new_name: str) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow911(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.RenameTable(name, new_name)
            return new_assay

        return _arrow911

    @staticmethod
    def add_column_at(table_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None, column_index: int | None=None, force_replace: bool | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow912(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.AddColumnAt(table_index, header, cells, column_index, force_replace)
            return new_assay

        return _arrow912

    @staticmethod
    def add_column(table_name: str, header: CompositeHeader, cells: Array[CompositeCell] | None=None, column_index: int | None=None, force_replace: bool | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow913(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.AddColumn(table_name, header, cells, column_index, force_replace)
            return new_assay

        return _arrow913

    @staticmethod
    def remove_column_at(table_index: int, column_index: int) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow914(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.RemoveColumnAt(table_index, column_index)
            return new_assay

        return _arrow914

    @staticmethod
    def remove_column(table_name: str, column_index: int) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow915(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.RemoveColumn(table_name, column_index)
            return new_assay

        return _arrow915

    @staticmethod
    def update_column_at(table_index: int, column_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow916(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.UpdateColumnAt(table_index, column_index, header, cells)
            return new_assay

        return _arrow916

    @staticmethod
    def update_column(table_name: str, column_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow917(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.UpdateColumn(table_name, column_index, header, cells)
            return new_assay

        return _arrow917

    @staticmethod
    def get_column_at(table_index: int, column_index: int) -> Callable[[ArcAssay], CompositeColumn]:
        def _arrow918(assay: ArcAssay) -> CompositeColumn:
            new_assay: ArcAssay = assay.Copy()
            return new_assay.GetColumnAt(table_index, column_index)

        return _arrow918

    @staticmethod
    def get_column(table_name: str, column_index: int) -> Callable[[ArcAssay], CompositeColumn]:
        def _arrow919(assay: ArcAssay) -> CompositeColumn:
            new_assay: ArcAssay = assay.Copy()
            return new_assay.GetColumn(table_name, column_index)

        return _arrow919

    @staticmethod
    def add_row_at(table_index: int, cells: Array[CompositeCell] | None=None, row_index: int | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow920(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.AddRowAt(table_index, cells, row_index)
            return new_assay

        return _arrow920

    @staticmethod
    def add_row(table_name: str, cells: Array[CompositeCell] | None=None, row_index: int | None=None) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow921(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.AddRow(table_name, cells, row_index)
            return new_assay

        return _arrow921

    @staticmethod
    def remove_row_at(table_index: int, row_index: int) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow922(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.RemoveColumnAt(table_index, row_index)
            return new_assay

        return _arrow922

    @staticmethod
    def remove_row(table_name: str, row_index: int) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow923(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.RemoveRow(table_name, row_index)
            return new_assay

        return _arrow923

    @staticmethod
    def update_row_at(table_index: int, row_index: int, cells: Array[CompositeCell]) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow924(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.UpdateRowAt(table_index, row_index, cells)
            return new_assay

        return _arrow924

    @staticmethod
    def update_row(table_name: str, row_index: int, cells: Array[CompositeCell]) -> Callable[[ArcAssay], ArcAssay]:
        def _arrow925(assay: ArcAssay) -> ArcAssay:
            new_assay: ArcAssay = assay.Copy()
            new_assay.UpdateRow(table_name, row_index, cells)
            return new_assay

        return _arrow925

    @staticmethod
    def get_row_at(table_index: int, row_index: int) -> Callable[[ArcAssay], Array[CompositeCell]]:
        def _arrow926(assay: ArcAssay) -> Array[CompositeCell]:
            new_assay: ArcAssay = assay.Copy()
            return new_assay.GetRowAt(table_index, row_index)

        return _arrow926

    @staticmethod
    def get_row(table_name: str, row_index: int) -> Callable[[ArcAssay], Array[CompositeCell]]:
        def _arrow927(assay: ArcAssay) -> Array[CompositeCell]:
            new_assay: ArcAssay = assay.Copy()
            return new_assay.GetRow(table_name, row_index)

        return _arrow927

    @staticmethod
    def set_performers(performers: Array[Person], assay: ArcAssay) -> ArcAssay:
        assay.Performers = performers
        return assay

    def Copy(self, __unit: None=None) -> ArcAssay:
        this: ArcAssay = self
        def f(c: ArcTable) -> ArcTable:
            return c.Copy()

        next_tables: Array[ArcTable] = ResizeArray_map(f, this.Tables)
        def f_1(c_1: Comment) -> Comment:
            return c_1.Copy()

        next_comments: Array[Comment] = ResizeArray_map(f_1, this.Comments)
        next_data_map: DataMap | None = map(DataMap__Copy, this.DataMap)
        def f_2(c_2: Person) -> Person:
            return c_2.Copy()

        next_performers: Array[Person] = ResizeArray_map(f_2, this.Performers)
        identifier: str = this.Identifier
        measurement_type: OntologyAnnotation | None = this.MeasurementType
        technology_type: OntologyAnnotation | None = this.TechnologyType
        technology_platform: OntologyAnnotation | None = this.TechnologyPlatform
        return ArcAssay.make(identifier, measurement_type, technology_type, technology_platform, next_tables, next_data_map, next_performers, next_comments)

    def UpdateBy(self, assay: ArcAssay, only_replace_existing: bool | None=None, append_sequences: bool | None=None) -> None:
        this: ArcAssay = self
        only_replace_existing_1: bool = default_arg(only_replace_existing, False)
        append_sequences_1: bool = default_arg(append_sequences, False)
        update_always: bool = not only_replace_existing_1
        if True if (assay.MeasurementType is not None) else update_always:
            this.MeasurementType = assay.MeasurementType

        if True if (assay.TechnologyType is not None) else update_always:
            this.TechnologyType = assay.TechnologyType

        if True if (assay.TechnologyPlatform is not None) else update_always:
            this.TechnologyPlatform = assay.TechnologyPlatform

        if True if (len(assay.Tables) != 0) else update_always:
            s: Array[ArcTable]
            origin: Array[ArcTable] = this.Tables
            next_1: Array[ArcTable] = assay.Tables
            if not append_sequences_1:
                def f(x: ArcTable) -> ArcTable:
                    return x

                s = ResizeArray_map(f, next_1)

            else: 
                combined: Array[ArcTable] = []
                enumerator: Any = get_enumerator(origin)
                try: 
                    while enumerator.System_Collections_IEnumerator_MoveNext():
                        e: ArcTable = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr928:
                            @property
                            def Equals(self) -> Callable[[ArcTable, ArcTable], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[ArcTable], int]:
                                return safe_hash

                        if not contains_1(e, combined, ObjectExpr928()):
                            (combined.append(e))


                finally: 
                    dispose(enumerator)

                enumerator_1: Any = get_enumerator(next_1)
                try: 
                    while enumerator_1.System_Collections_IEnumerator_MoveNext():
                        e_1: ArcTable = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr929:
                            @property
                            def Equals(self) -> Callable[[ArcTable, ArcTable], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[ArcTable], int]:
                                return safe_hash

                        if not contains_1(e_1, combined, ObjectExpr929()):
                            (combined.append(e_1))


                finally: 
                    dispose(enumerator_1)

                s = combined

            this.Tables = s

        if True if (len(assay.Performers) != 0) else update_always:
            s_1: Array[Person]
            origin_1: Array[Person] = this.Performers
            next_1_1: Array[Person] = assay.Performers
            if not append_sequences_1:
                def f_1(x_3: Person) -> Person:
                    return x_3

                s_1 = ResizeArray_map(f_1, next_1_1)

            else: 
                combined_1: Array[Person] = []
                enumerator_2: Any = get_enumerator(origin_1)
                try: 
                    while enumerator_2.System_Collections_IEnumerator_MoveNext():
                        e_2: Person = enumerator_2.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr930:
                            @property
                            def Equals(self) -> Callable[[Person, Person], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[Person], int]:
                                return safe_hash

                        if not contains_1(e_2, combined_1, ObjectExpr930()):
                            (combined_1.append(e_2))


                finally: 
                    dispose(enumerator_2)

                enumerator_1_1: Any = get_enumerator(next_1_1)
                try: 
                    while enumerator_1_1.System_Collections_IEnumerator_MoveNext():
                        e_1_1: Person = enumerator_1_1.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr931:
                            @property
                            def Equals(self) -> Callable[[Person, Person], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[Person], int]:
                                return safe_hash

                        if not contains_1(e_1_1, combined_1, ObjectExpr931()):
                            (combined_1.append(e_1_1))


                finally: 
                    dispose(enumerator_1_1)

                s_1 = combined_1

            this.Performers = s_1

        if True if (len(assay.Comments) != 0) else update_always:
            s_2: Array[Comment]
            origin_2: Array[Comment] = this.Comments
            next_1_2: Array[Comment] = assay.Comments
            if not append_sequences_1:
                def f_2(x_6: Comment) -> Comment:
                    return x_6

                s_2 = ResizeArray_map(f_2, next_1_2)

            else: 
                combined_2: Array[Comment] = []
                enumerator_3: Any = get_enumerator(origin_2)
                try: 
                    while enumerator_3.System_Collections_IEnumerator_MoveNext():
                        e_3: Comment = enumerator_3.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr932:
                            @property
                            def Equals(self) -> Callable[[Comment, Comment], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[Comment], int]:
                                return safe_hash

                        if not contains_1(e_3, combined_2, ObjectExpr932()):
                            (combined_2.append(e_3))


                finally: 
                    dispose(enumerator_3)

                enumerator_1_2: Any = get_enumerator(next_1_2)
                try: 
                    while enumerator_1_2.System_Collections_IEnumerator_MoveNext():
                        e_1_2: Comment = enumerator_1_2.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr933:
                            @property
                            def Equals(self) -> Callable[[Comment, Comment], bool]:
                                return equals

                            @property
                            def GetHashCode(self) -> Callable[[Comment], int]:
                                return safe_hash

                        if not contains_1(e_1_2, combined_2, ObjectExpr933()):
                            (combined_2.append(e_1_2))


                finally: 
                    dispose(enumerator_1_2)

                s_2 = combined_2

            this.Comments = s_2


    def __str__(self, __unit: None=None) -> str:
        this: ArcAssay = self
        arg: str = this.Identifier
        arg_1: OntologyAnnotation | None = this.MeasurementType
        arg_2: OntologyAnnotation | None = this.TechnologyType
        arg_3: OntologyAnnotation | None = this.TechnologyPlatform
        arg_4: Array[ArcTable] = this.Tables
        arg_5: Array[Person] = this.Performers
        arg_6: Array[Comment] = this.Comments
        return to_text(printf("ArcAssay({\r\n    Identifier = \"%s\",\r\n    MeasurementType = %A,\r\n    TechnologyType = %A,\r\n    TechnologyPlatform = %A,\r\n    Tables = %A,\r\n    Performers = %A,\r\n    Comments = %A\r\n})"))(arg)(arg_1)(arg_2)(arg_3)(arg_4)(arg_5)(arg_6)

    def AddToInvestigation(self, investigation: ArcInvestigation) -> None:
        this: ArcAssay = self
        this.Investigation = investigation

    def RemoveFromInvestigation(self, __unit: None=None) -> None:
        this: ArcAssay = self
        this.Investigation = None

    def UpdateReferenceByAssayFile(self, assay: ArcAssay, only_replace_existing: bool | None=None) -> None:
        this: ArcAssay = self
        update_always: bool = not default_arg(only_replace_existing, False)
        if True if (assay.MeasurementType is not None) else update_always:
            this.MeasurementType = assay.MeasurementType

        if True if (assay.TechnologyPlatform is not None) else update_always:
            this.TechnologyPlatform = assay.TechnologyPlatform

        if True if (assay.TechnologyType is not None) else update_always:
            this.TechnologyType = assay.TechnologyType

        if True if (len(assay.Tables) != 0) else update_always:
            this.Tables = assay.Tables

        if True if (len(assay.Comments) != 0) else update_always:
            this.Comments = assay.Comments

        this.DataMap = assay.DataMap
        if True if (len(assay.Performers) != 0) else update_always:
            this.Performers = assay.Performers


    def StructurallyEquals(self, other: ArcAssay) -> bool:
        this: ArcAssay = self
        def predicate(x: bool) -> bool:
            return x == True

        def _arrow936(__unit: None=None) -> bool:
            a: IEnumerable_1[ArcTable] = this.Tables
            b: IEnumerable_1[ArcTable] = other.Tables
            def folder(acc: bool, e: bool) -> bool:
                if acc:
                    return e

                else: 
                    return False


            def _arrow935(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow934(i_1: int) -> bool:
                    return equals(item(i_1, a), item(i_1, b))

                return map_1(_arrow934, range_big_int(0, 1, length(a) - 1))

            return fold(folder, True, to_list(delay(_arrow935))) if (length(a) == length(b)) else False

        def _arrow939(__unit: None=None) -> bool:
            a_1: IEnumerable_1[Person] = this.Performers
            b_1: IEnumerable_1[Person] = other.Performers
            def folder_1(acc_1: bool, e_1: bool) -> bool:
                if acc_1:
                    return e_1

                else: 
                    return False


            def _arrow938(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow937(i_2: int) -> bool:
                    return equals(item(i_2, a_1), item(i_2, b_1))

                return map_1(_arrow937, range_big_int(0, 1, length(a_1) - 1))

            return fold(folder_1, True, to_list(delay(_arrow938))) if (length(a_1) == length(b_1)) else False

        def _arrow942(__unit: None=None) -> bool:
            a_2: IEnumerable_1[Comment] = this.Comments
            b_2: IEnumerable_1[Comment] = other.Comments
            def folder_2(acc_2: bool, e_2: bool) -> bool:
                if acc_2:
                    return e_2

                else: 
                    return False


            def _arrow941(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow940(i_3: int) -> bool:
                    return equals(item(i_3, a_2), item(i_3, b_2))

                return map_1(_arrow940, range_big_int(0, 1, length(a_2) - 1))

            return fold(folder_2, True, to_list(delay(_arrow941))) if (length(a_2) == length(b_2)) else False

        return for_all(predicate, to_enumerable([this.Identifier == other.Identifier, equals(this.MeasurementType, other.MeasurementType), equals(this.TechnologyType, other.TechnologyType), equals(this.TechnologyPlatform, other.TechnologyPlatform), equals(this.DataMap, other.DataMap), _arrow936(), _arrow939(), _arrow942()]))

    def ReferenceEquals(self, other: ArcAssay) -> bool:
        this: ArcAssay = self
        return this is other

    def __eq__(self, other: Any=None) -> bool:
        this: ArcAssay = self
        return this.StructurallyEquals(other) if isinstance(other, ArcAssay) else False

    def GetLightHashCode(self, __unit: None=None) -> Any:
        this: ArcAssay = self
        return box_hash_array([this.Identifier, box_hash_option(this.MeasurementType), box_hash_option(this.TechnologyType), box_hash_option(this.TechnologyPlatform), box_hash_seq(this.Tables), box_hash_seq(this.Performers), box_hash_seq(this.Comments)])

    def __hash__(self, __unit: None=None) -> Any:
        this: ArcAssay = self
        return box_hash_array([this.Identifier, box_hash_option(this.MeasurementType), box_hash_option(this.TechnologyType), box_hash_option(this.TechnologyPlatform), box_hash_option(this.DataMap), box_hash_seq(this.Tables), box_hash_seq(this.Performers), box_hash_seq(this.Comments)])


ArcAssay_reflection = _expr944

def ArcAssay__ctor_Z4900C8CC(identifier: str, measurement_type: OntologyAnnotation | None=None, technology_type: OntologyAnnotation | None=None, technology_platform: OntologyAnnotation | None=None, tables: Array[ArcTable] | None=None, datamap: DataMap | None=None, performers: Array[Person] | None=None, comments: Array[Comment] | None=None) -> ArcAssay:
    return ArcAssay(identifier, measurement_type, technology_type, technology_platform, tables, datamap, performers, comments)


def _expr1009() -> TypeInfo:
    return class_type("ARCtrl.ArcStudy", None, ArcStudy, ArcTables_reflection())


class ArcStudy(ArcTables):
    def __init__(self, identifier: str, title: str | None=None, description: str | None=None, submission_date: str | None=None, public_release_date: str | None=None, publications: Array[Publication] | None=None, contacts: Array[Person] | None=None, study_design_descriptors: Array[OntologyAnnotation] | None=None, tables: Array[ArcTable] | None=None, datamap: DataMap | None=None, registered_assay_identifiers: Array[str] | None=None, comments: Array[Comment] | None=None) -> None:
        super().__init__(default_arg(tables, []))
        publications_1: Array[Publication] = default_arg(publications, [])
        contacts_1: Array[Person] = default_arg(contacts, [])
        study_design_descriptors_1: Array[OntologyAnnotation] = default_arg(study_design_descriptors, [])
        registered_assay_identifiers_1: Array[str] = default_arg(registered_assay_identifiers, [])
        comments_1: Array[Comment] = default_arg(comments, [])
        def _arrow1008(__unit: None=None) -> str:
            identifier_1: str = identifier.strip()
            check_valid_characters(identifier_1)
            return identifier_1

        self.identifier_0040533: str = _arrow1008()
        self.investigation: ArcInvestigation | None = None
        self.title_0040538: str | None = title
        self.description_0040539: str | None = description
        self.submission_date_0040540: str | None = submission_date
        self.public_release_date_0040541: str | None = public_release_date
        self.publications_0040542_002D1: Array[Publication] = publications_1
        self.contacts_0040543_002D1: Array[Person] = contacts_1
        self.study_design_descriptors_0040544_002D1: Array[OntologyAnnotation] = study_design_descriptors_1
        self.datamap_0040545: DataMap | None = datamap
        self.registered_assay_identifiers_0040546_002D1: Array[str] = registered_assay_identifiers_1
        self.comments_0040547_002D1: Array[Comment] = comments_1
        self.static_hash: int = 0

    @property
    def Identifier(self, __unit: None=None) -> str:
        this: ArcStudy = self
        return this.identifier_0040533

    @Identifier.setter
    def Identifier(self, i: str) -> None:
        this: ArcStudy = self
        this.identifier_0040533 = i

    @property
    def Investigation(self, __unit: None=None) -> ArcInvestigation | None:
        this: ArcStudy = self
        return this.investigation

    @Investigation.setter
    def Investigation(self, i: ArcInvestigation | None=None) -> None:
        this: ArcStudy = self
        this.investigation = i

    @property
    def Title(self, __unit: None=None) -> str | None:
        this: ArcStudy = self
        return this.title_0040538

    @Title.setter
    def Title(self, n: str | None=None) -> None:
        this: ArcStudy = self
        this.title_0040538 = n

    @property
    def Description(self, __unit: None=None) -> str | None:
        this: ArcStudy = self
        return this.description_0040539

    @Description.setter
    def Description(self, n: str | None=None) -> None:
        this: ArcStudy = self
        this.description_0040539 = n

    @property
    def SubmissionDate(self, __unit: None=None) -> str | None:
        this: ArcStudy = self
        return this.submission_date_0040540

    @SubmissionDate.setter
    def SubmissionDate(self, n: str | None=None) -> None:
        this: ArcStudy = self
        this.submission_date_0040540 = n

    @property
    def PublicReleaseDate(self, __unit: None=None) -> str | None:
        this: ArcStudy = self
        return this.public_release_date_0040541

    @PublicReleaseDate.setter
    def PublicReleaseDate(self, n: str | None=None) -> None:
        this: ArcStudy = self
        this.public_release_date_0040541 = n

    @property
    def Publications(self, __unit: None=None) -> Array[Publication]:
        this: ArcStudy = self
        return this.publications_0040542_002D1

    @Publications.setter
    def Publications(self, n: Array[Publication]) -> None:
        this: ArcStudy = self
        this.publications_0040542_002D1 = n

    @property
    def Contacts(self, __unit: None=None) -> Array[Person]:
        this: ArcStudy = self
        return this.contacts_0040543_002D1

    @Contacts.setter
    def Contacts(self, n: Array[Person]) -> None:
        this: ArcStudy = self
        this.contacts_0040543_002D1 = n

    @property
    def StudyDesignDescriptors(self, __unit: None=None) -> Array[OntologyAnnotation]:
        this: ArcStudy = self
        return this.study_design_descriptors_0040544_002D1

    @StudyDesignDescriptors.setter
    def StudyDesignDescriptors(self, n: Array[OntologyAnnotation]) -> None:
        this: ArcStudy = self
        this.study_design_descriptors_0040544_002D1 = n

    @property
    def DataMap(self, __unit: None=None) -> DataMap | None:
        this: ArcStudy = self
        return this.datamap_0040545

    @DataMap.setter
    def DataMap(self, n: DataMap | None=None) -> None:
        this: ArcStudy = self
        this.datamap_0040545 = n

    @property
    def RegisteredAssayIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcStudy = self
        return this.registered_assay_identifiers_0040546_002D1

    @RegisteredAssayIdentifiers.setter
    def RegisteredAssayIdentifiers(self, n: Array[str]) -> None:
        this: ArcStudy = self
        this.registered_assay_identifiers_0040546_002D1 = n

    @property
    def Comments(self, __unit: None=None) -> Array[Comment]:
        this: ArcStudy = self
        return this.comments_0040547_002D1

    @Comments.setter
    def Comments(self, n: Array[Comment]) -> None:
        this: ArcStudy = self
        this.comments_0040547_002D1 = n

    @property
    def StaticHash(self, __unit: None=None) -> int:
        this: ArcStudy = self
        return this.static_hash

    @StaticHash.setter
    def StaticHash(self, h: int) -> None:
        this: ArcStudy = self
        this.static_hash = h or 0

    @staticmethod
    def init(identifier: str) -> ArcStudy:
        return ArcStudy(identifier)

    @staticmethod
    def create(identifier: str, title: str | None=None, description: str | None=None, submission_date: str | None=None, public_release_date: str | None=None, publications: Array[Publication] | None=None, contacts: Array[Person] | None=None, study_design_descriptors: Array[OntologyAnnotation] | None=None, tables: Array[ArcTable] | None=None, datamap: DataMap | None=None, registered_assay_identifiers: Array[str] | None=None, comments: Array[Comment] | None=None) -> ArcStudy:
        return ArcStudy(identifier, title, description, submission_date, public_release_date, publications, contacts, study_design_descriptors, tables, datamap, registered_assay_identifiers, comments)

    @staticmethod
    def make(identifier: str, title: str | None, description: str | None, submission_date: str | None, public_release_date: str | None, publications: Array[Publication], contacts: Array[Person], study_design_descriptors: Array[OntologyAnnotation], tables: Array[ArcTable], datamap: DataMap | None, registered_assay_identifiers: Array[str], comments: Array[Comment]) -> ArcStudy:
        return ArcStudy(identifier, title, description, submission_date, public_release_date, publications, contacts, study_design_descriptors, tables, datamap, registered_assay_identifiers, comments)

    @property
    def is_empty(self, __unit: None=None) -> bool:
        this: ArcStudy = self
        return (len(this.Comments) == 0) if ((len(this.RegisteredAssayIdentifiers) == 0) if ((len(this.Tables) == 0) if ((len(this.StudyDesignDescriptors) == 0) if ((len(this.Contacts) == 0) if ((len(this.Publications) == 0) if (equals(this.PublicReleaseDate, None) if (equals(this.SubmissionDate, None) if (equals(this.Description, None) if equals(this.Title, None) else False) else False) else False) else False) else False) else False) else False) else False) else False

    @staticmethod
    def FileName() -> str:
        return "isa.study.xlsx"

    @property
    def RegisteredAssayIdentifierCount(self, __unit: None=None) -> int:
        this: ArcStudy = self
        return len(this.RegisteredAssayIdentifiers)

    @property
    def RegisteredAssayCount(self, __unit: None=None) -> int:
        this: ArcStudy = self
        return len(this.RegisteredAssays)

    @property
    def RegisteredAssays(self, __unit: None=None) -> Array[ArcAssay]:
        this: ArcStudy = self
        inv: ArcInvestigation
        investigation: ArcInvestigation | None = this.Investigation
        if investigation is not None:
            inv = investigation

        else: 
            raise Exception("Cannot execute this function. Object is not part of ArcInvestigation.")

        def chooser(assay_identifier: str) -> ArcAssay | None:
            return inv.TryGetAssay(assay_identifier)

        return list(choose(chooser, this.RegisteredAssayIdentifiers))

    @property
    def VacantAssayIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcStudy = self
        inv: ArcInvestigation
        investigation: ArcInvestigation | None = this.Investigation
        if investigation is not None:
            inv = investigation

        else: 
            raise Exception("Cannot execute this function. Object is not part of ArcInvestigation.")

        def predicate(arg: str) -> bool:
            return not inv.ContainsAssay(arg)

        return list(filter(predicate, this.RegisteredAssayIdentifiers))

    def AddRegisteredAssay(self, assay: ArcAssay) -> None:
        this: ArcStudy = self
        inv: ArcInvestigation
        investigation: ArcInvestigation | None = this.Investigation
        if investigation is not None:
            inv = investigation

        else: 
            raise Exception("Cannot execute this function. Object is not part of ArcInvestigation.")

        inv.AddAssay(assay)
        inv.RegisterAssay(this.Identifier, assay.Identifier)

    @staticmethod
    def add_registered_assay(assay: ArcAssay) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow945(study: ArcStudy) -> ArcStudy:
            new_study: ArcStudy = study.Copy()
            new_study.AddRegisteredAssay(assay)
            return new_study

        return _arrow945

    def InitRegisteredAssay(self, assay_identifier: str) -> ArcAssay:
        this: ArcStudy = self
        assay: ArcAssay = ArcAssay(assay_identifier)
        this.AddRegisteredAssay(assay)
        return assay

    @staticmethod
    def init_registered_assay(assay_identifier: str) -> Callable[[ArcStudy], tuple[ArcStudy, ArcAssay]]:
        def _arrow946(study: ArcStudy) -> tuple[ArcStudy, ArcAssay]:
            copy: ArcStudy = study.Copy()
            return (copy, copy.InitRegisteredAssay(assay_identifier))

        return _arrow946

    def RegisterAssay(self, assay_identifier: str) -> None:
        this: ArcStudy = self
        class ObjectExpr948:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow947(x: str, y: str) -> bool:
                    return x == y

                return _arrow947

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if contains(assay_identifier, this.RegisteredAssayIdentifiers, ObjectExpr948()):
            raise Exception(("Assay `" + assay_identifier) + "` is already registered on the study.")

        (this.RegisteredAssayIdentifiers.append(assay_identifier))

    @staticmethod
    def register_assay(assay_identifier: str) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow949(study: ArcStudy) -> ArcStudy:
            copy: ArcStudy = study.Copy()
            copy.RegisterAssay(assay_identifier)
            return copy

        return _arrow949

    def DeregisterAssay(self, assay_identifier: str) -> None:
        this: ArcStudy = self
        class ObjectExpr951:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow950(x: str, y: str) -> bool:
                    return x == y

                return _arrow950

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        ignore(remove_in_place(assay_identifier, this.RegisteredAssayIdentifiers, ObjectExpr951()))

    @staticmethod
    def deregister_assay(assay_identifier: str) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow952(study: ArcStudy) -> ArcStudy:
            copy: ArcStudy = study.Copy()
            copy.DeregisterAssay(assay_identifier)
            return copy

        return _arrow952

    def GetRegisteredAssay(self, assay_identifier: str) -> ArcAssay:
        this: ArcStudy = self
        class ObjectExpr954:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow953(x: str, y: str) -> bool:
                    return x == y

                return _arrow953

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if not contains(assay_identifier, this.RegisteredAssayIdentifiers, ObjectExpr954()):
            raise Exception(("Assay `" + assay_identifier) + "` is not registered on the study.")

        inv: ArcInvestigation
        investigation: ArcInvestigation | None = this.Investigation
        if investigation is not None:
            inv = investigation

        else: 
            raise Exception("Cannot execute this function. Object is not part of ArcInvestigation.")

        return inv.GetAssay(assay_identifier)

    @staticmethod
    def get_registered_assay(assay_identifier: str) -> Callable[[ArcStudy], ArcAssay]:
        def _arrow955(study: ArcStudy) -> ArcAssay:
            copy: ArcStudy = study.Copy()
            return copy.GetRegisteredAssay(assay_identifier)

        return _arrow955

    @staticmethod
    def get_registered_assays(__unit: None=None) -> Callable[[ArcStudy], Array[ArcAssay]]:
        def _arrow956(study: ArcStudy) -> Array[ArcAssay]:
            copy: ArcStudy = study.Copy()
            return copy.RegisteredAssays

        return _arrow956

    def GetRegisteredAssaysOrIdentifier(self, __unit: None=None) -> Array[ArcAssay]:
        this: ArcStudy = self
        match_value: ArcInvestigation | None = this.Investigation
        if match_value is None:
            def f_1(identifier_1: str) -> ArcAssay:
                return ArcAssay.init(identifier_1)

            return ResizeArray_map(f_1, this.RegisteredAssayIdentifiers)

        else: 
            i: ArcInvestigation = match_value
            def f(identifier: str) -> ArcAssay:
                match_value_1: ArcAssay | None = i.TryGetAssay(identifier)
                if match_value_1 is None:
                    return ArcAssay.init(identifier)

                else: 
                    return match_value_1


            return ResizeArray_map(f, this.RegisteredAssayIdentifiers)


    @staticmethod
    def get_registered_assays_or_identifier(__unit: None=None) -> Callable[[ArcStudy], Array[ArcAssay]]:
        def _arrow957(study: ArcStudy) -> Array[ArcAssay]:
            copy: ArcStudy = study.Copy()
            return copy.GetRegisteredAssaysOrIdentifier()

        return _arrow957

    @staticmethod
    def add_table(table: ArcTable, index: int | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow958(study: ArcStudy) -> ArcStudy:
            c: ArcStudy = study.Copy()
            c.AddTable(table, index)
            return c

        return _arrow958

    @staticmethod
    def add_tables(tables: IEnumerable_1[ArcTable], index: int | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow959(study: ArcStudy) -> ArcStudy:
            c: ArcStudy = study.Copy()
            c.AddTables(tables, index)
            return c

        return _arrow959

    @staticmethod
    def init_table(table_name: str, index: int | None=None) -> Callable[[ArcStudy], tuple[ArcStudy, ArcTable]]:
        def _arrow960(study: ArcStudy) -> tuple[ArcStudy, ArcTable]:
            c: ArcStudy = study.Copy()
            return (c, c.InitTable(table_name, index))

        return _arrow960

    @staticmethod
    def init_tables(table_names: IEnumerable_1[str], index: int | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow961(study: ArcStudy) -> ArcStudy:
            c: ArcStudy = study.Copy()
            c.InitTables(table_names, index)
            return c

        return _arrow961

    @staticmethod
    def get_table_at(index: int) -> Callable[[ArcStudy], ArcTable]:
        def _arrow962(study: ArcStudy) -> ArcTable:
            new_assay: ArcStudy = study.Copy()
            return new_assay.GetTableAt(index)

        return _arrow962

    @staticmethod
    def get_table(name: str) -> Callable[[ArcStudy], ArcTable]:
        def _arrow963(study: ArcStudy) -> ArcTable:
            new_assay: ArcStudy = study.Copy()
            return new_assay.GetTable(name)

        return _arrow963

    @staticmethod
    def update_table_at(index: int, table: ArcTable) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow964(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.UpdateTableAt(index, table)
            return new_assay

        return _arrow964

    @staticmethod
    def update_table(name: str, table: ArcTable) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow965(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.UpdateTable(name, table)
            return new_assay

        return _arrow965

    @staticmethod
    def set_table_at(index: int, table: ArcTable) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow966(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.SetTableAt(index, table)
            return new_assay

        return _arrow966

    @staticmethod
    def set_table(name: str, table: ArcTable) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow967(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.SetTable(name, table)
            return new_assay

        return _arrow967

    @staticmethod
    def remove_table_at(index: int) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow968(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.RemoveTableAt(index)
            return new_assay

        return _arrow968

    @staticmethod
    def remove_table(name: str) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow969(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.RemoveTable(name)
            return new_assay

        return _arrow969

    @staticmethod
    def map_table_at(index: int, update_fun: Callable[[ArcTable], None]) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow970(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.MapTableAt(index, update_fun)
            return new_assay

        return _arrow970

    @staticmethod
    def map_table(name: str, update_fun: Callable[[ArcTable], None]) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow971(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.MapTable(name, update_fun)
            return new_assay

        return _arrow971

    @staticmethod
    def rename_table_at(index: int, new_name: str) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow972(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.RenameTableAt(index, new_name)
            return new_assay

        return _arrow972

    @staticmethod
    def rename_table(name: str, new_name: str) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow973(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.RenameTable(name, new_name)
            return new_assay

        return _arrow973

    @staticmethod
    def add_column_at(table_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None, column_index: int | None=None, force_replace: bool | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow974(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.AddColumnAt(table_index, header, cells, column_index, force_replace)
            return new_assay

        return _arrow974

    @staticmethod
    def add_column(table_name: str, header: CompositeHeader, cells: Array[CompositeCell] | None=None, column_index: int | None=None, force_replace: bool | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow975(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.AddColumn(table_name, header, cells, column_index, force_replace)
            return new_assay

        return _arrow975

    @staticmethod
    def remove_column_at(table_index: int, column_index: int) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow976(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.RemoveColumnAt(table_index, column_index)
            return new_assay

        return _arrow976

    @staticmethod
    def remove_column(table_name: str, column_index: int) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow977(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.RemoveColumn(table_name, column_index)
            return new_assay

        return _arrow977

    @staticmethod
    def update_column_at(table_index: int, column_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow978(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.UpdateColumnAt(table_index, column_index, header, cells)
            return new_assay

        return _arrow978

    @staticmethod
    def update_column(table_name: str, column_index: int, header: CompositeHeader, cells: Array[CompositeCell] | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow979(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.UpdateColumn(table_name, column_index, header, cells)
            return new_assay

        return _arrow979

    @staticmethod
    def get_column_at(table_index: int, column_index: int) -> Callable[[ArcStudy], CompositeColumn]:
        def _arrow980(study: ArcStudy) -> CompositeColumn:
            new_assay: ArcStudy = study.Copy()
            return new_assay.GetColumnAt(table_index, column_index)

        return _arrow980

    @staticmethod
    def get_column(table_name: str, column_index: int) -> Callable[[ArcStudy], CompositeColumn]:
        def _arrow981(study: ArcStudy) -> CompositeColumn:
            new_assay: ArcStudy = study.Copy()
            return new_assay.GetColumn(table_name, column_index)

        return _arrow981

    @staticmethod
    def add_row_at(table_index: int, cells: Array[CompositeCell] | None=None, row_index: int | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow982(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.AddRowAt(table_index, cells, row_index)
            return new_assay

        return _arrow982

    @staticmethod
    def add_row(table_name: str, cells: Array[CompositeCell] | None=None, row_index: int | None=None) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow983(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.AddRow(table_name, cells, row_index)
            return new_assay

        return _arrow983

    @staticmethod
    def remove_row_at(table_index: int, row_index: int) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow984(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.RemoveColumnAt(table_index, row_index)
            return new_assay

        return _arrow984

    @staticmethod
    def remove_row(table_name: str, row_index: int) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow985(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.RemoveRow(table_name, row_index)
            return new_assay

        return _arrow985

    @staticmethod
    def update_row_at(table_index: int, row_index: int, cells: Array[CompositeCell]) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow986(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.UpdateRowAt(table_index, row_index, cells)
            return new_assay

        return _arrow986

    @staticmethod
    def update_row(table_name: str, row_index: int, cells: Array[CompositeCell]) -> Callable[[ArcStudy], ArcStudy]:
        def _arrow987(study: ArcStudy) -> ArcStudy:
            new_assay: ArcStudy = study.Copy()
            new_assay.UpdateRow(table_name, row_index, cells)
            return new_assay

        return _arrow987

    @staticmethod
    def get_row_at(table_index: int, row_index: int) -> Callable[[ArcStudy], Array[CompositeCell]]:
        def _arrow988(study: ArcStudy) -> Array[CompositeCell]:
            new_assay: ArcStudy = study.Copy()
            return new_assay.GetRowAt(table_index, row_index)

        return _arrow988

    @staticmethod
    def get_row(table_name: str, row_index: int) -> Callable[[ArcStudy], Array[CompositeCell]]:
        def _arrow989(study: ArcStudy) -> Array[CompositeCell]:
            new_assay: ArcStudy = study.Copy()
            return new_assay.GetRow(table_name, row_index)

        return _arrow989

    def AddToInvestigation(self, investigation: ArcInvestigation) -> None:
        this: ArcStudy = self
        this.Investigation = investigation

    def RemoveFromInvestigation(self, __unit: None=None) -> None:
        this: ArcStudy = self
        this.Investigation = None

    def Copy(self, copy_investigation_ref: bool | None=None) -> ArcStudy:
        this: ArcStudy = self
        copy_investigation_ref_1: bool = default_arg(copy_investigation_ref, False)
        next_tables: Array[ArcTable] = []
        next_assay_identifiers: Array[str] = list(this.RegisteredAssayIdentifiers)
        enumerator: Any = get_enumerator(this.Tables)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                table: ArcTable = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                copy: ArcTable = table.Copy()
                (next_tables.append(copy))

        finally: 
            dispose(enumerator)

        def f(c: Comment) -> Comment:
            return c.Copy()

        next_comments: Array[Comment] = ResizeArray_map(f, this.Comments)
        def f_1(c_1: Person) -> Person:
            return c_1.Copy()

        next_contacts: Array[Person] = ResizeArray_map(f_1, this.Contacts)
        def f_2(c_2: Publication) -> Publication:
            return c_2.Copy()

        next_publications: Array[Publication] = ResizeArray_map(f_2, this.Publications)
        def f_3(c_3: OntologyAnnotation) -> OntologyAnnotation:
            return c_3.Copy()

        next_study_design_descriptors: Array[OntologyAnnotation] = ResizeArray_map(f_3, this.StudyDesignDescriptors)
        next_data_map: DataMap | None = map(DataMap__Copy, this.DataMap)
        study: ArcStudy
        identifier: str = this.Identifier
        title: str | None = this.Title
        description: str | None = this.Description
        submission_date: str | None = this.SubmissionDate
        public_release_date: str | None = this.PublicReleaseDate
        study = ArcStudy.make(identifier, title, description, submission_date, public_release_date, next_publications, next_contacts, next_study_design_descriptors, next_tables, next_data_map, next_assay_identifiers, next_comments)
        if copy_investigation_ref_1:
            study.Investigation = this.Investigation

        return study

    def UpdateReferenceByStudyFile(self, study: ArcStudy, only_replace_existing: bool | None=None, keep_unused_ref_tables: bool | None=None) -> None:
        this: ArcStudy = self
        update_always: bool = not default_arg(only_replace_existing, False)
        if True if (study.Title is not None) else update_always:
            this.Title = study.Title

        if True if (study.Description is not None) else update_always:
            this.Description = study.Description

        if True if (study.SubmissionDate is not None) else update_always:
            this.SubmissionDate = study.SubmissionDate

        if True if (study.PublicReleaseDate is not None) else update_always:
            this.PublicReleaseDate = study.PublicReleaseDate

        if True if (len(study.Publications) != 0) else update_always:
            this.Publications = study.Publications

        if True if (len(study.Contacts) != 0) else update_always:
            this.Contacts = study.Contacts

        if True if (len(study.StudyDesignDescriptors) != 0) else update_always:
            this.StudyDesignDescriptors = study.StudyDesignDescriptors

        if True if (len(study.Tables) != 0) else update_always:
            tables: ArcTables = ArcTables.update_reference_tables_by_sheets(ArcTables(this.Tables), ArcTables(study.Tables), keep_unused_ref_tables)
            this.Tables = tables.Tables

        this.DataMap = study.DataMap
        if True if (len(study.RegisteredAssayIdentifiers) != 0) else update_always:
            this.RegisteredAssayIdentifiers = study.RegisteredAssayIdentifiers

        if True if (len(study.Comments) != 0) else update_always:
            this.Comments = study.Comments


    def StructurallyEquals(self, other: ArcStudy) -> bool:
        this: ArcStudy = self
        def predicate(x: bool) -> bool:
            return x == True

        def _arrow992(__unit: None=None) -> bool:
            a: IEnumerable_1[Publication] = this.Publications
            b: IEnumerable_1[Publication] = other.Publications
            def folder(acc: bool, e: bool) -> bool:
                if acc:
                    return e

                else: 
                    return False


            def _arrow991(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow990(i_1: int) -> bool:
                    return equals(item(i_1, a), item(i_1, b))

                return map_1(_arrow990, range_big_int(0, 1, length(a) - 1))

            return fold(folder, True, to_list(delay(_arrow991))) if (length(a) == length(b)) else False

        def _arrow995(__unit: None=None) -> bool:
            a_1: IEnumerable_1[Person] = this.Contacts
            b_1: IEnumerable_1[Person] = other.Contacts
            def folder_1(acc_1: bool, e_1: bool) -> bool:
                if acc_1:
                    return e_1

                else: 
                    return False


            def _arrow994(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow993(i_2: int) -> bool:
                    return equals(item(i_2, a_1), item(i_2, b_1))

                return map_1(_arrow993, range_big_int(0, 1, length(a_1) - 1))

            return fold(folder_1, True, to_list(delay(_arrow994))) if (length(a_1) == length(b_1)) else False

        def _arrow998(__unit: None=None) -> bool:
            a_2: IEnumerable_1[OntologyAnnotation] = this.StudyDesignDescriptors
            b_2: IEnumerable_1[OntologyAnnotation] = other.StudyDesignDescriptors
            def folder_2(acc_2: bool, e_2: bool) -> bool:
                if acc_2:
                    return e_2

                else: 
                    return False


            def _arrow997(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow996(i_3: int) -> bool:
                    return equals(item(i_3, a_2), item(i_3, b_2))

                return map_1(_arrow996, range_big_int(0, 1, length(a_2) - 1))

            return fold(folder_2, True, to_list(delay(_arrow997))) if (length(a_2) == length(b_2)) else False

        def _arrow1001(__unit: None=None) -> bool:
            a_3: IEnumerable_1[ArcTable] = this.Tables
            b_3: IEnumerable_1[ArcTable] = other.Tables
            def folder_3(acc_3: bool, e_3: bool) -> bool:
                if acc_3:
                    return e_3

                else: 
                    return False


            def _arrow1000(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow999(i_4: int) -> bool:
                    return equals(item(i_4, a_3), item(i_4, b_3))

                return map_1(_arrow999, range_big_int(0, 1, length(a_3) - 1))

            return fold(folder_3, True, to_list(delay(_arrow1000))) if (length(a_3) == length(b_3)) else False

        def _arrow1004(__unit: None=None) -> bool:
            a_4: IEnumerable_1[str] = this.RegisteredAssayIdentifiers
            b_4: IEnumerable_1[str] = other.RegisteredAssayIdentifiers
            def folder_4(acc_4: bool, e_4: bool) -> bool:
                if acc_4:
                    return e_4

                else: 
                    return False


            def _arrow1003(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1002(i_5: int) -> bool:
                    return item(i_5, a_4) == item(i_5, b_4)

                return map_1(_arrow1002, range_big_int(0, 1, length(a_4) - 1))

            return fold(folder_4, True, to_list(delay(_arrow1003))) if (length(a_4) == length(b_4)) else False

        def _arrow1007(__unit: None=None) -> bool:
            a_5: IEnumerable_1[Comment] = this.Comments
            b_5: IEnumerable_1[Comment] = other.Comments
            def folder_5(acc_5: bool, e_5: bool) -> bool:
                if acc_5:
                    return e_5

                else: 
                    return False


            def _arrow1006(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1005(i_6: int) -> bool:
                    return equals(item(i_6, a_5), item(i_6, b_5))

                return map_1(_arrow1005, range_big_int(0, 1, length(a_5) - 1))

            return fold(folder_5, True, to_list(delay(_arrow1006))) if (length(a_5) == length(b_5)) else False

        return for_all(predicate, to_enumerable([this.Identifier == other.Identifier, equals(this.Title, other.Title), equals(this.Description, other.Description), equals(this.SubmissionDate, other.SubmissionDate), equals(this.PublicReleaseDate, other.PublicReleaseDate), equals(this.DataMap, other.DataMap), _arrow992(), _arrow995(), _arrow998(), _arrow1001(), _arrow1004(), _arrow1007()]))

    def ReferenceEquals(self, other: ArcStudy) -> bool:
        this: ArcStudy = self
        return this is other

    def __str__(self, __unit: None=None) -> str:
        this: ArcStudy = self
        arg: str = this.Identifier
        arg_1: str | None = this.Title
        arg_2: str | None = this.Description
        arg_3: str | None = this.SubmissionDate
        arg_4: str | None = this.PublicReleaseDate
        arg_5: Array[Publication] = this.Publications
        arg_6: Array[Person] = this.Contacts
        arg_7: Array[OntologyAnnotation] = this.StudyDesignDescriptors
        arg_8: Array[ArcTable] = this.Tables
        arg_9: Array[str] = this.RegisteredAssayIdentifiers
        arg_10: Array[Comment] = this.Comments
        return to_text(printf("ArcStudy {\r\n    Identifier = %A,\r\n    Title = %A,\r\n    Description = %A,\r\n    SubmissionDate = %A,\r\n    PublicReleaseDate = %A,\r\n    Publications = %A,\r\n    Contacts = %A,\r\n    StudyDesignDescriptors = %A,\r\n    Tables = %A,\r\n    RegisteredAssayIdentifiers = %A,\r\n    Comments = %A,\r\n}"))(arg)(arg_1)(arg_2)(arg_3)(arg_4)(arg_5)(arg_6)(arg_7)(arg_8)(arg_9)(arg_10)

    def __eq__(self, other: Any=None) -> bool:
        this: ArcStudy = self
        return this.StructurallyEquals(other) if isinstance(other, ArcStudy) else False

    def __hash__(self, __unit: None=None) -> Any:
        this: ArcStudy = self
        return box_hash_array([this.Identifier, box_hash_option(this.Title), box_hash_option(this.Description), box_hash_option(this.SubmissionDate), box_hash_option(this.PublicReleaseDate), box_hash_option(this.DataMap), box_hash_seq(this.Publications), box_hash_seq(this.Contacts), box_hash_seq(this.StudyDesignDescriptors), box_hash_seq(this.Tables), box_hash_seq(this.RegisteredAssayIdentifiers), box_hash_seq(this.Comments)])

    def GetLightHashCode(self, __unit: None=None) -> Any:
        this: ArcStudy = self
        return box_hash_array([this.Identifier, box_hash_option(this.Title), box_hash_option(this.Description), box_hash_option(this.SubmissionDate), box_hash_option(this.PublicReleaseDate), box_hash_seq(this.Publications), box_hash_seq(this.Contacts), box_hash_seq(this.StudyDesignDescriptors), box_hash_seq(this.Tables), box_hash_seq(this.RegisteredAssayIdentifiers), box_hash_seq(this.Comments)])


ArcStudy_reflection = _expr1009

def ArcStudy__ctor_64321D5B(identifier: str, title: str | None=None, description: str | None=None, submission_date: str | None=None, public_release_date: str | None=None, publications: Array[Publication] | None=None, contacts: Array[Person] | None=None, study_design_descriptors: Array[OntologyAnnotation] | None=None, tables: Array[ArcTable] | None=None, datamap: DataMap | None=None, registered_assay_identifiers: Array[str] | None=None, comments: Array[Comment] | None=None) -> ArcStudy:
    return ArcStudy(identifier, title, description, submission_date, public_release_date, publications, contacts, study_design_descriptors, tables, datamap, registered_assay_identifiers, comments)


def _expr1119() -> TypeInfo:
    return class_type("ARCtrl.ArcInvestigation", None, ArcInvestigation)


class ArcInvestigation:
    def __init__(self, identifier: str, title: str | None=None, description: str | None=None, submission_date: str | None=None, public_release_date: str | None=None, ontology_source_references: Array[OntologySourceReference] | None=None, publications: Array[Publication] | None=None, contacts: Array[Person] | None=None, assays: Array[ArcAssay] | None=None, studies: Array[ArcStudy] | None=None, registered_study_identifiers: Array[str] | None=None, comments: Array[Comment] | None=None, remarks: Array[Remark] | None=None) -> None:
        this: FSharpRef[ArcInvestigation] = FSharpRef(None)
        this.contents = self
        ontology_source_references_1: Array[OntologySourceReference] = default_arg(ontology_source_references, [])
        publications_1: Array[Publication] = default_arg(publications, [])
        contacts_1: Array[Person] = default_arg(contacts, [])
        assays_1: Array[ArcAssay]
        ass: Array[ArcAssay] = default_arg(assays, [])
        enumerator: Any = get_enumerator(ass)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                a: ArcAssay = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                a.Investigation = this.contents

        finally: 
            dispose(enumerator)

        assays_1 = ass
        studies_1: Array[ArcStudy]
        sss: Array[ArcStudy] = default_arg(studies, [])
        enumerator_1: Any = get_enumerator(sss)
        try: 
            while enumerator_1.System_Collections_IEnumerator_MoveNext():
                s: ArcStudy = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                s.Investigation = this.contents

        finally: 
            dispose(enumerator_1)

        studies_1 = sss
        registered_study_identifiers_1: Array[str] = default_arg(registered_study_identifiers, [])
        comments_1: Array[Comment] = default_arg(comments, [])
        remarks_1: Array[Remark] = default_arg(remarks, [])
        self.identifier_00401122: str = identifier
        self.title_00401123: str | None = title
        self.description_00401124: str | None = description
        self.submission_date_00401125: str | None = submission_date
        self.public_release_date_00401126: str | None = public_release_date
        self.ontology_source_references_00401127_002D1: Array[OntologySourceReference] = ontology_source_references_1
        self.publications_00401128_002D1: Array[Publication] = publications_1
        self.contacts_00401129_002D1: Array[Person] = contacts_1
        self.assays_00401130_002D1: Array[ArcAssay] = assays_1
        self.studies_00401131_002D1: Array[ArcStudy] = studies_1
        self.registered_study_identifiers_00401132_002D1: Array[str] = registered_study_identifiers_1
        self.comments_00401133_002D1: Array[Comment] = comments_1
        self.remarks_00401134_002D1: Array[Remark] = remarks_1
        self.static_hash: int = 0
        self.init_00401103: int = 1

    @property
    def Identifier(self, __unit: None=None) -> str:
        this: ArcInvestigation = self
        return this.identifier_00401122

    @Identifier.setter
    def Identifier(self, i: str) -> None:
        this: ArcInvestigation = self
        this.identifier_00401122 = i

    @property
    def Title(self, __unit: None=None) -> str | None:
        this: ArcInvestigation = self
        return this.title_00401123

    @Title.setter
    def Title(self, n: str | None=None) -> None:
        this: ArcInvestigation = self
        this.title_00401123 = n

    @property
    def Description(self, __unit: None=None) -> str | None:
        this: ArcInvestigation = self
        return this.description_00401124

    @Description.setter
    def Description(self, n: str | None=None) -> None:
        this: ArcInvestigation = self
        this.description_00401124 = n

    @property
    def SubmissionDate(self, __unit: None=None) -> str | None:
        this: ArcInvestigation = self
        return this.submission_date_00401125

    @SubmissionDate.setter
    def SubmissionDate(self, n: str | None=None) -> None:
        this: ArcInvestigation = self
        this.submission_date_00401125 = n

    @property
    def PublicReleaseDate(self, __unit: None=None) -> str | None:
        this: ArcInvestigation = self
        return this.public_release_date_00401126

    @PublicReleaseDate.setter
    def PublicReleaseDate(self, n: str | None=None) -> None:
        this: ArcInvestigation = self
        this.public_release_date_00401126 = n

    @property
    def OntologySourceReferences(self, __unit: None=None) -> Array[OntologySourceReference]:
        this: ArcInvestigation = self
        return this.ontology_source_references_00401127_002D1

    @OntologySourceReferences.setter
    def OntologySourceReferences(self, n: Array[OntologySourceReference]) -> None:
        this: ArcInvestigation = self
        this.ontology_source_references_00401127_002D1 = n

    @property
    def Publications(self, __unit: None=None) -> Array[Publication]:
        this: ArcInvestigation = self
        return this.publications_00401128_002D1

    @Publications.setter
    def Publications(self, n: Array[Publication]) -> None:
        this: ArcInvestigation = self
        this.publications_00401128_002D1 = n

    @property
    def Contacts(self, __unit: None=None) -> Array[Person]:
        this: ArcInvestigation = self
        return this.contacts_00401129_002D1

    @Contacts.setter
    def Contacts(self, n: Array[Person]) -> None:
        this: ArcInvestigation = self
        this.contacts_00401129_002D1 = n

    @property
    def Assays(self, __unit: None=None) -> Array[ArcAssay]:
        this: ArcInvestigation = self
        return this.assays_00401130_002D1

    @Assays.setter
    def Assays(self, n: Array[ArcAssay]) -> None:
        this: ArcInvestigation = self
        this.assays_00401130_002D1 = n

    @property
    def Studies(self, __unit: None=None) -> Array[ArcStudy]:
        this: ArcInvestigation = self
        return this.studies_00401131_002D1

    @Studies.setter
    def Studies(self, n: Array[ArcStudy]) -> None:
        this: ArcInvestigation = self
        this.studies_00401131_002D1 = n

    @property
    def RegisteredStudyIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcInvestigation = self
        return this.registered_study_identifiers_00401132_002D1

    @RegisteredStudyIdentifiers.setter
    def RegisteredStudyIdentifiers(self, n: Array[str]) -> None:
        this: ArcInvestigation = self
        this.registered_study_identifiers_00401132_002D1 = n

    @property
    def Comments(self, __unit: None=None) -> Array[Comment]:
        this: ArcInvestigation = self
        return this.comments_00401133_002D1

    @Comments.setter
    def Comments(self, n: Array[Comment]) -> None:
        this: ArcInvestigation = self
        this.comments_00401133_002D1 = n

    @property
    def Remarks(self, __unit: None=None) -> Array[Remark]:
        this: ArcInvestigation = self
        return this.remarks_00401134_002D1

    @Remarks.setter
    def Remarks(self, n: Array[Remark]) -> None:
        this: ArcInvestigation = self
        this.remarks_00401134_002D1 = n

    @property
    def StaticHash(self, __unit: None=None) -> int:
        this: ArcInvestigation = self
        return this.static_hash

    @StaticHash.setter
    def StaticHash(self, h: int) -> None:
        this: ArcInvestigation = self
        this.static_hash = h or 0

    @staticmethod
    def FileName() -> str:
        return "isa.investigation.xlsx"

    @staticmethod
    def init(identifier: str) -> ArcInvestigation:
        return ArcInvestigation(identifier)

    @staticmethod
    def create(identifier: str, title: str | None=None, description: str | None=None, submission_date: str | None=None, public_release_date: str | None=None, ontology_source_references: Array[OntologySourceReference] | None=None, publications: Array[Publication] | None=None, contacts: Array[Person] | None=None, assays: Array[ArcAssay] | None=None, studies: Array[ArcStudy] | None=None, registered_study_identifiers: Array[str] | None=None, comments: Array[Comment] | None=None, remarks: Array[Remark] | None=None) -> ArcInvestigation:
        return ArcInvestigation(identifier, title, description, submission_date, public_release_date, ontology_source_references, publications, contacts, assays, studies, registered_study_identifiers, comments, remarks)

    @staticmethod
    def make(identifier: str, title: str | None, description: str | None, submission_date: str | None, public_release_date: str | None, ontology_source_references: Array[OntologySourceReference], publications: Array[Publication], contacts: Array[Person], assays: Array[ArcAssay], studies: Array[ArcStudy], registered_study_identifiers: Array[str], comments: Array[Comment], remarks: Array[Remark]) -> ArcInvestigation:
        return ArcInvestigation(identifier, title, description, submission_date, public_release_date, ontology_source_references, publications, contacts, assays, studies, registered_study_identifiers, comments, remarks)

    @property
    def AssayCount(self, __unit: None=None) -> int:
        this: ArcInvestigation = self
        return len(this.Assays)

    @property
    def AssayIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcInvestigation = self
        def mapping(x: ArcAssay) -> str:
            return x.Identifier

        return list(map_1(mapping, this.Assays))

    @property
    def UnregisteredAssays(self, __unit: None=None) -> Array[ArcAssay]:
        this: ArcInvestigation = self
        def f(a: ArcAssay) -> bool:
            def predicate(s: ArcStudy, a: Any=a) -> bool:
                def _arrow1010(i: str, s: Any=s) -> bool:
                    return i == a.Identifier

                return exists(_arrow1010, s.RegisteredAssayIdentifiers)

            return not exists(predicate, this.RegisteredStudies)

        return ResizeArray_filter(f, this.Assays)

    def AddAssay(self, assay: ArcAssay, register_in: Array[ArcStudy] | None=None) -> None:
        this: ArcInvestigation = self
        assay_ident: str = assay.Identifier
        def predicate(x_1: str) -> bool:
            return x_1 == assay_ident

        def mapping(x: ArcAssay) -> str:
            return x.Identifier

        match_value: int | None = try_find_index(predicate, map_1(mapping, this.Assays))
        if match_value is None:
            pass

        else: 
            raise Exception(((("Cannot create assay with name " + assay_ident) + ", as assay names must be unique and assay at index ") + str(match_value)) + " has the same name.")

        assay.Investigation = this
        (this.Assays.append(assay))
        if register_in is not None:
            enumerator: Any = get_enumerator(value_4(register_in))
            try: 
                while enumerator.System_Collections_IEnumerator_MoveNext():
                    study: ArcStudy = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                    study.RegisterAssay(assay.Identifier)

            finally: 
                dispose(enumerator)



    @staticmethod
    def add_assay(assay: ArcAssay, register_in: Array[ArcStudy] | None=None) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1012(inv: ArcInvestigation) -> ArcInvestigation:
            new_investigation: ArcInvestigation = inv.Copy()
            new_investigation.AddAssay(assay, register_in)
            return new_investigation

        return _arrow1012

    def InitAssay(self, assay_identifier: str, register_in: Array[ArcStudy] | None=None) -> ArcAssay:
        this: ArcInvestigation = self
        assay: ArcAssay = ArcAssay(assay_identifier)
        this.AddAssay(assay, register_in)
        return assay

    @staticmethod
    def init_assay(assay_identifier: str, register_in: Array[ArcStudy] | None=None) -> Callable[[ArcInvestigation], ArcAssay]:
        def _arrow1014(inv: ArcInvestigation) -> ArcAssay:
            new_investigation: ArcInvestigation = inv.Copy()
            return new_investigation.InitAssay(assay_identifier, register_in)

        return _arrow1014

    def DeleteAssayAt(self, index: int) -> None:
        this: ArcInvestigation = self
        this.Assays.pop(index)

    @staticmethod
    def delete_assay_at(index: int) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1017(inv: ArcInvestigation) -> ArcInvestigation:
            new_investigation: ArcInvestigation = inv.Copy()
            new_investigation.DeleteAssayAt(index)
            return new_investigation

        return _arrow1017

    def DeleteAssay(self, assay_identifier: str) -> None:
        this: ArcInvestigation = self
        index: int = this.GetAssayIndex(assay_identifier) or 0
        this.DeleteAssayAt(index)

    @staticmethod
    def delete_assay(assay_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1018(inv: ArcInvestigation) -> ArcInvestigation:
            new_inv: ArcInvestigation = inv.Copy()
            new_inv.DeleteAssay(assay_identifier)
            return new_inv

        return _arrow1018

    def RemoveAssayAt(self, index: int) -> None:
        this: ArcInvestigation = self
        ident: str = this.GetAssayAt(index).Identifier
        this.Assays.pop(index)
        enumerator: Any = get_enumerator(this.Studies)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                study: ArcStudy = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                study.DeregisterAssay(ident)

        finally: 
            dispose(enumerator)


    @staticmethod
    def remove_assay_at(index: int) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1019(inv: ArcInvestigation) -> ArcInvestigation:
            new_investigation: ArcInvestigation = inv.Copy()
            new_investigation.RemoveAssayAt(index)
            return new_investigation

        return _arrow1019

    def RemoveAssay(self, assay_identifier: str) -> None:
        this: ArcInvestigation = self
        index: int = this.GetAssayIndex(assay_identifier) or 0
        this.RemoveAssayAt(index)

    @staticmethod
    def remove_assay(assay_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1021(inv: ArcInvestigation) -> ArcInvestigation:
            new_inv: ArcInvestigation = inv.Copy()
            new_inv.RemoveAssay(assay_identifier)
            return new_inv

        return _arrow1021

    def RenameAssay(self, old_identifier: str, new_identifier: str) -> None:
        this: ArcInvestigation = self
        def action(a: ArcAssay) -> None:
            if a.Identifier == old_identifier:
                a.Identifier = new_identifier


        iterate(action, this.Assays)
        def action_1(s: ArcStudy) -> None:
            def predicate(ai: str, s: Any=s) -> bool:
                return ai == old_identifier

            index: int | None = try_find_index(predicate, s.RegisteredAssayIdentifiers)
            if index is not None:
                index_1: int = index or 0
                s.RegisteredAssayIdentifiers[index_1] = new_identifier


        iterate(action_1, this.Studies)

    @staticmethod
    def rename_assay(old_identifier: str, new_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1023(inv: ArcInvestigation) -> ArcInvestigation:
            new_inv: ArcInvestigation = inv.Copy()
            new_inv.RenameAssay(old_identifier, new_identifier)
            return new_inv

        return _arrow1023

    def SetAssayAt(self, index: int, assay: ArcAssay) -> None:
        this: ArcInvestigation = self
        assay_ident: str = assay.Identifier
        def predicate(x: str) -> bool:
            return x == assay_ident

        def mapping(a: ArcAssay) -> str:
            return a.Identifier

        match_value: int | None = try_find_index(predicate, map_1(mapping, remove_at(index, this.Assays)))
        if match_value is None:
            pass

        else: 
            raise Exception(((("Cannot create assay with name " + assay_ident) + ", as assay names must be unique and assay at index ") + str(match_value)) + " has the same name.")

        assay.Investigation = this
        this.Assays[index] = assay
        this.DeregisterMissingAssays()

    @staticmethod
    def set_assay_at(index: int, assay: ArcAssay) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1025(inv: ArcInvestigation) -> ArcInvestigation:
            new_investigation: ArcInvestigation = inv.Copy()
            new_investigation.SetAssayAt(index, assay)
            return new_investigation

        return _arrow1025

    def SetAssay(self, assay_identifier: str, assay: ArcAssay) -> None:
        this: ArcInvestigation = self
        index: int = this.GetAssayIndex(assay_identifier) or 0
        this.SetAssayAt(index, assay)

    @staticmethod
    def set_assay(assay_identifier: str, assay: ArcAssay) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1026(inv: ArcInvestigation) -> ArcInvestigation:
            new_investigation: ArcInvestigation = inv.Copy()
            new_investigation.SetAssay(assay_identifier, assay)
            return new_investigation

        return _arrow1026

    def GetAssayIndex(self, assay_identifier: str) -> int:
        this: ArcInvestigation = self
        def _arrow1029(a: ArcAssay) -> bool:
            return a.Identifier == assay_identifier

        index: int = find_index(_arrow1029, this.Assays) or 0
        if index == -1:
            raise Exception(("Unable to find assay with specified identifier \'" + assay_identifier) + "\'!")

        return index

    @staticmethod
    def get_assay_index(assay_identifier: str) -> Callable[[ArcInvestigation], int]:
        def _arrow1030(inv: ArcInvestigation) -> int:
            return inv.GetAssayIndex(assay_identifier)

        return _arrow1030

    def GetAssayAt(self, index: int) -> ArcAssay:
        this: ArcInvestigation = self
        return this.Assays[index]

    @staticmethod
    def get_assay_at(index: int) -> Callable[[ArcInvestigation], ArcAssay]:
        def _arrow1031(inv: ArcInvestigation) -> ArcAssay:
            new_investigation: ArcInvestigation = inv.Copy()
            return new_investigation.GetAssayAt(index)

        return _arrow1031

    def GetAssay(self, assay_identifier: str) -> ArcAssay:
        this: ArcInvestigation = self
        match_value: ArcAssay | None = this.TryGetAssay(assay_identifier)
        if match_value is None:
            raise Exception(ArcTypesAux_ErrorMsgs_unableToFindAssayIdentifier(assay_identifier, this.Identifier))

        else: 
            return match_value


    @staticmethod
    def get_assay(assay_identifier: str) -> Callable[[ArcInvestigation], ArcAssay]:
        def _arrow1032(inv: ArcInvestigation) -> ArcAssay:
            new_investigation: ArcInvestigation = inv.Copy()
            return new_investigation.GetAssay(assay_identifier)

        return _arrow1032

    def TryGetAssay(self, assay_identifier: str) -> ArcAssay | None:
        this: ArcInvestigation = self
        def _arrow1033(a: ArcAssay) -> bool:
            return a.Identifier == assay_identifier

        return try_find(_arrow1033, this.Assays)

    @staticmethod
    def try_get_assay(assay_identifier: str) -> Callable[[ArcInvestigation], ArcAssay | None]:
        def _arrow1034(inv: ArcInvestigation) -> ArcAssay | None:
            new_investigation: ArcInvestigation = inv.Copy()
            return new_investigation.TryGetAssay(assay_identifier)

        return _arrow1034

    def ContainsAssay(self, assay_identifier: str) -> bool:
        this: ArcInvestigation = self
        def predicate(a: ArcAssay) -> bool:
            return a.Identifier == assay_identifier

        return exists(predicate, this.Assays)

    @staticmethod
    def contains_assay(assay_identifier: str) -> Callable[[ArcInvestigation], bool]:
        def _arrow1035(inv: ArcInvestigation) -> bool:
            return inv.ContainsAssay(assay_identifier)

        return _arrow1035

    @property
    def RegisteredStudyIdentifierCount(self, __unit: None=None) -> int:
        this: ArcInvestigation = self
        return len(this.RegisteredStudyIdentifiers)

    @property
    def RegisteredStudies(self, __unit: None=None) -> Array[ArcStudy]:
        this: ArcInvestigation = self
        def f(identifier: str) -> ArcStudy | None:
            return this.TryGetStudy(identifier)

        return ResizeArray_choose(f, this.RegisteredStudyIdentifiers)

    @property
    def RegisteredStudyCount(self, __unit: None=None) -> int:
        this: ArcInvestigation = self
        return len(this.RegisteredStudies)

    @property
    def VacantStudyIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcInvestigation = self
        def f(arg: str) -> bool:
            return not this.ContainsStudy(arg)

        return ResizeArray_filter(f, this.RegisteredStudyIdentifiers)

    @property
    def StudyCount(self, __unit: None=None) -> int:
        this: ArcInvestigation = self
        return len(this.Studies)

    @property
    def StudyIdentifiers(self, __unit: None=None) -> Array[str]:
        this: ArcInvestigation = self
        def mapping(x: ArcStudy) -> str:
            return x.Identifier

        return to_array(map_1(mapping, this.Studies))

    @property
    def UnregisteredStudies(self, __unit: None=None) -> Array[ArcStudy]:
        this: ArcInvestigation = self
        def f(s: ArcStudy) -> bool:
            def _arrow1042(__unit: None=None, s: Any=s) -> bool:
                source: Array[str] = this.RegisteredStudyIdentifiers
                def _arrow1041(__unit: None=None) -> Callable[[str], bool]:
                    x: str = s.Identifier
                    def _arrow1040(y: str) -> bool:
                        return x == y

                    return _arrow1040

                return exists(_arrow1041(), source)

            return not _arrow1042()

        return ResizeArray_filter(f, this.Studies)

    def AddStudy(self, study: ArcStudy) -> None:
        this: ArcInvestigation = self
        study_1: ArcStudy = study
        def predicate(x: ArcStudy) -> bool:
            return x.Identifier == study_1.Identifier

        match_value: int | None = try_find_index(predicate, this.Studies)
        if match_value is None:
            pass

        else: 
            raise Exception(((("Cannot create study with name " + study_1.Identifier) + ", as study names must be unique and study at index ") + str(match_value)) + " has the same name.")

        study.Investigation = this
        (this.Studies.append(study))

    @staticmethod
    def add_study(study: ArcStudy) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1043(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.AddStudy(study)
            return copy

        return _arrow1043

    def InitStudy(self, study_identifier: str) -> ArcStudy:
        this: ArcInvestigation = self
        study: ArcStudy = ArcStudy.init(study_identifier)
        this.AddStudy(study)
        return study

    @staticmethod
    def init_study(study_identifier: str) -> Callable[[ArcInvestigation], tuple[ArcInvestigation, ArcStudy]]:
        def _arrow1044(inv: ArcInvestigation) -> tuple[ArcInvestigation, ArcStudy]:
            copy: ArcInvestigation = inv.Copy()
            return (copy, copy.InitStudy(study_identifier))

        return _arrow1044

    def RegisterStudy(self, study_identifier: str) -> None:
        this: ArcInvestigation = self
        study_ident: str = study_identifier
        def predicate(x: str) -> bool:
            return x == study_ident

        match_value: str | None = try_find(predicate, this.StudyIdentifiers)
        if match_value is not None:
            pass

        else: 
            raise Exception(("The given study with identifier \'" + study_ident) + "\' must be added to Investigation before it can be registered.")

        study_ident_1: str = study_identifier
        class ObjectExpr1046:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1045(x_1: str, y: str) -> bool:
                    return x_1 == y

                return _arrow1045

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        if contains(study_ident_1, this.RegisteredStudyIdentifiers, ObjectExpr1046()):
            raise Exception(("Study with identifier \'" + study_ident_1) + "\' is already registered!")

        (this.RegisteredStudyIdentifiers.append(study_identifier))

    @staticmethod
    def register_study(study_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1047(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.RegisterStudy(study_identifier)
            return copy

        return _arrow1047

    def AddRegisteredStudy(self, study: ArcStudy) -> None:
        this: ArcInvestigation = self
        this.AddStudy(study)
        this.RegisterStudy(study.Identifier)

    @staticmethod
    def add_registered_study(study: ArcStudy) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1048(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            study_1: ArcStudy = study.Copy()
            copy.AddRegisteredStudy(study_1)
            return copy

        return _arrow1048

    def DeleteStudyAt(self, index: int) -> None:
        this: ArcInvestigation = self
        this.Studies.pop(index)

    @staticmethod
    def delete_study_at(index: int) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1050(i: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = i.Copy()
            copy.DeleteStudyAt(index)
            return copy

        return _arrow1050

    def DeleteStudy(self, study_identifier: str) -> None:
        this: ArcInvestigation = self
        def _arrow1051(s: ArcStudy) -> bool:
            return s.Identifier == study_identifier

        index: int = find_index(_arrow1051, this.Studies) or 0
        this.DeleteStudyAt(index)

    @staticmethod
    def delete_study(study_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1052(i: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = i.Copy()
            copy.DeleteStudy(study_identifier)
            return copy

        return _arrow1052

    def RemoveStudyAt(self, index: int) -> None:
        this: ArcInvestigation = self
        ident: str = this.GetStudyAt(index).Identifier
        this.Studies.pop(index)
        this.DeregisterStudy(ident)

    @staticmethod
    def remove_study_at(index: int) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1056(inv: ArcInvestigation) -> ArcInvestigation:
            new_inv: ArcInvestigation = inv.Copy()
            new_inv.RemoveStudyAt(index)
            return new_inv

        return _arrow1056

    def RemoveStudy(self, study_identifier: str) -> None:
        this: ArcInvestigation = self
        index: int = this.GetStudyIndex(study_identifier) or 0
        this.RemoveStudyAt(index)

    @staticmethod
    def remove_study(study_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1059(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.RemoveStudy(study_identifier)
            return copy

        return _arrow1059

    def RenameStudy(self, old_identifier: str, new_identifier: str) -> None:
        this: ArcInvestigation = self
        def action(s: ArcStudy) -> None:
            if s.Identifier == old_identifier:
                s.Identifier = new_identifier


        iterate(action, this.Studies)
        def predicate(si: str) -> bool:
            return si == old_identifier

        index: int | None = try_find_index(predicate, this.RegisteredStudyIdentifiers)
        if index is not None:
            index_1: int = index or 0
            this.RegisteredStudyIdentifiers[index_1] = new_identifier


    @staticmethod
    def rename_study(old_identifier: str, new_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1063(inv: ArcInvestigation) -> ArcInvestigation:
            new_inv: ArcInvestigation = inv.Copy()
            new_inv.RenameStudy(old_identifier, new_identifier)
            return new_inv

        return _arrow1063

    def SetStudyAt(self, index: int, study: ArcStudy) -> None:
        this: ArcInvestigation = self
        study_1: ArcStudy = study
        def predicate(x: ArcStudy) -> bool:
            return x.Identifier == study_1.Identifier

        match_value: int | None = try_find_index(predicate, remove_at(index, this.Studies))
        if match_value is None:
            pass

        else: 
            raise Exception(((("Cannot create study with name " + study_1.Identifier) + ", as study names must be unique and study at index ") + str(match_value)) + " has the same name.")

        study.Investigation = this
        this.Studies[index] = study

    @staticmethod
    def set_study_at(index: int, study: ArcStudy) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1064(inv: ArcInvestigation) -> ArcInvestigation:
            new_inv: ArcInvestigation = inv.Copy()
            new_inv.SetStudyAt(index, study)
            return new_inv

        return _arrow1064

    def SetStudy(self, study_identifier: str, study: ArcStudy) -> None:
        this: ArcInvestigation = self
        index: int = this.GetStudyIndex(study_identifier) or 0
        this.SetStudyAt(index, study)

    @staticmethod
    def set_study(study_identifier: str, study: ArcStudy) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1071(inv: ArcInvestigation) -> ArcInvestigation:
            new_inv: ArcInvestigation = inv.Copy()
            new_inv.SetStudy(study_identifier, study)
            return new_inv

        return _arrow1071

    def GetStudyIndex(self, study_identifier: str) -> int:
        this: ArcInvestigation = self
        def _arrow1072(s: ArcStudy) -> bool:
            return s.Identifier == study_identifier

        index: int = find_index(_arrow1072, this.Studies) or 0
        if index == -1:
            raise Exception(("Unable to find study with specified identifier \'" + study_identifier) + "\'!")

        return index

    @staticmethod
    def get_study_index(study_identifier: str) -> Callable[[ArcInvestigation], int]:
        def _arrow1073(inv: ArcInvestigation) -> int:
            return inv.GetStudyIndex(study_identifier)

        return _arrow1073

    def GetStudyAt(self, index: int) -> ArcStudy:
        this: ArcInvestigation = self
        return this.Studies[index]

    @staticmethod
    def get_study_at(index: int) -> Callable[[ArcInvestigation], ArcStudy]:
        def _arrow1074(inv: ArcInvestigation) -> ArcStudy:
            new_inv: ArcInvestigation = inv.Copy()
            return new_inv.GetStudyAt(index)

        return _arrow1074

    def GetStudy(self, study_identifier: str) -> ArcStudy:
        this: ArcInvestigation = self
        match_value: ArcStudy | None = this.TryGetStudy(study_identifier)
        if match_value is None:
            raise Exception(ArcTypesAux_ErrorMsgs_unableToFindStudyIdentifier(study_identifier, this.Identifier))

        else: 
            return match_value


    @staticmethod
    def get_study(study_identifier: str) -> Callable[[ArcInvestigation], ArcStudy]:
        def _arrow1075(inv: ArcInvestigation) -> ArcStudy:
            new_inv: ArcInvestigation = inv.Copy()
            return new_inv.GetStudy(study_identifier)

        return _arrow1075

    def TryGetStudy(self, study_identifier: str) -> ArcStudy | None:
        this: ArcInvestigation = self
        def predicate(s: ArcStudy) -> bool:
            return s.Identifier == study_identifier

        return try_find(predicate, this.Studies)

    @staticmethod
    def try_get_study(study_identifier: str) -> Callable[[ArcInvestigation], ArcStudy | None]:
        def _arrow1076(inv: ArcInvestigation) -> ArcStudy | None:
            new_inv: ArcInvestigation = inv.Copy()
            return new_inv.TryGetStudy(study_identifier)

        return _arrow1076

    def ContainsStudy(self, study_identifier: str) -> bool:
        this: ArcInvestigation = self
        def predicate(s: ArcStudy) -> bool:
            return s.Identifier == study_identifier

        return exists(predicate, this.Studies)

    @staticmethod
    def contains_study(study_identifier: str) -> Callable[[ArcInvestigation], bool]:
        def _arrow1077(inv: ArcInvestigation) -> bool:
            return inv.ContainsStudy(study_identifier)

        return _arrow1077

    def RegisterAssayAt(self, study_index: int, assay_identifier: str) -> None:
        this: ArcInvestigation = self
        study: ArcStudy = this.GetStudyAt(study_index)
        def predicate(x: str) -> bool:
            return x == assay_identifier

        def mapping(a: ArcAssay) -> str:
            return a.Identifier

        match_value: str | None = try_find(predicate, map_1(mapping, this.Assays))
        if match_value is not None:
            pass

        else: 
            raise Exception("The given assay must be added to Investigation before it can be registered.")

        assay_ident_1: str = assay_identifier
        def predicate_1(x_1: str) -> bool:
            return x_1 == assay_ident_1

        match_value_1: int | None = try_find_index(predicate_1, study.RegisteredAssayIdentifiers)
        if match_value_1 is None:
            pass

        else: 
            raise Exception(((("Cannot create assay with name " + assay_ident_1) + ", as assay names must be unique and assay at index ") + str(match_value_1)) + " has the same name.")

        study.RegisterAssay(assay_identifier)

    @staticmethod
    def register_assay_at(study_index: int, assay_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1078(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.RegisterAssayAt(study_index, assay_identifier)
            return copy

        return _arrow1078

    def RegisterAssay(self, study_identifier: str, assay_identifier: str) -> None:
        this: ArcInvestigation = self
        index: int = this.GetStudyIndex(study_identifier) or 0
        this.RegisterAssayAt(index, assay_identifier)

    @staticmethod
    def register_assay(study_identifier: str, assay_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1079(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.RegisterAssay(study_identifier, assay_identifier)
            return copy

        return _arrow1079

    def DeregisterAssayAt(self, study_index: int, assay_identifier: str) -> None:
        this: ArcInvestigation = self
        study: ArcStudy = this.GetStudyAt(study_index)
        study.DeregisterAssay(assay_identifier)

    @staticmethod
    def deregister_assay_at(study_index: int, assay_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1080(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.DeregisterAssayAt(study_index, assay_identifier)
            return copy

        return _arrow1080

    def DeregisterAssay(self, study_identifier: str, assay_identifier: str) -> None:
        this: ArcInvestigation = self
        index: int = this.GetStudyIndex(study_identifier) or 0
        this.DeregisterAssayAt(index, assay_identifier)

    @staticmethod
    def deregister_assay(study_identifier: str, assay_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1081(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.DeregisterAssay(study_identifier, assay_identifier)
            return copy

        return _arrow1081

    def DeregisterStudy(self, study_identifier: str) -> None:
        this: ArcInvestigation = self
        class ObjectExpr1083:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow1082(x: str, y: str) -> bool:
                    return x == y

                return _arrow1082

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        ignore(remove_in_place(study_identifier, this.RegisteredStudyIdentifiers, ObjectExpr1083()))

    @staticmethod
    def deregister_study(study_identifier: str) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1084(i: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = i.Copy()
            copy.DeregisterStudy(study_identifier)
            return copy

        return _arrow1084

    def GetAllPersons(self, __unit: None=None) -> Array[Person]:
        this: ArcInvestigation = self
        persons: Array[Person] = []
        enumerator: Any = get_enumerator(this.Assays)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                a: ArcAssay = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                add_range_in_place(a.Performers, persons)

        finally: 
            dispose(enumerator)

        enumerator_1: Any = get_enumerator(this.Studies)
        try: 
            while enumerator_1.System_Collections_IEnumerator_MoveNext():
                s: ArcStudy = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                add_range_in_place(s.Contacts, persons)

        finally: 
            dispose(enumerator_1)

        add_range_in_place(this.Contacts, persons)
        class ObjectExpr1085:
            @property
            def Equals(self) -> Callable[[Person, Person], bool]:
                return equals

            @property
            def GetHashCode(self) -> Callable[[Person], int]:
                return safe_hash

        return Array_distinct(list(persons), ObjectExpr1085())

    def GetAllPublications(self, __unit: None=None) -> Array[Publication]:
        this: ArcInvestigation = self
        pubs: Array[Publication] = []
        enumerator: Any = get_enumerator(this.Studies)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                s: ArcStudy = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                add_range_in_place(s.Publications, pubs)

        finally: 
            dispose(enumerator)

        add_range_in_place(this.Publications, pubs)
        class ObjectExpr1086:
            @property
            def Equals(self) -> Callable[[Publication, Publication], bool]:
                return equals

            @property
            def GetHashCode(self) -> Callable[[Publication], int]:
                return safe_hash

        return Array_distinct(list(pubs), ObjectExpr1086())

    def DeregisterMissingAssays(self, __unit: None=None) -> None:
        this: ArcInvestigation = self
        inv: ArcInvestigation = this
        existing_assays: Array[str] = inv.AssayIdentifiers
        enumerator: Any = get_enumerator(inv.Studies)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                study: ArcStudy = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                enumerator_1: Any = get_enumerator(list(study.RegisteredAssayIdentifiers))
                try: 
                    while enumerator_1.System_Collections_IEnumerator_MoveNext():
                        registered_assay: str = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                        class ObjectExpr1088:
                            @property
                            def Equals(self) -> Callable[[str, str], bool]:
                                def _arrow1087(x: str, y: str) -> bool:
                                    return x == y

                                return _arrow1087

                            @property
                            def GetHashCode(self) -> Callable[[str], int]:
                                return string_hash

                        if not contains(registered_assay, existing_assays, ObjectExpr1088()):
                            value_1: None = study.DeregisterAssay(registered_assay)
                            ignore(None)


                finally: 
                    dispose(enumerator_1)


        finally: 
            dispose(enumerator)


    @staticmethod
    def deregister_missing_assays(__unit: None=None) -> Callable[[ArcInvestigation], ArcInvestigation]:
        def _arrow1089(inv: ArcInvestigation) -> ArcInvestigation:
            copy: ArcInvestigation = inv.Copy()
            copy.DeregisterMissingAssays()
            return copy

        return _arrow1089

    def UpdateIOTypeByEntityID(self, __unit: None=None) -> None:
        this: ArcInvestigation = self
        def _arrow1093(__unit: None=None) -> IEnumerable_1[ArcTable]:
            def _arrow1090(study: ArcStudy) -> IEnumerable_1[ArcTable]:
                return study.Tables

            def _arrow1092(__unit: None=None) -> IEnumerable_1[ArcTable]:
                def _arrow1091(assay: ArcAssay) -> IEnumerable_1[ArcTable]:
                    return assay.Tables

                return collect(_arrow1091, this.Assays)

            return append_3(collect(_arrow1090, this.Studies), delay(_arrow1092))

        io_map: Any = ArcTablesAux_getIOMap(list(to_list(delay(_arrow1093))))
        enumerator: Any = get_enumerator(this.Studies)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                study_1: ArcStudy = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                ArcTablesAux_applyIOMap(io_map, study_1.Tables)

        finally: 
            dispose(enumerator)

        enumerator_1: Any = get_enumerator(this.Assays)
        try: 
            while enumerator_1.System_Collections_IEnumerator_MoveNext():
                assay_1: ArcAssay = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                ArcTablesAux_applyIOMap(io_map, assay_1.Tables)

        finally: 
            dispose(enumerator_1)


    def Copy(self, __unit: None=None) -> ArcInvestigation:
        this: ArcInvestigation = self
        next_assays: Array[ArcAssay] = []
        next_studies: Array[ArcStudy] = []
        enumerator: Any = get_enumerator(this.Assays)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                assay: ArcAssay = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                copy: ArcAssay = assay.Copy()
                (next_assays.append(copy))

        finally: 
            dispose(enumerator)

        enumerator_1: Any = get_enumerator(this.Studies)
        try: 
            while enumerator_1.System_Collections_IEnumerator_MoveNext():
                study: ArcStudy = enumerator_1.System_Collections_Generic_IEnumerator_1_get_Current()
                copy_1: ArcStudy = study.Copy()
                (next_studies.append(copy_1))

        finally: 
            dispose(enumerator_1)

        def f(c: Comment) -> Comment:
            return c.Copy()

        next_comments: Array[Comment] = ResizeArray_map(f, this.Comments)
        def f_1(c_1: Remark) -> Remark:
            return c_1.Copy()

        next_remarks: Array[Remark] = ResizeArray_map(f_1, this.Remarks)
        def f_2(c_2: Person) -> Person:
            return c_2.Copy()

        next_contacts: Array[Person] = ResizeArray_map(f_2, this.Contacts)
        def f_3(c_3: Publication) -> Publication:
            return c_3.Copy()

        next_publications: Array[Publication] = ResizeArray_map(f_3, this.Publications)
        def f_4(c_4: OntologySourceReference) -> OntologySourceReference:
            return c_4.Copy()

        next_ontology_source_references: Array[OntologySourceReference] = ResizeArray_map(f_4, this.OntologySourceReferences)
        next_study_identifiers: Array[str] = list(this.RegisteredStudyIdentifiers)
        return ArcInvestigation(this.Identifier, this.Title, this.Description, this.SubmissionDate, this.PublicReleaseDate, next_ontology_source_references, next_publications, next_contacts, next_assays, next_studies, next_study_identifiers, next_comments, next_remarks)

    def StructurallyEquals(self, other: ArcInvestigation) -> bool:
        this: ArcInvestigation = self
        def predicate(x: bool) -> bool:
            return x == True

        def _arrow1096(__unit: None=None) -> bool:
            a: IEnumerable_1[Publication] = this.Publications
            b: IEnumerable_1[Publication] = other.Publications
            def folder(acc: bool, e: bool) -> bool:
                if acc:
                    return e

                else: 
                    return False


            def _arrow1095(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1094(i_1: int) -> bool:
                    return equals(item(i_1, a), item(i_1, b))

                return map_1(_arrow1094, range_big_int(0, 1, length(a) - 1))

            return fold(folder, True, to_list(delay(_arrow1095))) if (length(a) == length(b)) else False

        def _arrow1099(__unit: None=None) -> bool:
            a_1: IEnumerable_1[Person] = this.Contacts
            b_1: IEnumerable_1[Person] = other.Contacts
            def folder_1(acc_1: bool, e_1: bool) -> bool:
                if acc_1:
                    return e_1

                else: 
                    return False


            def _arrow1098(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1097(i_2: int) -> bool:
                    return equals(item(i_2, a_1), item(i_2, b_1))

                return map_1(_arrow1097, range_big_int(0, 1, length(a_1) - 1))

            return fold(folder_1, True, to_list(delay(_arrow1098))) if (length(a_1) == length(b_1)) else False

        def _arrow1102(__unit: None=None) -> bool:
            a_2: IEnumerable_1[OntologySourceReference] = this.OntologySourceReferences
            b_2: IEnumerable_1[OntologySourceReference] = other.OntologySourceReferences
            def folder_2(acc_2: bool, e_2: bool) -> bool:
                if acc_2:
                    return e_2

                else: 
                    return False


            def _arrow1101(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1100(i_3: int) -> bool:
                    return equals(item(i_3, a_2), item(i_3, b_2))

                return map_1(_arrow1100, range_big_int(0, 1, length(a_2) - 1))

            return fold(folder_2, True, to_list(delay(_arrow1101))) if (length(a_2) == length(b_2)) else False

        def _arrow1105(__unit: None=None) -> bool:
            a_3: IEnumerable_1[ArcAssay] = this.Assays
            b_3: IEnumerable_1[ArcAssay] = other.Assays
            def folder_3(acc_3: bool, e_3: bool) -> bool:
                if acc_3:
                    return e_3

                else: 
                    return False


            def _arrow1104(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1103(i_4: int) -> bool:
                    return equals(item(i_4, a_3), item(i_4, b_3))

                return map_1(_arrow1103, range_big_int(0, 1, length(a_3) - 1))

            return fold(folder_3, True, to_list(delay(_arrow1104))) if (length(a_3) == length(b_3)) else False

        def _arrow1108(__unit: None=None) -> bool:
            a_4: IEnumerable_1[ArcStudy] = this.Studies
            b_4: IEnumerable_1[ArcStudy] = other.Studies
            def folder_4(acc_4: bool, e_4: bool) -> bool:
                if acc_4:
                    return e_4

                else: 
                    return False


            def _arrow1107(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1106(i_5: int) -> bool:
                    return equals(item(i_5, a_4), item(i_5, b_4))

                return map_1(_arrow1106, range_big_int(0, 1, length(a_4) - 1))

            return fold(folder_4, True, to_list(delay(_arrow1107))) if (length(a_4) == length(b_4)) else False

        def _arrow1111(__unit: None=None) -> bool:
            a_5: IEnumerable_1[str] = this.RegisteredStudyIdentifiers
            b_5: IEnumerable_1[str] = other.RegisteredStudyIdentifiers
            def folder_5(acc_5: bool, e_5: bool) -> bool:
                if acc_5:
                    return e_5

                else: 
                    return False


            def _arrow1110(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1109(i_6: int) -> bool:
                    return item(i_6, a_5) == item(i_6, b_5)

                return map_1(_arrow1109, range_big_int(0, 1, length(a_5) - 1))

            return fold(folder_5, True, to_list(delay(_arrow1110))) if (length(a_5) == length(b_5)) else False

        def _arrow1114(__unit: None=None) -> bool:
            a_6: IEnumerable_1[Comment] = this.Comments
            b_6: IEnumerable_1[Comment] = other.Comments
            def folder_6(acc_6: bool, e_6: bool) -> bool:
                if acc_6:
                    return e_6

                else: 
                    return False


            def _arrow1113(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1112(i_7: int) -> bool:
                    return equals(item(i_7, a_6), item(i_7, b_6))

                return map_1(_arrow1112, range_big_int(0, 1, length(a_6) - 1))

            return fold(folder_6, True, to_list(delay(_arrow1113))) if (length(a_6) == length(b_6)) else False

        def _arrow1117(__unit: None=None) -> bool:
            a_7: IEnumerable_1[Remark] = this.Remarks
            b_7: IEnumerable_1[Remark] = other.Remarks
            def folder_7(acc_7: bool, e_7: bool) -> bool:
                if acc_7:
                    return e_7

                else: 
                    return False


            def _arrow1116(__unit: None=None) -> IEnumerable_1[bool]:
                def _arrow1115(i_8: int) -> bool:
                    return equals(item(i_8, a_7), item(i_8, b_7))

                return map_1(_arrow1115, range_big_int(0, 1, length(a_7) - 1))

            return fold(folder_7, True, to_list(delay(_arrow1116))) if (length(a_7) == length(b_7)) else False

        return for_all(predicate, to_enumerable([this.Identifier == other.Identifier, equals(this.Title, other.Title), equals(this.Description, other.Description), equals(this.SubmissionDate, other.SubmissionDate), equals(this.PublicReleaseDate, other.PublicReleaseDate), _arrow1096(), _arrow1099(), _arrow1102(), _arrow1105(), _arrow1108(), _arrow1111(), _arrow1114(), _arrow1117()]))

    def ReferenceEquals(self, other: ArcInvestigation) -> bool:
        this: ArcInvestigation = self
        return this is other

    def __str__(self, __unit: None=None) -> str:
        this: ArcInvestigation = self
        arg: str = this.Identifier
        arg_1: str | None = this.Title
        arg_2: str | None = this.Description
        arg_3: str | None = this.SubmissionDate
        arg_4: str | None = this.PublicReleaseDate
        arg_5: Array[OntologySourceReference] = this.OntologySourceReferences
        arg_6: Array[Publication] = this.Publications
        arg_7: Array[Person] = this.Contacts
        arg_8: Array[ArcAssay] = this.Assays
        arg_9: Array[ArcStudy] = this.Studies
        arg_10: Array[str] = this.RegisteredStudyIdentifiers
        arg_11: Array[Comment] = this.Comments
        arg_12: Array[Remark] = this.Remarks
        return to_text(printf("ArcInvestigation {\r\n    Identifier = %A,\r\n    Title = %A,\r\n    Description = %A,\r\n    SubmissionDate = %A,\r\n    PublicReleaseDate = %A,\r\n    OntologySourceReferences = %A,\r\n    Publications = %A,\r\n    Contacts = %A,\r\n    Assays = %A,\r\n    Studies = %A,\r\n    RegisteredStudyIdentifiers = %A,\r\n    Comments = %A,\r\n    Remarks = %A,\r\n}"))(arg)(arg_1)(arg_2)(arg_3)(arg_4)(arg_5)(arg_6)(arg_7)(arg_8)(arg_9)(arg_10)(arg_11)(arg_12)

    def __eq__(self, other: Any=None) -> bool:
        this: ArcInvestigation = self
        return this.StructurallyEquals(other) if isinstance(other, ArcInvestigation) else False

    def __hash__(self, __unit: None=None) -> Any:
        this: ArcInvestigation = self
        return box_hash_array([this.Identifier, box_hash_option(this.Title), box_hash_option(this.Description), box_hash_option(this.SubmissionDate), box_hash_option(this.PublicReleaseDate), box_hash_seq(this.Publications), box_hash_seq(this.Contacts), box_hash_seq(this.OntologySourceReferences), box_hash_seq(this.Assays), box_hash_seq(this.Studies), box_hash_seq(this.RegisteredStudyIdentifiers), box_hash_seq(this.Comments), box_hash_seq(this.Remarks)])

    def GetLightHashCode(self, __unit: None=None) -> Any:
        this: ArcInvestigation = self
        return box_hash_array([this.Identifier, box_hash_option(this.Title), box_hash_option(this.Description), box_hash_option(this.SubmissionDate), box_hash_option(this.PublicReleaseDate), box_hash_seq(this.Publications), box_hash_seq(this.Contacts), box_hash_seq(this.OntologySourceReferences), box_hash_seq(this.RegisteredStudyIdentifiers), box_hash_seq(this.Comments), box_hash_seq(this.Remarks)])


ArcInvestigation_reflection = _expr1119

def ArcInvestigation__ctor_Z2ED5C612(identifier: str, title: str | None=None, description: str | None=None, submission_date: str | None=None, public_release_date: str | None=None, ontology_source_references: Array[OntologySourceReference] | None=None, publications: Array[Publication] | None=None, contacts: Array[Person] | None=None, assays: Array[ArcAssay] | None=None, studies: Array[ArcStudy] | None=None, registered_study_identifiers: Array[str] | None=None, comments: Array[Comment] | None=None, remarks: Array[Remark] | None=None) -> ArcInvestigation:
    return ArcInvestigation(identifier, title, description, submission_date, public_release_date, ontology_source_references, publications, contacts, assays, studies, registered_study_identifiers, comments, remarks)


def ArcTypesAux_ErrorMsgs_unableToFindAssayIdentifier(assay_identifier: Any, investigation_identifier: Any) -> str:
    return ((("Error. Unable to find assay with identifier \'" + str(assay_identifier)) + "\' in investigation ") + str(investigation_identifier)) + "."


def ArcTypesAux_ErrorMsgs_unableToFindStudyIdentifier(study_identifer: Any, investigation_identifier: Any) -> str:
    return ((("Error. Unable to find study with identifier \'" + str(study_identifer)) + "\' in investigation ") + str(investigation_identifier)) + "."


__all__ = ["ArcAssay_reflection", "ArcStudy_reflection", "ArcInvestigation_reflection", "ArcTypesAux_ErrorMsgs_unableToFindAssayIdentifier", "ArcTypesAux_ErrorMsgs_unableToFindStudyIdentifier"]

