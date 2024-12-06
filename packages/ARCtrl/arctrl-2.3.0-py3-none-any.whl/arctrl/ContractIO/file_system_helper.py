from __future__ import annotations
from collections.abc import Callable
from pathlib import Path
import shutil
import os
from typing import Any
from ..fable_modules.fable_library.array_ import map
from ..fable_modules.fable_library.async_builder import (singleton, Async)
from ..fable_modules.fable_library.seq import (is_empty, empty, map as map_1, concat, append, to_array)
from ..fable_modules.fable_library.string_ import (starts_with_exact, trim as trim_1, replace, substring)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (IEnumerable_1, to_enumerable)
from ..fable_modules.fs_spreadsheet.fs_workbook import FsWorkbook
from ..fable_modules.fs_spreadsheet_py.fs_extension import (FsSpreadsheet_FsWorkbook__FsWorkbook_fromXlsxFile_Static_Z721C83C5, FsSpreadsheet_FsWorkbook__FsWorkbook_toXlsxFile_Static)
from ..cross_async import all

shutil

os

Path

def directory_exists_async(path: str) -> Async[bool]:
    def _arrow3213(__unit: None=None, path: Any=path) -> Async[bool]:
        return singleton.Return(Path(path).is_dir())

    return singleton.Delay(_arrow3213)


def create_directory_async(path: str) -> Async[None]:
    def _arrow3214(__unit: None=None, path: Any=path) -> Async[None]:
        Path(path).mkdir(parents=True, exist_ok=True)
        return singleton.Zero()

    return singleton.Delay(_arrow3214)


def ensure_directory_async(path: str) -> Async[None]:
    def _arrow3216(__unit: None=None, path: Any=path) -> Async[None]:
        def _arrow3215(_arg: bool) -> Async[None]:
            return singleton.ReturnFrom(create_directory_async(path)) if (not _arg) else singleton.Zero()

        return singleton.Bind(directory_exists_async(path), _arrow3215)

    return singleton.Delay(_arrow3216)


def ensure_directory_of_file_async(file_path: str) -> Async[None]:
    def _arrow3217(__unit: None=None, file_path: Any=file_path) -> Async[None]:
        return singleton.ReturnFrom(ensure_directory_async(Path(file_path).parent))

    return singleton.Delay(_arrow3217)


def file_exists_async(path: str) -> Async[bool]:
    def _arrow3218(__unit: None=None, path: Any=path) -> Async[bool]:
        return singleton.Return(Path(path).is_file())

    return singleton.Delay(_arrow3218)


def read_file_text_async(path: str) -> Async[str]:
    def _arrow3220(__unit: None=None, path: Any=path) -> Async[str]:
        def _arrow3219(__unit: None=None) -> str:
            with open(path, 'r', encoding='utf-8') as f: return f.read()

        return singleton.Return(_arrow3219())

    return singleton.Delay(_arrow3220)


def read_file_binary_async(path: str) -> Async[bytearray]:
    def _arrow3222(__unit: None=None, path: Any=path) -> Async[bytearray]:
        def _arrow3221(__unit: None=None) -> bytearray:
            with open(path, 'rb') as f: return f.read()

        return singleton.Return(_arrow3221())

    return singleton.Delay(_arrow3222)


def read_file_xlsx_async(path: str) -> Async[FsWorkbook]:
    def _arrow3223(__unit: None=None, path: Any=path) -> Async[FsWorkbook]:
        return singleton.Return(FsSpreadsheet_FsWorkbook__FsWorkbook_fromXlsxFile_Static_Z721C83C5(path))

    return singleton.Delay(_arrow3223)


def move_file_async(old_path: str, new_path: str) -> Async[None]:
    def _arrow3224(__unit: None=None, old_path: Any=old_path, new_path: Any=new_path) -> Async[None]:
        shutil.move(old_path, new_path)
        return singleton.Zero()

    return singleton.Delay(_arrow3224)


def move_directory_async(old_path: str, new_path: str) -> Async[None]:
    return move_file_async(old_path, new_path)


def delete_file_async(path: str) -> Async[None]:
    def _arrow3225(__unit: None=None, path: Any=path) -> Async[None]:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
        return singleton.Zero()

    return singleton.Delay(_arrow3225)


def delete_directory_async(path: str) -> Async[None]:
    def _arrow3226(__unit: None=None, path: Any=path) -> Async[None]:
        shutil.rmtree(path, ignore_errors=True)
        return singleton.Zero()

    return singleton.Delay(_arrow3226)


def write_file_text_async(path: str, text: str) -> Async[None]:
    def _arrow3227(__unit: None=None, path: Any=path, text: Any=text) -> Async[None]:
        with open(path, 'w') as f: f.write(text)
        return singleton.Zero()

    return singleton.Delay(_arrow3227)


def write_file_binary_async(path: str, bytes: bytearray) -> Async[None]:
    def _arrow3228(__unit: None=None, path: Any=path, bytes: Any=bytes) -> Async[None]:
        with open(path, 'wb') as f: f.write(bytes)
        return singleton.Zero()

    return singleton.Delay(_arrow3228)


def write_file_xlsx_async(path: str, wb: FsWorkbook) -> Async[None]:
    def _arrow3229(__unit: None=None, path: Any=path, wb: Any=wb) -> Async[None]:
        FsSpreadsheet_FsWorkbook__FsWorkbook_toXlsxFile_Static(path, wb)
        return singleton.Zero()

    return singleton.Delay(_arrow3229)


