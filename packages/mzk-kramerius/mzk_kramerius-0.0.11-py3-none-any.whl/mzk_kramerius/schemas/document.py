from typing import Dict, Optional
from ..datatypes import Field, Model


class KrameriusDocument:
    def __init__(self, document: Dict):
        self.document = document

    def get_field_value(self, field: Field):
        return (
            self.document[field.value]
            if field.value in self.document
            else None
        )

    @property
    def pid(self):
        return self.get_field_value(Field.Pid)

    @property
    def parentPid(self):
        return self.get_field_value(Field.ParentPid)

    @property
    def ownPidPath(self):
        return self.get_field_value(Field.OwnPidPath)

    @property
    def inCollections(self):
        return self.get_field_value(Field.InCollections) or []

    @property
    def licenses(self):
        return self.get_field_value(Field.Licenses) or []

    @property
    def ancestralLicenses(self):
        return self.get_field_value(Field.AncestralLicenses) or []

    @property
    def containsLicenses(self):
        return self.get_field_value(Field.ContainsLicenses) or []

    @property
    def model(self) -> Model:
        field_value = self.get_field_value(Field.Model)
        try:
            return Model(field_value)
        except ValueError:
            raise ValueError(f"Invalid model value: {field_value}")

    @property
    def modelPath(self):
        return self.get_field_value(Field.ModelPath)

    @property
    def barcode(self):
        return self.get_field_value(Field.Barcode)

    @property
    def signature(self):
        return self.get_field_value(Field.Signature)

    @property
    def cnb(self):
        return self.get_field_value(Field.Cnb)

    @property
    def sysno(self):
        return self.get_field_value(Field.Sysno)

    @property
    def date_min(self):
        return self.get_field_value(Field.DateMin)

    @property
    def date_max(self):
        return self.get_field_value(Field.DateMax)

    @property
    def date_range_start_year(self) -> Optional[int]:
        return self.get_field_value(Field.DateRangeStartYear)

    @property
    def date_range_end_year(self) -> Optional[int]:
        return self.get_field_value(Field.DateRangeEndYear)

    @property
    def title(self):
        return self.get_field_value(Field.Title)

    @property
    def title_sort(self):
        return self.get_field_value(Field.TitleSort)

    @property
    def part_number_sort(self):
        return self.get_field_value(Field.PartNumberSort)

    @property
    def part_number_string(self):
        return self.get_field_value(Field.PartNumberString)

    @property
    def publishers_facet(self):
        return self.get_field_value(Field.PublishersFacet)

    @property
    def publication_places_facet(self):
        return self.get_field_value(Field.PublicationPlacesFacet)

    @property
    def languages_facet(self):
        return self.get_field_value(Field.LanguagesFacet)

    @property
    def pages_count(self):
        return self.get_field_value(Field.PagesCount)

    @property
    def keywords_facet(self):
        return self.get_field_value(Field.KeywordsFacet)

    def __str__(self) -> str:
        return (
            f"PID: {self.pid}\n"
            f"Parent PID: {self.parentPid}\n"
            f"Licenses: {self.licenses}\n"
            f"Model: {self.model}\n"
            f"Model path: {self.modelPath}\n"
            f"Barcode: {self.barcode}\n"
            f"Signature: {self.signature}\n"
            f"CNB: {self.cnb}\n"
            f"Sysno: {self.sysno}\n"
            f"Title: {self.title}\n"
            f"Date min: {self.date_min}\n"
            f"Date max: {self.date_max}\n"
            f"Date range start year: {self.date_range_start_year}\n"
            f"Date range end year: {self.date_range_end_year}\n"
            f"Part number sort: {self.part_number_sort}\n"
            f"Part number string: {self.part_number_string}\n"
        )
