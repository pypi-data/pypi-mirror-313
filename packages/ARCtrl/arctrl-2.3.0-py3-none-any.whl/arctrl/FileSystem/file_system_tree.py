from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.array_ import (try_find, exists, map, head, filter, tail, equals_with, iterate, choose, append as append_1)
from ..fable_modules.fable_library.list import (cons, to_array as to_array_1, reverse, FSharpList, empty)
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.reflection import (TypeInfo, string_type, array_type, union_type)
from ..fable_modules.fable_library.seq import (to_array, delay, append, singleton)
from ..fable_modules.fable_library.seq2 import (Array_groupBy, Array_distinct)
from ..fable_modules.fable_library.types import (Array, Union)
from ..fable_modules.fable_library.util import (IEnumerable_1, string_hash, array_hash, curry2)
from .path import (split, combine_many)

def _expr457() -> TypeInfo:
    return union_type("ARCtrl.FileSystem.FileSystemTree", [], FileSystemTree, lambda: [[("name", string_type)], [("name", string_type), ("children", array_type(FileSystemTree_reflection()))]])


class FileSystemTree(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> list[str]:
        return ["File", "Folder"]

    @property
    def Name(self, __unit: None=None) -> str:
        this: FileSystemTree = self
        (pattern_matching_result, n) = (None, None)
        if this.tag == 1:
            pattern_matching_result = 0
            n = this.fields[0]

        else: 
            pattern_matching_result = 0
            n = this.fields[0]

        if pattern_matching_result == 0:
            return n


    @property
    def is_folder(self, __unit: None=None) -> bool:
        this: FileSystemTree = self
        return True if (this.tag == 1) else False

    @property
    def is_file(self, __unit: None=None) -> bool:
        this: FileSystemTree = self
        return True if (this.tag == 0) else False

    @staticmethod
    def ROOT_NAME() -> str:
        return "root"

    @staticmethod
    def create_file(name: str) -> FileSystemTree:
        return FileSystemTree(0, name)

    @staticmethod
    def create_folder(name: str, children: Array[FileSystemTree] | None=None) -> FileSystemTree:
        return FileSystemTree(1, name, default_arg(children, []))

    @staticmethod
    def create_root_folder(children: Array[FileSystemTree]) -> FileSystemTree:
        return FileSystemTree(1, FileSystemTree.ROOT_NAME(), children)

    def TryGetChildByName(self, name: str) -> FileSystemTree | None:
        this: FileSystemTree = self
        def predicate(c: FileSystemTree) -> bool:
            return c.Name == name

        return None if (this.tag == 0) else try_find(predicate, this.fields[1])

    @staticmethod
    def try_get_child_by_name(name: str) -> Callable[[FileSystemTree], FileSystemTree | None]:
        def _arrow422(fst: FileSystemTree) -> FileSystemTree | None:
            return fst.TryGetChildByName(name)

        return _arrow422

    def ContainsChildWithName(self, name: str) -> bool:
        this: FileSystemTree = self
        def predicate(c: FileSystemTree) -> bool:
            return c.Name == name

        return False if (this.tag == 0) else exists(predicate, this.fields[1])

    @staticmethod
    def contains_child_with_name(name: str) -> Callable[[FileSystemTree], bool]:
        def _arrow424(fst: FileSystemTree) -> bool:
            return fst.ContainsChildWithName(name)

        return _arrow424

    def AddFile(self, path: str) -> FileSystemTree:
        this: FileSystemTree = self
        existing_paths: Array[str] = this.ToFilePaths()
        def _arrow427(__unit: None=None) -> IEnumerable_1[str]:
            def _arrow426(__unit: None=None) -> IEnumerable_1[str]:
                return existing_paths

            return append(singleton(path), delay(_arrow426))

        file_paths: Array[str] = to_array(delay(_arrow427))
        return FileSystemTree.from_file_paths(file_paths)

    @staticmethod
    def add_file(path: str) -> Callable[[FileSystemTree], FileSystemTree]:
        def _arrow430(tree: FileSystemTree) -> FileSystemTree:
            return tree.AddFile(path)

        return _arrow430

    @staticmethod
    def from_file_paths(paths: Array[str]) -> FileSystemTree:
        def loop(paths_1: Array[Array[str]], parent: FileSystemTree) -> FileSystemTree:
            def mapping(arg: Array[str], paths_1: Any=paths_1, parent: Any=parent) -> FileSystemTree:
                name: str = head(arg)
                return FileSystemTree.create_file(name)

            def predicate(p: Array[str], paths_1: Any=paths_1, parent: Any=parent) -> bool:
                return len(p) == 1

            files: Array[FileSystemTree] = map(mapping, filter(predicate, paths_1), None)
            def mapping_2(tupled_arg: tuple[str, Array[Array[str]]], paths_1: Any=paths_1, parent: Any=parent) -> FileSystemTree:
                parent_1: FileSystemTree = FileSystemTree.create_folder(tupled_arg[0], [])
                def mapping_1(array_7: Array[str], tupled_arg: Any=tupled_arg) -> Array[str]:
                    return tail(array_7)

                return loop(map(mapping_1, tupled_arg[1], None), parent_1)

            def projection(x_2: Array[str], paths_1: Any=paths_1, parent: Any=parent) -> str:
                return head(x_2)

            def predicate_1(p_1: Array[str], paths_1: Any=paths_1, parent: Any=parent) -> bool:
                return len(p_1) > 1

            class ObjectExpr437:
                @property
                def Equals(self) -> Callable[[str, str], bool]:
                    def _arrow436(x_3: str, y_2: str) -> bool:
                        return x_3 == y_2

                    return _arrow436

                @property
                def GetHashCode(self) -> Callable[[str], int]:
                    return string_hash

            folders: Array[FileSystemTree] = map(mapping_2, Array_groupBy(projection, filter(predicate_1, paths_1), ObjectExpr437()), None)
            if parent.tag == 1:
                def _arrow439(__unit: None=None, paths_1: Any=paths_1, parent: Any=parent) -> IEnumerable_1[FileSystemTree]:
                    def _arrow438(__unit: None=None) -> IEnumerable_1[FileSystemTree]:
                        return folders

                    return append(files, delay(_arrow438))

                return FileSystemTree.create_folder(parent.fields[0], to_array(delay(_arrow439)))

            else: 
                return parent


        class ObjectExpr442:
            @property
            def Equals(self) -> Callable[[Array[str], Array[str]], bool]:
                def _arrow441(x: Array[str], y: Array[str]) -> bool:
                    def _arrow440(x_1: str, y_1: str) -> bool:
                        return x_1 == y_1

                    return equals_with(_arrow440, x, y)

                return _arrow441

            @property
            def GetHashCode(self) -> Callable[[Array[str]], int]:
                return array_hash

        return loop(Array_distinct(map(split, paths, None), ObjectExpr442()), FileSystemTree.create_folder(FileSystemTree.ROOT_NAME(), []))

    def ToFilePaths(self, remove_root: bool | None=None) -> Array[str]:
        this: FileSystemTree = self
        res: Array[str] = []
        def loop(output: FSharpList[str], parent: FileSystemTree) -> None:
            if parent.tag == 1:
                def action(filest: FileSystemTree, output: Any=output, parent: Any=parent) -> None:
                    loop(cons(parent.fields[0], output), filest)

                iterate(action, parent.fields[1])

            else: 
                item: str = combine_many(to_array_1(reverse(cons(parent.fields[0], output))))
                (res.append(item))


        if default_arg(remove_root, True):
            if this.tag == 0:
                (res.append(this.fields[0]))

            else: 
                iterate(curry2(loop)(empty()), this.fields[1])


        else: 
            loop(empty(), this)

        return list(res)

    @staticmethod
    def to_file_paths(remove_root: bool | None=None) -> Callable[[FileSystemTree], Array[str]]:
        def _arrow443(root: FileSystemTree) -> Array[str]:
            return root.ToFilePaths(remove_root)

        return _arrow443

    def FilterFiles(self, predicate: Callable[[str], bool]) -> FileSystemTree | None:
        this: FileSystemTree = self
        def loop(parent: FileSystemTree) -> FileSystemTree | None:
            if parent.tag == 1:
                return FileSystemTree(1, parent.fields[0], choose(loop, parent.fields[1], None))

            else: 
                n: str = parent.fields[0]
                if predicate(n):
                    return FileSystemTree(0, n)

                else: 
                    return None



        return loop(this)

    @staticmethod
    def filter_files(predicate: Callable[[str], bool]) -> Callable[[FileSystemTree], FileSystemTree | None]:
        def _arrow444(tree: FileSystemTree) -> FileSystemTree | None:
            return tree.FilterFiles(predicate)

        return _arrow444

    def FilterFolders(self, predicate: Callable[[str], bool]) -> FileSystemTree | None:
        this: FileSystemTree = self
        def loop(parent: FileSystemTree) -> FileSystemTree | None:
            if parent.tag == 1:
                n_1: str = parent.fields[0]
                if predicate(n_1):
                    return FileSystemTree(1, n_1, choose(loop, parent.fields[1], None))

                else: 
                    return None


            else: 
                return FileSystemTree(0, parent.fields[0])


        return loop(this)

    @staticmethod
    def filter_folders(predicate: Callable[[str], bool]) -> Callable[[FileSystemTree], FileSystemTree | None]:
        def _arrow445(tree: FileSystemTree) -> FileSystemTree | None:
            return tree.FilterFolders(predicate)

        return _arrow445

    def Filter(self, predicate: Callable[[str], bool]) -> FileSystemTree | None:
        this: FileSystemTree = self
        def loop(parent: FileSystemTree) -> FileSystemTree | None:
            if parent.tag == 1:
                n_1: str = parent.fields[0]
                if predicate(n_1):
                    filtered_children: Array[FileSystemTree] = choose(loop, parent.fields[1], None)
                    if len(filtered_children) == 0:
                        return None

                    else: 
                        return FileSystemTree(1, n_1, filtered_children)


                else: 
                    return None


            else: 
                n: str = parent.fields[0]
                if predicate(n):
                    return FileSystemTree(0, n)

                else: 
                    return None



        return loop(this)

    @staticmethod
    def filter(predicate: Callable[[str], bool]) -> Callable[[FileSystemTree], FileSystemTree | None]:
        def _arrow446(tree: FileSystemTree) -> FileSystemTree | None:
            return tree.Filter(predicate)

        return _arrow446

    def Union(self, other_fst: FileSystemTree) -> FileSystemTree:
        this: FileSystemTree = self
        def _arrow447(__unit: None=None) -> Array[str]:
            array_1: Array[str] = this.ToFilePaths()
            return append_1(other_fst.ToFilePaths(), array_1, None)

        class ObjectExpr449:
            @property
            def Equals(self) -> Callable[[str, str], bool]:
                def _arrow448(x: str, y: str) -> bool:
                    return x == y

                return _arrow448

            @property
            def GetHashCode(self) -> Callable[[str], int]:
                return string_hash

        paths: Array[str] = Array_distinct(_arrow447(), ObjectExpr449())
        return FileSystemTree.from_file_paths(paths)

    def Copy(self, __unit: None=None) -> FileSystemTree:
        this: FileSystemTree = self
        def mapping(c: FileSystemTree) -> FileSystemTree:
            return c.Copy()

        return FileSystemTree(0, this.fields[0]) if (this.tag == 0) else FileSystemTree(1, this.fields[0], map(mapping, this.fields[1], None))

    @staticmethod
    def create_git_keep_file(__unit: None=None) -> FileSystemTree:
        return FileSystemTree.create_file(".gitkeep")

    @staticmethod
    def create_readme_file(__unit: None=None) -> FileSystemTree:
        return FileSystemTree.create_file("README.md")

    @staticmethod
    def create_empty_folder(name: str) -> FileSystemTree:
        return FileSystemTree.create_folder(name, [FileSystemTree.create_git_keep_file()])

    @staticmethod
    def create_assay_folder(assay_name: str, has_data_map: bool | None=None) -> FileSystemTree:
        has_data_map_1: bool = default_arg(has_data_map, False)
        dataset: FileSystemTree = FileSystemTree.create_empty_folder("dataset")
        protocols: FileSystemTree = FileSystemTree.create_empty_folder("protocols")
        readme: FileSystemTree = FileSystemTree.create_readme_file()
        assay_file: FileSystemTree = FileSystemTree.create_file("isa.assay.xlsx")
        if has_data_map_1:
            data_map_file: FileSystemTree = FileSystemTree.create_file("isa.datamap.xlsx")
            return FileSystemTree.create_folder(assay_name, [dataset, protocols, assay_file, readme, data_map_file])

        else: 
            return FileSystemTree.create_folder(assay_name, [dataset, protocols, assay_file, readme])


    @staticmethod
    def create_study_folder(study_name: str, has_data_map: bool | None=None) -> FileSystemTree:
        has_data_map_1: bool = default_arg(has_data_map, False)
        resources: FileSystemTree = FileSystemTree.create_empty_folder("resources")
        protocols: FileSystemTree = FileSystemTree.create_empty_folder("protocols")
        readme: FileSystemTree = FileSystemTree.create_readme_file()
        study_file: FileSystemTree = FileSystemTree.create_file("isa.study.xlsx")
        if has_data_map_1:
            data_map_file: FileSystemTree = FileSystemTree.create_file("isa.datamap.xlsx")
            return FileSystemTree.create_folder(study_name, [resources, protocols, study_file, readme, data_map_file])

        else: 
            return FileSystemTree.create_folder(study_name, [resources, protocols, study_file, readme])


    @staticmethod
    def create_investigation_file(__unit: None=None) -> FileSystemTree:
        return FileSystemTree.create_file("isa.investigation.xlsx")

    @staticmethod
    def create_assays_folder(assays: Array[FileSystemTree]) -> FileSystemTree:
        return FileSystemTree.create_folder("assays", append_1([FileSystemTree.create_git_keep_file()], assays, None))

    @staticmethod
    def create_studies_folder(studies: Array[FileSystemTree]) -> FileSystemTree:
        return FileSystemTree.create_folder("studies", append_1([FileSystemTree.create_git_keep_file()], studies, None))

    @staticmethod
    def create_workflows_folder(workflows: Array[FileSystemTree]) -> FileSystemTree:
        return FileSystemTree.create_folder("workflows", append_1([FileSystemTree.create_git_keep_file()], workflows, None))

    @staticmethod
    def create_runs_folder(runs: Array[FileSystemTree]) -> FileSystemTree:
        return FileSystemTree.create_folder("runs", append_1([FileSystemTree.create_git_keep_file()], runs, None))


FileSystemTree_reflection = _expr457

__all__ = ["FileSystemTree_reflection"]

