from pydantic import BaseModel
from datetime import datetime
from ..datatypes import (
    ProcessType,
    ProcessState,
    PathType,
    IndexationType,
    License,
    Pid,
)


class EmptyParams(BaseModel):
    pass


class ImportParams(BaseModel):
    inputDataDir: str
    startIndexer: bool
    license: License
    collections: str
    pathtype: PathType


class ImportMetsParams(ImportParams):
    policy: str
    useIIPServer: bool


class IndexParams(BaseModel):
    type: IndexationType
    pid: Pid
    ignoreInconsistentObjects: bool


class AddLicenseParams(BaseModel):
    pid: Pid
    license: License


class RemoveLicenseParams(AddLicenseParams):
    pass


class DeleteTreeParams(BaseModel):
    pid: Pid
    ignoreIncosistencies: bool


ProcessParams = (
    ImportParams
    | ImportMetsParams
    | IndexParams
    | AddLicenseParams
    | RemoveLicenseParams
    | DeleteTreeParams
    | EmptyParams
)


class KrameriusPlanProcess(BaseModel):
    defid: ProcessType
    params: ProcessParams | None


class KrameriusProcess(BaseModel):
    uuid: str
    name: str
    state: ProcessState
    planned: datetime
    started: datetime
    finished: datetime
