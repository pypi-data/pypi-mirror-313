from __future__ import annotations
from ..fable_modules.fable_library.types import Array
from ..FileSystem.path import split as split_1
from .arc_assay import _007CAssayPath_007C__007C
from .arc_investigation import _007CInvestigationPath_007C__007C
from .arc_study import _007CStudyPath_007C__007C
from .contract import (Contract, DTOType)
from .datamap import _007CDatamapPath_007C__007C

def try_isaread_contract_from_path(path: str) -> Contract | None:
    split: Array[str] = split_1(path)
    active_pattern_result: str | None = _007CInvestigationPath_007C__007C(split)
    if active_pattern_result is not None:
        p: str = active_pattern_result
        return Contract.create_read(p, DTOType(2))

    else: 
        active_pattern_result_1: str | None = _007CAssayPath_007C__007C(split)
        if active_pattern_result_1 is not None:
            p_1: str = active_pattern_result_1
            return Contract.create_read(p_1, DTOType(0))

        else: 
            active_pattern_result_2: str | None = _007CStudyPath_007C__007C(split)
            if active_pattern_result_2 is not None:
                p_2: str = active_pattern_result_2
                return Contract.create_read(p_2, DTOType(1))

            else: 
                active_pattern_result_3: str | None = _007CDatamapPath_007C__007C(split)
                if active_pattern_result_3 is not None:
                    p_3: str = active_pattern_result_3
                    return Contract.create_read(p_3, DTOType(3))

                else: 
                    return None






__all__ = ["try_isaread_contract_from_path"]

