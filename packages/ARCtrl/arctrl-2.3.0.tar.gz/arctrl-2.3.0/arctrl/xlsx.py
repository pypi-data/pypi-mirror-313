from __future__ import annotations
from .fable_modules.fable_library.list import (FSharpList, of_seq)
from .fable_modules.fable_library.option import map
from .fable_modules.fable_library.reflection import (TypeInfo, class_type)
from .fable_modules.fable_library.types import Array
from .fable_modules.fs_spreadsheet.fs_workbook import FsWorkbook
from .fable_modules.fs_spreadsheet_py.fs_extension import FsSpreadsheet_FsWorkbook__FsWorkbook_toXlsxFile_Static
from .Core.arc_types import (ArcAssay, ArcStudy, ArcInvestigation)
from .Core.data_map import DataMap
from .Spreadsheet.arc_assay import (ARCtrl_ArcAssay__ArcAssay_fromFsWorkbook_Static_32154C9D, ARCtrl_ArcAssay__ArcAssay_toFsWorkbook_Static_Z2508BE4F)
from .Spreadsheet.arc_investigation import (ARCtrl_ArcInvestigation__ArcInvestigation_fromFsWorkbook_Static_32154C9D, ARCtrl_ArcInvestigation__ArcInvestigation_toFsWorkbook_Static_Z720BD3FF)
from .Spreadsheet.arc_study import (ARCtrl_ArcStudy__ArcStudy_fromFsWorkbook_Static_32154C9D, ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_Z4CEFA522)
from .Spreadsheet.data_map import (from_fs_workbook, to_fs_workbook)

def _expr3306() -> TypeInfo:
    return class_type("ARCtrl.XlsxHelper.DatamapXlsx", None, XlsxHelper_DatamapXlsx)


class XlsxHelper_DatamapXlsx:
    def __init__(self, __unit: None=None) -> None:
        pass

    def from_fs_workbook(self, fswb: FsWorkbook) -> DataMap:
        return from_fs_workbook(fswb)

    def to_fs_workbook(self, datamap: DataMap) -> FsWorkbook:
        return to_fs_workbook(datamap)

    def to_xlsx_file(self, path: str, datamap: DataMap) -> None:
        FsSpreadsheet_FsWorkbook__FsWorkbook_toXlsxFile_Static(path, to_fs_workbook(datamap))


XlsxHelper_DatamapXlsx_reflection = _expr3306

def XlsxHelper_DatamapXlsx__ctor(__unit: None=None) -> XlsxHelper_DatamapXlsx:
    return XlsxHelper_DatamapXlsx(__unit)


def _expr3307() -> TypeInfo:
    return class_type("ARCtrl.XlsxHelper.AssayXlsx", None, XlsxHelper_AssayXlsx)


class XlsxHelper_AssayXlsx:
    def __init__(self, __unit: None=None) -> None:
        pass

    def from_fs_workbook(self, fswb: FsWorkbook) -> ArcAssay:
        return ARCtrl_ArcAssay__ArcAssay_fromFsWorkbook_Static_32154C9D(fswb)

    def to_fs_workbook(self, assay: ArcAssay) -> FsWorkbook:
        return ARCtrl_ArcAssay__ArcAssay_toFsWorkbook_Static_Z2508BE4F(assay)

    def to_xlsx_file(self, path: str, assay: ArcAssay) -> None:
        FsSpreadsheet_FsWorkbook__FsWorkbook_toXlsxFile_Static(path, ARCtrl_ArcAssay__ArcAssay_toFsWorkbook_Static_Z2508BE4F(assay))


XlsxHelper_AssayXlsx_reflection = _expr3307

def XlsxHelper_AssayXlsx__ctor(__unit: None=None) -> XlsxHelper_AssayXlsx:
    return XlsxHelper_AssayXlsx(__unit)


def _expr3308() -> TypeInfo:
    return class_type("ARCtrl.XlsxHelper.StudyXlsx", None, XlsxHelper_StudyXlsx)


class XlsxHelper_StudyXlsx:
    def __init__(self, __unit: None=None) -> None:
        pass

    def from_fs_workbook(self, fswb: FsWorkbook) -> tuple[ArcStudy, FSharpList[ArcAssay]]:
        return ARCtrl_ArcStudy__ArcStudy_fromFsWorkbook_Static_32154C9D(fswb)

    def to_fs_workbook(self, study: ArcStudy, assays: Array[ArcAssay] | None=None) -> FsWorkbook:
        return ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_Z4CEFA522(study, map(of_seq, assays))

    def to_xlsx_file(self, path: str, study: ArcStudy, assays: Array[ArcAssay] | None=None) -> None:
        FsSpreadsheet_FsWorkbook__FsWorkbook_toXlsxFile_Static(path, ARCtrl_ArcStudy__ArcStudy_toFsWorkbook_Static_Z4CEFA522(study, map(of_seq, assays)))


XlsxHelper_StudyXlsx_reflection = _expr3308

def XlsxHelper_StudyXlsx__ctor(__unit: None=None) -> XlsxHelper_StudyXlsx:
    return XlsxHelper_StudyXlsx(__unit)


def _expr3309() -> TypeInfo:
    return class_type("ARCtrl.XlsxHelper.InvestigationXlsx", None, XlsxHelper_InvestigationXlsx)


class XlsxHelper_InvestigationXlsx:
    def __init__(self, __unit: None=None) -> None:
        pass

    def from_fs_workbook(self, fswb: FsWorkbook) -> ArcInvestigation:
        return ARCtrl_ArcInvestigation__ArcInvestigation_fromFsWorkbook_Static_32154C9D(fswb)

    def to_fs_workbook(self, investigation: ArcInvestigation) -> FsWorkbook:
        return ARCtrl_ArcInvestigation__ArcInvestigation_toFsWorkbook_Static_Z720BD3FF(investigation)

    def to_xlsx_file(self, path: str, investigation: ArcInvestigation) -> None:
        FsSpreadsheet_FsWorkbook__FsWorkbook_toXlsxFile_Static(path, ARCtrl_ArcInvestigation__ArcInvestigation_toFsWorkbook_Static_Z720BD3FF(investigation))


XlsxHelper_InvestigationXlsx_reflection = _expr3309

def XlsxHelper_InvestigationXlsx__ctor(__unit: None=None) -> XlsxHelper_InvestigationXlsx:
    return XlsxHelper_InvestigationXlsx(__unit)


def _expr3310() -> TypeInfo:
    return class_type("ARCtrl.XlsxController", None, XlsxController)


class XlsxController:
    @staticmethod
    def Datamap() -> XlsxHelper_DatamapXlsx:
        return XlsxHelper_DatamapXlsx()

    @staticmethod
    def Assay() -> XlsxHelper_AssayXlsx:
        return XlsxHelper_AssayXlsx()

    @staticmethod
    def Study() -> XlsxHelper_StudyXlsx:
        return XlsxHelper_StudyXlsx()

    @staticmethod
    def Investigation() -> XlsxHelper_InvestigationXlsx:
        return XlsxHelper_InvestigationXlsx()


XlsxController_reflection = _expr3310

__all__ = ["XlsxHelper_DatamapXlsx_reflection", "XlsxHelper_AssayXlsx_reflection", "XlsxHelper_StudyXlsx_reflection", "XlsxHelper_InvestigationXlsx_reflection", "XlsxController_reflection"]

