from enum import Enum


class SdnntSyncAction(Enum):
    AddDnnto = "add_dnnto"
    AddDnntt = "add_dnntt"
    RemoveDnnto = "remove_dnnto"
    RemoveDnntt = "remove_dnntt"
    ChangeDnntoToDnntt = "change_dnnto_dnntt"
    ChangeDnnttToDnnto = "change_dnntt_dnnto"
    PartialChange = "partial_change"


class SdnntState(Enum):
    Assigned = "A"
    Withdrawn = "N"
    ProposalForAssignment = "PA"
    LicenseRestriction = "NL"
    FreeWorks = "X"
    Deleted = "D"
    ProposalForAssignmentCurator = "NPA"
    LikelyFreeWorks = "PX"
    WorkStatusAfter18Months = "NLX"
    LikelyToBeDeleted = "DX"


class SdnntRecordType(Enum):
    Granularity = "granularity"
    Main = "main"
