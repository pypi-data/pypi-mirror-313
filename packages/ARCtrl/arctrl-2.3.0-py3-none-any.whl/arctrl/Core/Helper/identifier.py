from typing import Any
from ...fable_modules.fable_library.guid import new_guid
from ...fable_modules.fable_library.reg_exp import (get_item, groups)
from ...fable_modules.fable_library.string_ import starts_with_exact
from ...FileSystem.path import combine_many
from .regex import ActivePatterns__007CRegex_007C__007C

def try_check_valid_characters(identifier: str) -> bool:
    if ActivePatterns__007CRegex_007C__007C("^[a-zA-Z0-9_\\- ]+$", identifier) is not None:
        return True

    else: 
        return False



def check_valid_characters(identifier: str) -> None:
    if try_check_valid_characters(identifier):
        pass

    else: 
        raise Exception(("New identifier \"" + identifier) + "\"contains forbidden characters! Allowed characters are: letters, digits, underscore (_), dash (-) and whitespace ( ).")



def create_missing_identifier(__unit: None=None) -> str:
    def _arrow518(__unit: None=None) -> str:
        copy_of_struct: str = new_guid()
        return str(copy_of_struct)

    return "MISSING_IDENTIFIER_" + _arrow518()


def is_missing_identifier(str_1: str) -> bool:
    return starts_with_exact(str_1, "MISSING_IDENTIFIER_")


def remove_missing_identifier(str_1: str) -> str:
    if starts_with_exact(str_1, "MISSING_IDENTIFIER_"):
        return ""

    else: 
        return str_1



def Assay_identifierFromFileName(file_name: str) -> str:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("^(assays(\\/|\\\\))?(?<identifier>[a-zA-Z0-9_\\- ]+)((\\/|\\\\)isa.assay.xlsx)?$", file_name)
    if active_pattern_result is not None:
        m: Any = active_pattern_result
        return get_item(groups(m), "identifier") or ""

    else: 
        raise Exception(("Cannot parse assay identifier from FileName `" + file_name) + "`")



def Assay_tryIdentifierFromFileName(file_name: str) -> str | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("^(assays(\\/|\\\\))?(?<identifier>[a-zA-Z0-9_\\- ]+)((\\/|\\\\)isa.assay.xlsx)?$", file_name)
    if active_pattern_result is not None:
        m: Any = active_pattern_result
        return get_item(groups(m), "identifier") or ""

    else: 
        return None



def Assay_fileNameFromIdentifier(identifier: str) -> str:
    check_valid_characters(identifier)
    return combine_many(["assays", identifier, "isa.assay.xlsx"])


def Assay_tryFileNameFromIdentifier(identifier: str) -> str | None:
    if try_check_valid_characters(identifier):
        return combine_many(["assays", identifier, "isa.assay.xlsx"])

    else: 
        return None



def Assay_datamapFileNameFromIdentifier(identifier: str) -> str:
    check_valid_characters(identifier)
    return combine_many(["assays", identifier, "isa.datamap.xlsx"])


def Assay_tryDatamapFileNameFromIdentifier(identifier: str) -> str | None:
    if try_check_valid_characters(identifier):
        return combine_many(["assays", identifier, "isa.datamap.xlsx"])

    else: 
        return None



def Study_identifierFromFileName(file_name: str) -> str:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("^(studies(\\/|\\\\))?(?<identifier>[a-zA-Z0-9_\\- ]+)((\\/|\\\\)isa.study.xlsx)?$", file_name)
    if active_pattern_result is not None:
        m: Any = active_pattern_result
        return get_item(groups(m), "identifier") or ""

    else: 
        raise Exception(("Cannot parse study identifier from FileName `" + file_name) + "`")



def Study_tryIdentifierFromFileName(file_name: str) -> str | None:
    active_pattern_result: Any | None = ActivePatterns__007CRegex_007C__007C("^(studies(\\/|\\\\))?(?<identifier>[a-zA-Z0-9_\\- ]+)((\\/|\\\\)isa.study.xlsx)?$", file_name)
    if active_pattern_result is not None:
        m: Any = active_pattern_result
        return get_item(groups(m), "identifier") or ""

    else: 
        return None



def Study_fileNameFromIdentifier(identifier: str) -> str:
    check_valid_characters(identifier)
    return combine_many(["studies", identifier, "isa.study.xlsx"])


def Study_tryFileNameFromIdentifier(identifier: str) -> str | None:
    if try_check_valid_characters(identifier):
        return combine_many(["studies", identifier, "isa.study.xlsx"])

    else: 
        return None



def Study_datamapFileNameFromIdentifier(identifier: str) -> str:
    check_valid_characters(identifier)
    return combine_many(["studies", identifier, "isa.datamap.xlsx"])


def Study_tryDatamapFileNameFromIdentifier(identifier: str) -> str | None:
    if try_check_valid_characters(identifier):
        return combine_many(["studies", identifier, "isa.datamap.xlsx"])

    else: 
        return None



__all__ = ["try_check_valid_characters", "check_valid_characters", "create_missing_identifier", "is_missing_identifier", "remove_missing_identifier", "Assay_identifierFromFileName", "Assay_tryIdentifierFromFileName", "Assay_fileNameFromIdentifier", "Assay_tryFileNameFromIdentifier", "Assay_datamapFileNameFromIdentifier", "Assay_tryDatamapFileNameFromIdentifier", "Study_identifierFromFileName", "Study_tryIdentifierFromFileName", "Study_fileNameFromIdentifier", "Study_tryFileNameFromIdentifier", "Study_datamapFileNameFromIdentifier", "Study_tryDatamapFileNameFromIdentifier"]

