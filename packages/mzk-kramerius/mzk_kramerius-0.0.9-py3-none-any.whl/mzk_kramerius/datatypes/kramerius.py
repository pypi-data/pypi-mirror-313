from enum import Enum
import uuid
from typing import Any, Dict, Literal
from typing_extensions import Annotated
from pydantic import AfterValidator


Method = Literal["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]
type Params = Dict[str, Any]


def validate_pid(pid: str) -> str:
    try:
        uuid_ = pid[5:] if pid.startswith("uuid:") else pid
        uuid.UUID(uuid_)
        return f"uuid:{uuid_}"
    except ValueError:
        raise ValueError("Invalid UUID format")


Pid = Annotated[
    str,
    AfterValidator(lambda x: validate_pid(x)),
]


class Field(Enum):
    Pid = "pid"
    ParentPid = "own_parent.pid"
    OwnPidPath = "own_pid_path"
    InCollections = "in_collections"

    Accessibility = "accessibility"
    Licenses = "licenses"
    ContainsLicenses = "contains_licenses"
    AncestralLicenses = "licenses_of_ancestors"
    Model = "model"
    ModelPath = "own_model_path"
    ParentModel = "own_parent.model"
    Level = "level"

    Barcode = "id_barcode"
    Signature = "shelf_locators"
    Cnb = "id_ccnb"
    Sysno = "id_sysno"

    PhysicalLocation = "physical_locations.facet"

    DateMin = "date.min"
    DateMax = "date.max"
    DateRangeStartYear = "date_range_start.year"
    DateRangeEndYear = "date_range_end.year"

    Title = "title.search"
    TitleSort = "title.sort"
    PartNumberSort = "part.number.sort"
    PartNumberString = "part.number.str"

    PublishersFacet = "publishers.facet"
    PublicationPlacesFacet = "publication_places.facet"
    LanguagesFacet = "languages.facet"

    PageCount = "count_page"

    KeywordsFacet = "keywords.facet"
    ImageFullMimeType = "ds.img_full.mime"


class Model(Enum):
    Periodical = "periodical"
    PeriodicalVolume = "periodicalvolume"
    PeriodicalItem = "periodicalitem"
    Supplement = "supplement"
    Article = "article"
    Monograph = "monograph"
    MonographUnit = "monographunit"
    Page = "page"
    Sheetmusic = "sheetmusic"
    Convolute = "convolute"
    Collection = "collection"
    InternalPart = "internalpart"
    Track = "track"
    Map = "map"


class Accessibility(Enum):
    Public = "public"
    Private = "private"


class MimeType(Enum):
    Pdf = "application/pdf"
