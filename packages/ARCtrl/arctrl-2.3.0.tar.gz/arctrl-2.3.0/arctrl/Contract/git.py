from __future__ import annotations
from typing import Any
from ..fable_modules.fable_library.option import (default_arg, value)
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.seq import (to_array, delay, append, singleton, empty)
from ..fable_modules.fable_library.string_ import replace
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..FileSystem.default_gitattributes import dga
from ..FileSystem.default_gitignore import dgi
from .contract import (CLITool, Contract, DTOType, DTO)

def git_with_args(arguments: Array[str]) -> CLITool:
    return CLITool.create("git", arguments)


def create_git_contract_at(path: str, arguments: Array[str]) -> Contract:
    return Contract.create_execute(git_with_args(arguments), path)


def create_git_contract(arguments: Array[str]) -> Contract:
    return Contract.create_execute(git_with_args(arguments))


gitignore_contract: Contract = Contract.create_create(".gitignore", DTOType(8), DTO(1, dgi))

gitattributes_contract: Contract = Contract.create_create(".gitattributes", DTOType(8), DTO(1, dga))

def _expr3100() -> TypeInfo:
    return class_type("ARCtrl.Contract.Git.Init", None, Init)


class Init:
    ...

Init_reflection = _expr3100

def _expr3101() -> TypeInfo:
    return class_type("ARCtrl.Contract.Git.Clone", None, Clone)


class Clone:
    ...

Clone_reflection = _expr3101

def Init_get_init(__unit: None=None) -> str:
    return "init"


def Init_get_branchFlag(__unit: None=None) -> str:
    return "-b"


def Init_get_remote(__unit: None=None) -> str:
    return "remote"


def Init_get_add(__unit: None=None) -> str:
    return "add"


def Init_get_origin(__unit: None=None) -> str:
    return "origin"


def Init_createInitContract_6DFDD678(branch: str | None=None) -> Contract:
    branch_1: str = default_arg(branch, "main")
    return create_git_contract([Init_get_init(), Init_get_branchFlag(), branch_1])


def Init_createAddRemoteContract_Z721C83C5(remote_url: str) -> Contract:
    return create_git_contract([Init_get_remote(), Init_get_add(), Init_get_origin(), remote_url])


def Clone_get_clone(__unit: None=None) -> str:
    return "clone"


def Clone_get_branchFlag(__unit: None=None) -> str:
    return "-b"


def Clone_get_noLFSConfig(__unit: None=None) -> str:
    return "-c \"filter.lfs.smudge = git-lfs smudge --skip -- %f\" -c \"filter.lfs.process = git-lfs filter-process --skip\""


def Clone_formatRepoString(username: str, pass_: str, url: str) -> str:
    return replace(url, "https://", "https://" + (((username + ":") + pass_) + "@"))


def Clone_createCloneContract_5000466F(remote_url: str, merge: bool | None=None, branch: str | None=None, token: tuple[str, str] | None=None, nolfs: bool | None=None) -> Contract:
    nolfs_1: bool = default_arg(nolfs, False)
    merge_1: bool = default_arg(merge, False)
    remote_url_1: str = remote_url if (token is None) else Clone_formatRepoString(token[0], token[1], remote_url)
    def _arrow3107(__unit: None=None, remote_url: Any=remote_url, merge: Any=merge, branch: Any=branch, token: Any=token, nolfs: Any=nolfs) -> IEnumerable_1[str]:
        def _arrow3106(__unit: None=None) -> IEnumerable_1[str]:
            def _arrow3105(__unit: None=None) -> IEnumerable_1[str]:
                def _arrow3104(__unit: None=None) -> IEnumerable_1[str]:
                    def _arrow3103(__unit: None=None) -> IEnumerable_1[str]:
                        def _arrow3102(__unit: None=None) -> IEnumerable_1[str]:
                            return singleton(".") if merge_1 else empty()

                        return append(singleton(remote_url_1), delay(_arrow3102))

                    return append(singleton(value(branch)) if (branch is not None) else empty(), delay(_arrow3103))

                return append(singleton(Clone_get_branchFlag()) if (branch is not None) else empty(), delay(_arrow3104))

            return append(singleton(Clone_get_noLFSConfig()) if nolfs_1 else empty(), delay(_arrow3105))

        return append(singleton(Clone_get_clone()), delay(_arrow3106))

    return create_git_contract(to_array(delay(_arrow3107)))


__all__ = ["git_with_args", "create_git_contract_at", "create_git_contract", "gitignore_contract", "gitattributes_contract", "Init_reflection", "Clone_reflection", "Init_get_init", "Init_get_branchFlag", "Init_get_remote", "Init_get_add", "Init_get_origin", "Init_createInitContract_6DFDD678", "Init_createAddRemoteContract_Z721C83C5", "Clone_get_clone", "Clone_get_branchFlag", "Clone_get_noLFSConfig", "Clone_formatRepoString", "Clone_createCloneContract_5000466F"]