def trim(path: str) -> str:
    if starts_with_exact(path, "./"):
        return trim_1(replace(path, "./", ""), "/")

    else: 
        return trim_1(path, "/")



def make_relative(directory_path: str, path: str) -> str:
    if True if (True if (directory_path == ".") else (directory_path == "/")) else (directory_path == ""):
        return path

    else: 
        directory_path_1: str = trim(directory_path)
        path_1: str = trim(path)
        if starts_with_exact(path_1, directory_path_1):
            return substring(path_1, len(directory_path_1))

        else: 
            return path_1




def standardize_slashes(path: str) -> str:
    return replace(path, "\\", "/")


def get_sub_directories_async(path: str) -> Async[Array[str]]:
    def _arrow3230(__unit: None=None, path: Any=path) -> Async[Array[str]]:
        paths: Array[str] = [str(entry) for entry in Path(path).iterdir() if entry.is_dir()]
        return singleton.Return(map(standardize_slashes, paths, None))

    return singleton.Delay(_arrow3230)


def get_sub_files_async(path: str) -> Async[Array[str]]:
    def _arrow3231(__unit: None=None, path: Any=path) -> Async[Array[str]]:
        paths: Array[str] = [str(entry) for entry in Path(path).iterdir() if entry.is_file()]
        return singleton.Return(map(standardize_slashes, paths, None))

    return singleton.Delay(_arrow3231)


def get_all_file_paths_async(directory_path: str) -> Async[Array[str]]:
    directory_path_1: str = standardize_slashes(directory_path)
    def _arrow3237(__unit: None=None, directory_path: Any=directory_path) -> Async[Array[str]]:
        def all_files(dirs: IEnumerable_1[str]) -> Async[IEnumerable_1[str]]:
            def _arrow3235(__unit: None=None, dirs: Any=dirs) -> Async[IEnumerable_1[str]]:
                def _arrow3234(_arg: Array[Array[str]]) -> Async[IEnumerable_1[str]]:
                    sub_files_1: IEnumerable_1[str] = concat(_arg)
                    def _arrow3233(_arg_1: Array[Array[str]]) -> Async[IEnumerable_1[str]]:
                        def _arrow3232(_arg_2: Array[IEnumerable_1[str]]) -> Async[IEnumerable_1[str]]:
                            sub_dir_contents_1: IEnumerable_1[str] = concat(_arg_2)
                            return singleton.Return(append(sub_dir_contents_1, sub_files_1))

                        return singleton.Bind(all(map_1(all_files, _arg_1)), _arrow3232)

                    return singleton.Bind(all(map_1(get_sub_directories_async, dirs)), _arrow3233)

                return singleton.Return(empty()) if is_empty(dirs) else singleton.Bind(all(map_1(get_sub_files_async, dirs)), _arrow3234)

            return singleton.Delay(_arrow3235)

        def _arrow3236(_arg_3: IEnumerable_1[str]) -> Async[Array[str]]:
            def mapping_1(arg_2: str) -> str:
                return standardize_slashes(make_relative(directory_path_1, arg_2))

            all_files_relative: Array[str] = map(mapping_1, to_array(_arg_3), None)
            return singleton.Return(all_files_relative)

        return singleton.Bind(all_files(to_enumerable([directory_path_1])), _arrow3236)

    return singleton.Delay(_arrow3237)


def rename_file_or_directory_async(old_path: str, new_path: str) -> Async[None]:
    def _arrow3240(__unit: None=None, old_path: Any=old_path, new_path: Any=new_path) -> Async[None]:
        def _arrow3239(_arg: bool) -> Async[None]:
            def _arrow3238(_arg_1: bool) -> Async[None]:
                if _arg:
                    return singleton.ReturnFrom(move_file_async(old_path, new_path))

                elif _arg_1:
                    return singleton.ReturnFrom(move_directory_async(old_path, new_path))

                else: 
                    return singleton.Zero()


            return singleton.Bind(directory_exists_async(old_path), _arrow3238)

        return singleton.Bind(file_exists_async(old_path), _arrow3239)

    return singleton.Delay(_arrow3240)


def delete_file_or_directory_async(path: str) -> Async[None]:
    def _arrow3243(__unit: None=None, path: Any=path) -> Async[None]:
        def _arrow3242(_arg: bool) -> Async[None]:
            def _arrow3241(_arg_1: bool) -> Async[None]:
                if _arg:
                    return singleton.ReturnFrom(delete_file_async(path))

                elif _arg_1:
                    return singleton.ReturnFrom(delete_directory_async(path))

                else: 
                    return singleton.Zero()


            return singleton.Bind(directory_exists_async(path), _arrow3241)

        return singleton.Bind(file_exists_async(path), _arrow3242)

    return singleton.Delay(_arrow3243)


__all__ = ["directory_exists_async", "create_directory_async", "ensure_directory_async", "ensure_directory_of_file_async", "file_exists_async", "read_file_text_async", "read_file_binary_async", "read_file_xlsx_async", "move_file_async", "move_directory_async", "delete_file_async", "delete_directory_async", "write_file_text_async", "write_file_binary_async", "write_file_xlsx_async", "trim", "make_relative", "standardize_slashes", "get_sub_directories_async", "get_sub_files_async", "get_all_file_paths_async", "rename_file_or_directory_async", "delete_file_or_directory_async"]

