from __future__ import annotations
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from ..datatypes import SolrConjuction, Field, SolrValue, StartCursorMark


class SearchQuery(BaseModel):
    field: Field | None = None
    value: SolrValue | None = None
    list_conjunction: SolrConjuction | None = None
    not_subquery: Optional["SearchQuery"] = None
    sub_queries: List["SearchQuery"] | None = None
    conjuctions: List[SolrConjuction] | None = None

    def _append_part(
        self, conjuction: SolrConjuction, part: "SearchQuery"
    ) -> "SearchQuery":
        if not self.sub_queries:
            return SearchQuery(
                sub_queries=[self, part], conjuctions=[conjuction]
            )
        self.conjuctions.append(conjuction)
        self.sub_queries.append(part)
        return self

    def _has_multiple_subqueries(self) -> bool:
        return self.sub_queries is not None and len(self.sub_queries) > 1

    @classmethod
    def _parse_args(cls, *args) -> "SearchQuery":
        if len(args) == 1 and isinstance(args[0], SearchQuery):
            return args[0]
        elif len(args) == 2:
            field, value = args
            return SearchQuery(
                field=field, value=value, list_conjunction=SolrConjuction.And
            )
        elif len(args) == 3:
            field, value, list_conjunction = args
            return SearchQuery(
                field=field, value=value, list_conjunction=list_conjunction
            )
        else:
            raise ValueError(
                "Invalid arguments: pass either a SearchQuery, "
                "a field and value pair, "
                "or a field, value, and list_conjunction triplet."
            )

    @classmethod
    def base_(cls, *args) -> "SearchQuery":
        return cls._parse_args(*args)

    @classmethod
    def not_(cls, *args) -> "SearchQuery":
        subquery = cls._parse_args(*args)
        return cls(not_subquery=subquery)

    def and_(self, *args) -> "SearchQuery":
        subquery = self._parse_args(*args)
        return self._append_part(SolrConjuction.And, subquery)

    def or_(self, *args) -> "SearchQuery":
        subquery = self._parse_args(*args)
        return self._append_part(SolrConjuction.Or, subquery)

    def _parse_value(self, value: SolrValue) -> str:
        if isinstance(value, str):
            return f'"{value}"' if value != "*" else value
        elif isinstance(value, Enum):
            return f'"{value.value}"'
        elif isinstance(value, list):
            if not value:
                raise ValueError("List values cannot be empty.")
            if not all(isinstance(v, (str, int, float, Enum)) for v in value):
                raise TypeError(
                    "List values must be of type str, int, float, or Enum."
                )
            if not self.list_conjunction:
                raise ValueError(
                    "List conjunction must be provided for list values."
                )
            return f"({self.list_conjunction.value.join(
                [self._parse_value(v) for v in value]
            )})"
        elif isinstance(value, tuple) and len(value) == 2:
            value_1 = self._parse_value(value[0])
            value_2 = self._parse_value(value[1])
            return f"[{value_1} TO {value_2}]"
        elif isinstance(value, int) or isinstance(value, float):
            return str(value)
        raise TypeError(f"Unsupported value type: {type(value)}")

    def build(self) -> str:
        if self.not_subquery is not None:
            return (
                f"-{self.not_subquery.build()}"
                if not self.not_subquery._has_multiple_subqueries()
                else f"-({self.not_subquery.build()})"
            )
        if self.sub_queries:
            parts = [
                (
                    sub.build()
                    if not sub._has_multiple_subqueries()
                    else f"({sub.build()})"
                )
                for sub in self.sub_queries
            ]
            return f"{self.conjuctions[0].value}".join(parts)
        if self.field is not None and self.value is not None:
            return f"{self.field.value}:{self._parse_value(self.value)}"
        raise ValueError("Invalid query structure.")


def base_(*args) -> SearchQuery:
    return SearchQuery.base_(*args)


def not_(*args) -> SearchQuery:
    return SearchQuery.not_(*args)


class SearchParams(BaseModel):
    query: str
    rows: int | None = None
    start: int | None = None
    fl: List[Field] | None = None
    fq: str | None = None
    sort: str | None = None
    cursorMark: str | None = None
    facet: bool | None = None
    facet_field: str | None = None
    facet_min_count: int | None = None

    def with_pagination(self):
        self.sort = "pid ASC"
        self.cursorMark = StartCursorMark
        return self

    def build(self):

        params = {
            "q": (
                self.query.build()
                if isinstance(self.query, SearchQuery)
                else self.query
            )
        }
        for value, key in [
            (self.rows, "rows"),
            (self.start, "start"),
            (
                ",".join([fl.value for fl in self.fl]) if self.fl else None,
                "fl",
            ),
            (self.fq, "fq"),
            (self.sort, "sort"),
            (self.cursorMark, "cursorMark"),
            ("true" if self.facet else None, "facet"),
            (self.facet_field, "facet.field"),
            (self.facet_min_count, "facet.mincount"),
        ]:
            if value is not None:
                params[key] = value

        return params
