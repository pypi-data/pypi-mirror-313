from pydantic import BaseModel
from ..datatypes import (
    Pid,
    SdnntSyncAction,
    License,
    Model,
    SdnntState,
    SdnntRecordType,
)
from datetime import datetime
from typing import List
import textwrap


class SdnntBaseRecord(BaseModel):
    id: str
    pid: Pid | None = None
    type: SdnntRecordType

    sync_actions: List[SdnntSyncAction] | None = None
    state: SdnntState
    sync_sort: int
    fetched: datetime

    real_kram_exists: bool = False
    real_kram_model: Model | None = None
    real_kram_licenses: List[License] | None = None
    real_kram_date: str | None = None
    real_kram_titles_search: List[str] | None = None


class SdnntGranularityRecord(SdnntBaseRecord):
    parent_id: str
    license: License | None = None

    def __repr__(self):
        return textwrap.dedent(
            f"""
        id: {self.id}
        parent_id: {self.parent_id}
        pid: {self.pid}
        type: {self.type}
        sync_actions: {self.sync_actions}
        state: {self.state}
        sync_sort: {self.sync_sort}
        fetched: {self.fetched}
        license: {self.license}
        real_kram_exists: {self.real_kram_exists}
        real_kram_model: {self.real_kram_model}
        real_kram_licenses: {self.real_kram_licenses}
        real_kram_date: {self.real_kram_date}
        real_kram_titles_search: {self.real_kram_titles_search}
        """
        )

    def __str__(self):
        return self.__repr__()


class SdnntRecord(SdnntBaseRecord):
    catalog: str | None = None
    title: str | None = None

    has_granularity: bool

    type_of_rec: str
    controlField_date1: str | None = None
    controlField_date2: str | None = None
    controlField_typeofdate: str | None = None

    def __repr__(self):
        return textwrap.dedent(
            f"""
        id: {self.id}
        pid: {self.pid}
        catalog: {self.catalog}
        title: {self.title}
        type: {self.type}
        has_granularity: {self.has_granularity}
        sync_actions: {self.sync_actions}
        state: {self.state}
        sync_sort: {self.sync_sort}
        fetched: {self.fetched}
        type_of_rec: {self.type_of_rec}
        controlField_date1: {self.controlField_date1}
        controlField_date2: {self.controlField_date2}
        controlField_typeofdate: {self.controlField_typeofdate}
        real_kram_exists: {self.real_kram_exists}
        real_kram_model: {self.real_kram_model}
        real_kram_licenses: {self.real_kram_licenses}
        real_kram_date: {self.real_kram_date}
        real_kram_titles_search: {self.real_kram_titles_search}
        """
        )

    def __str__(self):
        return self.__repr__()


class SdnntResponse(BaseModel):
    numFound: int
    start: int
    numFoundExact: bool
    docs: List[SdnntRecord]


SdnntGranularityResponse = List[SdnntGranularityRecord]
